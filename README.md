# Kritva Actuator Embedded

Proprietary and confidential. Copyright (c) 2026 Kritvaos. All rights reserved.

Child repository of `KritvaOS/kritva-actuator` (the parent). Owner: Embedded Intern.

**Status: Concept.** Firmware, controller hardware, electronics and firmware documents for the whole actuator family (S, M, L). Firmware is one code base with a per-variant configuration (motor, gear ratio, limits), not three forks. No firmware is committed yet.

The common interface (`ACTUATOR_INTERFACE.md`), CAN protocol, units and requirements are owned by the parent and are **not** redefined here.

## Stages and variant classes

**Status: provisional planning information. Not approved requirements.** Stage scope is held in `planning/v1/ROADMAP.md` and `planning/v1/MILESTONE.md`; class ranges in `docs/architecture/ACTUATOR_FAMILY_SPEC.md` (ACT-DEC-025, PROPOSED). Budgets are provisional. Nothing here authorises purchase, fabrication or design freeze.

### Stage comparison: A0 and A1

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
| Deliverable | Working motor-control platform with firmware, tests and documents | Validated actuator with CAD, BOM, firmware, test reports |

Planning status (2026-10-18): A0 exits at P12 (10 Jan 2027), six weeks later than the original week-6 target (ACT-DEC-032). The M prototype checkpoint is P23 (22-28 Mar 2027), after Gate A (by P14) and a two-week release and procurement gap (ACT-DEC-033). The custom controller PCB and CAN firmware stay the A1 baseline; a development-board substitute is a reviewed deviation. Stage names above are the official names. Reforecast: `planning/v2/ROADMAP_48_WEEKS.md` (P1 = 19 Oct 2026; 58-week horizon ending 28 Nov 2027 is proposed, awaiting Project Lead confirmation).

### Variant classes (provisional)

| Class | Repository baseline (ACT-DEC-025, PROPOSED) | Wider planning range (under review, not approved) | Typical joints |
|---|---|---|---|
| Kritva-S | 2-5 N·m continuous, 5-10 N·m peak, about 60 RPM | 2-5 / 5-10 N·m | Wrist, neck |
| Kritva-M | 10 N·m continuous, 20-25 N·m peak, 45 RPM (elbow baseline and A0 reference, ACT-DEC-008) | 5-20 / 20-40 N·m | Elbow, shoulder (shoulder not yet in the spec) |
| Kritva-L | 25-40 N·m continuous, 50-80 N·m peak, about 20-40 RPM | 20-80 / 80-150 N·m | Hip, knee, ankle (ankle not yet in the spec) |

Use the repository baseline column for sizing and reviews. The wider range is a discussion input; it becomes a requirement only after the owner records it in `planning/v1/DECISIONS.md`. For L the two columns differ materially, so confirm the intended load cases first.

## Documents to read

Read in this order. "parent" means a path inside the `kritva-actuator` parent repository (clone it with `--recurse-submodules`, see below); "this repo" means this repository. Statuses in the documents matter: values marked PROPOSED, provisional or TBD are not approved requirements. Tool flows are proposed, not frozen. Passing checks does not close a gate.

### A. Before you start (first week)

| # | Document | Where | What to take from it |
|---|---|---|---|
| 1 | `README.md` | parent | Stages A0/A1/A2, design baseline (proposed, not frozen), repository structure, roles, safety |
| 2 | `AGENTS.md` | this repo and parent | Rules for people and AI agents: gates, what not to change, no waivers |
| 3 | `planning/v1/DECISIONS.md` | parent | Decision index and status. Read ACT-DEC-001 to 009, 014, 015, 024 to 033 and the pending list (section 5) before choosing parts |
| 4 | `planning/v2/ROADMAP_48_WEEKS.md` | parent | Current reforecast (P-weeks): A0 exit P12, Gate A, release gap, M fabrication, PCB spins, gates. Sections 3 to 5 |
| 5 | `planning/v2/WORKSTREAMS.md` | parent | Who owns what, hand-offs between workstreams |
| 6 | `docs/standards/SUBMODULE_WORKFLOW.md` | parent | How child commits are pinned in the parent; branches and pull requests |

