# hardware/

Electronics implementation of the Kritva Actuator. Owner: **Electronics/Embedded Intern**. Reviewer for safety-critical items (power stage, protections, e-stop path): **Independent Electrical/Firmware Reviewer**.

Design documents: [docs/electronics/](../docs/electronics/). Requirements: [requirements/ELECTRICAL_REQUIREMENTS.md](../requirements/ELECTRICAL_REQUIREMENTS.md).

| Folder | Contents |
|---|---|
| `motor_controller/development_board/` | A0 development-board configuration: jumper and solder-bridge settings, pin map, modifications, board documentation links, the selected-board record (ACT-DEC-005) |
| `motor_controller/custom_pcb/schematics/` | A1 controller schematic source (KiCad proposed, TBC) and PDF exports per revision |
| `motor_controller/custom_pcb/pcb/` | Layout source, stack-up, design-rule settings |
| `motor_controller/custom_pcb/manufacturing/` | Released Gerber/drill/pick-and-place/BOM zip per revision (Git LFS), assembly notes |
| `power_stage/` | Inverter, gate-driver and input-protection design notes and calculations (MOSFET losses, shunt sizing, fuse) |
| `sensing/` | Current sensing, encoder interfaces, temperature sensing, output-encoder PCB |
| `connectors/` | Connector pin-outs and cable drawings (power, motor, feedback, encoder, CAN, e-stop) |
| `bom/ELECTRICAL_BOM.csv` | Electrical BOM; schema in [scripts/bom/README.md](../scripts/bom/README.md); run `make check-bom` |

## Part numbering

| Part number | Part |
|---|---|
| KA-ELE-0001 | Controller PCB |
| KA-ELE-0002 | Output-encoder PCB |

PCB revisions use letters (A, B, ...). Each released revision has a tag and a manufacturing zip.

## Rules

1. **Before fabrication:** pass the schematic and PCB review E2, recorded in `audit/electronics/ELECTRONICS_DESIGN_AUDIT.md`.
2. **Bring-up** follows [docs/electronics/HARDWARE_BRINGUP.md](../docs/electronics/HARDWARE_BRINGUP.md). The records go to `results/motor_control/`.
3. **Power-stage sizing** comes from the motor current, never from the supply voltage alone (SYS-REQ-044).
4. **Never commit** generated fabrication outputs outside `manufacturing/`, and never commit KiCad backups (see `.gitignore`).
