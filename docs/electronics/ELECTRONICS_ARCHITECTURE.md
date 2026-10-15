# Kritva Actuator: Electronics Architecture

| Field | Value |
|---|---|
| Document ID | KA-DOC-ELEC-ARCH |
| Repository | `KritvaOS/kritva-actuator` |
| Revision | 0.1 (Draft: proposed, pending approval) |
| Date | 2026-10-11 |
| Document owner | Electronics/Embedded Intern |
| Reviewer / Approver | Independent Electrical/Firmware Reviewer / Project Lead |
| Applies to | A0 (development board), A1 (custom PCB) |
| Classification | Proprietary and confidential |

> **Status note.** The MCU family (STM32G4 proposed, ACT-DEC-004), the A0 development board (ACT-DEC-005) and all component choices are **proposed**. Part numbers are candidates and must be verified against their datasheets. Ratings depend on the motor still to be selected.

---

## 1. Purpose

This document describes the electronics architecture that implements `requirements/ELECTRICAL_REQUIREMENTS.md`. It covers:

- the A0 bench configuration based on a development board;
- the A1 custom controller PCB architecture;
- power-tree, sensing, communication and safety chains;
- the **A0 development-board selection record** (task ACT-01-002a, gate E1).

## 2. A0 configuration (development board)

```
  Bench PSU 24 V (current-limited, >= 10 A capable)
      |
  [E-stop relay, DC-rated] -- latching e-stop button (SAF-REQ-058)
      |
  [Inline fuse] --> MOTOR-CONTROL DEVELOPMENT BOARD (MCU + gate driver + inverter + shunts)
                        |  U V W                       | SWD / USB-UART
                        v                              v
                    BLDC/PMSM motor on fixture       Linux PC: host tools
                        |  Halls / motor encoder
                        +--> board encoder input
```

| Function | A0 provision |
|---|---|
| Inverter, gate driver, current sensing | On the development board |
| MCU | On the board (STM32G4-class preferred, to match ACT-DEC-004) |
| Hardware overcurrent | The board's comparator or break input if present. If absent, this is a **recorded limitation**, mitigated by the PSU current limit |
| E-stop | A relay in the 24 V line, operated by a latching e-stop button |
| Feedback | Motor Halls and/or a motor-side magnetic encoder; output encoder added for gearbox tests |
| Communication | USB/UART to the host PC |

## 3. A1 custom controller PCB

### 3.1 Block diagram

```
 24 V in --[fuse]--[reverse-polarity: ideal-diode / P-FET]--[TVS]--[bulk C + film C]--+--> inverter DC bus
                                                                                     |
                     +--------------------------- 5 V buck --> 3.3 V LDO ---------> MCU, sensors, CAN
                     |
 E-stop/enable in ---+--> gate-driver ENABLE (hardware AND with MCU enable) + MCU monitor input
                                     |
     MCU (STM32G4-class) -- 6x PWM --> 3-phase gate driver (bootstrap, dead time, UVLO, nFAULT)
          |                                    |
          | ADC <-- shunt amplifiers <-- 3x low-side shunts (or 2 + reconstruction)
          | COMP/break <-- overcurrent comparator (hardware trip)
          | ADC <-- Vbus divider, NTC (MOSFET), NTC (board), motor thermistor (if fitted)
          | SPI1 <-- output encoder (via cable from the stationary encoder PCB)
          | SPI2/ABI/Hall <-- motor-side feedback
          | FDCAN <-> CAN transceiver (+ selectable 120 ohm) <-> CAN connector
          | USART/USB <-> debug connector
          | SWD <-> programming header
          | GPIO: status LED, HW revision straps
          v
     MOSFET half-bridges x3 --> U V W --> motor
     [optional brake chopper / clamp on DC bus for regeneration]
```

### 3.2 Key design choices (proposed)

| Topic | Proposal | Rationale | Reference |
|---|---|---|---|
| MCU | STM32G4 family (for example STM32G431 or STM32G474, candidate) | Motor-control timers, fast ADCs, comparators, FDCAN | ACT-DEC-004 |
| Gate driver | 3-phase driver with integrated dead time, UVLO and a fault output (a smart driver with SPI configuration is optional) | Protection and simplicity | ELEC-REQ power stage |
| MOSFETs | 40–60 V rated, low R_DS(on), current rating ≥ 1.5 × peak phase current (TBC with the motor Kt) | 24 V bus plus regeneration margin (≥ 32 V withstand) | ELEC-REQ power stage |
| Current sensing | 3 low-side shunts with differential amplifiers, sampled at the PWM centre | Robust FOC current reconstruction | ELEC-REQ current sensing |
| Hardware overcurrent | Comparator on the summed or individual shunt signals, driving the PWM break input | Firmware-independent trip, < 10 µs (TBC) | SAF-REQ-030 |
| E-stop | Hardware AND between the e-stop chain and the MCU enable at the gate-driver enable pin; the e-stop is also read by the MCU | Firmware-independent motor-power removal | SAF-REQ-055 |
| Regeneration | Firmware bus-voltage limiting, plus a TVS or clamp; a brake-chopper footprint (optional fit) | HAZ-012 | SAF-REQ-037 |
| CAN | Transceiver with a selectable 120 Ω termination; isolation not fitted for A1 (TBC) | IF-REQ CAN | ACT-DEC-006 |
| Logic power | 24 V → 5 V buck → 3.3 V LDO for the analog and MCU rails | Noise and efficiency | — |
| Form factor | Circular or rectangular board within the rear envelope agreed with mechanical (DEP-009) | Integration | ACTUATOR_ARCHITECTURE §7 |