### B. Requirements, architecture and interfaces

| # | Document | Where | What to take from it |
|---|---|---|---|
| 1 | `requirements/ELECTRICAL_REQUIREMENTS.md` | parent | Electrical limits and the A0 dev-board decision criteria (section 7) |
| 2 | `requirements/FIRMWARE_REQUIREMENTS.md` | parent | Firmware requirements and behaviours |
| 3 | `requirements/SAFETY_REQUIREMENTS.md` | parent | Safe-state, fault and test safety rules |
| 4 | `requirements/INTERFACE_REQUIREMENTS.md` | parent | Interface requirements |
| 5 | `requirements/SYSTEM_REQUIREMENTS.md` | parent | System limits and budget |
| 6 | `docs/architecture/ACTUATOR_ARCHITECTURE.md` | parent | Actuator architecture |
| 7 | `docs/architecture/SOFTWARE_HARDWARE_BOUNDARY.md` | parent | What belongs to firmware, hardware and KritvaOS |
| 8 | `docs/architecture/ACTUATOR_FAMILY_SPEC.md` | parent | S/M/L classes (provisional): one firmware configured per variant |
| 9 | `docs/interfaces/CAN_PROTOCOL.md` | parent | CAN messages, IDs, scaling, timeouts, fault vocabulary (owned by the parent) |
| 10 | `docs/interfaces/INTERFACE_CONTROL_DOCUMENT.md` | parent | The common interface |
| 11 | `docs/interfaces/ACTUATOR_INTERFACE.md` | parent | Actuator-to-KritvaOS interface |
| 12 | `docs/interfaces/SIGNAL_AND_UNIT_CONVENTIONS.md` | parent | Units, signs and conventions |

### C. Electronics and firmware design (this repository)

| # | Document | Where | What to take from it |
|---|---|---|---|
| 1 | `docs/electronics/ELECTRONICS_ARCHITECTURE.md` | this repo | Controller electronics architecture |
| 2 | `docs/electronics/MOTOR_CONTROLLER_SPECIFICATION.md` | this repo | Motor controller specification |
| 3 | `docs/electronics/HARDWARE_BRINGUP.md` | this repo | Bring-up steps for A0 and for the custom PCB |
| 4 | `docs/firmware/FIRMWARE_ARCHITECTURE.md` | this repo | Firmware layers, loop rates, variant configuration |
| 5 | `docs/firmware/MOTOR_CONTROL.md` | this repo | FOC, current loop, position/speed/torque control |
| 6 | `docs/firmware/CALIBRATION_PROCEDURE.md` | this repo | Calibration steps and records |
| 7 | `firmware/README.md and hardware/README.md` | this repo | Layout of firmware and hardware folders |

### D. Standards and tool flow

| # | Document | Where | What to take from it |
|---|---|---|---|
| 1 | `docs/standards/TOOLFLOW_ELECTRONICS_EMBEDDED.md` | parent | Your tool flow (KiCad, Arm GCC, CMake, tests, CAN tools, FOC references with licences). Proposed, not frozen |
| 2 | `docs/standards/OPEN_SOURCE_TOOLFLOW.md` | parent | Full reasoning, licences and checked GitHub and YouTube links |
| 3 | `docs/standards/BOM_STANDARD.md` | parent | BOM rules for `hardware/bom/ELECTRICAL_BOM.csv` |
| 4 | `docs/standards/DESIGN_REVIEW_CHECKLIST.md` | parent | Design review items |
| 5 | `docs/standards/RELEASE_CHECKLIST.md` | parent | What a release needs |
| 6 | `docs/standards/PROGRAM_ALIGNMENT.md` | parent | Status reporting and HOLD rules |

### E. Validation, audit and planning

