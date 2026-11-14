# Workflow context and native Langfuse integration — start here

Updated: 2026-11-14, discussion iteration 23.
Status: **draft documentation workspace; preliminary structure agreed; detailed context design not yet written or approved; no application implementation in this PR.**

This is the permanent working home for Stage 02 workflow-integration planning, under the existing M4. PR #36's local setup/mock M1–M3 remain accepted and merged. The repository baseline inspected for this opening commit is `d12b5fc2867d3646b6fab2eb71f1447ff177d8c1`; research retains its original `44d6919` baseline. Earlier saved session files are dated snapshots, not a second active specification. Use this PR branch until it merges; do not assume these files are already on main.

## Read in this order

1. Follow the repository's [design entry instructions](../../../AGENTS.md), [design contract](../../../governance/design-contract.md) and [guarded-file register](../../../governance/guarded-files.md). Check [project progress](../../../progress.md) and the [Stage 02 summary](../README.md).
2. Read [requirements.md](requirements.md): this **is the current specification**, including scope, milestone goals and deferred requirements.
3. Read [decisions.md](decisions.md): agreed choices, superseded choices and unresolved questions. Do not convert examples or research recommendations into approvals.
4. Read the complete [discussion record](history/context-discussion.md) at the beginning of each discussion iteration or handoff. Update it after meaningful instructions/decisions; checkpoint during active work when new information accumulates. There is no unattended timer.
5. Before tracing work, read the [CrewAI research](research/crewai-langfuse.md) and [reproducible probe](research/probe/README.md). Eight isolated cases/44 spans passed; actual application integration and local-server/UI acceptance remain pending.
6. Review [repository-updates.md](repository-updates.md) before proposing guarded edits, implementation, review readiness or merge. It names the outstanding documentation changes and their triggers.

## Milestones and their documents

| Milestone | Starting point | Goal | Document and present status |
|---|---|---|---|
| M4.R — research | Merged setup and existing deterministic flows | Establish released-version compatibility and automatic coverage before integration | [Research](research/crewai-langfuse.md), delivered with explicit limits; no dependency adoption yet |
| M4.1 — context | Existing runner/factory/Workflow ABC; no execution context | Define, pass and derive typed context; prove invocation/parent/sibling isolation without backend export | `01-context-design.md` will be created **after preliminary alignment**; it does not exist yet |
| M4.2 — runner | Approved, implemented and tested context | Use native Langfuse root scope, correct IDs and configured lifecycle/disabled behavior | Future `02-runner-design.md`; separate PR |
| M4.3 — CrewAI | Runner scope plus tested research candidate | Automatically observe executed start/listen/router paths in local Langfuse | Future `03-crewai-design.md`; separate PR |
| Later — logs and advanced features | Stable context and real tracing | Add local logging separately; later usage/scores/evaluations as real operations require | Deferred; no logger, viewer or agent-runtime design adopted here |

Each implementation milestone gets its own detailed design MD and focused PR. This opening draft holds shared records and research; it deliberately does not include the detailed M4.1 document. Another Codex agent can implement M4.1 after its design is agreed, explicitly approved and locked. Do not start M4.2 merely because a draft context design exists.

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

## Current next discussion

Agreed: two ordinary typed dataclasses, `ExecutionContext` containing `ObservabilityContext`, together in one shared definition file outside provider adapters; no Context ABC and no observability broker. Runner creates per invocation, factory forwards through the workflow constructor, workflow holds `self.context` and supplies its Flow. An agent invocation receives a derived context; nested helpers can reuse it; the original parent remains unchanged.

Still to align before writing the detailed design: exact file path; minimal fields/types/defaults; dataclass options; constructor/Flow propagation details and creation timing; shallow replacement/nested-mutability policy; trace-reference behavior before tracing and when disabled; focused tests. SDK span activation is separate from copying context data. Agent runtime lifetime stays outside this decision.

Iteration 22 now presents a concrete preliminary proposal, P02 in decisions.md: `app/src/agent_playbook/context/models.py`, two frozen keyword-only dataclasses, explicit workflow/run identity plus optional trace/agent fields, and constructor propagation through the existing code. This is review material, not a new accepted decision. PR #43 contains the planning records; `01-context-design.md` still does not exist. Sharon requested a simple explanation before the detailed document.

Iteration 23 revises P02's trace-binding recommendation through P03: the runner can allocate a valid trace ID locally before creating the context and later supply the same ID to Langfuse. Existing traces should be inherited when intentionally continued. None was a proposed milestone choice, not an SDK requirement. D24 records that invocation IDs remain fixed once assigned; final field optionality/disabled-mode policy still needs alignment.

## Handoff and closeout

Start another agent at this README on the PR branch. Give it the approved milestone document and exact reviewed revision when available; this README alone is not an implementation brief. Record review/acceptance in decisions and history, update affected repository records from the checklist, regenerate Atlas, and verify before reporting readiness. No merge is authorized by the creation of this draft.

Principle assessment: approval/no drift (1,3,12) is handled by this explicit draft and pending reconciliation; security/configuration/locality (2,6,10) is retained without runtime changes; learning/incremental scope (4,9) uses milestones; evidence/quality (7,8,15) separates preserved research from new documentation checks; history/sandbox (11,13) is preserved; official docs (14) have no supported-behavior change. Principle 5's tracing-specific conflict is recorded for review, while agent provider isolation remains intact.
