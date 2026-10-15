# Kritva Actuator: Firmware Architecture

| Field | Value |
|---|---|
| Document ID | KA-DOC-FW-ARCH |
| Repository | `KritvaOS/kritva-actuator` |
| Revision | 0.1 (Draft: proposed, pending approval) |
| Date | 2026-10-11 |
| Document owner | Electronics/Embedded Intern |
| Reviewer / Approver | Independent Electrical/Firmware Reviewer / Project Lead |
| Applies to | A0, A1, A2 |
| Classification | Proprietary and confidential |

> **Status note.** This architecture is proposed for review at F1. It is written MCU-neutral, with the STM32G4 family as the proposed target (ACT-DEC-004). Loop rates and timing figures are proposals until they are measured on the target.

---

## 1. Purpose

This document defines the firmware structure (modules, layers, interfaces), the execution model (interrupts, tasks, rates, priorities), data flow, memory and storage, the build system and the test strategy. It implements `requirements/FIRMWARE_REQUIREMENTS.md`.

## 2. Design principles

1. **Layering with HAL isolation:** vendor code lives only in `platform/` (FW-REQ-002).
2. **Configuration over code:** the motor, gearbox and joint are described by parameters (FW-REQ-003).
3. **Deterministic, interrupt-driven control:** no dynamic memory after initialisation, no blocking calls in the ISRs (FW-REQ-007).
4. **Safety first:** hardware protection is configured at boot, and the gates are off until ENABLED (FW-REQ-031).
5. **Testable on the host:** the maths, logic, state machine and protocol parsers compile and run in host unit tests (FW-REQ-072).

## 3. Module structure

```
firmware/
├── platform/          HAL: clock, gpio, pwm (adv. timer), adc (injected/synchronised), comp/break,
│                      spi, fdcan, usart/usb-cdc, flash/nvm, iwdg, systick, cpu-load, hw-rev straps
├── foc/               clarke_park.c, pi.c, svpwm.c, voltage_limit.c, current_loop.c (20 kHz ISR body)
├── encoder/           hall.c, motor_encoder_spi.c / abi.c, output_encoder_spi.c, angle_estimator.c,
│                      velocity_estimator.c, validity.c, cross_check.c
├── motor_control/     motor_params.c, calibration_rl.c, calibration_offset.c, torque_estimate.c,
│                      i2t.c, regen_limit.c
├── joint_control/     position_loop.c, velocity_loop.c, trajectory_limiter.c, soft_limits.c,
│                      gravity_ff.c, mode_manager.c
├── diagnostics/       state_machine.c, fault_manager.c, fault_log.c, telemetry.c, capture.c,
│                      counters.c, watchdog_supervisor.c, selftest.c
├── communication/     cli.c, binary_proto.c (USB/UART), can_proto.c (v1), command_arbiter.c,
│                      param_service.c, version.c
├── config/            param_table.c (IDs, ranges, defaults - generated from ACTUATOR_INTERFACE §7),
│                      nvm_store.c (two-copy + CRC)
└── app/               main.c (init order), scheduler (background loop)
```

`communication/can/firmware/` holds the shared CAN frame packing/unpacking code that is generated from `docs/interfaces/CAN_PROTOCOL.md`, so the firmware and the host tools use the same definitions.

## 4. Execution model

| Context | Trigger | Rate | Priority (0 = highest) | Work | Budget (proposed) |
|---|---|---|---|---|---|
| Break / fault ISR | Hardware PWM break, gate-driver nFAULT | Event | 0 | Latch the fault and set the state to FAULT. The PWM is already off in hardware | < 2 µs |
| Current-loop ISR | ADC end-of-conversion (triggered by PWM centre) | 20 kHz | 1 | Read the currents and Vbus; motor angle; Clarke/Park; PI; inverse Park; SVPWM; software overcurrent check; capture | ≤ 15 µs (≤ 30 % of 50 µs) |
| Encoder ISR / DMA | SPI complete | 1–2 kHz (output) | 2 | Store the angle and its validity | < 3 µs |
| Control-loop task | Timer | 2 kHz velocity / 1 kHz position | 3 | Velocity and position loops, trajectory, limits, I²t, cross-check | ≤ 40 µs per 1 ms |
| Supervisor task | Timer | 1 kHz | 4 | State machine, fault manager, thermal, watchdog supervision | ≤ 20 µs |
| Communication ISRs | FDCAN RX/TX, USART/USB | Event | 5 | Frame queues only; no parsing in the ISR | < 3 µs |
| Background loop | — | Continuous | Lowest | Protocol parsing, parameter service, telemetry packing, NVM writes (only when DISABLED), CLI | Remaining |

The CPU load target is ≤ 70 % at maximum rates, with current-loop jitter ≤ 1 µs (FW-REQ-061). Both are measured with GPIO markers and the cycle counter (FW-REQ-044).

### 4.1 Data flow

```
ADC(Ia,Ib,Ic,Vbus) --> foc.current_loop --> PWM duties
   ^ theta_e (encoder.angle_estimator @20 kHz)
   ^ Iq* (joint_control.velocity_loop @2 kHz) <-- dq* (position_loop @1 kHz) <-- trajectory_limiter
                                                     ^ q (output encoder)          ^ command_arbiter
diagnostics.fault_manager <-- checks from every module ---> state_machine ---> PWM enable gate
telemetry/capture <-- shared state snapshot (double-buffered, lock-free)
```