| # | Document | Where | What to take from it |
|---|---|---|---|
| 1 | `docs/validation/VALIDATION_PLAN.md` | parent | How the actuator will be validated |
| 2 | `docs/validation/TEST_EQUIPMENT.md` | parent | Fixtures and instruments; restrained-fixture rule (ACT-DEC-015) |
| 3 | `audit/electronics/ELECTRONICS_DESIGN_AUDIT.md` | parent | What the independent electrical reviewer checks (E0 to E4) |
| 4 | `audit/firmware/FIRMWARE_REVIEW.md` | parent | Firmware review checks (F0 to F4) |
| 5 | `audit/electronics/ELECTRONICS_ACCEPTANCE_AUDIT.md and audit/firmware/FIRMWARE_ACCEPTANCE_AUDIT.md` | parent | Acceptance criteria for gates |
| 6 | `planning/v1/MILESTONE.md` | parent | A0 scope first (your first milestone), then A1 and Gates A/B/C |
| 7 | `planning/v1/ROADMAP.md` | parent | A0 plan, budget (dev board about ₹3,000 to ₹5,000), contingency if the custom PCB slips |
| 8 | `planning/v1/M0_DECISION_SHEET.md` | parent | Pending decisions that affect the controller |
| 9 | `planning/v1/tasks/ACT-01/README.md` | parent | Electronics task folder guide (legacy ACT-01 IDs map to ACT-EMB in `planning/v2/TASK_ID_MAPPING.csv`) |
| 10 | `docs/training/README.md` | parent | Long training reference; read sections 1 to 4A and 5, then the A0 baseline |

### F. Notes for the embedded intern

A0 is the dev-board electronics exit (P12). The custom controller PCB and CAN firmware are the A1 baseline; a development-board substitute is a reviewed deviation. Controller decisions pending in the parent `DECISIONS.md` section 5 (encoder IC, safe-state option, CAN payload encoding, motor model) must be recorded before the PCB design is released. Firmware is one parameterised code base, not three forks.

If a document you need is missing or contradicts another, raise it with the Project Lead; do not change the interface, CAN protocol, units or decisions in this repository.

## Clone

```bash
# This repository only
git clone https://github.com/KritvaOS/kritva-actuator-embedded.git
cd kritva-actuator-embedded
# The whole actuator family (parent plus the four children as submodules)
git clone --recurse-submodules https://github.com/KritvaOS/kritva-actuator.git
```

To push over SSH without changing the stored HTTPS URL, run once: `git config --global url."git@github.com:".pushInsteadOf "https://github.com/"`. Never put credentials in a remote URL. Work in this repository on a branch; do not push to the parent. Only the Project Lead updates the parent's pointer to a child commit, and the parent pins a reviewed commit (parent `docs/standards/SUBMODULE_WORKFLOW.md`). Released PCB manufacturing zips are meant to use Git LFS (`hardware/README.md`); no LFS rule exists in this repository yet, so agree one with the owner before committing large binaries.

## Folder structure and responsibilities

