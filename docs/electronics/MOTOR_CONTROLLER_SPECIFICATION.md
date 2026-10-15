# Kritva Actuator: Motor Controller Specification

| Field | Value |
|---|---|
| Document ID | KA-DOC-ELEC-MCSPEC |
| Repository | `KritvaOS/kritva-actuator` |
| Revision | 0.2 (Draft: proposed, pending approval) |
| Date | 2026-10-11 |
| Document owner | Electronics/Embedded Intern |
| Reviewer / Approver | Independent Electrical/Firmware Reviewer / Project Lead |
| Applies to | A1 custom PCB (A0 board checked against the same table) |
| Classification | Proprietary and confidential |

> **Status note.** This is a target specification for the A1 controller PCB. Values marked TBC depend on the selected motor (Kt, R, L, pole pairs) and are recalculated in ACT-01-001/ACT-01-005. The A0 development board is checked against the same table, and any shortfall is recorded as a limitation.

---

## 1. Purpose

This document is the **datasheet-style specification** of the Kritva motor controller. It sets the electrical ratings, interfaces, protections and environmental limits that the A1 PCB design (`hardware/motor_controller/custom_pcb/`) must meet, and against which the A0 board is assessed.

## 2. Sizing basis

The values come from `mechanical/calculations/TORQUE_AND_SPEED.md` (20:1, η = 0.85):

| Item | Value |
|---|---|
| Motor torque: hold / continuous / peak 20 / peak 25 | 0.358 / 0.588 / 1.176 / 1.471 N·m |
| Motor speed at 45 RPM output | 900 RPM |

Phase current I = T_motor / Kt, using the conventions in `mechanical/calculations/TORQUE_AND_SPEED.md` §2.1: Kt in N·m per A phase-peak; thermal ratings use RMS = peak/√2. The Kt values below are illustrative (TBC). The selected motor's datasheet values are converted with that table, then replaced by the A0 measurements (MC-01–MC-04) before E2:

| Kt (N·m/A) | Continuous | Peak 25 N·m |
|---|---|---|
| 0.05 | 11.8 A | 29.4 A |
| 0.08 | 7.4 A | 18.4 A |
| 0.12 | 4.9 A | 12.3 A |

**Design target (TBC).** These targets cover a motor with Kt ≥ 0.06 N·m/A:

- **≥ 12 A continuous** and **≥ 25 A peak (≥ 2 s)** phase current;
- power-stage rating ≥ 1.5 × peak (MOSFET continuous rating at the actual case temperature).

## 3. Electrical ratings

| Parameter | Minimum | Typical | Maximum | Unit | Notes |
|---|---|---|---|---|---|
| Supply voltage, operating | 20 | 24 | 28 | V | Proposed (TBC) |
| Supply voltage, withstand (including regeneration transients) | — | — | 32 (≥ 36 design target) | V | MOSFETs and capacitors rated 40–60 V |
| Reverse-polarity protection | Yes | — | −28 V | V | No damage |
| Phase current, continuous | 12 | — | — | A (peak of sinusoid) | TBC with the motor |
| Phase current, peak (≥ 2 s) | 25 | — | — | A | TBC |
| Hardware overcurrent trip | — | 1.2 × peak setting | — | A | < 10 µs response (TBC) |
| PWM frequency | 16 | 20 | 40 | kHz | Configurable |
| Dead time | — | Per the driver and MOSFETs | — | ns | Configurable |
| Current-sense range | ±30 | — | — | A | Resolution ≤ 15 mA/LSB (12-bit, TBC) |
| Current-sense bandwidth | ≥ 100 | — | — | kHz | Amplifier |
| Bus-voltage measurement | 0 | — | 40 | V | ±1 % accuracy (TBC) |
| Quiescent power (enabled, no load) | — | — | 2 | W | TBC |
| Logic supply | — | 3.3 / 5 | — | V | Internal |

## 4. Interfaces

