# Kritva Actuator: Calibration Procedure

| Field | Value |
|---|---|
| Document ID | KA-DOC-FW-CAL |
| Repository | `KritvaOS/kritva-actuator` |
| Revision | 0.1 (Draft: proposed, pending approval) |
| Date | 2026-10-11 |
| Document owner | Electronics/Embedded Intern |
| Reviewer / Approver | Independent Electrical/Firmware Reviewer / Project Lead |
| Applies to | A0 (motor), A1 (motor + output) |
| Classification | Proprietary and confidential |

> **Status note.** This procedure is proposed. Calibration currents and tolerances are TBC with the selected motor and encoders. Calibration is a recorded hazard (HAZ-015), so it must follow this procedure exactly.

---

## 1. Purpose and when to calibrate

This document defines how to calibrate:

- motor electrical parameters;
- motor-encoder electrical offset and direction;
- output-encoder zero and direction;
- optionally, cogging and gravity compensation.

It also defines how results are stored and recorded. It implements FW-REQ-020 to 026 and IF-REQ-135.

**Calibration is required:**

1. at first assembly;
2. after any change to the motor, the encoder, the magnet, the phase wiring or the gearbox;
3. after a firmware major-version change that alters the calibration format;
4. whenever `CALIBRATION_INVALID` is reported.

## 2. Safety conditions (SAF-REQ-013)

- The actuator is mounted on the **restrained fixture**. The **output is free** (no arm or load) for steps C1–C4 unless a step says otherwise.
- Calibration runs only in the DISABLED.CALIBRATING sub-state, at a current limited to ≤ 30 % of the rated current (TBC). The PSU current limit is set according to `HARDWARE_BRINGUP.md`.
- The e-stop is within reach. Nobody is inside the clear zone.

## 3. Procedure

| Step | Name | Command | Method | Pass criterion | Stored parameters |
|---|---|---|---|---|---|
| C0 | Pre-check | `state`, `faults` | DISABLED; no faults; Vbus in range; encoders valid | All OK | — |
| C1 | Phase R and L | `cal MOTOR_RL` | DC injection on the d-axis at a known current for R; voltage step and current-slope measurement for L | R and L within 10 % of the LCR meter or datasheet (TBC); repeatability ≤ 3 % over 3 runs | `motor_phase_resistance`, `motor_phase_inductance` |
| C2 | Pole pairs and direction | `cal DIRECTION_CHECK` | Rotate an open-loop vector one electrical revolution forwards and back; compare with the encoder change | Measured pole pairs equal the datasheet value; direction sign determined | `motor_direction`, `motor_pole_pairs` check |
| C3 | Motor encoder electrical offset | `cal MOTOR_OFFSET` | Lock the rotor to the d-axis at the calibration current at several electrical angles in both directions; average; correct for hysteresis | Repeatability ≤ 2° electrical over 5 runs (TBC) | `motor_encoder_offset` |
| C4 | Closed-loop verification | `tor` (small) | Small Iq command, output free: the rotor turns smoothly in the expected direction | Id ≈ 0 ± 5 % rated; positive Iq gives positive velocity | — |
| C5 | Output encoder zero (A1) | `cal OUTPUT_ZERO` | Place the joint at the **reference pose** using the fixture datum (full extension, q = 0) and store the offset | After a power cycle, the reported q at the datum is within the accuracy limit (approved before the test) | `output_encoder_offset` |
| C6 | Output direction and ratio check (A1) | `cal DIRECTION_CHECK` (output) | Move slowly into flexion; confirm that q increases, and that Δq ≈ Δmotor_pos/N | Positive flexion gives increasing q; ratio error ≤ 1 % (excluding backlash) | `output_direction` |
| C7 | Backlash measurement (A1) | Host script | Lock the output on the fixture; apply ±small torque; measure motor_pos − N·q hysteresis | Recorded; used for `backlash_tolerance` (CTRL-REQ-005) | `backlash_tolerance` |
| C8 | Hard-stop and soft-limit check (A1) | Host script, low speed | Move slowly to each soft limit (at ≤ 10 % v_max); confirm the hard-stop angles are outside the soft limits by the margin | Margins ≥ configured | `q_min_soft`, `q_max_soft`, `q_hard_*` verified |
| C9 | Gravity feed-forward (optional) | Host script | Hold several poses; record the holding Iq; fit m_eq·g·r_eq and the offset | Fit residual recorded | `gravity_ff_*` |
| C10 | Cogging map (optional, A2) | Host script | Slow constant-speed sweep; record Iq versus angle | Ripple reduction recorded | Cogging LUT |
| C11 | Save | `save` | Two-copy NVM write with CRC; validity flag set | Read-back CRC matches | All of the above |

## 4. Records

Store each calibration under `results/motor_control/YYYY-MM-DD_CAL_<serial>/`. The record contains:

- actuator serial, hardware revision, firmware version and hash;
- operator and date;
- the motor, gearbox and encoder serial numbers;
- every measured value and the stored parameter, plus the pass/fail of each step;
- a configuration CRC after saving.

The host tool exports a JSON calibration file, which is committed alongside the record (FW-REQ-026).

## 5. Failure handling

- Any step failure leads to: no save, the validity flag left cleared, `CALIBRATION_INVALID` reported, and enable blocked.
- If repeatability is not met: check the magnet bonding and air gap, the encoder supply and the wiring. Re-run.
- If the direction is unexpected: **do not** compensate by swapping signs in random places. Use the documented `motor_direction` and `output_direction` parameters only, and record why the direction differs.

## 6. Revision history

| Rev | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-11 | Kritvaos Actuator Team | Initial draft |
