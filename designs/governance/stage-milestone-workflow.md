# Stage and milestone working method

**Status: GUARDED — standing method requested by Sharon on 2026-11-15.** Applies to all future stages and milestone design/implementation handoffs. Complements the [design contract](design-contract.md) and [Codex handover rules](codex-handover-rules.md); it does not approve individual designs.

## 1. Shared workspace and ownership

A stage is a coherent product/development goal; a milestone is a bounded outcome within it that can be designed, tested, reviewed and accepted independently. Define milestones by observable outcomes, not by arbitrary file counts or phases of writing code. Each has a stable ID, concise name, starting prerequisites, included/excluded behavior, dependencies and completion evidence. Combine or split only through an explicit recorded decision; preserve old IDs/history and explain their mapping.

The stage or named working package owns shared requirements, decisions, progress, research and history. For nested packages, the stage README links to them. Do not duplicate competing requirements across levels; link to the canonical owner. Keep shared research/history at the working-package root because they can inform several milestones.

Recommended shared files:
- README.md: start here, goal, reading order, milestone/status table, canonical references and next action.
- requirements.md: stable requirement IDs, scope, constraints, acceptance intent and deferred requirements.
- decisions.md: accepted/proposed/superseded decisions, rationale and open questions with owners.
- progress.md: milestone implementation/verification/acceptance/merge states and evidence; link to designs/progress.md as the repository-wide authority. Existing packages may retain their authoritative status table in README rather than create competing progress copies.
- repository-updates.md when needed: affected guarded/public/Atlas surfaces and reconciliation work.
- research/ and history/: dated evidence, sources, limitations and discussion records.

## 2. Every milestone gets a folder

Use m<number>-<short-slug>/, with at most three descriptive words in the slug, e.g. m1-context/. A combined milestone can use m2-3-workflow-tracing/. IDs remain unambiguous through the parent stage/package; document mappings to global IDs such as M4.1.

Each milestone folder contains:
- README.md — scope, prerequisites, status, reading order, approval revision and next action.
- design.md — responsibilities, placement, contracts/behavior, failure boundaries, dependencies, explicit exclusions, requirement/decision mapping and any guarded amendments.
- test-cases.md — stable test IDs, scenarios, meaningful observable assertions, test level, environment/manual needs and links to requirements.
- implementation-plan.md — work order, concrete files/checks, approved baseline, orchestration/review instructions and handoff entry.
- reviews/status.md and round-01/, round-02/, round-03/ reports as actually used.

Create review reports during implementation, not fictitious empty PASS reports during design. Prefer the four standard filenames without repeated milestone prefixes. Milestone-specific evidence belongs inside that milestone; general research/history stays shared. Preserve existing locked baselines: this method does not authorize a repository-wide migration or renumbering. Authorized moves update links/guard registrations and retain immutable historical references without changing approved semantics.

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

Update milestone/shared progress, relevant public guides and Atlas from verified results. Preserve all failed checks/findings and their eventual dispositions. Record blocked/manual work honestly. Ongoing planning PRs marked MERGE LAST remain open until all covered work is merged, final records reconciled and Sharon separately authorizes them.

New fields or capabilities trigger an impact check against requirements, decisions, approved contracts/tests and affected milestones. Resolve drift explicitly before implementation. This method changes development governance, not the application's runtime architecture.