| Interface | Specification | Connector (proposed) |
|---|---|---|
| Power input | 24 V, 2-pin, locking, polarised; rated ≥ 15 A | XT30 or a locking Molex-type equivalent (TBC) |
| Motor phases | 3-wire, rated ≥ 25 A peak | Screw terminals or soldered pads (TBC) |
| Motor feedback | Hall (3 × open-collector with pull-ups, 5 V) and/or encoder SPI/ABI (3.3 V) | JST-GH or similar locking connector |
| Output encoder | SPI (CS, CLK, MISO, MOSI), 3.3 V, GND, shield; cable ≤ 150 mm | Locking connector |
| Motor thermistor | 2-wire NTC | Shared with the feedback connector |
| CAN | CAN_H, CAN_L, GND (+ optional 24 V pass-through, TBC); 120 Ω selectable | 2 × locking connectors (daisy chain) |
| USB/UART | USB-C (CDC) or a 3.3 V UART header | — |
| SWD | 10-pin Cortex debug header | — |
| E-stop / enable | 2-wire, normally-closed loop, fail-safe (a wire break means e-stop) | Locking connector |
| Status | RGB or 2 × LED | — |

## 5. Protection functions

| Function | Implementation | Response | Requirement |
|---|---|---|---|
| Hardware overcurrent | Comparator → PWM break | < 10 µs (TBC) | SAF-REQ-030 |
| Software overcurrent | Firmware | 3 samples | SAF-REQ-031 |
| Gate-driver UVLO and faults | Driver | Immediate | CTRL-REQ-003 |
| Overvoltage | Firmware plus TVS/clamp (± brake chopper) | 1 ms | SAF-REQ-037 |
| Undervoltage | Firmware plus UVLO | 10 ms | FW fault table |
| Overtemperature | NTCs plus firmware | 10–100 ms | SAF-REQ-032 |
| Reverse polarity | Ideal-diode / P-FET | Passive | SAF-REQ-034 |
| Input overcurrent | Fuse (rating TBD) | Passive | SAF-REQ-033 |
| E-stop | Hardware gate-enable removal | ≤ 10 ms | SAF-REQ-055 |
| Watchdog | Independent WDG; gates default off | ≤ 20 ms | SAF-REQ-024 |
| ESD | TVS on external lines (CAN, encoder, USB) | Passive | SAF-REQ-072 |

## 6. Environmental and mechanical

| Parameter | Value |
|---|---|
| Operating ambient | 0–40 °C (TBC) |
| MOSFET case temperature limit | ≤ 100 °C at continuous load (TBC) |
| Cooling | Conduction to the aluminium housing through a thermal pad |
| Board size | To fit the rear envelope (DEP-009) |
| Mounting | ≥ 3 screws; no stress on the connectors |

## 7. A0 development-board compliance check

The selected development board is compared row by row with sections 3–5. Deviations are recorded here as limitations, with their mitigations. For example: "no hardware overcurrent — mitigated by the PSU current limit set at X A".

| Row | Requirement | Board value | Compliant? | Mitigation |
|---|---|---|---|---|
| | | | | |

## 8. Verification

| Item | Method | Record |
|---|---|---|
| Phase-current capability (continuous, peak) | Bench test on a locked-rotor fixture with thermal monitoring | `results/motor_control/`, `results/thermal/` |
| Overcurrent trip time | Oscilloscope, injected trip (FI-01) | `results/motor_control/` |
| E-stop response | FI-14 | `tests/safety/` |
| Reverse polarity | Current-limited PSU test | `results/integration/` |
| Thermal at continuous | 30 min at the continuous current | `results/thermal/` |

## 9. Open items

| # | Item | Owner | Needed by |
|---|---|---|---|
| 1 | Final current ratings from the selected motor | Electronics/Embedded Intern | E2 |
| 2 | Connector selection | Electronics/Embedded Intern + Mechanical Intern | E2 |
| 3 | Fuse rating | Electronics/Embedded Intern | E2 |
| 4 | Development-board compliance table (§7) | Electronics/Embedded Intern | E1 |

## 10. Revision history

| Rev | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-11 | Kritvaos Actuator Team | Initial draft |
| 0.2 | 2026-10-12 | Kritvaos Actuator Team | Reference motor-constant conventions; measured Kt before E2 (EXT-AUD-008) |
