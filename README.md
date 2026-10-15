# Kritva Actuator Embedded

Proprietary and confidential. Copyright (c) 2026 Kritvaos. All rights reserved.

Child repository of `KritvaOS/kritva-actuator` (the parent). Owner: Embedded Intern.

**Status: Concept.** Firmware, controller hardware, electronics and firmware documents for the whole actuator family (S, M, L). Firmware is one code base with a per-variant configuration (motor, gear ratio, limits), not three forks.

The common interface (`ACTUATOR_INTERFACE.md`), CAN protocol, units and requirements are owned by the parent and are **not** redefined here.

## Layout

| Folder | Content |
|---|---|
| `firmware/` | foc, encoder, joint_control, motor_control, diagnostics, communication, platform |
| `firmware/variants/` | Per-variant configuration for S, M, L |
| `hardware/` | Development board notes, power stage, sensing, connectors, custom PCB (schematics, pcb, manufacturing), `bom/ELECTRICAL_BOM.csv` (prefix `EB-NNN`) |
| `docs/electronics/`, `docs/firmware/` | Electronics and firmware documents (migrated from the parent at Stage 4) |
| `communication/can/` | CAN firmware layer |
| `tests/` | Unit, firmware, hardware tests |
| `results/` | Raw bring-up and characterisation evidence |
| `scripts/` | Vendored checks (`check_bom.py`) |

## Workflow

1. Branch, pull request, owner and independent reviewer approval (ACT-DEC-014).
2. `make check` must pass.
3. Power-stage and motor-control safety are not self-approved.
4. Loaded and fault tests only on a restrained, guarded, instrumented fixture.