| Path | Content | Responsible | Notes |
|---|---|---|---|
| `firmware/` | `platform/` (the only place for vendor or MCU-specific code), `foc/`, `motor_control/`, `encoder/`, `joint_control/`, `diagnostics/`, `communication/`, `variants/` (per-variant configuration for S, M, L) | Embedded owner | Safety-relevant code (fault manager, limits, state machine, watchdog) needs the Independent Electrical/Firmware Reviewer. See `firmware/README.md` |
| `hardware/motor_controller/development_board/` | A0 development-board configuration and selected-board record | Embedded owner | |
| `hardware/motor_controller/custom_pcb/` | `schematics/`, `pcb/`, `manufacturing/` for the A1 controller | Embedded owner | Review E2 before fabrication |
| `hardware/power_stage/`, `sensing/`, `connectors/` | Inverter and protection notes, sensing, connector pin-outs | Embedded owner | Power-stage sizing from motor current, never supply voltage alone |
| `hardware/bom/ELECTRICAL_BOM.csv` | Electrical BOM, item prefix `EB-NNN` | Embedded owner | Checked by `check_bom.py`. See `hardware/README.md` |
| `docs/electronics/`, `docs/firmware/` | Electronics architecture, controller specification, bring-up; firmware architecture, motor control, calibration | Embedded owner | |
| `communication/can/` | CAN firmware layer | Embedded owner | Protocol is owned by the parent |
| `tests/unit/`, `tests/firmware/`, `tests/hardware/` | Unit, firmware and hardware tests (empty today); `tests/commit_message_check/` tests the commit checker | Embedded owner | Hardware tests only on a restrained, guarded, instrumented fixture |
| `results/motor_control/` | Raw bring-up and characterisation evidence | Embedded owner | Record firmware commit and hardware configuration |
| `scripts/check_bom.py` | Vendored BOM check | Project Lead | Change it in the parent, not here |
| `scripts/status/` | `gen_status.py` (writes and validates `status/status.json`) and its tests | Project Lead | |
| `scripts/security/check_commit_messages.py` | Commit message checker used by CI | Project Lead / Security Owner | |
| `status/tasks.csv` | Task facts (ID, execution, readiness, commit) | Embedded owner edits, Project Lead approves | Source for the status report |
| `status/status.json`, `status.schema.json`, `workstream.json` | Generated status report, vendored schema (with `.sha256`), workstream ID | Generated | Never hand-edit `status.json` |
| `Makefile` | `make check`, `check-bom`, `check-status` | Project Lead | |
| `.github/workflows/` | `checks.yml`, `commit-message-check.yml`, `secret-scan.yml` | Project Lead | |
| `.github/CODEOWNERS` | Required reviewers | Project Lead | Single owner today |
| `AGENTS.md`, `SECURITY.md`, `.gitignore`, `LICENSE` | Contributor and AI-assistant rules, security reporting, ignored files (build outputs, KiCad backups), licence | Project Lead | |

## Tool installation

Required for the checks: `git`, `make`, `python3` (CI uses 3.11 for `checks` and 3.12 for `commit-message-check`). The checks use the Python standard library.

```bash
# Debian / Ubuntu
sudo apt install git make python3
```

On Windows use WSL or Git Bash. Confirm with `python3 --version` and `make --version`.

Engineering tools are proposed in the parent and are **not yet frozen**: KiCad (PCB, with `kicad-cli` for ERC/DRC and exports), Arm GNU toolchain with CMake, the STM32CubeG4 peripheral layer, Unity and pytest for tests, and CAN tools (python-can, cantools, SavvyCAN, can-utils). Read `docs/standards/TOOLFLOW_ELECTRONICS_EMBEDDED.md` and `OPEN_SOURCE_TOOLFLOW.md` in the parent for the flow, licences and checked references, and do not install different versions for released work. The planned firmware build is `cmake -S firmware -B build -G Ninja ...` (see `firmware/README.md`). Optional: gitleaks 8.18.4 to run the secret scan locally.

Before copying any external code, add it to the third-party code register in `firmware/README.md` and get the Project Lead's approval (FW-REQ-074).

## Checks, unit tests and regression

```bash
make check                                  # electrical BOM schema and status (what CI runs)
python3 -m unittest discover -s tests/commit_message_check -v     # commit checker tests (run by CI)
python3 -m unittest discover -s scripts/status -p "test_*.py" -v  # status generator tests (run locally; not in CI yet)
```

Firmware unit tests (`tests/unit/`), per-variant builds and bench tests do not exist yet. When they are added, host-side unit tests run for every pull request, M, S and L configurations build from the same source, and hardware-in-loop tests run only on a guarded fixture with a test-readiness record, never automatically after a merge. Regression today means the three groups above pass before every pull request and again in CI on every pull request and on every push to `main`. A passing build or unit test is not evidence of physical safety; mark simulated or mocked results as such.

## Workflow

1. Branch, pull request, owner and independent reviewer approval (ACT-DEC-014).
2. `make check` must pass.
3. Power-stage and motor-control safety are not self-approved.
4. Loaded and fault tests only on a restrained, guarded, instrumented fixture.
5. The mechanical HOLD was lifted in the parent (ACT-DEC-029, 2026-10-18). That does not authorise fabrication, procurement or loaded testing on its own: the gates and independent review still apply. `AGENTS.md` in this repository was updated to match.

## Git branch, commit and pull request rules

