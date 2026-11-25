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

**Next action:** design agent resolves the open M1 choices with Sharon one at a time, reconciles affected guarded architecture and structure explicitly, then prepares the three detailed files for a single revision approval. No implementation handoff is active.
