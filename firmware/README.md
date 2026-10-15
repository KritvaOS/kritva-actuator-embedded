# firmware/

Actuator motor-control firmware. Owner: **Electronics/Embedded Intern**. Reviewer for safety-relevant code (fault manager, limits, state machine, watchdog supervision): **Independent Electrical/Firmware Reviewer**.

- Requirements: [requirements/FIRMWARE_REQUIREMENTS.md](../requirements/FIRMWARE_REQUIREMENTS.md)
- Design: [docs/firmware/FIRMWARE_ARCHITECTURE.md](../docs/firmware/FIRMWARE_ARCHITECTURE.md), [MOTOR_CONTROL.md](../docs/firmware/MOTOR_CONTROL.md), [CALIBRATION_PROCEDURE.md](../docs/firmware/CALIBRATION_PROCEDURE.md)
- Interfaces: [docs/interfaces/](../docs/interfaces/)

| Folder | Contents |
|---|---|
| `platform/` | HAL and board support. **The only place for vendor or MCU-specific code** (FW-REQ-002) |
| `foc/` | Clarke/Park transforms, PI current controllers, SVPWM, voltage limiting, the current-loop ISR body |
| `motor_control/` | Motor parameters, R/L and offset calibration, torque estimate, I²t, regeneration limiting |
| `encoder/` | Hall, motor-encoder and output-encoder drivers; angle and velocity estimation; validity and cross-checks |
| `joint_control/` | Position and velocity loops, trajectory limiter, soft limits, gravity feed-forward, mode manager |
| `diagnostics/` | State machine, fault manager, fault log, telemetry, capture buffer, counters, watchdog supervisor, self-test |
| `communication/` | USB/UART CLI and binary protocol, CAN protocol v1, command arbiter, parameter service, version |

## Status

No firmware has been committed yet. The MCU family (ACT-DEC-004) and the A0 board (ACT-DEC-005) are pending, and the build system is added in ACT-01-002. CI (`.github/workflows/firmware-build.yml`) activates when `firmware/CMakeLists.txt` exists.

## Build (planned)

```bash
cmake -S firmware -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DKA_BOARD=<dev_board|ka_pcb_revA>
cmake --build build
```

Build variants are `release`, `debug` and `test`. The `test` variant has fault-injection hooks and must **never** be flashed on the robot.

## Third-party code register (FW-REQ-074)

Every file that is taken from, or derived from, external code must be listed here **before** it is merged. Its licence must have been reviewed and the reuse approved by the Project Lead.

| File(s) | Origin (project, version, URL) | Licence | Modified? | Notice retained? | Approved by / date |
|---|---|---|---|---|---|
| — | — | — | — | — | — |
