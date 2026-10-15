# Kritva Actuator: Motor and Joint Control Design

| Field | Value |
|---|---|
| Document ID | KA-DOC-FW-MOTOR |
| Repository | `KritvaOS/kritva-actuator` |
| Revision | 0.1 (Draft: proposed, pending approval) |
| Date | 2026-10-11 |
| Document owner | Electronics/Embedded Intern |
| Reviewer / Approver | Independent Electrical/Firmware Reviewer / Project Lead |
| Applies to | A0, A1 |
| Classification | Proprietary and confidential |

> **Status note.** This is the proposed control design. Gains are computed from the measured motor parameters (R, L, Kt, J) once the motor is selected. The example numbers below are illustrative only.

---

## 1. Purpose

This document describes the control algorithms:

- the FOC current loop;
- velocity and position estimation;
- the velocity and position loops;
- the trajectory limiter and soft limits;
- the torque estimate;
- I²t and regeneration limiting;
- gain design and tuning.

It implements the CTRL-REQ items in `requirements/FIRMWARE_REQUIREMENTS.md`.

## 2. Control structure (cascade)

```
 q_cmd -> [trajectory limiter: v_max, a_max, soft limits, approach-speed limit]
       -> q_ref, dq_ref
       -> [position loop: P (+ D on velocity error), 1 kHz] -> dq* (+ dq_ff)
       -> [velocity loop: PI, 2 kHz] -> Iq* (+ Iq_ff from tau_ff and gravity_ff) -> [Iq limit, I2t]
       -> [current loop: PI d/q, 20 kHz, Id* = 0] -> Vd, Vq -> [voltage limit + anti-windup]
       -> inverse Park -> SVPWM -> inverter -> motor -> gearbox -> joint
 feedback: Ia, Ib, Ic -> Clarke/Park (theta_e from motor feedback)
           motor_vel -> /N -> dq_est ; output encoder -> q
```

Modes (INTERFACE_REQUIREMENTS §8.8):

- **POSITION** uses the full cascade.
- **VELOCITY** bypasses the position loop.
- **TORQUE** sets Iq* = τ / (Kt · N · η_model), with the speed and position limits still active.

## 3. FOC current loop

### 3.1 Transforms (amplitude-invariant)

```
Clarke:   Iα = Ia ;  Iβ = (Ia + 2·Ib)/√3          (with Ia + Ib + Ic = 0; 3-shunt: use the two best phases per sector)
Park:     Id =  Iα·cosθe + Iβ·sinθe
          Iq = −Iα·sinθe + Iβ·cosθe
Inverse:  Vα = Vd·cosθe − Vq·sinθe ;  Vβ = Vd·sinθe + Vq·cosθe
```

### 3.2 PI gain design (pole-zero cancellation)

For a phase with resistance R and inductance L, choose the closed-loop bandwidth ω_c (≥ 2π·1 kHz, CTRL-REQ-011). Then:

```
Kp = L · ω_c        Ki = R · ω_c        (Ki in V/(A·s))
```

Discrete implementation at T_s = 50 µs, with integrator clamping (anti-windup) when the voltage vector saturates. The PWM and computation delay (≈ 1.5 T_s) limits ω_c in practice to about ω_s/10–ω_s/20. At 20 kHz that is about 1–2 kHz.

**Example (illustrative).** With R = 0.3 Ω, L = 150 µH and ω_c = 2π·1000 rad/s, the gains are Kp ≈ 0.94 V/A and Ki ≈ 1 885 V/(A·s).

### 3.3 Voltage limiting and modulation

- SVPWM, with the voltage limit V_max = V_bus/√3 (linear region), normalised by the measured V_bus every cycle (CTRL-REQ-016).
- Circular limiting: when |Vdq| > V_max, scale Vq after prioritising Vd, and stop both integrators.

### 3.4 Commutation angle

θ_e = p · (motor_pos − offset) · direction, from the motor encoder or Halls (CTRL-REQ-014). With Halls only, θ_e is extrapolated between transitions using the estimated speed, above a minimum speed (TBC). Below that speed, the 60° sector centre is used.

## 4. Estimation

| Quantity | Method | Notes |
|---|---|---|
| Motor velocity | PLL or tracking observer on the motor angle (bandwidth about 200–500 Hz, TBC) | Smoother than differentiation |
| Output velocity | motor_vel / N | Primary, for the velocity loop |
| Output position | Output encoder q (absolute) | Position loop (A1). Compared with motor_pos/N for the cross-check |
| Torque | τ_est = Kt · Iq · N · η_model | Reported as an estimate (CTRL-REQ-017). Friction and backlash cause error, which is quantified in characterisation |

