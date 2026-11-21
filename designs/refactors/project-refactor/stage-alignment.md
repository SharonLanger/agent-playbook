# Existing-stage alignment

Sharon requested applying the approved stage structure to existing stages on 2026-11-19 and assigned a Sol sub-agent. This follow-up builds on the [approved standard](stage-structure.md) and its completed review. It applies to the completed stages already on main through draft [PR #59](https://github.com/SharonLanger/agent-playbook/pull/59). The starting PR head is [`a8d71539`](https://github.com/SharonLanger/agent-playbook/commit/a8d7153965f1006fa0ce8d79697ac21a98e4dfc6) and the checked main base is [`cdbc06c2`](https://github.com/SharonLanger/agent-playbook/commit/cdbc06c2e9a9b87910b5145ac116aeb8a81e06e4).

## Record ownership

| Stage | Existing source and destination | Retained boundaries |
|---|---|---|
| [00 — Development environment](../../stages/00-environment/README.md) | The guarded [plan](../../stages/00-environment/plan.md#substages), [findings](../../stages/00-environment/findings.md) and [progress evidence](../../progress.md#langfuse-branch-detail-earlier-integration-checkpoint) supply a new README milestone index for 00.1–00.7. | Design PR #15, implementation PRs #17–#23 and stage closeout PR #26 retain their roles. The guarded architecture and plan stay at their paths, including the documented CrewAI import/scope discrepancy and original status headings. |
| [01 — CrewAI Flows](../../stages/01-crewai-flows/README.md) | The approved [sequence](../../stages/01-crewai-flows/plan.md) and [findings](../../stages/01-crewai-flows/findings.md) supply the README index for 01.1–01.5. | The five substages shipped in one batch in PR #30 after design PR #29. Workflow IDs identify implementation contracts. Later workflow examples and runtime/contract refactors retain their own evidence and PRs. |
| [02 — Langfuse](../../stages/02-langfuse/README.md) | The original [milestone plan](../../stages/02-langfuse/milestones.md), [closeout](../../stages/02-langfuse/closeout.md) and [workflow-integration package](../../stages/02-langfuse/m4-workflow-integration/README.md) supply the canonical README index. Earlier status and handoff records are marked historical there. | M1–M3 share PR #36. M4.R is a research prerequisite. The existing package maps M4.1 to `m1-context/` and M4.2 + M4.3 to `m2-3-workflow-tracing/`. Those contracts, review rounds, approved revisions, PR #44/#50 evidence and PR #47's accepted closeout retain their history. |
| [03 — Orchestration patterns](../../stages/03-orchestration-patterns/README.md) | The source README's requirements table and immediately following scope note move verbatim to [requirements.md](../../stages/03-orchestration-patterns/requirements.md). The original README heading links to the relocated text. | Protection follows the approved text. The source at `a8d71539` includes the later R11 cleanup decision. `6067fb652f0bffe2fa1f8a0e53f045a421a16f11` remains the earlier pinned S03.M1 contract. The [decision log](../../stages/03-orchestration-patterns/decisions.md) and [milestone package](../../stages/03-orchestration-patterns/m1-recipe-batch/README.md) retain their paths and contents. The README records the actual #53 implementation and #52 closeout merges. |

The stage READMEs own current milestone navigation and next actions. Historical stage-wide plans, requirements, tests and verification remain with their original owners. Stages 00, 01 and Stage 02 M1–M3 predate the modern standalone milestone package. Their joint records and older approvals remain the evidence for those milestones. The repository [progress roll-up](../../progress.md) continues to own project-wide status.

## Scope and branch coordination

The [design index](../../README.md) and [Atlas](../../atlas/README.md) link the completed stage indexes. Stage 02 navigation reflects the accepted closeout and distinguishes the historical observability research from delivered integration. Logging remains a separate workstream with separate evidence.

[Stage 04 PR #45](https://github.com/SharonLanger/agent-playbook/pull/45) owns the draft Stage 04 workspace. [Logging design PR #51](https://github.com/SharonLanger/agent-playbook/pull/51) and [logging M3 PR #57](https://github.com/SharonLanger/agent-playbook/pull/57) have separate owners and scope. Shared design index, exploration index and Atlas changes may need reconciliation when their owners integrate main. The three guarded combined-tracing contract files referenced by logging design retain their paths and bytes in this work.

The [charter](../../charter.md), [principles](../../principles.md), [design contract](../../governance/design-contract.md) and [guard register](../../governance/guarded-files.md) govern this alignment. Relocating the Stage 03 requirements preserves their approved meaning and existing scope. The [exploration index](../../explorations/README.md) identifies the Stage 02 research context. Supported commands, configuration and behavior remain the same, so official application guides require no amendment. The shared-learning and root-sandbox migration remains proposed.

## Stage 02 documentation relocation — 2026-11-21

Sharon authorized relocating the completed Stage 02 documentation. This supersedes the earlier location-retention statement only for Stage 02. The former `workflow-integration/` package is now [M4 workflow integration](../../stages/02-langfuse/m4-workflow-integration/README.md), and the existing joint local records are grouped under [M1–M3 local Langfuse](../../stages/02-langfuse/m1-3-local-langfuse/README.md). Approved contracts, pinned references, review evidence and acceptance history retain their original authority. The earlier PR #59 scope and acceptance checks below remain historical.

## Acceptance checks

| ID | Check |
|---|---|
| AL01 | Stage 00–03 READMEs have one canonical milestone table and a next action. Existing substage IDs and batch or combined milestone histories are retained. |
| AL02 | The recorded design authority, implementation PR, verification, acceptance and merge evidence agree with the original stage records and actual PR states. Earlier status is identified as historical. |
| AL03 | Stage 03's exact R01–R12 table and attached scope note match the starting README bytes and are accessible from the old heading. Approved semantics and frozen stage contracts retain their protection and original revision evidence. |
| AL04 | The edited documentation and Atlas resolve the intended stage, plan and evidence links and anchors. Atlas generates successfully and its freshness/reference check passes. Stage 02's completed status and the separate logging scope agree with merged evidence. |
| AL05 | The diff stays within stage indexes, Stage 03 shared requirements, navigation, generated Atlas and refactor records. Existing stage packages, the completed structure-review evidence and prior publication-link cleanup are preserved. |
| AL06 | The change stays on existing draft PR #59. Stage 04 and logging workspaces are separately owned; their branch heads and contracts are preserved. |

This alignment has its own review scope. Apply the [bounded independent-review procedure](../../governance/codex-handover-rules.md#roles-and-rounds) to each frozen candidate and retain actual review rounds under `reviews/stage-alignment/`. The earlier SS01–SS06 verdict covers the original governance change.
