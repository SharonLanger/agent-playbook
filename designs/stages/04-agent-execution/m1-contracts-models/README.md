# S04.M1 — contracts and typed models

> Draft design workspace. The Stage 04 boundary is approved. This milestone's detailed design, tests, implementation plan and implementation remain unapproved.

## Purpose and authority

Define the application-owned interface for an agent, execution adapter and native event mapper, with typed requests, results, initial events, basic settings and permission data. [Stage 04 README](../README.md) owns the canonical milestone status. [Milestone plan](../milestone-plan.md#s04m1--behavioral-contracts-and-typed-data) owns this milestone's boundary. [Specification](../specifications.md) and [decisions](../decisions.md) own the shared requirements and approval history.

This package is a focused design proposal based on Stage 04 PR #45 at `b9d912fa5a8e984885d1808147cdb10297575ed5`, alongside main `d17972e4b7f40e9a1e0fbf23afe02c874c2a12b7`. This PR targets the Stage 04 design branch. Its approval and merge into that branch do not merge or close PR #45. Implementation needs a separate PR against main after the detailed contract, test cases and implementation plan are approved and pinned.

## Read in order

1. Read root [AGENTS.md](../../../../AGENTS.md), [design instructions](../../../AGENTS.md), [charter](../../../charter.md), [principles](../../../principles.md), [architecture](../../../architecture.md), [project structure](../../../project-structure.md), [roadmap](../../../roadmap.md), [progress](../../../progress.md), the [design contract](../../../governance/design-contract.md), [guard register](../../../governance/guarded-files.md), [stage workflow](../../../governance/stage-milestone-workflow.md) and [Codex handover rules](../../../governance/codex-handover-rules.md).
2. Read the entire [Stage 04 specification](../specifications.md), [decision board](../decisions.md), [milestone plan](../milestone-plan.md), [research](../research/README.md) and the relevant [history](../history/README.md). The active records distinguish approved decisions from exploration.
3. Use [design-agent-handover.md](design-agent-handover.md) as the entry brief for this milestone. Work through [design.md](design.md), [test-cases.md](test-cases.md) and [implementation-plan.md](implementation-plan.md) together.

## Draft status

| Item | State |
|---|---|
| M1 boundary | Approved as recorded in Stage 04 D40/BC03 |
| This detailed design, tests and plan | Draft for discussion, no approved SHA |
| Implementation PR, verification, Sharon's acceptance | None, pending |

**Current decision:** D54 approves construction-time schema validation and propagation of creation errors. D55 approves TypeError/ValueError with model/field/rule diagnostics. D56 approves immutable event snapshots including nested data while preserving future schema evolution/hook responses. Concrete representation/conversion, field constraints, remaining diagnostic details and the other listed choices remain open; this is not approval of the complete detailed package.

**Continuation checkpoint (2026-11-26):** the [current reconciliation](../decisions.md#current-m1-decision-reconciliation--2026-11-26) collects the earlier approvals, alternatives and the exact residual work from the seven-item list. D57 records Sharon's consolidation request. Continue here with Sharon or from the handover; avoid asking him to decide settled behavior again.

**Next action:** propose the smallest concrete ExecutionRequest, then work through the remaining choices one at a time. Reconcile affected guarded architecture and structure explicitly and complete design/test/plan for one candidate-revision approval. M1 is ready for continued detailed design; no implementation handoff is active.