## 5. Velocity and position loops

### 5.1 Velocity loop (2 kHz)

- PI controller: Iq* = Kp_v·e_v + Ki_v·∫e_v, with anti-windup at the Iq limit.
- Design: the inertia seen at the motor is J_m = J_rotor + J_arm/N². The velocity bandwidth target is about 50–100 Hz (TBC), well below the current loop.
- **Example (illustrative).** J_arm = 0.171 kg·m² and N = 20 give J_arm/N² = 4.3 × 10⁻⁴ kg·m², plus the rotor J. The load dominates over a small rotor, so retune when the payload changes (gain scheduling is optional).

### 5.2 Position loop (1 kHz)

- P controller on the position error with velocity feed-forward: dq* = Kp_p·(q_ref − q) + dq_ref. Optional damping on the velocity error.
- Bandwidth about 5–15 Hz (TBC), limited by backlash and compliance. Backlash can cause limit cycles, so add a **small dead-band or a reduced gain inside ±backlash** (configurable, TBC).

### 5.3 Gravity feed-forward (optional, CTRL-REQ-026)

```
τ_g_ff = m_eq · g · r_eq · sin(q + q_offset)
```

Using the conventions document, at full extension (q = 0, forearm hanging down) the gravity torque is 0. It is maximal at q = 90°: the m·g·r product is 6.08 N·m for the baseline load. The actual model is calibrated on the fixture.

## 6. Trajectory limiter and soft limits

- **Trapezoidal profile.** The profile is limited by v_max (≤ 4.712 rad/s) and a_max (TBC). S-curve jerk limiting is optional.
- **Soft limits.** The target is clamped to [q_min_soft, q_max_soft]. The velocity towards a limit is capped at v_lim = sqrt(2·a_max·d) (CTRL-REQ-032), and additionally capped to `v_limit_zone` within `v_limit_zone_angle` of a limit. The proposal is 50 % of v_max within 10°. This keeps the stop energy within the bumper capacity: ≤ 29 RPM for a 2 mm / 25 mm bumper (LOAD_CASES §8).
- **Hard stops** are the last line of defence and are never part of normal control.

## 7. Limits and protections in the control path

| Limit | Implementation |
|---|---|
| Phase current | Iq* clamp at i_max_phase; Id controlled to 0 |
| Output torque | Iq* clamp equivalent to tau_max (≤ the approved peak) |
| I²t | Integrator of (Iq² − I_cont²). Above the threshold, the current limit is reduced to I_cont until it recovers (CTRL-REQ-033) |
| Velocity | Trajectory and velocity-command clamp; `VELOCITY_LIMIT` fault at 1.2 × v_max |
| Regeneration | If V_bus > the warning threshold, limit the regenerative current: restrict the negative power by clamping the Iq that opposes the motion (CTRL-REQ-018) |
| Tracking error | `TRACKING_ERROR` if \|q_ref − q\| > threshold for longer than time |

## 8. Tuning procedure (summary)

1. **Current loop.** Compute Kp and Ki from the measured R and L. Verify with an Iq step on the locked rotor (rise time and overshoot per CTRL-REQ-011). Capture at 20 kHz.
2. **Velocity loop.** Start with a low gain. Step 0 → 900 RPM (motor) unloaded, then with the arm on the fixture. Raise the gain until the overshoot is about 10 %, then back off by 30 %.
3. **Position loop.** Use small steps of 5–10° on the fixture with the arm. Tune Kp_p for settling ≤ 150 ms (TBC) without oscillation. Check the behaviour around backlash.
4. **Record** all gains, the conditions and the plots in `results/motor_control/`. Store the gains in the configuration.

## 9. Open items

| # | Item | Owner | Needed by |
|---|---|---|---|
| 1 | Measured R, L, Kt, rotor J | Electronics/Embedded Intern | ACT-01-002b |
| 2 | Bandwidth targets confirmed | Electronics/Embedded Intern + Project Lead | F1 |
| 3 | Backlash handling strategy, after the gearbox is measured | Electronics/Embedded Intern | ACT-01-003 |
| 4 | a_max value (SYS-REQ-013) | Project Lead | Before tuning with the arm |

## 10. Revision history

| Rev | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-11 | Kritvaos Actuator Team | Initial draft |
