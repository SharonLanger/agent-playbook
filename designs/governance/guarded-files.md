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

- `designs/stages/02-langfuse/workflow-integration/01-context-design.md`
- `designs/stages/02-langfuse/workflow-integration/01-context-test-cases.md`
- `designs/stages/02-langfuse/workflow-integration/01-context-implementation-plan.md`
