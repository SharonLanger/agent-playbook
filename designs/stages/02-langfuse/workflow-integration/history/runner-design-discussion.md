# M4.2 runner tracing — preliminary discussion

Status: **DISCUSSION ONLY. No detailed M4.2 design, test contract or implementation approval yet.** Started 2026-11-14, discussion iteration 30.

This file supplements the [complete discussion through iteration 29](context-discussion.md), [shared requirements](../requirements.md) and [decisions](../decisions.md). It records new instructions, proposals, open decisions and possible follow-ups while another Codex implements M4.1. It is not a competing application specification. Read this entire record on each new M4.2 discussion iteration and preserve earlier decisions when updating it.

## Baseline and active-work boundary

- M4.1's delegated design/test/implementation package is pinned to `11bba581291c1b166973848ea8db6a9e2a142413` in PR #43. Sharon reports that its implementing Codex is working. No implementation result or completion is inferred.
- Shared records including D30/R31 were last published at `9aaf31e4b0e6345ed7162da765f37dbe94167f4b`. That is this discussion branch's starting point.
- New instruction, iteration 30: do not edit the implementing agent's parts. Save proposed changes separately for an explicit follow-up handoff. This session will not edit his code, tests, three M4.1 milestone documents, approval records or round reports.
- This file is the only change on separate branch `docs/m4-2-runner-discussion`. Do not advance PR #43, its branch, the implementation branch or shared navigation/progress/Atlas while recording these parallel notes. Reconcile discovery/status in the eventual M4.2 documentation PR after alignment. This isolation follows Sharon's explicit instruction and does not change guarded architecture meaning.
- No milestone boundary change is selected: M4.1 context/wiring; M4.2 runner tracing; M4.3 automatic CrewAI observations; logging later. Any proposed boundary change must be recorded and checked against shared requirements/decisions before adoption.

## Accepted instructions for the next package

1. Start with a simple preliminary design discussion; agree on the broad behavior before producing the detailed milestone documents.
2. Later provide separate `02-runner-design.md`, `02-runner-test-cases.md` and `02-runner-implementation-plan.md`. These are planned filenames, not files created or approved now.
3. Use the same implementation procedure: orchestrator, coder, two independent reviewers for design drift and test gaps, permanent reports for each round, at most three total rounds, then stop if unresolved. Retain the final report back to this design session before user acceptance/merge.
4. An eventual M4.1 follow-up does not silently reset its existing three-round cap or instruct a fourth round. Coordinate it with the recorded round state and an explicit handoff. A requirement change needs its own recorded decision before code.

## Existing agreed requirements carried forward

- Native Langfuse SDK and existing configuration/client setup; no observability broker or replacement tracing framework.
- Use the existing ExecutionContext and nested ObservabilityContext. Do not change that model or add SDK objects/trace-ID allocation as a prerequisite here.
- Every workflow-associated observation carries the exact existing correlation_id, plus selected workflow/run metadata. Native propagation begins at the root before children. D30/R31 apply to later automatic CrewAI observations too.
- Future logs use correlation_id without requiring trace_id. Optional SDK trace/span IDs can narrow a search when several traces share one correlation group.
- Existing local Langfuse deployment only; no additional collector or logging service. Logging, agent runtime lifecycle and advanced scores/evaluations remain separately scoped.
- Keep current workflow outputs, validation, error classification and CrewAI scheduling. Telemetry handling must not erase the original workflow exception.

## First proposal: one observation around the workflow lifecycle

This is a recommendation for discussion, not an accepted detailed contract:

1. The existing application path loads configuration, selects the workflow and creates its execution context.
2. Start one native current Langfuse observation for that workflow invocation. Apply correlation_id, workflow_id and workflow_run_id through native attribute propagation immediately, before child work.
3. Within that observation, keep the existing workflow construction, input decoding/preparation, execution, output validation and serialization path.
4. End the observation when that path returns or raises. Preserve the actual workflow outcome. Later delivery/flush housekeeping is not part of the workflow's business execution duration.
5. Keep automatic CrewAI Flow/start/listen/router observations for M4.3; the M4.2 active scope supplies their future parent. No separate manual span for every lifecycle phase is proposed now.

Why this boundary: failures during preparation or output validation are part of the invocation the user is debugging, even if kickoff never runs or finishes successfully. Observing only kickoff would miss them. Configuration/selection/context-creation failures before this boundary cannot yet carry this invocation context; keep their existing diagnostics and decide any additional telemetry explicitly. Do not move M4.1's context creation earlier merely to expand coverage.

## Remaining decisions, in suggested order

| Order | Decision | Starting recommendation / unresolved detail |
|---|---|---|
| 1 | What does the workflow observation cover? | Whole existing lifecycle after context creation, as above; agree before exact code placement |
| 2 | Who owns the SDK client and delivery? | Reuse a client across invocations within one process; each invocation has its own observation. Flush before a short CLI exits; exact initialization, flush/shutdown and Python-call ownership remain to design |
| 3 | What happens when tracing is disabled or unavailable? | Disabled should create no exporter/contact. For telemetry delivery failure, recommend preserving the workflow outcome with a visible bounded diagnostic; distinguish delivery failure from invalid application configuration. Exact policy is not selected |
| 4 | What data is sent? | Required identity fields, stable operation name and safe outcome information. Input/output/exception payload exposure needs an explicit small allowlist/masking policy; never send the whole context/configuration automatically |
| 5 | What evidence proves it works? | Real SDK export assertions, repeat/error/disabled/outage behavior, correlation on every emitted observation, existing workflow regressions and explicit local-server/UI acceptance. Detailed cases follow agreed behavior |

Only the boundary proposal is being presented for agreement first. Do not turn the other recommendations into accepted decisions just because they appear in this table. Scores, sessions, client pools, async/process transport, generic field registries and new abstractions are not implicit additions.

## Potential M4.1 follow-ups

None identified at this point. Required correlation data and forwarding are already part of the pinned M4.1 contract; the Langfuse metadata projection belongs to M4.2.

If a necessary M4.1 change is discovered, create a separate `context-followups.md` beside this file. Each entry must state the affected approved contract/file, concrete problem, smallest proposed change, why M4.2 cannot handle it locally, test impact, whether it changes a decision, and its pending/approved/handed-off status. Do not apply the change to active M4.1 work. No placeholder follow-up file is needed while there are no entries.

## Iteration 30 record and verification limits

Sharon confirms Codex is working, requests no changes to its parts, asks for proposed changes to be saved separately, and wants the same design/test/two-reviewer package for the next milestone after preliminary alignment. The same three-round maximum and final-review handoff remain applicable. This file captures those instructions without touching shared or delegated files.

References already checked in iteration 29: [Langfuse metadata](https://langfuse.com/docs/observability/features/metadata), [Python API](https://python.reference.langfuse.com/langfuse), installed SDK 5.2.0 and the [research record](../research/crewai-langfuse.md). The bounded metadata check does not prove application or server integration. No new SDK/API claim, runtime probe, application test or implementation is added in this iteration.

Before detailed design: reconcile any actual M4.1 implementation findings, settle the decisions above and present required tracing-specific guarded changes. Do not edit the global principles/architecture or SDK import boundaries during this preliminary discussion. No roadmap or stage renumbering is requested.
