# f-02-implementer-handoff — Implement the writer and reviewer handoff

- Project: `agent-playbook`
- Source repository: https://github.com/SharonLanger/agent-playbook
- Status: Draft; not approved for implementation.
- Revision: Draft 1
- Inspection baseline: `9c674a76ee2dec04e5f05e5bdd6b8c564e761c86`
- Feature identifier: `f-02-implementer-handoff`

## Problem and intended outcome

agents/code-writer.md is a stop placeholder. Define an implementer that can consume an approved design, deliver code and tests, and respond to a reviewer without changing the requirements to fit its implementation.

## Scope and approach

Implement the existing agents/code-writer.md role; retain that filename to avoid a second overlapping role. Use a direct session invocation first. The user supplies the exact project name, source repository, feature/design path and approved revision, working branch, and report destination. An existing review report is an optional input for a fix pass.

The implementer reads relevant repository instructions and approved deviations, writes code and meaningful tests, runs required checks, and fixes routine failures. It may create or update an authorized feature branch and PR. It must not push to main/master, merge, rewrite the approved design, or approve its own review.

Use a single implementation report with code revision, design revision, changed behavior, commands/results, unresolved problems, and dispositions for review findings. Prefer objective test results to narrative claims. Define a small result contract with three proposed outcomes: ready_for_review, needs_design_decision, and blocked, plus report path and code revision. These outcome names are proposed by this draft and become the agreed contract only after approval.

Ordinary internal implementation choices remain with the implementer. Material design questions stop the affected work and return to the user until the deviation feature is available. Tests and code stay within the same role.

## Acceptance criteria

- The implementer starts from an explicitly approved design and identifies the revision used.
- It writes tests alongside code and reports failed, skipped, unrun, or stale checks accurately.
- It reports ready_for_review only when required checks pass, or an explicit approved exception exists and is identified.
- It addresses each must-fix review finding or explains a disagreement with evidence; it cannot declare a reviewer finding resolved on the reviewer's behalf.
- It escalates changes to scope, public behavior, security assumptions, or acceptance criteria.
- It leaves a usable report and branch/PR reference for a fresh reviewer.
- A report from a prior revision is not represented as approval of new code.

## Verification scenarios

| Scenario | Expected behavior |
| --- | --- |
| Small approved feature with clear acceptance tests | Implement behavior and tests; run relevant checks; report code and evidence revisions. |
| Implementation introduces a test failure | Fix it within scope before requesting review; do not silently skip or weaken the test. |
| Missing tooling or credentials | Report blocked with the failed command and what is needed; do not claim unrun checks passed. |
| Required behavior appears impossible under the approved design | Return needs_design_decision with evidence and proposed alternatives. |
| Internal helper refactor preserving behavior | Proceed within project rules without unnecessary replanning. |
| Reviewer returns a concrete defect | Fix it, add a relevant regression check, rerun affected checks, and map the finding to evidence. |
| Reviewer suggests an optional refactor | Explain whether it was taken; do not treat it as a mandatory design expansion. |
| Resume after an interruption | Inspect the branch, existing PR, and report before continuing; do not duplicate an already-created PR. |

Use one small real feature after approval and supplement only missing cases with bounded examples. Verify the diff, test evidence, and report against source state. No orchestrator or automated retry service is required.

## Delivery sequence and dependencies

Evaluate f-01-reviewer-trial before finalizing the handoff format. Then implement the role and README invocation, run one implementer-to-reviewer handoff manually, and save a concise outcome record. Keep automated coordination deferred.

## Open decisions

Select the small feature for the implementation trial. Choose a finite check/fix attempt limit before that run; at the limit, save findings and report blocked. Token estimates and hard cost enforcement remain outside this feature.
