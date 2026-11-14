# Workflow context and native Langfuse integration — start here

Updated: 2026-11-14, discussion iteration 29.
Status: **M4.1 implementation handoff sent to Codex at 11bba58, per Sharon; implementation/final review pending. M4.2 preliminary design begins. This PR remains documentation-only and unmerged.**

This is the permanent working home for Stage 02 workflow-integration planning, under the existing M4. PR #36's local setup/mock M1–M3 remain accepted and merged. The repository baseline inspected for this opening commit is `d12b5fc2867d3646b6fab2eb71f1447ff177d8c1`; research retains its original `44d6919` baseline. Earlier saved session files are dated snapshots, not a second active specification. Use this PR branch until it merges; do not assume these files are already on main.

## Read in this order

1. Follow the repository's [design entry instructions](../../../AGENTS.md), [design contract](../../../governance/design-contract.md) and [guarded-file register](../../../governance/guarded-files.md). Check [project progress](../../../progress.md) and the [Stage 02 summary](../README.md).
2. Read [requirements.md](requirements.md): this **is the current specification**, including scope, milestone goals and deferred requirements.
3. Read [decisions.md](decisions.md): agreed choices, superseded choices and unresolved questions. Do not convert examples or research recommendations into approvals.
4. Read the complete [discussion record](history/context-discussion.md) at the beginning of each discussion iteration or handoff. Update it after meaningful instructions/decisions; checkpoint during active work when new information accumulates. There is no unattended timer.
5. Before tracing work, read the [CrewAI research](research/crewai-langfuse.md) and [reproducible probe](research/probe/README.md). Eight isolated cases/44 spans passed; actual application integration and local-server/UI acceptance remain pending.
6. Review the [M4.1 design](01-context-design.md), [test cases](01-context-test-cases.md) and [Codex implementation/review plan](01-context-implementation-plan.md). Their headers preserve the drafted snapshot; Sharon reports forwarding the explicit implementation authorization at revision 11bba58. The implementing Codex records that approval and applies the enumerated amendments on its own branch. No acceptance/merge is implied.
7. Review [repository-updates.md](repository-updates.md) before proposing guarded edits, implementation, review readiness or merge. It names the outstanding documentation changes and their triggers.

## Milestones and their documents

| Milestone | Starting point | Goal | Document and present status |
|---|---|---|---|
| M4.R — research | Merged setup and existing deterministic flows | Establish released-version compatibility and automatic coverage before integration | [Research](research/crewai-langfuse.md), delivered with explicit limits; no dependency adoption yet |
| M4.1 — context | Existing runner/factory/Workflow ABC; no execution context | Define, pass and derive typed context; prove invocation/parent/sibling isolation without backend export | [Design](01-context-design.md), [test cases](01-context-test-cases.md), [implementation/review plan](01-context-implementation-plan.md): handoff at 11bba58 sent to implementing Codex; results/final review pending |
| M4.2 — runner | Approved, implemented and tested context | Use native Langfuse root scope, correct IDs and configured lifecycle/disabled behavior | Preliminary design active; future `02-runner-design.md` and separate implementation PR |
| M4.3 — CrewAI | Runner scope plus tested research candidate | Automatically observe executed start/listen/router paths in local Langfuse | Future `03-crewai-design.md`; separate PR |
| Later — logs and advanced features | Stable context and real tracing | Add local logging separately; later usage/scores/evaluations as real operations require | Deferred; no logger, viewer or agent-runtime design adopted here |

Each implementation milestone gets its own detailed design MD and focused PR. PR #43 now holds shared records, research and the draft detailed M4.1 package authorized by D28. Sharon reports sending the explicit M4.1 authorization/handoff. Preserve its pinned contract while that Codex implements and reviews it. M4.2 planning can run in parallel; tracing implementation waits for its own design and the verified context foundation.

## Rules that prevent design drift

The reference is concrete: **requirements.md + decisions.md**, checked against the repository's guarded authorities and the approved milestone design once one exists. History explains decisions; it is not a competing current contract. Research establishes bounded evidence, not approval.

