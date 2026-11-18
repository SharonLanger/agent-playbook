# Stage and milestone working method

**Status: GUARDED — standing method requested by Sharon on 2026-11-15.** Applies to all future stages and milestone design/implementation handoffs. Complements the [design contract](design-contract.md) and [Codex handover rules](codex-handover-rules.md); it does not approve individual designs.

## 1. Shared workspace and ownership

A stage is a coherent product/development goal; a milestone is a bounded outcome within it that can be designed, tested, reviewed and accepted independently. Define milestones by observable outcomes, not by arbitrary file counts or phases of writing code. Each has a stable ID, concise name, starting prerequisites, included/excluded behavior, dependencies and completion evidence. Combine or split only through an explicit recorded decision; preserve old IDs/history and explain their mapping.

Place a new stage under `designs/stages/<two-digit-number>-<slug>/`. Keep requirements, decisions and material shared across milestones at their stage or named working-package root. The stage README links to any nested package and its canonical records.

| Stage file or folder | Responsibility |
|---|---|
| `README.md` | Stage goal and boundary, reading order, the one canonical stage milestone/status table, links to evidence and the next action |
| `requirements.md` | Stable requirement IDs, scope, constraints, acceptance intent and deferred requirements |
| `decisions.md` | Accepted, proposed and superseded decisions, rationale and open questions with owners |
| `learning/` | Stage tutorials and exercises when there is material to retain |
| `research/` | Shared research, dated evidence, sources and limitations when there is material to retain |

Keep stage-level milestone tracking in the README. Link to [repository-wide progress](../progress.md) for the project roll-up. Avoid creating a competing stage `milestones.md` or `progress.md`. Link to the owning requirement, decision or evidence instead of copying it across levels. Additional records, such as discussion history or repository reconciliation, belong with their owner when needed.

Existing stages and named working packages may retain their established paths, filenames, IDs and historical records. Link to those records from the stage README. Changing their layout or guards requires the applicable explicit approval.

## Stage Design PR lifecycle

Maintain one ongoing draft **Stage Design PR** per stage, titled `[Stage XX Design] <stage name>` (for example `[Stage 04 Design] Agent execution foundation`). Open one focused implementation PR for each milestone that enters implementation, titled `[Stage XX · MYY] <milestone outcome>`. Preserve documented nested and combined milestone ID mappings.

The Stage Design PR normally changes only its stage's requirements, decisions, milestones, designs, test cases, research and review records. Necessary shared roadmap/progress/governance/Atlas amendments must be explicitly identified and follow guarded-change approval. Runtime source, application configuration, dependencies and executable application tests belong in separate implementation PRs. General governance PRs such as #48 are not themselves Stage Design PRs.

Keep the Stage Design PR draft and open throughout the stage. Approved milestone documents can be consumed through immutable commit links before this PR merges. Its existence, design approval, passing checks, milestone acceptance or implementation-PR merge never authorizes merging the Stage Design PR. Do not enable auto-merge.

Put this notice first in its description:

> **STAGE DESIGN WORKSPACE — KEEP OPEN**
>
> This PR maintains this stage's documentation throughout its milestones. Design approval and implementation-PR merge instructions do not authorize merging this PR. Keep it draft until stage closeout. Merge only after Sharon explicitly authorizes this Stage Design PR.

The stage README owns the canonical milestone table. Keep a compact milestone/PR index and a link to that table in the PR description. Track:

| Milestone ID and outcome | Design and approved SHA | Implementation and PR | Verification and review evidence | Acceptance | Merge state |
|---|---|---|---|---|---|
| Each milestone | Link and draft status or exact approved revision | Actual implementation state and PR link when opened | Observed result and permanent report links | Pending / accepted / explicitly deferred | Actual state |

Agree on the stage boundary and the full set of bounded milestone outcomes and dependencies upfront. Draft each milestone's design, test cases and implementation plan together as that milestone comes up. Before starting its implementation, explicitly approve and pin the exact revision of those three documents. Later milestone details may stay draft. Approval of one milestone never approves another.

At closeout, all milestones must be accepted with their implementation PRs merged, or explicitly removed/deferred by Sharon with the reason and changed scope retained. Reconcile final evidence, progress, links and Atlas, then report readiness. Merge only after an explicit instruction identifying this Stage Design PR. Never infer that instruction from work on a related PR. An instruction to abandon/close without merging is a separate user decision. Existing PR titles and stage layouts are updated by their owners; this convention does not authorize mass renaming or migration.

## 2. Every milestone gets a folder

