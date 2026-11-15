# Agent execution foundation — start here

> **DO NOT MERGE PR #45 — MERGE LAST, AFTER ALL STAGE 04 IMPLEMENTATION PRs.** This is the ongoing design workspace. Keep it open through every milestone; reconcile final documentation after the entire Stage 04 implementation is accepted and merged, then merge this PR only with Sharon's explicit final authorization. Individual design/milestone approval does not authorize merging it.

Updated: 2026-11-15 · Working records revision 18
Status: **draft planning PR authorized by Sharon; no runtime implementation, stage activation, locked milestone baseline or merge authorization.**

This is the permanent planning home for the proposed agent execution foundation. Use branch `docs/agent-execution-foundation-planning` until merged; do not assume these files exist on main. The original branch baseline was `d12b5fc2867d3646b6fab2eb71f1447ff177d8c1`. A read-only refresh of main at `fefe4cc1065642b710a018ecb1088ececde852db` confirms the Stage 04 sequencing exception and merged basic workflow context. This branch has not incorporated main; shared documentation reconciliation remains necessary. No roadmap edits here.

## Read in this order

1. Follow [design instructions](../../AGENTS.md), the [design contract](../../governance/design-contract.md) and [guarded-file register](../../governance/guarded-files.md). Check [progress](../../progress.md), [roadmap](../../roadmap.md), charter, principles, architecture and structure as required there.
2. Read the complete [specification](specifications.md): current accepted requirements, desired layout and explicit open questions.
3. Read the complete [decision board](decisions.md): approvals, alternatives, objections, corrections, research evidence and unresolved questions. **Approved in discussion** is different from **canonical milestone approved/locked**.
4. Read [milestone-plan.md](milestone-plan.md): bounded checkpoints, prerequisites, exclusions, proposed acceptance and the mandatory plan-first change log.
5. Read [history](history/README.md) for provenance and the subsequent discussion. Original records remain exact snapshots. They do not compete with the active specification/board.
6. Consult [research references](research/README.md) when designing mappings, settings and capabilities.
7. Check [repository-updates.md](repository-updates.md) before an implementation lock, scope change or review-ready claim. [verification.md](verification.md) records this documentation PR's evidence.

## What the package establishes

The accepted architecture direction is small: application agent roles, an injected common wrapper, a provider execution adapter, a native-to-shared event mapper and one typed asynchronous callback. The three ABCs are Agent, ExecutionAdapter and EventMapper. EventHandler is a callable signature. The native runtime keeps its model/tool loop; CrewAI keeps workflow scheduling.

| Planned checkpoint | Bounded deliverable |
|---|---|
| S04.M1 | Three ABCs, callback, agreed events/request/result and basic settings/permission data |
| S04.M2 | Harness, fake adapter and fake native-message mapper; deterministic success/failure path |
| S04.M3 | One DemoAgent using the foundation, with an explicit event handler and task/result path |
| S04.M4 | One maintained CrewAI demonstration invokes that agent through existing application infrastructure |

These are **draft milestone allocations for review**, not an instruction to build all four. The initial five event names/basic meanings are accepted (D34); D36 accepts the basic event/result fields; D37 accepts frozen dataclasses and role match dispatch; D38 forbids guessed tool pairing; validation, missing-ID policy, lifecycle/failure guarantees and acceptance details still require design. Real native SDKs/adapters/mappers and real coder/reviewer roles remain later integration. Context/Langfuse and actual logging integration stay with their separate owning work; no duplicate subsystem is introduced. A fake proves local behavior, not provider permission enforcement.

## Required working rules

- Before every substantive iteration, read the full current specification, decision board and milestone plan. Use stable IDs; do not infer approvals from examples, research or this README.
- A milestone boundary change starts as a **Pending delta in the milestone plan**. Check every affected decision/specification and prerequisite. Surface contradictions before changing agreed meaning.
- Once authorized, update the effective boundary, decision history, specification and affected milestone design/acceptance documents together. Preserve the old reason and the new approval. Do not change code first and rewrite the plan afterward.
- Keep proposed, accepted discussion choice, approved/locked design, implemented, verified, user-accepted and merged distinct. Recording an idea is not approval; opening this PR is not approval to merge or implement it.
- Detailed milestone designs must identify their exact baseline, in/out scope, contracts/placement, requirement/decision IDs, dependencies, open blockers, acceptance cases and next-agent instructions. Those files do not exist yet; start with S04.M1 after boundary review.
- Keep the roadmap and guarded meaning unchanged in this PR. Before implementation, propose the specific canonical amendments listed in repository-updates.md.
- Read only maintained source/tests needed for the task. Personal examples remain excluded. Do not create a separate event bus, tracing broker, generic framework, context model or permission engine to fill a deferred dependency.
- After meaningful progress, update these records and actual status/check evidence. This is an iteration rule, not an unattended scheduled task.

## Parallel work

The organization follows the useful parts of [PR #43](https://github.com/SharonLanger/agent-playbook/pull/43): one entry point, one current specification, decisions with evidence, preserved history and explicit reconciliation gates. Its context design remains separate. At the inspected head `11bba581291c1b166973848ea8db6a9e2a142413`, it was draft and unmerged.

Parallel design is appropriate; different subfolders do not remove shared configuration, assembly, workflow-constructor or documentation dependencies. Reinspect current main/PR state before implementing a crossing boundary. Merge navigation and catalog edits by meaning, then regenerate Atlas; never hand-merge generated HTML.

## Next step

Ready to begin S04.M1 detailed design. Keep its existing boundary and work through: (1) start/finish emission ownership and returned-result consistency, (2) callback ordering/failure and missing-evidence behavior, (3) request/basic settings/permissions and model validation. Reconcile approved requirements/decisions and current canonical authority before locking the milestone. Then prepare its detailed design, acceptance cases and implementation handoff. These questions are inputs to detailed design, not reasons to design every later milestone first. No runtime implementation is authorized.

## Parallel-work gate proposal

D39 requires independent progress without placeholder context. BC03 in the milestone plan proposes M1–M3 standalone and M4 gated on concrete merged/compatible workflow/context contracts. Whole Stage 02/03 completion is not a blanket prerequisite. Existing context has for_agent; a separate AgentContext remains exploratory. Review this gate allocation alongside M1 detailed design; no runtime implementation starts from the proposal.
