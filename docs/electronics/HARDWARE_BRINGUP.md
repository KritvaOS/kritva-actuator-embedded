# Kritva Actuator: Hardware Bring-Up Procedure

| Field | Value |
|---|---|
| Document ID | KA-DOC-ELEC-BRINGUP |
| Repository | `KritvaOS/kritva-actuator` |
| Revision | 0.1 (Draft: proposed, pending approval) |
| Date | 2026-10-11 |
| Document owner | Electronics/Embedded Intern |
| Reviewer / Approver | Independent Electrical/Firmware Reviewer / Project Lead |
| Applies to | A0 (development board), A1 (custom PCB) |
| Classification | Proprietary and confidential |

> **Status note.** This is a proposed procedure. Current limits and thresholds are TBC with the selected board and motor. **Do not skip steps or increase limits until the previous step passes and is recorded.** It follows the staged approach in SAFETY_REQUIREMENTS (SAF-REQ-063/066).

---

## 1. Purpose

This document gives a safe, staged procedure for bringing up:

- the A0 development board with the selected motor;
- later, the A1 custom PCB, in the same order and with extra board-level checks.

Each step has a **pass criterion** and a **record**, stored in `results/motor_control/YYYY-MM-DD_BU-<step>_<board>/`.

## 2. Bench setup

```
 [Bench PSU 24 V, adjustable current limit]
        | (+)                                  [Latching e-stop] --controls--> [DC-rated relay]
        +--> [DC relay contact] --> [inline fuse] --> board V+          |
        | (-) --------------------------------------> board GND
 board U V W --> motor (clamped to the fixture; output free or on the fixture)
 board SWD/USB --> PC (host tools, debugger)
 Instruments: oscilloscope (with an isolated or differential probe for the switch nodes),
              current probe (DC, >= 30 A), DMM, thermocouple reader / IR thermometer
```

**Rules:**

- The motor must be **clamped**. The output is free (no arm) until step BU-09.
- Use safety glasses.
- The e-stop must be within reach and must be tested **before** the first power-up.
- Use a fire-safe bench, with an extinguisher available (SAF-REQ-070).
- Work with two people for any loaded step (SAF-REQ-064).

## 3. Record template (every step)

| Field | Value |
|---|---|
| Step ID | BU-NN |
| Date, operator, observer | |
| Board / PCB revision and serial | |
| Motor model and serial | |
| Firmware version and git hash | |
| PSU voltage / current limit | |
| Ambient temperature | |
| Instruments (ID, calibration) | |
| Result (measured values) | |
| Pass / fail against the criterion | |
| Notes and anomalies | |

## 4. Procedure

| Step | Action | Settings | Pass criterion |
|---|---|---|---|
| **BU-00 Inspection** | Visual check of the board, wiring and connector polarity; check the MOSFET orientation (A1); continuity checks; check for shorts between V+ and GND, and between each phase and the supply | Unpowered | No shorts (> 1 kΩ V+–GND with the capacitors charged as expected); correct polarity |
| **BU-01 E-stop test** | Power the relay circuit only; press and release the e-stop | — | The relay opens on press; it does not re-close on release without an explicit reset (latching) |
| **BU-02 First power, logic only** | Power on with the motor **disconnected** (A1: if possible, logic rails first from a separate supply) | PSU 24 V, **current limit 0.2 A** | Current within the board's quiescent specification; rails 5 V and 3.3 V within ±3 %; no hot components (touch or IR) |
| **BU-03 MCU and debug** | Connect SWD, flash the test firmware, blink the LED, open USB/UART | 0.2 A | Programming works; the CLI responds to `version`; the reset cause is reported |
| **BU-04 Sensing offsets** | PWM off; read the current-sense offsets, Vbus and NTCs | 0.2 A | Offsets within the expected range; Vbus reading within ±1 % of the DMM; temperatures plausible |
| **BU-05 PWM without motor** | Enable the PWM at a fixed 50 % duty on all phases, motor disconnected; scope the gates and phases | 0.3 A | Complementary signals; measured dead time as configured; no shoot-through (no current spike) |
| **BU-06 Protection checks** | Inject the hardware overcurrent trip (lowered threshold or test input); check the gate-driver fault reporting; check the watchdog (test build); check that the e-stop removes the PWM | 0.3 A | HW trip disables the gates < 10 µs (TBC); faults are reported; watchdog reset with the gates off; e-stop works (FI-01, FI-03, FI-13, FI-14) |
| **BU-07 Motor connected, open-loop** | Connect the motor; apply a low-voltage open-loop rotating vector (V/f) | **Current limit 1 A** | The motor rotates smoothly; phase currents are balanced (±10 %); the direction is recorded |
| **BU-08 Motor parameters and feedback** | Measure R and L (FW-REQ-020); check the Hall or encoder sequence; align the electrical offset (FW-REQ-021); measure Kv/Kt (back-EMF while spun by hand or by a drive motor) | 1–2 A | R and L within 10 % of the LCR meter; Hall sequence valid; offset repeatable within ≤ 2° electrical; Kt recorded |
| **BU-09 Closed-loop current (FOC)** | Iq steps of 10 %, 25 % and 50 % of the continuous current with the rotor locked on the fixture (short steps only) | Current limit raised to the continuous current only after BU-06 passes | Iq tracks its command; rise time and overshoot per CTRL-REQ-011; Id ≈ 0 |
| **BU-10 Velocity loop** | Unloaded speed steps up to the motor speed for 45 RPM output (900 RPM at 20:1) | Continuous current limit | Stable; overshoot ≤ 10 %; no audible instability |
| **BU-11 Position loop** | Position steps on the motor shaft (A0, ratio = 1), then with the gearbox and output encoder (A1) | As above | Settles without oscillation; tracking error recorded |
| **BU-12 Communication timeout and faults** | Pull the USB cable during motion; command out-of-range values; corrupt frames | — | Safe state within timeout + 5 ms (FI-11); invalid commands rejected (FI-20) |
| **BU-13 Thermal (continuous)** | Locked-rotor or dynamometer at the continuous current for 30 min (or until stable) | Continuous current | MOSFET/board/motor temperatures stabilise below their limits; warnings are raised before faults (FI-06) |
| **BU-14 Peak current** | Peak current pulses at the defined duration and repetition | Peak current, 2 s (TBC) | No fault except the expected I²t reduction; temperatures recorded |
| **BU-15 Regeneration** | Fast deceleration from maximum speed with an inertia load; backdrive test | — | Bus voltage ≤ 32 V (TBC) (FI-04) |

**A1-only additional steps** (before BU-02 on the custom PCB):

- **BU-A1:** check the bare-board impedance of each rail.
- **BU-A2:** reverse-polarity test on a current-limited supply (SAF-REQ-034).
- **BU-A3:** check that the fuse is fitted and rated.

## 5. Stop conditions

Stop immediately (e-stop), record the event, and do not continue until the cause is understood if any of these occur:

- smoke, a burning smell, or a component above 80 °C at logic-only power;
- unexpected motion, or motion in the wrong direction;
- supply current above the expected value for the step by more than 50 %;
- any protection failing to act in BU-06.

Each such event gets a non-conformance Issue (`test_failure` template).

## 6. Exit criteria (A0 bring-up complete)

BU-00 to BU-15 have passed with records, and their evidence is linked from `planning/v1/tasks/ACT-01/` (ACT-01-002). That evidence supports the A0 exit (MILESTONE.md) and gate E3.

## 7. Revision history

| Rev | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-11 | Kritvaos Actuator Team | Initial draft |
