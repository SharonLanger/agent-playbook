# Workflow context and native Langfuse integration — start here

Updated: 2026-11-14, iteration 35.
Status: **M4.1 implemented, independently reviewed and accepted by Sharon; merged via PR #44 at 942e59344c429454263319e783ea76ad297b7ea6. M4.2 remains design-only; M4.3 and logging are deferred.**

This is the permanent Stage 02 M4 workspace. PR #43 merged as `c8f129ee8c978067bf576b0ab563bfab74c9d6fe`. PR #44 carries the accepted M4.1 implementation. M1–M3 remain accepted; all Stage 02 is not complete.

## Read in this order

1. Follow [design instructions](../../../AGENTS.md), [design contract](../../../governance/design-contract.md), [guards](../../../governance/guarded-files.md), [progress](../../../progress.md) and [stage summary](../README.md).
2. Read [requirements](requirements.md) and [decisions](decisions.md); they are the shared reference, not a new broker design.
3. Read [discussion history](history/context-discussion.md), the [final context review](history/context-final-review.md) and [review status](reviews/context/status.md). Later runner discussions/drafts are maintained on `docs/m4-2-runner-discussion` until integrated separately.
4. Read the approved [M4.1 design](01-context-design.md), [test cases](01-context-test-cases.md) and [implementation/review plan](01-context-implementation-plan.md).
5. Before tracing work, read [CrewAI research](research/crewai-langfuse.md), its [probe evidence](research/probe/README.md) and [repository reconciliation](repository-updates.md). Research is not application or live-server acceptance.

## Milestones and their documents

| Milestone | Goal | Status |
|---|---|---|
| M4.R | Verify released CrewAI/Langfuse feasibility | Delivered research: eight cases/44 spans, with documented limits |
| M4.1 | Typed context, real runner/factory/Workflow/Flow propagation and isolated derivation | Approved at 11bba581; implementation candidate 16c1580; two review rounds; accepted, merged via PR #44 |
| M4.2 | Native workflow observation and exact correlation metadata | Draft design/test/plan on the separate runner discussion branch; policies await agreement |
| M4.3 | Automatic CrewAI Flow/start/listen/router observations | Follows runner integration; separate design/acceptance |
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

D30/R31 require exact correlation_id on every workflow-associated Langfuse observation and later local log. M4.2 supplies native root/child metadata propagation; M4.3 validates automatic CrewAI descendants. Metadata alone does not establish trace parentage. Future scores/entity APIs and process boundaries require their own integration checks.

Next: agree M4.2 lifecycle, client/delivery, failure and safe-data policies before approving its detailed package. No broker, logger or agent-lifecycle expansion is implied.

## Historical approval checkpoint

### Approval and implementation checkpoint — 2026-11-14

Sharon's instruction to implement M4.1 as orchestrator approved the design,
CTX-01–17 test cases, plan and G01–G08 at
`11bba581291c1b166973848ea8db6a9e2a142413`. The approved three-file contract
is locked. [Review status](reviews/context/status.md) tracks the focused,
unmerged M4.1 implementation branch; earlier draft status prose above is the
planning snapshot at the approved revision. Later tracing and agent work stay out
of this milestone.