Shared data between contexts uses **single-writer, double-buffered snapshots** or atomic types. The higher-priority writer never waits.

## 5. Initialisation order

1. Clocks, the watchdog (started early) and GPIO, with the gate-driver enable held low.
2. Read the hardware-revision straps (FW-REQ-006), then load the configuration and calibration from NVM, checking their CRCs.
3. Configure the PWM, with the outputs held inactive and the break input enabled. Configure the comparator thresholds.
4. ADC: calibrate, then measure the current offsets with the PWM off.
5. Encoder interfaces: read and validate.
6. Communication peripherals.
7. Self-test (FW-REQ-034). On a pass, enter DISABLED_UNCONFIGURED or DISABLED; on a failure, enter FAULT.
8. Start the timers and ISRs, then enter the background loop.

## 6. State machine and fault manager

- The **state machine** is exactly that of INTERFACE_REQUIREMENTS §8.8.1 (FW-REQ-030), with the CALIBRATING sub-state inside DISABLED.
- **PWM enable** is a single function. It is the only path to the gate-driver enable, and it checks the state on every call.
- **Fault manager.**
  1. Each fault source calls `fault_raise(code, data)`.
  2. The manager applies the fault table in FIRMWARE_REQUIREMENTS §13: the class, the reaction (immediate PWM off, or a controlled stop) and latching.
  3. It records the first fault and updates the counters and the NVM log. The log is written in the background, only when the PWM is off or when the write is deferred safely.
- **Watchdog supervisor.** The current-loop ISR and the control task each set an alive flag. The supervisor refreshes the IWDG only if both flags are set within the window (CTRL-REQ-004).

## 7. Memory and storage

| Region | Content | Protection |
|---|---|---|
| Flash: application | Firmware image | CRC check by the bootloader (A1) |
| Flash: configuration A/B | Parameter set (two copies) | CRC32, version, sequence counter |
| Flash: calibration A/B | Calibration data | CRC32, validity flag |
| Flash: fault log | Ring buffer of ≥ 16 entries | CRC per entry |
| RAM | Static allocation only; stack canaries | Stack overflow results in `INTERNAL_ERROR` |

## 8. Build, configuration and tooling

| Item | Proposal (TBC with ACT-DEC-004) |
|---|---|
| Language | C11 (C++17 subset optional; decided at F1) |
| Toolchain | arm-none-eabi-gcc (pinned version) with CMake and Ninja; vendor HAL/LL generated into `platform/` only |
| Build variants | `release`, `debug`, `test` (fault-injection hooks enabled; never flashed on the robot) |
| Static analysis | cppcheck and/or clang-tidy in CI (`.github/workflows/firmware-build.yml`) |
| Unit tests | Host build of `foc`, `joint_control`, `diagnostics`, `communication` parsers, `config`, using a lightweight framework (for example Unity or GoogleTest, TBC) in `tests/unit/` |
| Version embedding | Generated header with the semver, git hash, build date and HW support list (FW-REQ-005) |
| Code generation | The parameter table and CAN frames are generated from the interface documents' tables (single source) |

## 9. Reuse of reference implementations

| Reference | Licence | Possible use | Rule |
|---|---|---|---|
| SimpleFOC | MIT | Learning; algorithm comparison | Re-implement, or reuse with the notice retained, after licence review |
| moteus | Apache-2.0 | Architecture reference (STM32G4) | Same; the NOTICE file must be retained if code is reused |
| Vendor motor-control SDK | Vendor licence | A0 quick-start | Check the redistribution terms before committing any SDK code |
| ODrive | Check the version-specific licence | Reference only | Licence review required |

All reuse is recorded in the third-party register in `firmware/README.md` (FW-REQ-074).

## 10. Test strategy

| Level | Location | What | Gate |
|---|---|---|---|
| Unit (host) | `tests/unit/` | Transforms, PI, SVPWM sector logic, trajectory limiter, soft limits, state machine, fault table, parsers, CRC, parameter validation | F2 |
| Firmware-in-target | `tests/firmware/` | Peripheral drivers, timing, NVM power-fail, protocol conformance | F2/F3 |
| Hardware-in-the-loop | `tests/hardware/`, `tests/safety/` | Fault injection FI-01–FI-24, timeouts, e-stop | F3 |
| Performance | `tests/performance/` | Loop bandwidth, tracking, thermal | Gate B |

## 11. Open items

| # | Item | Owner | Needed by |
|---|---|---|---|
| 1 | MCU and board confirmation, and the HAL choice (HAL vs LL vs bare registers) | Electronics/Embedded Intern | F1 |
| 2 | Language decision (C vs a C++ subset) | Electronics/Embedded Intern | F1 |
| 3 | Unit-test framework choice | Electronics/Embedded Intern | F1 |
| 4 | Timing measured on the target | Electronics/Embedded Intern | F3 |
| 5 | Bootloader scope | Project Lead | F1 |

## 12. Revision history

| Rev | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-11 | Kritvaos Actuator Team | Initial draft |
