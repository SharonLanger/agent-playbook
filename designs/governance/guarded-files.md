# Guarded-file register

Status: **GUARDED.** The existing protection set is preserved; additions below were approved by Sharon for PR #35 on 2026-11-13. This register is a minimum, not an exhaustive exemption list.

## Core guarded documents

- `designs/charter.md`
- `designs/principles.md`
- `designs/architecture.md`
- `designs/project-structure.md`
- `designs/governance/design-contract.md` — new guarded process contract.
- `designs/governance/guarded-files.md` — this register; removing entries requires approval.

## Existing stage protection retained

- `designs/stages/00-environment/architecture.md`
- `designs/stages/00-environment/plan.md`
- `designs/stages/01-crewai-flows/architecture.md`
- `designs/stages/01-crewai-flows/file-structure.md`
- `designs/stages/01-crewai-flows/plan.md`
- `designs/stages/01-crewai-flows/test-plan.md` — acceptance requirements within the approved stage design.
- `designs/stages/01-crewai-flows/workflows/wf-01-step-sequence.md`
- `designs/stages/01-crewai-flows/workflows/wf-02-shared-state.md`
- `designs/stages/01-crewai-flows/workflows/wf-03-conditional-route.md`

Stage 00 architecture/plan still have old proposed-status wording. Progress records later approval/acceptance; that inconsistency does not make them editable without approval. They are not rewritten by this PR. Stage 01 README identifies architecture, file structure, plan and workflow contracts as approved baselines. Their protection and historical material remain intact.

## Approved workflow-contract baseline

- `designs/refactors/workflow-contract/README.md`
- `designs/refactors/workflow-contract/design.md`
- `designs/refactors/workflow-contract/file-structure.md`
- `designs/refactors/workflow-contract/test-plan.md`
- `designs/refactors/workflow-contract/implementation-plan.md`
- `designs/refactors/workflow-contract/review-follow-up.md`
- `designs/refactors/workflow-contract/review-test-quality.md` — requested second-review test corrections; no new runtime architecture.

Sharon approved this design and the enumerated guarded changes for PR #40. On 2026-11-13 he requested the review follow-up: lazy dependency imports now, constructor and diagnostic corrections, and completion of the agreed test plan. After the second review of f61683c, Sharon requested another detailed handoff for Q1–Q4 and replacement of ineffective tests where coverage is preserved. The added file and companion status/navigation corrections clarify existing acceptance; they do not change runtime contracts. These approval records do not authorize merging either PR or adding deferred features.

## Rules beyond the list

Any other document or portion explicitly approved, locked or guarded remains protected, including future stage baselines. Approved behavioral contracts represented in diagrams or copied into instructions retain protection. A rename, generated view, omission from this register or obsolete status heading never removes it.

Progress, findings, exploration notes and navigation may evolve from verified evidence without becoming frozen baselines. That permission does not permit rewriting historical acceptance, altering guarded meaning through a summary, or labeling a new idea approved.

Use the logical-change approval process in [design-contract.md](design-contract.md). Record additions to this register when a new baseline is approved. Preserve prior guard records during merges, particularly when reconciling PR #34 and #35.

## M4.1 approved baseline — 2026-11-14

Sharon's implementation instruction explicitly approved revision `11bba581291c1b166973848ea8db6a9e2a142413` and guarded amendments G01–G08 in design section 9. The following files are guarded from that approval:

- `designs/stages/02-langfuse/m4-workflow-integration/m4-1-context/design.md`
- `designs/stages/02-langfuse/m4-workflow-integration/m4-1-context/test-cases.md`
- `designs/stages/02-langfuse/m4-workflow-integration/m4-1-context/implementation-plan.md`

## Reusable development process — 2026-11-15

Sharon requested the generalized stage/milestone and Codex handover process as guarded reusable rules, published separately from ongoing stage design. This registration preserves all existing protections and does not approve any milestone implementation.

- `designs/governance/stage-milestone-workflow.md`
- `designs/governance/codex-handover-rules.md`

The 2026-11-15 PR #48 alignment extends these procedures with the Stage Design PR lifecycle, incremental milestone approval and separate explicit merge gate. It also amends charter/principle 9 for the narrow Stage 04 sequencing exception. All existing protections remain; no draft Stage 04 milestone is registered as a locked baseline by this change.