### Branch names

Never commit to `main`; it is protected. Branch from an up-to-date `main`:

```bash
git switch main && git pull --ff-only
git switch -c <type>/<TASK-ID>-<short-topic>      # task work
git switch -c chore/<short-topic>                 # repository housekeeping
```

Examples: `feat/ACT-EMB-003-encoder-rollover`, `docs/ACT-EMB-004-fault-table`, `chore/status-regenerate`. Use lowercase and hyphens. The `ACT-EMB` task IDs are in `status/tasks.csv`. These names are a recommendation that matches the existing `chore/...` branches; CI does not enforce them.

### Commit messages

Use a short imperative subject in one of these forms (parent `docs/standards/PROGRAM_ALIGNMENT.md`, section 3):

```text
ACT-EMB-003: add encoder rollover handling        <- preferred when the work belongs to a task
type(scope): summary                            <- repository style, for example chore(status): regenerate status.json
```

Suggested `type` values: `feat`, `fix`, `docs`, `test`, `chore`, `hw` (schematic, PCB or BOM). One atomic change per commit. Do not claim a test, review or acceptance that did not happen. Do not rewrite or renumber history.

What CI **does** enforce (`commit-message-check`): a commit must not contain a `Claude-Session:` trailer or a `claude.ai/code/session` link. A `Co-Authored-By:` line is allowed. Everything else above is a convention.

To catch a rejected message before pushing, install the local hook once (from the repository root):

```bash
printf '#!/bin/sh\npython3 scripts/security/check_commit_messages.py --file "$1"\n' > .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

### Pull requests

1. Push the branch and open a pull request into `main`.
2. Run `make check` and the unit tests first (see Checks above).
3. `main` requires `secret-scan`, `commit-message-check` and Code Owner review (owner statement; see `AGENTS.md`). With one owner, the PR author cannot approve their own PR: ask the owner to merge using the bypass, or add a second reviewer.
4. Power-stage and motor-control safety are not self-approved: safety-relevant firmware and hardware need the Independent Electrical/Firmware Reviewer (ACT-DEC-014). A green CI run never closes a gate.

## How to find out why a pull request failed

1. Open the pull request, scroll to the checks box at the bottom (or open the **Checks** tab). A red cross marks the failed check.
2. Click **Details** next to it and expand the failed step. The error line is usually at the end of that step.
3. Or from a terminal with the GitHub CLI: `gh pr checks <PR-number>`, then `gh run list --branch <branch>` and `gh run view <run-id> --log-failed`.
4. Reproduce it locally with the command in the table, fix, commit, and push to the same branch; the checks rerun.

| Failed check | What it ran | Reproduce locally | Usual cause and fix |
|---|---|---|---|
| `checks` | `make check`: electrical BOM schema, status | `make check` (or `make check-bom`, `make check-status`) | `check-bom`: wrong column or duplicate item ID in `hardware/bom/ELECTRICAL_BOM.csv`. `check-status`: `status/status.json` is out of date; run `python3 scripts/status/gen_status.py --root .` and commit the result (never edit it by hand) |
| `commit-message-check` | Unit tests of the checker, then the checker on every commit in the PR | `python3 -m unittest discover -s tests/commit_message_check -v` then `python3 scripts/security/check_commit_messages.py --range origin/main..HEAD` | A commit carries a `Claude-Session:` trailer or session link. Amend the latest unpushed commit (`git commit --amend`). For commits already pushed, ask the owner before rewriting history |
| `secret-scan` | gitleaks 8.18.4 over the full git history | Install gitleaks 8.18.4, then `gitleaks detect --source . --redact --verbose --exit-code 1` | A credential, key or token is in the history. Do not add an allowlist entry. Tell the Security Owner (Dinesh) at once; the secret must be revoked or rotated, and removing it in a later commit is not enough |

There is no firmware build job in this repository yet (it is planned with `firmware/CMakeLists.txt`). If the failure is in a step you did not touch, rerun the job once from the Actions page; if it fails again, ask the owner. If the log shows a missing tool or Python module, the runner image changed: report it rather than disabling the check.
