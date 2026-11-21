# Repository reconciliation and implementation gates

> **DO NOT MERGE PR #45 — MERGE LAST, AFTER ALL STAGE 04 IMPLEMENTATION PRs.** This is the ongoing design workspace. Keep it open through every milestone; reconcile final documentation after the entire Stage 04 implementation is accepted and merged, then merge this PR only with Sharon's explicit final authorization. Individual design/milestone approval does not authorize merging it.

Status: **open checklist for future design/implementation; no guarded changes made by this PR.**

[Start here](README.md) · [Milestone boundaries](milestone-plan.md) · [Decision board](decisions.md)

## Current scope

D52 establishes the stage-local default. [D53](decisions.md#shared-navigation-exception) authorizes four shared navigation files. The [alignment checkpoint](decisions.md#scope-and-methodology-checkpoint) and [milestone table](README.md#canonical-milestone-and-readiness-index) record current status. The evidence below identifies earlier baselines by revision.

## Original change record

**Objective and authorization:** Sharon requested the permanent draft design PR and explicit milestone boundaries with plan-first consistency checks. D27–D32 capture the scope. Existing D02–D26 govern role/provider separation, three ABCs, owned shared events, autonomous execution and minimal reuse.

**Placement:** repository → `designs/` → permanent stage planning → `04-agent-execution/`. Inputs are the revision-12 working records, original reconstructed handover, subsequent discussion, canonical main design and PR #43's organization. Outputs are the active spec/board, draft milestone plan and retained evidence. This documentation package does not establish runtime component ownership ahead of canonical reconciliation.

**Authorities consulted:** root/designs instructions, design contract, guarded register, charter, principles, architecture, structure, roadmap, progress and active Stage 02 architecture/milestones at main `d12b5fc2867d3646b6fab2eb71f1447ff177d8c1`. Relevant [execution exploration](../../explorations/agent-execution/README.md) retains earlier Protocol/iterator, richer schema and folder alternatives. Current discussion accepts separate ABCs/callbacks instead; other exploratory features are not adopted.

## Before locking or implementing a milestone

| ID | Affected authority / surface | Proposed logical reconciliation | Gate / status |
|---|---|---|---|
| RU01 | [Architecture](../../architecture.md) | Explain execution-owned native-message normalization versus telemetry projection; identify role, harness, mapper and callback ownership while preserving native loop/CrewAI boundaries. Use the native tracing boundary on current main. | C01/Q12 open. Present exact logical amendment per file and obtain scoped approval before editing. |
| RU02 | [Project structure](../../project-structure.md) | Add the agreed roles boundary, three separate behavioral-contract files, owned execution data/harness/fake and later native integrations. Resolve first-demo/helper paths without generating speculative folders. | C01/Q12/Q34 open; same guarded approval gate. |
| RU03 | [Charter](../../charter.md), [principles](../../principles.md), [roadmap](../../roadmap.md) | Before implementation lock, review how this proposed foundation-first allocation fits future-stage/current-stage and learning sequence rules. Draft planning itself does not alter these rules. Native work must still respect the agreed learning prerequisites unless deliberately changed. | The merged roadmap records the Stage 04 sequencing exception. Check the actual milestone dependencies before lock. |
| RU04 | [Guarded register](../../governance/guarded-files.md) and milestone design | Once a concrete milestone baseline is approved/locked, register its guarded authority with approval evidence. Protection already follows explicitly approved content even if omitted from the register. | Do not register this entire draft as locked merely because it exists. |
| RU05 | [Merged Stage 02 workflow/context package](../02-langfuse/m4-workflow-integration/README.md) | Re-read actual context fields, constructor propagation and correlation requirements before integration. Decide standalone-agent context use; retain execution ownership of adapter/session lifetime. | Q09/Q35; no context implementation or copying of draft schema in this PR. |
| RU06 | Logging/observability owner | Define how normalized execution evidence is observed and recorded, failure/redaction policy, correlation and acceptance. No tracing broker or execution-owned logging backend. | Q17/Q38 remain open. D12's product requirement is not fulfilled by a fake/test recorder. |
| RU07 | Existing application assembly/configuration/workflow contract | During S04.M4 detail, specify only needed construction, selected YAML data, role invocation and sync/async boundary. Preserve validation/lifecycle and CrewAI scheduling. | Not a prerequisite to designing isolated M1 data; required before workflow implementation. |
| RU08 | Official app/docs, checks and release inputs | Publish supported commands/configuration only with working implementation. Use maintained independent test fixtures, standard quality gates and applicable release checks. | No current public-guide impact: this PR changes no supported behavior, commands, defaults, installation or output. |
| RU09 | Progress, navigation and Atlas | Add Stage 04 navigation in `designs/README.md`, `designs/explorations/README.md`, `designs/atlas/README.md` and `designs/atlas/catalog.json`. Record milestone status in the stage README. | D53. Sharon owns HTML regeneration. Project-wide progress awaits separate discussion. |
| RU10 | Native integration | Select/reverify SDK/runtime versions, licensing if code/dependencies are reused, native mapping/capability evidence, permission enforcement and lifecycle acceptance. | Later design, separate from fake contract acceptance; no dependency adopted here. |

No unresolved item in this table prevents **creating the draft planning PR**. Items become blocking at their named design/implementation gate. No author may resolve a conflict by simply relabeling an exploration as approved.

## Principle-by-principle assessment

| Principle | Evidence / applicability in this PR |
|---|---|
| 1 Explicit approvals | D31 permits documentation PR; guarded meaning and roadmap unchanged; RU01–RU04 name future approvals. |
| 2 Security | No credentials, live provider invocation or sensitive native traces added. Future diagnostic/permission scope remains explicit. |
| 3 No design drift | Full active spec/board reading and D32's plan-first pending-change process; C01 retained. |
| 4 Learning first | Bounded milestones with future design, approval, implementation, checks and findings; no skipped implementation gate. |
| 5 Isolated integrations | D02/D03/D04/D22/D26 keep provider types/loops inside integrations and common contracts independent. |
| 6 External configuration | No new loader or hard-coded credentials/settings; schema remains a detailed-design question. |
| 7 Reproducible quality gates | Documentation/Atlas/source checks now. Application gates apply when code changes; no new dependencies or CI. |
| 8 Evidence over claims | Baseline and PR #43 heads recorded; fake/native limitations retained; verification reported separately. |
| 9 Incremental scope | Parallel draft planning requested; stage activation/implementation commitments await deliberate review. The merged roadmap records the Stage 04 exception. |
| 10 Local-first | Deterministic offline foundation planned; no assertion that later live model calls are offline. |
| 11 No silent migration | Historical sandbox unchanged; original working records retained byte-for-byte. |
| 12 Traceability | Requirement, decision, question, milestone and boundary-change IDs with a permanent entry point. |
| 13 Personal sandbox isolation | No access or changes to personal examples; future maintained fixtures must be independent. |
| 14 Official documentation | No supported behavior change; public docs unchanged for that concrete reason. Future working demo requires public instructions. |
| 15 Honest status | Accepted discussion choices distinguished from pending schema/acceptance details, implementation, verification, acceptance and merge. |

## Review checklist

- Preserve all original D01–D26, Q00–Q34, proposals, corrections and source snapshots; active amendments must state reasons.
- Confirm D27–D32 match direct discussion scope and do not turn the four detailed draft milestones or P01 into approved schemas.
- Check that every milestone declares inputs, exclusions, dependencies and exit limits.
- Check a proposed scope change must be recorded in the plan **before** decisions/specification are amended, without treating that proposal as authorization.
- Verify roadmap, all guarded files, app source/tests/settings/dependencies and historical sandbox are untouched.
- Verify that the PR diff is limited to Stage 04 and its explicitly approved exceptions, including after integrating a newer main.
- Record checks for the exact candidate. Do not merge this PR or begin implementation without the corresponding user instruction.

## PR #45 final merge gate — D33

Keep PR #45 open as the ongoing design workspace. After every Stage 04 implementation milestone has its required evidence/acceptance and its implementation PR is merged, reconcile all current records against main, preserve decision history, resolve remaining draft status/conflicts and run documentation/Atlas checks. Only then is PR #45 eligible for Sharon's explicit final merge instruction. Do not merge it merely to make a milestone design available to an implementation branch; reference the approved contract from that focused PR by immutable commit link. No merge happens automatically.

## Main integration and remaining gates — revision 19

Main fefe4cc1065642b710a018ecb1088ececde852db supplies the approved Stage 04 sequencing exception and reusable governance; older sequencing-unresolved entries above are historical. Preserve its charter, principles, architecture, structure, guard register and other-stage files exactly. C01/Q12 is not resolved by main integration: M1 design must present execution-event versus observability ownership and agents/ placement amendments before implementation lock. No such guarded change is made here. Stage Design naming/readiness table and progressive milestone planning are applied within this package.