## M4.2/M4.3 approved baseline — 2026-11-15

Sharon explicitly approved the M4.2/M4.3 design, tests and plan at `ab3fab459c97eed44cc0b202402e559a827a71cf` and RUN-G01–08 in the implementation handoff on 2026-11-15. Stage Design PR #47 has merged, and the following guarded documents are now present in the repository. Use the local links for current reading; the immutable links preserve the exact approved baseline:

| Guarded path | Immutable authority |
|---|---|
| [designs/stages/02-langfuse/m4-workflow-integration/m4-2-3-workflow-tracing/design.md](../stages/02-langfuse/m4-workflow-integration/m4-2-3-workflow-tracing/design.md) | [Pinned approved file](https://github.com/SharonLanger/agent-playbook/blob/ab3fab459c97eed44cc0b202402e559a827a71cf/designs/stages/02-langfuse/workflow-integration/m2-3-workflow-tracing/design.md) |
| [designs/stages/02-langfuse/m4-workflow-integration/m4-2-3-workflow-tracing/test-cases.md](../stages/02-langfuse/m4-workflow-integration/m4-2-3-workflow-tracing/test-cases.md) | [Pinned approved file](https://github.com/SharonLanger/agent-playbook/blob/ab3fab459c97eed44cc0b202402e559a827a71cf/designs/stages/02-langfuse/workflow-integration/m2-3-workflow-tracing/test-cases.md) |
| [designs/stages/02-langfuse/m4-workflow-integration/m4-2-3-workflow-tracing/implementation-plan.md](../stages/02-langfuse/m4-workflow-integration/m4-2-3-workflow-tracing/implementation-plan.md) | [Pinned approved file](https://github.com/SharonLanger/agent-playbook/blob/ab3fab459c97eed44cc0b202402e559a827a71cf/designs/stages/02-langfuse/workflow-integration/m2-3-workflow-tracing/implementation-plan.md) |

All previous guards and the recorded approval baseline remain. PR #47's merge does not remove protection or authorize changes to these documents or frozen shared requirements/decisions.


## LOG-G06 — logging M2 approved baseline, 2026-11-16

Sharon approved M2 behavior and LOG-G01–06 at immutable revision `caeb1637bd9aa611447703f4c19c38becacfe412`. The following contract files remain guarded after design closeout in #51. The links preserve the approved revision.

| Guarded path | Immutable authority |
|---|---|
| `designs/refactors/logging/m2-application-logging/design.md` | [Pinned approved file](https://github.com/SharonLanger/agent-playbook/blob/caeb1637bd9aa611447703f4c19c38becacfe412/designs/refactors/logging/m2-application-logging/design.md) |
| `designs/refactors/logging/m2-application-logging/test-cases.md` | [Pinned approved file](https://github.com/SharonLanger/agent-playbook/blob/caeb1637bd9aa611447703f4c19c38becacfe412/designs/refactors/logging/m2-application-logging/test-cases.md) |
| `designs/refactors/logging/m2-application-logging/implementation-plan.md` | [Pinned approved file](https://github.com/SharonLanger/agent-playbook/blob/caeb1637bd9aa611447703f4c19c38becacfe412/designs/refactors/logging/m2-application-logging/implementation-plan.md) |


All earlier protection and Stage 02 history remain intact.

## PR CI and local version tracking — 2026-11-21

[Sharon’s approval](https://github.com/SharonLanger/agent-playbook/pull/63#issuecomment-7062463938) locked the [implementation package](https://github.com/SharonLanger/agent-playbook/tree/6ce53c2377dc21541d94ca8a461bd02d66af7655/designs/refactors/pr-ci) at `6ce53c2377dc21541d94ca8a461bd02d66af7655`. The package README tracks status and evidence. Implementation acceptance and hosted enforcement have their own gates.

- `designs/refactors/pr-ci/requirements.md`
- `designs/refactors/pr-ci/decisions.md`
- `designs/refactors/pr-ci/design.md`
- `designs/refactors/pr-ci/test-cases.md`
- `designs/refactors/pr-ci/implementation-plan.md`