1. Before every iteration, read the complete discussion record and current requirements/decisions. Identify the affected IDs and relevant open questions.
2. State conflicts before changing agreed meaning. Preserve the previous decision and record its replacement/reason. Never silently restore the rejected tracing broker, add speculative context sections, or choose the separate agent-runtime lifecycle.
3. Every detailed design must state its baseline, scope, exact contracts/placement, covered requirement IDs, unresolved items, implementation steps and meaningful acceptance checks. Link shared definitions rather than redefining them.
4. When a change affects context fields, constructors, propagation or another milestone, explain the impact first and update every affected current document in the same PR. Adding a field should not require unrelated forwarding methods to change.
5. Keep accepted discussion choices, approved/locked design, implementation, tested evidence, user acceptance and merge status separate. Resolve or explicitly defer relevant questions before coding that part.
6. Run checks appropriate to the actual changes. Record exact versions/revisions and distinguish isolated export from live ingestion. Unverified CrewAI decorators/features remain unverified; tested start/listen/router coverage does not imply universal coverage.
7. Complete the affected items in repository-updates.md before the relevant readiness gate. Guarded logical changes require file-specific review under the repository contract. Do not add this draft to the guarded register as if approved.
8. Keep application examples excluded. Preserve the separate agent-execution adapter boundary and deferred local-logging requirements. Context is not automatically safe to serialize into telemetry.

## M4.1 handoff and M4.2 preliminary design

D27 accepts application correlation_id. The draft places it directly on ExecutionContext, with one nested ObservabilityContext for workflow/run and optional agent fields. Constructor generation happens only for a new independent group; child derivation preserves the value. SDK trace/span identity stays outside this initial model under D25/D26. Correlation metadata does not automatically connect traces.

The [design](01-context-design.md) specifies app/src/agent_playbook/context/models.py, frozen keyword-only dataclasses, required constructor forwarding, runner creation timing, a small for_agent replacement helper and private CrewAI Flow storage. These choices are pinned by the implementation handoff at 11bba58; this session does not change those three milestone documents while implementation proceeds. The application's context is separate from CrewAI's existing execution_context field and from business state.

M4.1 includes real runner → factory → Workflow → Flow wiring and isolation tests. M4.2 adds native runner tracing; M4.3 adds automatic CrewAI observations. Agent runtime lifetime, logging, SDK lifecycle and cross-process transport are not prerequisites to this data-only milestone.

The separate [test cases](01-context-test-cases.md) define CTX-01–17. D29's [implementation plan](01-context-implementation-plan.md) requires a coder plus independent design-drift and test-gap reviewers, the same candidate revision for both reviews, permanent per-round reports and a maximum of three total rounds. Stop with unresolved findings after round three.

Next here: define the M4.2 runner tracing boundary and client lifetime while awaiting Codex's M4.1 return report. Later tracing-specific guarded reconciliation remains separate; no implementation or final acceptance is claimed from the handoff alone.

D30/R31 require the same correlation_id on every workflow-associated Langfuse observation and later local record. Use native propagate_attributes immediately at the root, before children/events. Local logs need no trace ID for this shared grouping; optional SDK IDs allow finer filtering when a correlation ID spans several traces. SDK-native events inherit scope; scores/other future APIs and process transport must be checked separately. The [requirements](requirements.md) contain the preliminary scope and acceptance outline; no detailed M4.2 contract is approved yet.

## Handoff and closeout

Start another agent at this README on the PR branch. After approval, give it 01-context-implementation-plan.md and the exact approved revision/approval reference; this README alone is not an implementation brief. Record review/acceptance in decisions and history, update affected repository records from the checklist, regenerate Atlas, and verify before reporting readiness. No merge is authorized by the creation of this draft.

Sharon will copy the implementing Codex's final report back to this design session for a final review. Use the implementation plan's section 8 return-report format, with permanent links to the actual candidate and every round's reports. That final review neither resets the three-round cap nor authorizes a merge.

Principle assessment: approval/no drift (1,3,12) is handled by this explicit draft and pending reconciliation; security/configuration/locality (2,6,10) is retained without runtime changes; learning/incremental scope (4,9) uses milestones; evidence/quality (7,8,15) separates preserved research from new documentation checks; history/sandbox (11,13) is preserved; official docs (14) have no supported-behavior change. Principle 5's tracing-specific conflict is recorded for review, while agent provider isolation remains intact.
