# Agent execution foundation — start here

> **DO NOT MERGE PR #45 — MERGE LAST, AFTER ALL STAGE 04 IMPLEMENTATION PRs.** This is the ongoing design workspace. Keep it open through every milestone; reconcile final documentation after the entire Stage 04 implementation is accepted and merged, then merge this PR only with Sharon's explicit final authorization. Individual design/milestone approval does not authorize merging it.

Updated: 2026-11-25 · Working records revision 33
Status: **draft planning PR authorized by Sharon; no runtime implementation, stage activation, locked milestone baseline or merge authorization.**

This is the permanent Stage 04 design workspace on `docs/agent-execution-foundation-planning`. Focused M1 design proceeds in [draft PR #72](https://github.com/SharonLanger/agent-playbook/pull/72), targeting this stage branch; changes recorded there remain on its branch until separately merged. The checked main baseline is [`d17972e4`](https://github.com/SharonLanger/agent-playbook/commit/d17972e4b7f40e9a1e0fbf23afe02c874c2a12b7). The [navigation exception](decisions.md#shared-navigation-exception) adds four shared discovery files to the stage package. Stage 04's boundary and four milestone allocations/gates are approved; detailed milestone designs and implementation are not. PR #45 follows `[Stage 04 Design] Agent execution foundation` and stays draft through stage closeout.

## Read in this order

1. Follow [stage working method](../../governance/stage-milestone-workflow.md) and [Codex handover rules](../../governance/codex-handover-rules.md), plus [design instructions](../../AGENTS.md), the [design contract](../../governance/design-contract.md) and [guarded-file register](../../governance/guarded-files.md). Check [progress](../../progress.md), [roadmap](../../roadmap.md), charter, principles, architecture and structure as required there.
2. Read the complete [specification](specifications.md): current accepted requirements, desired layout and explicit open questions.
3. Read the complete [decision board](decisions.md): approvals, alternatives, objections, corrections, research evidence and unresolved questions. **Approved in discussion** is different from **canonical milestone approved/locked**.
4. Read [milestone-plan.md](milestone-plan.md): bounded checkpoints, prerequisites, exclusions, proposed acceptance and the mandatory plan-first change log.
5. Read [history](history/README.md) for provenance and the subsequent discussion. Original records remain exact snapshots. They do not compete with the active specification/board.
6. Consult [research references](research/README.md) when designing mappings, settings and capabilities.
7. Check [repository-updates.md](repository-updates.md) before an implementation lock, scope change or review-ready claim. [verification.md](verification.md) records this documentation PR's evidence.

## What the package establishes

The accepted architecture direction is small: application agent roles, an injected common wrapper, a provider execution adapter, a native-to-shared event mapper and one typed asynchronous callback. The three ABCs are Agent, ExecutionAdapter and EventMapper. EventHandler is a callable signature. The native runtime keeps its model/tool loop; CrewAI keeps workflow scheduling.

## Canonical milestone and readiness index

| Milestone / bounded outcome | Design readiness and approval | Implementation PR | Review evidence | Acceptance / merge |
|---|---|---|---|---|
| S04.M1 — three ABCs, callback, event/request/result/settings/permission data | [Draft package](m1-contracts-models/README.md) in #72; D54–D56 validation, standard exceptions and immutable event snapshots approved; detailed design not locked; no approved SHA | Not opened | None | Pending / unmerged |
| S04.M2 — harness and fake adapter/mapper with success/failure | Boundary approved; detailed design waits for M1 contract approval; implementation requires accepted/merged M1 | Not opened | None | Pending / unmerged |
| S04.M3 — standalone DemoAgent with task/result and handler | Boundary approved; detailed design waits for M2 path; implementation requires accepted/merged M2 | Not opened | None | Pending / unmerged |
| S04.M4 — one maintained CrewAI integration | Boundary approved; detailed design waits for M3 invocation plus current workflow/context compatibility; implementation requires accepted/merged M3 and concrete external prerequisites | Not opened | None | Pending / unmerged |

[Milestone plan](milestone-plan.md#design-progression-and-readiness--d40d41) owns the detailed inclusions/exclusions, gates and question sequence. M1–M3 require no context/tracing/workflow. M4 does not wait for all of Stage 02/03, only actual dependencies. Real SDKs/adapters and coder/reviewer roles stay Stage 05; no tracing/logging subsystem is added.

M1 has a [draft detailed package](m1-contracts-models/README.md) in PR #72. Future packages: m2-fake-execution/, m3-demo-agent/, m4-workflow-integration/. Create README.md, design.md, test-cases.md and implementation-plan.md together when each enters detailed design; the later packages do not exist yet. No empty review evidence is created. specifications.md remains this stage's shared requirement owner.

## Required working rules

- Before every substantive iteration, read the full current specification, decision board and milestone plan. Use stable IDs; do not infer approvals from examples, research or this README.
- A milestone boundary change starts as a **Pending delta in the milestone plan**. Check every affected decision/specification and prerequisite. Surface contradictions before changing agreed meaning.
- Once authorized, update the effective boundary, decision history, specification and affected milestone design/acceptance documents together. Preserve the old reason and the new approval. Do not change code first and rewrite the plan afterward.
- Keep proposed, accepted discussion choice, approved/locked design, implemented, verified, user-accepted and merged distinct. Recording an idea is not approval; opening this PR is not approval to merge or implement it.
- Detailed milestone designs must identify their exact baseline, in/out scope, contracts/placement, requirement/decision IDs, dependencies, open blockers, acceptance cases and next-agent instructions. M1's files are drafts; complete them together as choices are resolved.
- Keep the roadmap and guarded meaning unchanged in this PR. Before implementation, propose the specific canonical amendments listed in repository-updates.md.
- Read only maintained source/tests needed for the task. Personal examples remain excluded. Do not create a separate event bus, tracing broker, generic framework, context model or permission engine to fill a deferred dependency.
- At implementation handoff, pin the approved design, test cases and plan. Freeze that contract. The design-drift and test-gap reviewers review the same candidate SHA in each round. Keep their evidence under the milestone and follow the three-round limit in the [handover rules](../../governance/codex-handover-rules.md). The design session records its final review before user acceptance and merge.
- After meaningful progress, update these records and actual status/check evidence. This is an iteration rule, not an unattended scheduled task.

## Next step

Sharon resumed M1 detailed design in #72. The [current alignment checkpoint](decisions.md#m1-alignment-checkpoint--2026-11-25) records the baseline and remaining choices. D54/D55 settle construction-time validation, propagation and standard exceptions with model/field/rule diagnostics; D56 adds immutable event snapshots while preserving future hook responses; continue remaining schema choices one at a time. The milestone table above owns current status. Earlier readiness assessments in the plan and the dated revision sections describe their original checkpoints.

Stage 02 context and tracing, Stage 03 orchestration and the logging refactor have merged. For M4, check the [actual workflow integration](../02-langfuse/m4-workflow-integration/README.md) against M3’s invocation contract. The [progress record](../../progress.md) links the merged evidence.

## Approved parallel-work gates

D39 requires independent progress without placeholder context. D40 accepts BC03 in the milestone plan: M1–M3 standalone and M4 gated on concrete merged/compatible workflow/context contracts. Whole Stage 02/03 completion is not a blanket prerequisite. Existing context has for_agent; a separate AgentContext remains exploratory. Boundaries are approved; no runtime implementation starts before its milestone design/test/plan is approved and pinned.

While an implementation handoff is active, freeze its governing milestone and shared contract files; capture new issues separately as follow-ups under the merged Codex rules. No Stage 04 handoff is active now.

Current discussion: P13/BC04 evaluates a narrow runtime-control hook alongside observation events. Scope change is pending; review before adding hook contracts or M2 acceptance.

Product target (D50/D51): replaceable execution supporting a real coder/reviewer workflow after native integration. P14 records the reference comparison and proposed control/data boundaries; current Stage 04 deliverables and pending BC04 status remain unchanged.