## 4. Power tree and budget

The canonical power budget is in ELECTRICAL_REQUIREMENTS §5.3. Summary:

- Continuous input ≈ **76 W (≈ 3.2 A at 24 V)**.
- Peak at 25 N·m and 45 RPM ≈ **198 W (≈ 8.2 A at 24 V)**.
- Phase current depends on Kt (TORQUE_AND_SPEED §4). With Kt = 0.08 N·m/A at 20:1, it is about **7.4 A continuous and 18.4 A peak**.

| Rail | Consumers | Estimate | Note |
|---|---|---|---|
| 24 V bus | Inverter | Up to the peak phase power | Fused |
| 5 V | Gate driver (if needed), encoders (if 5 V), CAN transceiver | < 0.5 W | |
| 3.3 V | MCU, encoders (3.3 V), amplifiers | < 0.5 W | Analog rail filtered |

## 5. Sensing chain

| Signal | Sensor | Interface | Rate | Notes |
|---|---|---|---|---|
| Phase currents | Shunts + amplifiers | ADC, synchronous | 20 kHz | Offsets calibrated at boot with the PWM off |
| Bus voltage | Divider | ADC | 20 kHz | Used for duty normalisation and over/undervoltage |
| MOSFET temperature | NTC near the MOSFETs | ADC | 100 Hz | |
| Board temperature | NTC | ADC | 10 Hz | |
| Motor temperature | Motor thermistor if fitted; otherwise a thermal model | ADC | 100 Hz | SAF-REQ-032 |
| Motor position | Halls and/or a magnetic encoder | GPIO / ABI / SPI | 20 kHz | Commutation |
| Output position | Absolute magnetic encoder (candidate ICs such as AS5047P, AS5048A or MT6835; verify) | SPI | 1–2 kHz | Stationary PCB near the output bearing |

## 6. A0 development-board selection record (ACT-01-002a, E1)

**Status: OPEN.** Scored against ELECTRICAL_REQUIREMENTS §7.2. Fill this in from datasheets and quotations only.

| Criterion (weight) | B-G431B-ESC1 | NUCLEO-G474RE + X-NUCLEO-IHM08M1-class | ODrive-class reference |
|---|---|---|---|
| 1 24 V compatibility (3, gate) | | | |
| 2 Phase-current rating vs motor (3, gate) | | | |
| 3 Current sensing for FOC (3, gate) | | | |
| 4 MCU family alignment (3) | | | |
| 5 Encoder/Hall interfaces (3, gate) | | | |
| 6 Hardware overcurrent / break (2) | | | |
| 7 Debug access (2, gate) | | | |
| 8 CAN availability (1) | | | |
| 9 Documentation and licence (2) | | | |
| 10 Availability in India (2, gate) | | | |
| 11 Cost (2) | | | |
| 12 Physical robustness (1) | | | |
| 13 Transferability to the A1 PCB (2) | | | |
| 14 Learning value (1) | | | |
| **Weighted total** | | | |
| Gate failures | | | |
| Recommendation | | | |

**Notes for evaluators.**

- Small ESC-type boards may have continuous current limits below the high-Kt/low-Kv motor needs at peak torque. Check them against TORQUE_AND_SPEED §4 (RISK-005).
- A two-board Nucleo set-up gives the most flexible pin access, but needs careful wiring for current-sense integrity.
- ODrive-class hardware is valuable as a **reference**. Firmware reuse needs the licence review (FW-REQ-074).

The proposed decision text for ACT-DEC-005 is written here once the table is complete.

## 7. Grounding, EMC and layout principles (A1)

1. Keep the high-current loop small: bulk/film capacitor → high-side FET → low-side FET → shunt → back to the capacitor.
2. Use **Kelvin connections** on the shunts. Route the amplifier inputs as differential pairs, away from the switch nodes.
3. Use a star or partitioned ground: power ground and analog ground join at the shunt or capacitor return, under control.
4. Use short, shielded encoder cables, terminated and ESD-protected at the connector.
5. Twist the CAN pair. Termination is only at the bus ends.
6. Provide a thermal path from the MOSFETs to the aluminium housing through a thermal pad.
7. Provide test points for every rail, every PWM phase, the shunt signals, Vbus, SPI and CAN.

## 8. Open items

| # | Item | Owner | Needed by |
|---|---|---|---|
| 1 | Complete the development-board selection (§6) and ACT-DEC-005 | Electronics/Embedded Intern | E1 |
| 2 | Confirm ACT-DEC-004 (MCU) | Electronics/Embedded Intern | E1 |
| 3 | Size the MOSFETs, shunts and fuse from the selected motor Kt and R | Electronics/Embedded Intern | E2 |
| 4 | Decide on CAN isolation | Project Lead | E2 |
| 5 | PCB envelope agreed with mechanical | Both interns | E2 |
| 6 | Brake chopper fitted or not (regeneration test result) | Electronics/Embedded Intern | E3 |

## 9. Revision history

| Rev | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-11 | Kritvaos Actuator Team | Initial draft |
