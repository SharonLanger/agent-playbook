# Stage 03 — Orchestration patterns

Status: **Scope discussion / draft. No milestone contract or implementation is approved.**

This README combines the initial specification, reading entry and stage index so the initial workspace contains exactly two files, as Sharon requested on 2026-11-15. [decisions.md](decisions.md) records agreements, their sources, rationale, placement and unresolved choices. Split into additional documents only when useful; preserve IDs and history.

## Goal and established boundaries

Understand and verify a small selected set of branching, parallel-work, joining and failure-propagation scenarios. CrewAI remains scheduler and workflow-state owner. Reuse the accepted workflow lifecycle, context and native tracing foundation.

| ID | Established requirement or constraint | Source |
|---|---|---|
| S03-R01 | Keep the scope bounded; choose exact scenarios through this design discussion. | Roadmap Stage 03; current request |
| S03-R02 | Reuse Stage 01's sequence, typed state and exclusive-route learning rather than repeat it. | Roadmap; Stage 01 summary |
| S03-R03 | Verify outputs, branch/join behavior, controlled failure and isolation across branches/runs; correlated traces support inspection. | Roadmap Stage 03 |
| S03-R04 | Keep scheduling/state with CrewAI; keep context and business steps provider-free. | Architecture and project structure |
| S03-R05 | Logging is separate work owned by another session and is not a prerequisite. | Sharon's Stage 02 completion instruction; current progress |
| S03-R06 | No native-agent dependency, unlimited pattern catalogue or durable recovery framework. | Roadmap Stage 03 boundary |
| S03-R07 | Use one draft Stage Design PR, incremental milestone approval and separate implementation PRs. | Stage working method; agreed approach |
| S03-R08 | Preserve an inspectable decision history explaining what, why, where and approval status. | Sharon's two-file request |

These are inherited boundaries and session agreements, not approval of the proposed scenarios below.

## Starting point and relationship to other work

Baseline inspected: main `4ed7a318e25653d481705d9cb40c35de9ab649c7`, 2026-11-15.

- Stages 00–01 are accepted foundations. Stage 01 supplies basic sequence, shared typed state and exclusive branching.
- [Current progress](../../progress.md) records Stage 02 completed, accepted and merged through PR #47. Context and native workflow tracing are available. This supersedes the earlier pending-status observation in this conversation.
- Application logging belongs to the separate `designs/refactors/logging/` workstream. This package does not choose its logger, storage or viewer.
- Stage 04 owns the shared agent execution foundation; its narrow early-start exception does not transfer its scope here. Stage 05 owns real provider integration.
- This task reviews design records; it does not independently rerun predecessor runtime acceptance.

## Candidate use-case groups — proposals only

One possible teaching example is a document-check workflow using deterministic Python checks. No actual agents, external document service or repository scanner are implied. The example domain and group selection await Sharon's choice.

| Group | Concrete use cases | Shared capability and learning outcome | Selection |
|---|---|---|---|
| G1 — Parallel checks and one combined result | Run structure and reference checks on the same document; combine both results; reverse completion order; run two documents concurrently. | Fan-out, join after all required work, stable result ownership, overlapping execution and branch/run isolation. | Proposed core |
| G2 — Conditional work and convergence | A basic request takes a short path; a thorough request runs the parallel checks; both produce the same report shape. | Compose routing with the G1 join; execute only the chosen path and avoid waiting for a branch that was never selected. | Proposed core |
| G3 — Failure propagation through parallel work | One required check raises while its sibling is active; a required check fails after its sibling succeeds; the combine step raises. | Explicit failure ownership, truthful overall failure, declared sibling behavior, no misleading success and no indefinite join. | Proposed core |

G1–G3 are discussion IDs, not approved milestone IDs. They may become milestones or be combined after scope agreement.

### G1 details

Proposed evidence: both required results appear once in the combined report; completion order does not misassociate values; the join does not run prematurely; independent runs do not share business state or trace identity accidentally. Verify overlapping execution using controlled synchronization, not a speed threshold or a screenshot alone. These are proposed acceptance goals, not a claim about the pinned CrewAI version.

### G2 details

Stage 01 already demonstrated choosing exactly one branch. The new value would be composition: a route can contain parallel work and still converge correctly. Specify which prerequisites belong to each route, what the common output is, and how many times convergence occurs. Prefer fixed small paths initially; selecting arbitrary subsets is not included automatically.

### G3 details

A business check returning a negative finding is different from a step raising an execution error. Decide how each is represented. Also decide what happens to already-running siblings, whether successful sibling output is retained, when the caller receives failure and what the trace records. Propagating a failure does not automatically guarantee immediate cancellation. No retry, fallback or partial-success policy is approved.

### Optional additions — not recommended for the initial selection

- Bounded retry: one controlled transient failure followed by success, plus exhaustion. Adds retry scope, side-effect and attempt-tracing questions.
- Variable-size fan-out: process a small input list with a concurrency bound, then aggregate. Adds task identity, admission limits and empty-input behavior.

Keep these as options, not commitments. Human approval waits, nested workflow frameworks, distributed workers, durable resume/replay and real-agent products are outside the proposed initial selection.

## Evidence across every selected group

Use the maintained application execution path and deterministic fixtures. Inspect meaningful outputs and behavior as well as native correlated traces. Check isolation in the relevant concurrent scenarios. Trace correlation does not by itself prove parentage or correct scheduling. Separate automated evidence, local UI acceptance and merge state.

Before detailed design, inspect the actual pinned CrewAI/runtime contracts and focused prior evidence. Research native behavior only for selected questions; do not assume a framework primitive provides our desired semantics. Prefer native supported capabilities and surface any gap before designing custom scheduling.

## Canonical milestone index

No milestones have been agreed. Candidate groups are not implementation authorization.

| Milestone ID and outcome | Design and approved SHA | Implementation PRs | Review evidence | Acceptance | Merge state |
|---|---|---|---|---|---|
| Not allocated — scope selection first | No locked revision | Not opened | None | Pending scope discussion | No Stage 03 implementation |

## Working process

1. Agree selected scenarios, exclusions and milestone boundaries.
2. Record an alignment checkpoint and settle prerequisite/API questions.
3. Draft each selected milestone's design, test cases and implementation plan together in its own folder.
4. Obtain explicit approval of the exact revision before implementation; freeze its contract during implementation.
5. Use the prescribed implementation handoff and independent reviews. This design session reviews the actual returned diff/evidence.
6. Record implementation, verification, Sharon's acceptance and merge separately.

Keep the Stage Design PR draft/open throughout the stage, with no auto-merge. Merge it only after stage closeout and Sharon's explicit instruction identifying that PR.

## Governing references

- [Roadmap](../../roadmap.md), [charter](../../charter.md), [principles](../../principles.md)
- [Architecture](../../architecture.md), [placement](../../project-structure.md), [progress](../../progress.md)
- [Design contract](../../governance/design-contract.md), [guarded register](../../governance/guarded-files.md)
- [Stage working method](../../governance/stage-milestone-workflow.md), [implementation handoffs](../../governance/codex-handover-rules.md)
- [Stage 01](../01-crewai-flows/README.md), [Stage 02](../02-langfuse/README.md)
- [Exploration index](../../explorations/README.md)

Next action: discuss G1–G3 with Sharon; select the useful scope before allocating milestones.