Under a new stage, place each milestone directly in `m<number>-<outcome-slug>/`. Use at most three descriptive words in the slug, as in `m1-context/`. Existing named working packages keep their milestones at the established package root. Combined folders such as `m2-3-workflow-tracing/` retain their paths and IDs. Document the mapping to global IDs such as M4.1.

| Milestone file or folder | Responsibility |
|---|---|
| `README.md` | Scope, prerequisites, status, reading order, approval revision and next action |
| `design.md` | Responsibilities, placement, contracts, failure boundaries, dependencies, exclusions, requirement/decision mapping and any guarded amendments |
| `test-cases.md` | Stable test IDs, scenarios, observable assertions, test level, environment/manual needs and links to requirements |
| `implementation-plan.md` | Work order, concrete files and checks, approved baseline, orchestration and handoff |
| `reviews/status.md` | Approved revision, reviewed candidates, rounds used, findings and test evidence |
| `reviews/round-01/` through `reviews/round-03/` | `implementation.md`, `design-drift.md`, `test-gap.md` and `orchestrator.md` for each round actually run |

Create the review directory and its records when implementation review begins. Create only the rounds actually run and retain findings and failures under the [Codex handover rules](codex-handover-rules.md#roles-and-rounds). Keep milestone-specific evidence inside its milestone and shared research and history with their owner. Any separately authorized move must update links and guard registrations and retain immutable historical references and approved semantics.

## 3. Before detailed design: alignment checkpoint

Read the full relevant discussion record and current canonical requirements/decisions, applicable guarded authorities, relevant research and actual implementation/base. Reuse unchanged material already read; do not rely on a handoff's assertion of approval.

Record a short dated alignment checkpoint in decisions/history (no extra mandatory file):
1. Goal and prerequisite state: what exists versus what is proposed.
2. Requirement/decision consistency: omissions, contradictions, obsolete assumptions and scope boundaries.
3. Research support: what was demonstrated, on which versions, and what remains unverified.
4. Dependencies and affected guarded files: concrete logical changes requiring authorization.
5. Open questions: which block design, which can be proposals in a draft, and which are explicitly deferred.
6. Outcome: ready to draft, draft with listed unresolved choices, or blocked with reason.

Raise contradictions before changing accepted meaning. Never silently choose the convenient requirement, reinterpret a proposal as approval, or delete a deferred requirement. Ask the smallest necessary question; progress on independent work. Record meaningful decisions/instructions each iteration and reread the full applicable history before updating it.

## 4. Draft and approve

The design session creates the milestone's design/test/plan together so tests measure the promised behavior and implementation steps cannot introduce hidden scope. Prefer existing SDK/open-source capabilities; custom code must have a current purpose. Assess every applicable principle and explain non-applicable ones briefly.

Trace requirements → decisions → design behavior → test cases. Verify the three documents agree on scope, failure behavior, versions, ownership, exclusions and acceptance. Test cases describe meaningful outcomes, not tests merely mirroring code. Review evidence must distinguish simulated/offline checks from actual integrated/local/manual acceptance.

Present unresolved policy choices and exact guarded logical amendments explicitly. Obtain approval of the concrete revision before implementation. Pin approval reference and full SHA; preserve approved contracts. Keep proposed, approved, implemented, verified, accepted and merged distinct.

## 5. Implementation handoff and return

Before preparing or executing a handoff, read [Codex handover rules](codex-handover-rules.md). The design session supplies a fully filled copyable prompt with immutable links and concrete paths, not a vague instruction to find the design.

Codex orchestrates one coder and two independent reviewers (design drift and test gaps), using Sol as specified in those rules, with at most three rounds and permanent reports. The implementation plan references that process and supplies milestone-specific details. It must not weaken the process or invent additional rounds.

Return one complete copyable evidence handoff to the originating design session. That session performs the final review of the actual diff/evidence. User acceptance and explicit merge authorization follow separately; no reviewer self-approves a merge.

## 6. Closure and maintenance

Update milestone/shared progress, relevant public guides and Atlas from verified results. Preserve all failed checks/findings and their eventual dispositions. Record blocked/manual work honestly. Stage Design PRs follow the separate closeout and explicit merge gate above. Older PRs labelled MERGE LAST retain their keep-open restriction until their owners adopt this convention; changing the label does not grant merge permission.

New fields or capabilities trigger an impact check against requirements, decisions, approved contracts/tests and affected milestones. Resolve drift explicitly before implementation. This method changes development governance, not the application's runtime architecture.
