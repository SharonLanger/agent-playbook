# Workflow context and native Langfuse integration — start here

## Stage 02 closeout — 2026-11-15

Stage 02 is completed, accepted by Sharon and merged through Stage Design PR #47. Local Langfuse setup/mock work (PR #36), execution context (PR #44), and native runner plus automatic CrewAI tracing (PR #50) are delivered. PR #50 merged at `b08060f0acba74f19bc8a32aedb21316eed149c1`; its reviewed candidate passed 408 tests, static/lint/format checks and installed-release verification. Sharon completed local success, branch, correlation, input/output, readable-name and controlled-failure acceptance. Stage 03 can proceed under its own design approvals.

Application logging is separate work owned by a different agent under `designs/refactors/logging/`, with its own design and implementation PRs. It is outside completed Stage 02 and does not block Stage 03. Earlier logging requirements and research remain historical inputs; this closeout selects no logger, store, viewer or logging architecture and does not create or edit the logging agent’s files.

## Historical checkpoints


Updated: 2026-11-15, final implementation acceptance.
Status: **M4.2 + M4.3 are implemented, verified, accepted by Sharon and merged via PR #50 at b08060f0acba74f19bc8a32aedb21316eed149c1. The 408-test gate and installed release passed; RUN-18 local acceptance is complete, including the controlled failed step. M1–M3 and M4.1 remain accepted/merged. Stage Design PR #47 remains draft/open pending explicit stage closeout authorization. Logging and later agent telemetry enhancements remain deferred.**

This is the permanent Stage 02 M4 workspace. PR #43 merged as `c8f129ee8c978067bf576b0ab563bfab74c9d6fe`. PR #44 carries the accepted M4.1 implementation. M1–M3 remain accepted; implementation is complete through M4.3, with stage closeout still separate.

**MERGE LAST:** [PR #47](https://github.com/SharonLanger/agent-playbook/pull/47) is the ongoing documentation workspace. Keep it draft/open until all covered implementation work is merged, records reconciled and Sharon explicitly authorizes this documentation PR.

Before every implementation handoff, read [Codex handover rules](../../../governance/codex-handover-rules.md). They define the outgoing copyable prompt, coder/two-reviewer procedure, three-round cap and copyable return report.

## Read in this order

1. Follow [design instructions](../../../AGENTS.md), [design contract](../../../governance/design-contract.md), [guards](../../../governance/guarded-files.md), [progress](../../../progress.md) and [stage summary](../README.md).
2. Read [requirements](requirements.md) and [decisions](decisions.md); they are the shared reference, not a new broker design.
3. Read [discussion history](history/context-discussion.md), the [final context review](history/context-final-review.md) and [review status](m1-context/reviews/status.md). The combined runner and CrewAI tracing review drafts are grouped under [M2–M3](m2-3-workflow-tracing/README.md).
4. Read the approved [M4.1 design](m1-context/design.md), [test cases](m1-context/test-cases.md) and [implementation/review plan](m1-context/implementation-plan.md).
5. Before tracing work, read [CrewAI research](research/crewai-langfuse.md), its [probe evidence](research/probe/README.md) and [repository reconciliation](repository-updates.md). Research is not application or live-server acceptance.

## Milestones and their documents

| Milestone | Goal | Status |
|---|---|---|
| M4.R | Verify released CrewAI/Langfuse feasibility | Delivered research: eight cases/44 spans, with documented limits |
| M4.1 (M1) | Typed context, real runner/factory/Workflow/Flow propagation and isolated derivation | Approved at 11bba581; implementation candidate 16c1580; two review rounds; accepted, merged via PR #44; see [M1 package](m1-context/README.md) |
| M4.2 + M4.3 (M2–M3) | Native runner tracing, correlation and automatic existing CrewAI Flow/step observations | Accepted and merged via PR #50; [design](m2-3-workflow-tracing/design.md), [tests](m2-3-workflow-tracing/test-cases.md), [plan](m2-3-workflow-tracing/implementation-plan.md) and [round-02 amendment](m2-3-workflow-tracing/round-02-revision.md) form the approved contract; [final status](m2-3-workflow-tracing/reviews/status.md) records acceptance |
| Historical M4.3 | Previously separate CrewAI integration milestone | Incorporated into the combined milestone; research and earlier decisions retained |
| Later | Local logging, usage, scores/evaluations as needed | Deferred; no agent runtime or logger selected here |

## Rules that prevent design drift

The reference is requirements.md + decisions.md + the approved milestone design/test/plan, checked against the guarded repository authorities.

1. Read the complete relevant discussion record each iteration; record meaningful instructions, decisions, unresolved questions and contradictions before changing agreed meaning.
2. Distinguish proposed, approved, implemented, verified, accepted and merged. A draft or research result does not authorize implementation.
3. Each milestone has its own design, test cases and focused implementation PR. Preserve earlier pinned contracts and review evidence.
4. Use one coder and two independent reviewers (design drift and test gaps), one frozen candidate and permanent reports per round, at most three total rounds. Final review does not reset the cap.
5. Guarded logical changes require the applicable authorization; do not weaken separate agent-provider boundaries or access personal examples.
6. Update affected product guides, shared records and Atlas with verified evidence; regenerate Atlas rather than hand-merging HTML.

## Correlation and next design

ExecutionContext already contains correlation_id; nested ObservabilityContext holds workflow/run and optional agent identity. Factory, workflow and Flow share the original context; for_agent derives isolated child values. No SDK object or allocated trace/span identity is stored in it.

D30/R31 require exact correlation_id on every workflow-associated Langfuse observation and later local log. The combined milestone supplies native metadata propagation and validates automatic CrewAI descendants together. Metadata alone does not establish trace parentage. Future scores/entity APIs and process boundaries require their own integration checks.

Next: review the stage closeout record and deferred scope, then obtain explicit authorization before merging Stage Design PR #47. No further M4.2/M4.3 coding round is required.

## Historical approval checkpoint

### Approval and implementation checkpoint — 2026-11-14

Sharon's instruction to implement M4.1 as orchestrator approved the design,
CTX-01–17 test cases, plan and G01–G08 at
`11bba581291c1b166973848ea8db6a9e2a142413`. The approved three-file contract
is locked. [Review status](m1-context/reviews/status.md) tracks the focused,
unmerged M4.1 implementation branch; earlier draft status prose above is the
planning snapshot at the approved revision. Later tracing and agent work stay out
of this milestone.
