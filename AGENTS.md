# Kritva Actuator Embedded Agent Instructions

These instructions apply to the `kritva-actuator-embedded` repository, a child of `KritvaOS/kritva-actuator` (the parent).

## Boundaries

- This repository holds firmware, controller hardware, electronics and firmware documents for the whole actuator family (S, M, L). Firmware is one code base with per-variant configuration in `firmware/variants/`, not three forks.
- Passing firmware or unit checks is not evidence of physical safety. Do not invent hardware behaviour; mark simulated or mocked results as such.
- The CAN protocol and interface are owned by the parent; do not redefine them here.

- The mechanical HOLD (kritva-program D-003) was lifted by Dinesh in ACT-DEC-029 (2026-10-18). That does not authorise CAD release, procurement, fabrication or design freeze work by itself: these need Gate A and the pending decisions in the parent `planning/v1/DECISIONS.md`, with independent review (ACT-DEC-014). Fabrication starts only after Gate A passes plus the release and procurement gap (ACT-DEC-033). Do not treat any check in this repository as physical safety or design acceptance.
- Status reports (`status/status.json`, schema 2.0) are planning-only. Regenerate them from `status/tasks.csv`; do not edit them by hand, and do not mark tasks accepted. Nothing here creates program credit.
- Interface, CAN protocol, units and shared requirements are owned by the parent `kritva-actuator` repository (ICD at `docs/interfaces/`). Do not redefine them in a child repository.

## Validation before a pull request

    make check

## Secrets and data

- Never commit credentials, tokens, private keys, production data or personal data. Use obviously fake values in examples and mark them as such.
- If a secret is committed by mistake, tell the Security Owner (Dinesh, D-032) at once. Removing it in a later commit does not make it safe; it must be revoked or rotated.
- The `secret-scan` workflow (gitleaks) runs on every push and pull request. Do not add allowlist entries to silence it; propose them to the owner with the reason.

## Commits and pull requests

- Work on a branch and open a pull request. Do not push to `main`. Do not force-push shared branches or rewrite history without the owner's explicit approval.
- Use short imperative messages in the repository's existing style (`type(scope): summary`).
- Do not add `Claude-Session:` or session-URL trailers to commit messages or pull request descriptions. The `commit-message-check` workflow rejects them. A `Co-Authored-By:` line is allowed.
- `main` is protected by a ruleset that requires `secret-scan`, `commit-message-check` and Code Owner review (owner statement, D-040; not independently verified). With one owner, the PR author cannot self-approve: ask the owner to merge using the bypass or add a second reviewer.

## When unsure

Say what you do not know and ask the owner. Do not invent evidence, test results, hardware behaviour or approvals, and do not claim a check passed unless you ran it.
