# Kritva Actuator Embedded

> Firmware, controller hardware, electronics and firmware documents for the whole actuator family (S, M, L). One firmware code base with a per-variant configuration, not three forks. This is a private repository.

| Property | Value |
|---|---|
| Project | KritvaOS |
| Repository | `KritvaOS/kritva-actuator-embedded` |
| Repository Type | Firmware and electronics (child of the actuator parent repository) |
| Visibility Class | PRIVATE (future private; ACT-DEC-023, D-037, D-039 in kritva-program) |
| GitHub Setting | PUBLIC (verified 2026-10-18; temporary, ACT-DEC-023 amendments and D-028: owner action returns it to private) |
| Lifecycle Status | ACTIVE (concept stage; no firmware committed) |
| Repository Owner | Embedded Intern (role); Project Lead approves |
| Security Owner | Security Owner role ([SECURITY.md](SECURITY.md)) |
| Architecture | [docs/electronics/ELECTRONICS_ARCHITECTURE.md](docs/electronics/ELECTRONICS_ARCHITECTURE.md) and [docs/firmware/FIRMWARE_ARCHITECTURE.md](docs/firmware/FIRMWARE_ARCHITECTURE.md) |
| Milestones | [Parent planning/v1/MILESTONE.md](https://github.com/KritvaOS/kritva-actuator/blob/main/planning/v1/MILESTONE.md) and [parent planning/v2/ROADMAP_48_WEEKS.md](https://github.com/KritvaOS/kritva-actuator/blob/main/planning/v2/ROADMAP_48_WEEKS.md) |
| Tasks | [status/tasks.csv](status/tasks.csv) |
| Acceptance Criteria | [Parent audit/electronics/ELECTRONICS_ACCEPTANCE_AUDIT.md](https://github.com/KritvaOS/kritva-actuator/blob/main/audit/electronics/ELECTRONICS_ACCEPTANCE_AUDIT.md) and [parent audit/firmware/FIRMWARE_ACCEPTANCE_AUDIT.md](https://github.com/KritvaOS/kritva-actuator/blob/main/audit/firmware/FIRMWARE_ACCEPTANCE_AUDIT.md) |
| Status Reporting | [status/status.json](status/status.json) (generated) |
| License | [LICENSE](LICENSE) (proprietary, all rights reserved) |

This README follows the Kritva README standard (`v2/planning/standards/README_STANDARD.md` in [kritva-program](https://github.com/KritvaOS/kritva-program)). It is a navigation map; the documents it links own the detail. Proprietary and confidential. Copyright (c) 2026 Kritvaos. All rights reserved.

## 1. Purpose and Scope

Child repository of `KritvaOS/kritva-actuator` (the parent). It owns the actuator family's firmware, controller hardware (development board for A0, custom PCB for A1), power stage and sensing notes, electrical BOM, and the electronics and firmware design documents. Firmware is one code base with a per-variant configuration (motor, gear ratio, limits in `firmware/variants/`), not three forks.

**Status: Concept.** No firmware is committed yet. The folders for firmware, hardware, tests and results exist as scaffolding.

**Implementation state.** IMPLEMENTED today: the electrical BOM check (`scripts/check_bom.py`), the status generator and its tests, the commit message checker, the README check, the CI workflows, the electrical BOM file, and the electronics and firmware design documents (as documents; the electronics architecture document is OPEN, not complete). NOT YET IMPLEMENTED: all firmware (`firmware/`), the custom PCB design, the development-board configuration record, the unit, firmware and hardware tests, the firmware build job and every result in `results/`. A folder or document existing is not evidence that the design or firmware it names is built or accepted.

It does not own the common interface (`ACTUATOR_INTERFACE.md`), the CAN protocol, units, shared requirements, the mechanical design, program-level decisions or program credit. The parent owns the first four; the mechanical children own the mechanical design.

## 2. Position in the KritvaOS Ecosystem

This is the embedded child of the actuator family. The parent `kritva-actuator` is intended to track it as a submodule (`embedded/kritva-actuator-embedded`) and pin a reviewed commit; only the Project Lead updates that pointer. This README does not verify the current pointer. Four states are different: submodule configured in the parent's `.gitmodules`, pointer recorded by a parent commit, checkout initialised in a clone, and implementation verified. Work here goes on a branch in this repository; do not push to the parent. The roster and order of repositories in the program are owned by kritva-program (`v2/planning/repo-pipeline.json`), not by this README.

## 3. Architecture

The design is proposed, not frozen. The electronics and firmware architecture documents are in this repository ([docs/electronics/](docs/electronics/), [docs/firmware/](docs/firmware/)); the system architecture, interface control document and CAN protocol are in the parent and are not redefined here. The architecture describes target design: nothing in it is implemented as firmware yet.

- **Controller.** A development board for A0; a custom controller PCB for A1 (the repository baseline; a development-board substitute is a reviewed deviation).
- **Firmware.** Layers `platform/` (the only place for vendor or MCU-specific code), `foc/`, `motor_control/`, `encoder/`, `joint_control/`, `diagnostics/`, `communication/` and per-variant configuration in `variants/`.
- **Interfaces.** CAN and the common actuator interface are defined by the parent ICD and `CAN_PROTOCOL.md`.

### Variant classes (provisional)

| Class | Repository baseline (ACT-DEC-025, PROPOSED) | Wider planning range (under review, not approved) | Typical joints |
|---|---|---|---|
| Kritva-S | 2-5 N·m continuous, 5-10 N·m peak, about 60 RPM | 2-5 / 5-10 N·m | Wrist, neck |
| Kritva-M | 10 N·m continuous, 20-25 N·m peak, 45 RPM (elbow baseline and A0 reference, ACT-DEC-008) | 5-20 / 20-40 N·m | Elbow, shoulder (shoulder not yet in the spec) |
| Kritva-L | 25-40 N·m continuous, 50-80 N·m peak, about 20-40 RPM | 20-80 / 80-150 N·m | Hip, knee, ankle (ankle not yet in the spec) |

Use the repository baseline column for sizing and reviews. The wider range is a discussion input; it becomes a requirement only after the owner records it in `planning/v1/DECISIONS.md`. For L the two columns differ materially, so confirm the intended load cases first.

## 4. Documents to Read First

Read in this order. "parent" means a path inside the `kritva-actuator` parent repository (clone it with `--recurse-submodules`, see below); "this repo" means this repository. A label names a role, not an approval; the status a document declares is what counts, and each row shows the role first and the status after it. AUTHORITATIVE here marks the intended source of detail, not an approved baseline: implementation, purchasing, fabrication and release stay subject to the recorded decisions and gates. Values marked PROPOSED, provisional or not yet defined are not approved requirements. Links to the parent point at its `main` branch (current links); the parent record's own status and revision control, not this README. Tool flows are proposed, not frozen. Passing checks does not close a gate.

### A. Before you start (first week)

| # | Document | Where | Label, status | What to take from it |
|---|---|---|---|---|
| 1 | [`README.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/README.md) | parent | AUTHORITATIVE | Stages A0/A1/A2, design baseline (proposed, not frozen), repository structure, roles, safety |
| 2 | `AGENTS.md` | this repo and parent | AUTHORITATIVE | Rules for people and AI agents: gates, what not to change, no waivers |
| 3 | [`planning/v1/DECISIONS.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/planning/v1/DECISIONS.md) | parent | AUTHORITATIVE (each decision has its own status) | Decision index and status. Read ACT-DEC-001 to 009, 014, 015, 024 to 033 and the pending list (section 5) before choosing parts |
| 4 | [`planning/v2/ROADMAP_48_WEEKS.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/planning/v2/ROADMAP_48_WEEKS.md) | parent | REFERENCE (plan; read its own status line) | Current reforecast (P-weeks): A0 exit P12, Gate A, release gap, M fabrication, PCB spins, gates. Sections 3 to 5 |
| 5 | [`planning/v2/WORKSTREAMS.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/planning/v2/WORKSTREAMS.md) | parent | REFERENCE (plan; read its own status line) | Who owns what, hand-offs between workstreams |
| 6 | [`docs/standards/SUBMODULE_WORKFLOW.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/standards/SUBMODULE_WORKFLOW.md) | parent | REFERENCE | How child commits are pinned in the parent; branches and pull requests |

### B. Requirements, architecture and interfaces

| # | Document | Where | Label, status | What to take from it |
|---|---|---|---|---|
| 1 | [`requirements/ELECTRICAL_REQUIREMENTS.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/requirements/ELECTRICAL_REQUIREMENTS.md) | parent | AUTHORITATIVE (status per file) | Electrical limits and the A0 dev-board decision criteria (section 7) |
| 2 | [`requirements/FIRMWARE_REQUIREMENTS.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/requirements/FIRMWARE_REQUIREMENTS.md) | parent | AUTHORITATIVE (status per file) | Firmware requirements and behaviours |
| 3 | [`requirements/SAFETY_REQUIREMENTS.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/requirements/SAFETY_REQUIREMENTS.md) | parent | AUTHORITATIVE (status per file) | Safe-state, fault and test safety rules |
| 4 | [`requirements/INTERFACE_REQUIREMENTS.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/requirements/INTERFACE_REQUIREMENTS.md) | parent | AUTHORITATIVE (status per file) | Interface requirements |
| 5 | [`requirements/SYSTEM_REQUIREMENTS.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/requirements/SYSTEM_REQUIREMENTS.md) | parent | AUTHORITATIVE (status per file) | System limits and budget |
| 6 | [`docs/architecture/ACTUATOR_ARCHITECTURE.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/architecture/ACTUATOR_ARCHITECTURE.md) | parent | REFERENCE | Actuator architecture |
| 7 | [`docs/architecture/SOFTWARE_HARDWARE_BOUNDARY.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/architecture/SOFTWARE_HARDWARE_BOUNDARY.md) | parent | REFERENCE | What belongs to firmware, hardware and KritvaOS |
| 8 | [`docs/architecture/ACTUATOR_FAMILY_SPEC.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/architecture/ACTUATOR_FAMILY_SPEC.md) | parent | AUTHORITATIVE, PROPOSED (ACT-DEC-025) | S/M/L classes (provisional): one firmware configured per variant |
| 9 | [`docs/interfaces/CAN_PROTOCOL.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/interfaces/CAN_PROTOCOL.md) | parent | REFERENCE | CAN messages, IDs, scaling, timeouts, fault vocabulary (owned by the parent) |
| 10 | [`docs/interfaces/INTERFACE_CONTROL_DOCUMENT.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/interfaces/INTERFACE_CONTROL_DOCUMENT.md) | parent | REFERENCE | The common interface |
| 11 | [`docs/interfaces/ACTUATOR_INTERFACE.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/interfaces/ACTUATOR_INTERFACE.md) | parent | REFERENCE | Actuator-to-KritvaOS interface |
| 12 | [`docs/interfaces/SIGNAL_AND_UNIT_CONVENTIONS.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/interfaces/SIGNAL_AND_UNIT_CONVENTIONS.md) | parent | REFERENCE | Units, signs and conventions |

### C. Electronics and firmware design (this repository)

| # | Document | Where | Label, status | What to take from it |
|---|---|---|---|---|
| 1 | [`docs/electronics/ELECTRONICS_ARCHITECTURE.md`](docs/electronics/ELECTRONICS_ARCHITECTURE.md) | this repo | AUTHORITATIVE as the intended source of design detail; status per file, none approved (ELECTRONICS_ARCHITECTURE: OPEN) | Controller electronics architecture |
| 2 | [`docs/electronics/MOTOR_CONTROLLER_SPECIFICATION.md`](docs/electronics/MOTOR_CONTROLLER_SPECIFICATION.md) | this repo | AUTHORITATIVE as the intended source of design detail; status per file, none approved (ELECTRONICS_ARCHITECTURE: OPEN) | Motor controller specification |
| 3 | [`docs/electronics/HARDWARE_BRINGUP.md`](docs/electronics/HARDWARE_BRINGUP.md) | this repo | AUTHORITATIVE as the intended source of design detail; status per file, none approved (ELECTRONICS_ARCHITECTURE: OPEN) | Bring-up steps for A0 and for the custom PCB |
| 4 | [`docs/firmware/FIRMWARE_ARCHITECTURE.md`](docs/firmware/FIRMWARE_ARCHITECTURE.md) | this repo | AUTHORITATIVE as the intended source of design detail; status per file, none approved (ELECTRONICS_ARCHITECTURE: OPEN) | Firmware layers, loop rates, variant configuration |
| 5 | [`docs/firmware/MOTOR_CONTROL.md`](docs/firmware/MOTOR_CONTROL.md) | this repo | AUTHORITATIVE as the intended source of design detail; status per file, none approved (ELECTRONICS_ARCHITECTURE: OPEN) | FOC, current loop, position/speed/torque control |
| 6 | [`docs/firmware/CALIBRATION_PROCEDURE.md`](docs/firmware/CALIBRATION_PROCEDURE.md) | this repo | AUTHORITATIVE as the intended source of design detail; status per file, none approved (ELECTRONICS_ARCHITECTURE: OPEN) | Calibration steps and records |
| 7 | [`firmware/README.md`](firmware/README.md) and [`hardware/README.md`](hardware/README.md) | this repo | REFERENCE | Layout of firmware and hardware folders |

### D. Standards and tool flow

| # | Document | Where | Label, status | What to take from it |
|---|---|---|---|---|
| 1 | [`docs/standards/TOOLFLOW_ELECTRONICS_EMBEDDED.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/standards/TOOLFLOW_ELECTRONICS_EMBEDDED.md) | parent | REFERENCE, PROPOSED (not frozen) | Your tool flow (KiCad, Arm GCC, CMake, tests, CAN tools, FOC references with licences). Proposed, not frozen |
| 2 | [`docs/standards/OPEN_SOURCE_TOOLFLOW.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/standards/OPEN_SOURCE_TOOLFLOW.md) | parent | REFERENCE, PROPOSED (not frozen) | Full reasoning, licences and checked GitHub and YouTube links |
| 3 | [`docs/standards/BOM_STANDARD.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/standards/BOM_STANDARD.md) | parent | REFERENCE | BOM rules for `hardware/bom/ELECTRICAL_BOM.csv` |
| 4 | [`docs/standards/DESIGN_REVIEW_CHECKLIST.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/standards/DESIGN_REVIEW_CHECKLIST.md) | parent | REFERENCE | Design review items |
| 5 | [`docs/standards/RELEASE_CHECKLIST.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/standards/RELEASE_CHECKLIST.md) | parent | REFERENCE | What a release needs |
| 6 | [`docs/standards/PROGRAM_ALIGNMENT.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/standards/PROGRAM_ALIGNMENT.md) | parent | REFERENCE | Status reporting and HOLD rules |

### E. Validation, audit and planning

| # | Document | Where | Label, status | What to take from it |
|---|---|---|---|---|
| 1 | [`docs/validation/VALIDATION_PLAN.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/validation/VALIDATION_PLAN.md) | parent | REFERENCE | How the actuator will be validated |
| 2 | [`docs/validation/TEST_EQUIPMENT.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/validation/TEST_EQUIPMENT.md) | parent | REFERENCE | Fixtures and instruments; restrained-fixture rule (ACT-DEC-015) |
| 3 | [`audit/electronics/ELECTRONICS_DESIGN_AUDIT.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/audit/electronics/ELECTRONICS_DESIGN_AUDIT.md) | parent | REFERENCE (review criteria) | What the independent electrical reviewer checks (E0 to E4) |
| 4 | [`audit/firmware/FIRMWARE_REVIEW.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/audit/firmware/FIRMWARE_REVIEW.md) | parent | REFERENCE (review criteria) | Firmware review checks (F0 to F4) |
| 5 | [`audit/electronics/ELECTRONICS_ACCEPTANCE_AUDIT.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/audit/electronics/ELECTRONICS_ACCEPTANCE_AUDIT.md) and [`audit/firmware/FIRMWARE_ACCEPTANCE_AUDIT.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/audit/firmware/FIRMWARE_ACCEPTANCE_AUDIT.md) | parent | REFERENCE (review criteria) | Acceptance criteria for gates |
| 6 | [`planning/v1/MILESTONE.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/planning/v1/MILESTONE.md) | parent | REFERENCE (plan; read its own status line) | A0 scope first (your first milestone), then A1 and Gates A/B/C |
| 7 | [`planning/v1/ROADMAP.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/planning/v1/ROADMAP.md) | parent | REFERENCE (plan; read its own status line) | A0 plan, budget (dev board about ₹3,000 to ₹5,000), contingency if the custom PCB slips |
| 8 | [`planning/v1/M0_DECISION_SHEET.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/planning/v1/M0_DECISION_SHEET.md) | parent | REFERENCE (plan; read its own status line) | Pending decisions that affect the controller |
| 9 | [`planning/v1/tasks/ACT-01/README.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/planning/v1/tasks/ACT-01/README.md) | parent | REFERENCE (plan; read its own status line) | Electronics task folder guide (legacy ACT-01 IDs map to ACT-EMB in `planning/v2/TASK_ID_MAPPING.csv`) |
| 10 | [`docs/training/README.md`](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/training/README.md) | parent | REFERENCE | Long training reference; read sections 1 to 4A and 5, then the A0 baseline |

### F. Notes for the embedded intern

A0 is the dev-board electronics exit (P12). The custom controller PCB and CAN firmware are the A1 baseline; a development-board substitute is a reviewed deviation. Controller decisions pending in the parent `DECISIONS.md` section 5 (encoder IC, safe-state option, CAN payload encoding, motor model) must be recorded before the PCB design is released. Firmware is one parameterised code base, not three forks.

If a document you need is missing or contradicts another, raise it with the Project Lead; do not change the interface, CAN protocol, units or decisions in this repository.

## 5. Repository Structure and File Responsibilities

Labels: INPUT is edited by hand and read by a tool or review; GENERATED is written by a tool and never edited; EVIDENCE supports a claim and is append-only; AUTHORITATIVE owns a rule. A label is a role, not an approval. Most folders below are scaffolding with no content yet (see section 1).

| Path | Content | Label, status | Responsible | Notes |
|---|---|---|---|---|
| `firmware/` | `platform/` (the only place for vendor or MCU-specific code), `foc/`, `motor_control/`, `encoder/`, `joint_control/`, `diagnostics/`, `communication/`, `variants/` (per-variant configuration for S, M, L) | INPUT; NOT YET IMPLEMENTED (no firmware source) | Embedded owner | Safety-relevant code (fault manager, limits, state machine, watchdog) needs the Independent Electrical/Firmware Reviewer. See `firmware/README.md` |
| `hardware/motor_controller/development_board/` | A0 development-board configuration and selected-board record | INPUT | Embedded owner |  |
| `hardware/motor_controller/custom_pcb/` | `schematics/`, `pcb/`, `manufacturing/` for the A1 controller | INPUT; NOT YET IMPLEMENTED | Embedded owner | Review E2 before fabrication |
| `hardware/power_stage/`, `sensing/`, `connectors/` | Inverter and protection notes, sensing, connector pin-outs | INPUT | Embedded owner | Power-stage sizing from motor current, never supply voltage alone |
| `hardware/bom/ELECTRICAL_BOM.csv` | Electrical BOM, item prefix `EB-NNN` | INPUT; IMPLEMENTED (item rows exist; the schema check passes) | Embedded owner | Checked by `check_bom.py`. See `hardware/README.md` |
| `docs/electronics/`, `docs/firmware/` | Electronics architecture, controller specification, bring-up; firmware architecture, motor control, calibration | AUTHORITATIVE as the intended source of design detail; status per file, none approved | Embedded owner |  |
| `communication/can/` | CAN firmware layer | INPUT (protocol is owned by the parent) | Embedded owner | Protocol is owned by the parent |
| `tests/unit/`, `tests/firmware/`, `tests/hardware/` | Unit, firmware and hardware tests (empty today); `tests/commit_message_check/` tests the commit checker | EVIDENCE; NOT YET IMPLEMENTED (empty today) | Embedded owner | Hardware tests only on a restrained, guarded, instrumented fixture |
| `results/motor_control/` | Raw bring-up and characterisation evidence | EVIDENCE; NOT YET IMPLEMENTED | Embedded owner | Record firmware commit and hardware configuration |
| `scripts/check_bom.py` | Vendored BOM check | INPUT; IMPLEMENTED (vendored copy) | Project Lead | Change it in the parent, not here |
| `scripts/status/` | `gen_status.py` (writes and validates `status/status.json`) and its tests | INPUT | Project Lead |  |
| `scripts/security/check_commit_messages.py` | Commit message checker used by CI | INPUT | Project Lead / Security Owner |  |
| `status/tasks.csv` | Task facts (ID, execution, readiness, commit) | INPUT | Embedded owner edits, Project Lead approves | Source for the status report |
| `status/status.json`, `status.schema.json`, `workstream.json` | Generated status report, vendored schema (with `.sha256`), workstream ID | GENERATED (`status.json`); SNAPSHOT (vendored schema) | Generated | Never hand-edit `status.json` |
| `Makefile` | `make check`, `check-bom`, `check-status` | INPUT | Project Lead |  |
| `.github/workflows/` | `checks.yml`, `commit-message-check.yml`, `readme-check.yml`, `secret-scan.yml` | AUTHORITATIVE | Project Lead |  |
| `.github/CODEOWNERS` | Required reviewers | AUTHORITATIVE | Project Lead | Single owner today |
| `AGENTS.md`, `SECURITY.md`, `.gitignore`, `LICENSE` | Contributor and AI-assistant rules, security reporting, ignored files (build outputs, KiCad backups), licence | AUTHORITATIVE | Project Lead |  |

## 6. Toolchain and Development Workflow

| Tool | Purpose | Version | Check |
|---|---|---|---|
| git | Version control | any recent | `git --version` |
| GNU make | Local commands | any | `make --version` |
| Python 3 | The checks (standard library only) | 3.11 in the `checks` workflow, 3.12 in `commit-message-check` | `python3 --version` |
| KiCad, Arm GNU toolchain, CMake, STM32CubeG4, Unity, pytest, CAN tools | Engineering flow | PROPOSED in the parent, not frozen | not applicable yet |

### Setup

Required for the checks: `git`, `make`, `python3` (CI uses 3.11 for `checks` and 3.12 for `commit-message-check`). The checks use the Python standard library.

```bash
# Debian / Ubuntu
sudo apt install git make python3
```

On Windows use WSL or Git Bash. Confirm with `python3 --version` and `make --version`.

Engineering tools are proposed in the parent and are **not yet frozen**: KiCad (PCB, with `kicad-cli` for ERC/DRC and exports), Arm GNU toolchain with CMake, the STM32CubeG4 peripheral layer, Unity and pytest for tests, and CAN tools (python-can, cantools, SavvyCAN, can-utils). Read `docs/standards/TOOLFLOW_ELECTRONICS_EMBEDDED.md` and `OPEN_SOURCE_TOOLFLOW.md` in the parent for the flow, licences and checked references, and do not install different versions for released work. The planned firmware build is `cmake -S firmware -B build -G Ninja ...` (see `firmware/README.md`). Optional: gitleaks 8.18.4 to run the secret scan locally.

Before copying any external code, add it to the third-party code register in `firmware/README.md` and get the Project Lead's approval (FW-REQ-074).

### Clone

```bash
# This repository only
git clone https://github.com/KritvaOS/kritva-actuator-embedded.git
cd kritva-actuator-embedded
# The parent, with the child checkouts at the pointers the parent records
git clone --recurse-submodules https://github.com/KritvaOS/kritva-actuator.git
```

`--recurse-submodules` initialises the child checkouts at the pointers the parent records and needs read access to each child repository; which commit you get depends on the parent's current pointers.

To push over SSH without changing the stored HTTPS URL, you can set a URL rewrite. The command below MODIFIES your global Git configuration (it affects every repository for your user): `git config --global url."git@github.com:".pushInsteadOf "https://github.com/"`. Inspect it with `git config --global --get-regexp pushinsteadof` and remove it with `git config --global --unset url."git@github.com:".pushInsteadOf`. To limit the rewrite to one repository, run the same command with `--local` inside it instead of `--global`. Never put credentials in a remote URL. Work in this repository on a branch; do not push to the parent. Only the Project Lead updates the parent's pointer to a child commit, and the parent is intended to pin a reviewed commit (parent `docs/standards/SUBMODULE_WORKFLOW.md`, PROPOSED). Released PCB manufacturing zips are meant to use Git LFS (`hardware/README.md`); no LFS rule exists in this repository yet, so agree one with the owner before committing large binaries.

### Review and safety workflow

1. Branch, pull request, owner and independent reviewer approval (ACT-DEC-014).
2. `make check` must pass.
3. Power-stage and motor-control safety are not self-approved.
4. Loaded and fault tests only on a restrained, guarded, instrumented fixture.
5. The mechanical HOLD was lifted in the parent (ACT-DEC-029, 2026-10-18). That does not authorise fabrication, procurement or loaded testing on its own: the gates and independent review still apply. `AGENTS.md` in this repository was updated to match.

## 7. Dependencies and Interfaces

| Dependency | Direction | Kind | Contract | State |
|---|---|---|---|---|
| kritva-actuator (parent) | upstream | governance, requirements, interface | parent ICD, `CAN_PROTOCOL.md`, requirements, `planning/v1/DECISIONS.md` | ESTABLISHED as the owner of the interface; the pointer is intended to be pinned by the Project Lead (current pointer not verified here) |
| kritva-actuator-s, -m, -l | sibling | none specified | firmware configures per variant; mechanical design is theirs | PLANNED: no interface between the repositories is implemented, and the family layout is PROPOSED (ACT-DEC-024) |
| kritva-program | upstream | governance and status | status schema 2.0 (`status/`) | planning-only reporting; this repository earns no program credit |
| Engineering tools (KiCad, Arm GNU, CMake, STM32CubeG4, Unity, pytest, CAN tools) | upstream | tools | parent `TOOLFLOW_ELECTRONICS_EMBEDDED.md` | PROPOSED, not frozen |

Five kinds of relationship are kept apart: program ordering, Git submodule (the parent configures and pins this repository), source or build dependency, runtime integration, and governance or status reporting. The interface and CAN documents the parent owns are PROPOSED until approved, and no test yet checks that firmware conforms to them. A PROPOSED dependency is not an integration that exists. Before copying any external code, add it to the third-party code register in `firmware/README.md` and get the Project Lead's approval (FW-REQ-074).

## 8. Milestones and Implementation Plan

Stage scope is held in the parent `planning/v1/ROADMAP.md` and `planning/v1/MILESTONE.md`; the current reforecast is the parent `planning/v2/ROADMAP_48_WEEKS.md`. Stage names, budgets and dates here are provisional planning information, not approved requirements, and nothing here authorises purchase, fabrication or design freeze. Dates are planning targets, not commitments.

### Stage comparison: A0 and A1 (provisional planning information)

| Item | A0: Educational Motor Control | A1: Humanoid Smart Actuator |
|---|---|---|
| Primary objective | Learn and validate motor control; build the reusable electronics and firmware base | Working actuator module: motor, gearbox, output shaft and bearings, output encoder, controller, CAN |
| Motor | Low-cost commercial BLDC/PMSM | Commercial BLDC/PMSM selected from the sizing results (ACT-DEC-003, 008 pending) |
| Controller | Motor-control development board (about ₹3,000-₹5,000) | Custom controller PCB (repository baseline) |
| Position control | FOC with current sensing; basic closed-loop position and speed | Position, velocity and torque control on the actuator |
| Encoder | Motor-side feedback | Motor-side feedback plus output-side encoder |
| Communication | USB/UART | CAN (firmware and protocol per the parent ICD) |
| Diagnostics | Basic status, faults, logging | Fault handling, thermal and current limits, CAN diagnostics |
| Mechanical design | Mounting and bench fixture only | Commercial planetary gearbox, independent output shaft and bearings, housing (HOLD lifted by ACT-DEC-029; Gate A still required) |
| Validation | Bench tests on a restrained fixture | Elbow load case; Gates A/B/C with independent review (ACT-DEC-014, 015) |
| Budget (provisional) | ₹10,000-₹15,000 | ₹20,000-₹30,000, cumulative including A0 |
| Deliverable | Working motor-control platform with firmware, tests and documents | Target: an actuator ready for validation, with CAD, BOM, firmware and test reports. "Validated" is reserved for a specific unit and configuration whose acceptance evidence is recorded, and depends on the firmware and hardware being built, physical testing, independent review and Gates A, B and C; software checks alone cannot satisfy it |

Planning status (2026-10-18): A0 exits at P12 (10 Jan 2027), six weeks later than the original week-6 target (ACT-DEC-032). The M prototype checkpoint is P23 (22-28 Mar 2027), after Gate A (by P14) and a two-week release and procurement gap (ACT-DEC-033). The custom controller PCB and CAN firmware stay the A1 baseline; a development-board substitute is a reviewed deviation. Stage names above are the official names. Reforecast: `planning/v2/ROADMAP_48_WEEKS.md` (P1 = 19 Oct 2026; 58-week horizon ending 28 Nov 2027 is proposed, awaiting Project Lead confirmation).

## 9. Tasks and Acceptance Criteria

- **Where tasks live.** [status/tasks.csv](status/tasks.csv) holds the task facts (`ACT-EMB-nnn`, with the legacy `ACT-01-nnn` IDs mapped in the parent `planning/v2/TASK_ID_MAPPING.csv`). The Embedded owner edits it and the Project Lead approves.
- **Acceptance criteria.** The criteria for electronics and firmware gates are in the parent `audit/electronics/ELECTRONICS_ACCEPTANCE_AUDIT.md` and `audit/firmware/FIRMWARE_ACCEPTANCE_AUDIT.md`. Safety-relevant changes need the Independent Electrical/Firmware Reviewer (ACT-DEC-014).
- Work is not accepted because code, a commit, a merged pull request or a passing local test exists. Acceptance is a recorded review decision, not a status field.

## 10. Status Reporting and Program Integration

`status/status.json` (schema 2.0) is generated by `scripts/status/gen_status.py` from `status/tasks.csv`; never edit it by hand. The reports are planning-only: this repository reports facts only, its tasks are not in the approved program baseline, and nothing here creates program credit. Execution, evidence, acceptance and release readiness are kept apart:

| Dimension | Source record | Authority |
|---|---|---|
| Execution | `status/tasks.csv`, reported in `status/status.json` | The Embedded owner records it; the Project Lead approves |
| Evidence | None is recorded today (`results/` is empty). By type: a software test names the source commit, command and result; a calculation or simulation names the model, inputs and assumptions; a physical test names the hardware and firmware configuration, procedure, instruments and conditions, and result | The author records it; a reviewer other than the author checks it |
| Acceptance | The parent's gate and audit records (`audit/`) | The independent reviewer and the Project Lead, never a status report |
| Release readiness | The parent's Gates A, B and C | Project Lead with a qualified safety reviewer |

Evidence has types that are not interchangeable (software test, calculation, simulation, bench measurement, independently accepted physical test). `status/status.json` carries no evidence today, every task's execution is NOT_STARTED, and the readiness values PLANNABLE and HARDWARE-BLOCKED describe planning constraints, not safety or release approval. A generated view is a snapshot that can lag its inputs, cannot approve its own work, and does not establish physical safety or program credit. Regenerate it with `python3 scripts/status/gen_status.py --root .`.

## 11. Build, Test, Regression and Validation

CI runs four separate workflows (below). None is a firmware build or a hardware test: neither exists yet, and a passing check does not close a gate.

| Workflow | Trigger | What it runs |
|---|---|---|
| `checks` | push to `main`; pull requests | `make check` (electrical BOM schema and status only) |
| `commit-message-check` | pull requests | the unit tests of both commit checkers, then `check_commit_messages.py` on the commits in the pull request (rejects session trailers and links) and `check_commit_format.py` on the same commits (the D-053 form; blocking since D-070) |
| `readme-check` | pull requests; push to `main` | the README checker's unit tests, then `python3 scripts/check_readme.py README.md --root .` (structure, metadata and local links only; not a required check yet, D-067) |
| `secret-scan` | push to `main`; pull requests; manual dispatch | gitleaks over the git history |


| Check | Command | Effect | Runs in CI? |
|---|---|---|---|
| Electrical BOM schema | `make check-bom` | check | yes (`checks`) |
| Status report against `status/tasks.csv` | `make check-status` | check | yes (`checks`) |
| Both of the above | `make check` | check | yes |
| README standard | `make check-readme` | check | yes (`readme-check`; not a required check yet, D-067) |
| README checker regression tests | `python3 -m unittest discover -s tests/readme_check -v` | check | no, run locally |
| Commit checker tests | `python3 -m unittest discover -s tests/commit_message_check -v` | check | yes (`commit-message-check`) |
| Status generator tests | `python3 -m unittest discover -s scripts/status -p "test_*.py" -v` | check | no, run locally |
| Regenerate the status report | `python3 scripts/status/gen_status.py --root .` | generate (rewrites `status/status.json`) | no |
| Install the local commit-msg hook | `printf ... > .git/hooks/commit-msg` (section 12) | modify (writes a local hook file) | no |

The Makefile has only the check targets above (`make help` is not defined here); there is no clean or generate target.

Firmware unit tests (`tests/unit/`), per-variant builds and bench tests do not exist yet. When they are added, host-side unit tests run for every pull request, M, S and L configurations build from the same source, and hardware-in-loop tests run only on a guarded fixture with a test-readiness record, never automatically after a merge. Regression today means the three groups above pass before every pull request and again in CI on every pull request and on every push to `main`. A passing build or unit test is not evidence of physical safety; mark simulated or mocked results as such.

### How to find out why a pull request failed

1. Open the pull request, scroll to the checks box at the bottom (or open the **Checks** tab). A red cross marks the failed check.
2. Click **Details** next to it and expand the failed step. The error line is usually at the end of that step.
3. Or from a terminal with the GitHub CLI: `gh pr checks <PR-number>`, then `gh run list --branch <branch>` and `gh run view <run-id> --log-failed`.
4. Reproduce it locally with the command in the table, fix, commit, and push to the same branch; the checks rerun.

| Failed check | What it ran | Reproduce locally | Usual cause and fix |
|---|---|---|---|
| `checks` | `make check`: electrical BOM schema, status | `make check` (or `make check-bom`, `make check-status`) | `check-bom`: wrong column or duplicate item ID in `hardware/bom/ELECTRICAL_BOM.csv`. `check-status`: `status/status.json` is out of date; run `python3 scripts/status/gen_status.py --root .` and commit the result (never edit it by hand) |
| `commit-message-check` | Unit tests of both commit checkers, then both checkers on every commit in the PR | `python3 -m unittest discover -s tests/commit_message_check -v` then `python3 scripts/security/check_commit_messages.py --range origin/main..HEAD` and `python3 scripts/security/check_commit_format.py --range origin/main..HEAD` | A commit carries a `Claude-Session:` trailer or session link, or its message breaks the format (header `type(scope): summary`, one `Task:` or `Tasks:` footer; the output names the problem). Amend the latest unpushed commit (`git commit --amend`). For commits already pushed, ask the owner before rewriting history |
| `readme-check` | Unit tests of the README checker, then the checker on `README.md` | `python3 -m unittest discover -s tests/readme_check -v` then `make check-readme` | A required heading, metadata field or local link is missing or broken in `README.md`; `make check-readme` prints the message, fix the README. It is not a required check yet (D-067) |
| `secret-scan` | gitleaks 8.18.4 over the full git history | Install gitleaks 8.18.4, then `gitleaks detect --source . --redact --verbose --exit-code 1` | A credential, key or token is in the history. Do not add an allowlist entry. Tell the Security Owner (Dinesh) at once; the secret must be revoked or rotated, and removing it in a later commit is not enough |

There is no firmware build job in this repository yet (it is planned with `firmware/CMakeLists.txt`). If the failure is in a step you did not touch, rerun the job once from the Actions page; if it fails again, ask the owner. If the log shows a missing tool or Python module, the runner image changed: report it rather than disabling the check.

## 12. Git Workflow and Review

Controlling statement: the Kritva commit standard (kritva-program D-053), adopted here under D-070, which completes PD-019: header `type(scope): summary` (types feat, fix, docs, refactor, test, build, ci, chore, perf, revert, security; at most 90 characters; an optional `[TASK-ID]` suffix must match the footer), exactly one `Task:` or `Tasks:` footer line, and `Tasks: None (reason)` only on a docs or chore commit that implements no task; merge by merge commit. `AGENTS.md` repeats it. CI (`commit-message-check`) enforces it with `scripts/security/check_commit_format.py` and also rejects `Claude-Session:` trailers and `claude.ai/code/session` links. The standard applies to new commits; history is not rewritten, and the older task-ID subject form (`ACT-EMB-003: ...`) is no longer accepted for new commits.

### Branch names

Never commit to `main`; it is protected. Branch from an up-to-date `main`:

```bash
git switch main && git pull --ff-only
git switch -c <type>/<TASK-ID>-<short-topic>      # task work
git switch -c chore/<short-topic>                 # repository housekeeping
```

Examples: `feat/ACT-EMB-003-encoder-rollover`, `docs/ACT-EMB-004-fault-table`, `chore/status-regenerate`. Use lowercase and hyphens. The `ACT-EMB` task IDs are in `status/tasks.csv`. These names are a recommendation that matches the existing `chore/...` branches; CI does not enforce them.

### Commit messages

Use the Kritva commit standard (kritva-program D-053, adopted under D-070):

```text
feat(embedded): add shaft stress check inputs

Task: ACT-EMB-003
```

A commit that implements no task and only changes documents or housekeeping uses `docs` or `chore` and `Tasks: None (reason)`. Allowed `type` values are fixed by the checker: `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `ci`, `chore`, `perf`, `revert`, `security`; use `feat` or `fix` for CAD, drawing, schematic, PCB or BOM changes. One atomic change per commit. Do not claim a test, review or acceptance that did not happen. Do not rewrite or renumber history.

What CI **does** enforce (`commit-message-check`): the format above, and that a commit has no `Claude-Session:` trailer or `claude.ai/code/session` link. A `Co-Authored-By:` line is allowed. Branch names and the rest of this section are conventions.

Optionally, to catch a rejected message before pushing, install a local safeguard (it modifies `.git/hooks/commit-msg` in your clone and does not change CI policy):

```bash
printf '#!/bin/sh\npython3 scripts/security/check_commit_messages.py --file "$1" && python3 scripts/security/check_commit_format.py --file "$1"\n' > .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

### Pull requests

1. Push the branch and open a pull request into `main`.
2. Run `make check` and the unit tests first (see Checks above).
3. `main` requires `secret-scan`, `commit-message-check` and Code Owner review (owner statement; see `AGENTS.md`). With one owner, the PR author cannot approve their own PR: ask the owner to merge using the bypass, or add a second reviewer.
4. Power-stage and motor-control safety are not self-approved: safety-relevant firmware and hardware need the Independent Electrical/Firmware Reviewer (ACT-DEC-014). A green CI run never closes a gate.


## 13. Safety and Security

This repository will hold firmware and electronics that drive a motor. It is experimental and not human-safe. Software checks, analytical calculations and simulation validate only the stated model, inputs and software properties. They do not establish physical safety, component suitability, design acceptance or readiness for human use, and they do not close a gate; physical test evidence, independent review and the applicable gate approvals are required separately. Simulated or mocked results are marked as such.

The lifecycle status ACTIVE describes this repository, not hardware readiness. Lifting the mechanical HOLD (ACT-DEC-029) does not approve a design, waive a gate or authorise physical operation. The gates are defined in the parent: [planning/v1/MILESTONE.md](https://github.com/KritvaOS/kritva-actuator/blob/main/planning/v1/MILESTONE.md) (sections 6.4 and 8.4) and the records in the parent's `audit/release/`. The table below is this repository's gate summary, not the gate authority: it lists only the embedded contribution to each gate and not the complete closure criteria, and it does not state current status. Closing an embedded input does not close the parent gate or authorise the controlled activity; the parent record controls.

| Gate | Controls | Required closed inputs (embedded) | Decision maker | Prohibited while open |
|---|---|---|---|---|
| A, design release | Release for fabrication | E1; E2 schematic stage for housing and connector interfaces | Project Lead | Procurement, design freeze and fabrication (including the custom PCB), and the first loaded test |
| B, bench validation | Claims that bench performance targets are met | E3, F3 (bench scope) | Project Lead | Treating any controller or firmware performance as demonstrated |
| C, safety and release | Safety sign-off and release | E4, F3 | Project Lead with a qualified safety reviewer | Release, and any use outside the restrained, guarded, instrumented fixture |

The independent review (ACT-DEC-014, ACT-DEC-015) applies throughout. Power-stage and motor-control safety are not self-approved. Loaded and fault tests run only on a restrained, guarded, instrumented fixture; mark simulated or mocked results as such. The mechanical HOLD lifted by ACT-DEC-029 does not authorise fabrication, procurement or loaded testing on its own.

**Reporting a vulnerability:** follow [`SECURITY.md`](SECURITY.md); its reporting route is not yet verified as a dedicated private channel, and it says so. Never put details of an unfixed vulnerability in a public issue, pull request or commit message.

- Never commit secrets, private keys, tokens, passwords, production data or personal data. Use obviously fake values and mark them as fake.
- If a secret is committed by mistake, tell the Security Owner at once; removing it in a later commit does not make it safe. Do not add `secret-scan` allowlist entries.

## 14. Release and Versioning

There is no firmware release, build job or version tag in this repository yet; a firmware build job is planned with `firmware/CMakeLists.txt`. A release needs the parent's [release checklist](https://github.com/KritvaOS/kritva-actuator/blob/main/docs/standards/RELEASE_CHECKLIST.md) and the gates; a release is complete only when those criteria are met, not when code is merged. This README records no release state.

## 15. Ownership and Escalation

| Role | Responsibility |
|---|---|
| Embedded Intern (repository owner) | Works the embedded tasks; edits `status/tasks.csv` |
| Project Lead | Approves tasks, owns scripts and workflows, updates the parent's pointer to this repository |
| Independent Electrical/Firmware Reviewer | Reviews safety-relevant firmware and hardware (ACT-DEC-014) |
| Security Owner | Handles vulnerability reports and committed secrets |

If a document you need is missing or contradicts another, raise it with the Project Lead; do not change the interface, CAN protocol, units or decisions in this repository.

## 16. Related Repositories and References

| Repository | Relationship |
|---|---|
| [kritva-actuator](https://github.com/KritvaOS/kritva-actuator) | Parent: interface, CAN protocol, requirements, decisions, validation, audit |
| [kritva-actuator-s](https://github.com/KritvaOS/kritva-actuator-s), [kritva-actuator-m](https://github.com/KritvaOS/kritva-actuator-m), [kritva-actuator-l](https://github.com/KritvaOS/kritva-actuator-l) | Mechanical variants that this firmware is configured for |
| [kritva-program](https://github.com/KritvaOS/kritva-program) | Program plan, baseline, decisions, README standard |

## 17. License

Proprietary and confidential. Copyright (c) 2026 Kritvaos. All rights reserved. See [LICENSE](LICENSE).
