# Repository reconciliation checklist

Status: **pending review checklist, not permission to edit guarded meaning**. Updated 2026-11-14, iteration 21. The draft PR creates a review home; it does not complete M4.1 or Stage 02. [README](README.md) · [Decisions](decisions.md) · [Requirements](requirements.md)

## This opening documentation PR

- [x] Preserve current requirements, decisions, unresolved/deferred issues, complete discussion history and historical specification.
- [x] Preserve CrewAI report, exact probe source/results/dependencies and original provenance.
- [x] Add a start-here README, concrete cross-design reference and handoff rules.
- [x] Link the package from Stage 02 and the exploration index; expose it as draft/research in Atlas, not implemented or approved design.
- [x] Opening documentation checks: Atlas build/freshness, 67 relative links, stable requirement/decision/question IDs, full discussion preservation, unchanged 13-file probe and unchanged guarded baselines passed. Published PR scope is checked separately; no application tests or probe rerun claimed.
- [ ] Discuss remaining M4.1 details with Sharon before creating `01-context-design.md`.

No official product guide changes are needed yet: runtime behavior, supported CLI/configuration and dependencies do not change. No application test rerun is required for this documentation-only opening; preserved probe/application results belong to their original revisions. `app/examples/` remains excluded.

Preservation detail: the full Git whitespace check reports eight blank-at-EOF warnings in the eight unchanged copied Flow fixture modules. Keep them byte-identical to the recorded source hashes. The whitespace check with only that category disabled passes; current Markdown has no trailing whitespace. This is not a runtime/test failure.

## Before approving the detailed design / marking its PR ready

| File / surface | Logical change to present | Reason, limit and trigger |
|---|---|---|
| designs/principles.md, principle 5 | Narrow exception allowing native Langfuse instrumentation at reviewed call sites; preserve centralized configuration and separate agent-provider contracts | D11 rejects the mandatory tracing broker. Guarded: explain the exact addition/removal and consequences before editing |
| designs/architecture.md | Align observability responsibilities and tracing imports with context + SDK/native instrumentation; remove the mandatory neutral observation path for this phase | Guarded: preserve CrewAI scheduling, workflow lifecycle, error ownership, redaction and independent agent adapters; assess associated diagrams/Atlas semantics |
| designs/project-structure.md | Record the exact agreed context file responsibility/dependencies; reconcile tracing import rules | Guarded: exact path still open; do not create an unused package or decide agent lifecycle by placement |
| AGENTS.md engineering boundary | Review whether the general adapter instruction needs a tracing-specific cross-reference after the approved principle change | Follow file-specific approval if protected meaning is represented here; do not silently leave contradictory agent instructions |
| designs/stages/02-langfuse/architecture.md | Reconcile the earlier M4 observability-handle placeholder with agreed context/native tracing contracts | Approved boundaries protected; preserve accepted M1–M3 and their external configuration/client behavior |
| designs/stages/02-langfuse/milestones.md and README.md | Describe the finalized M4.R/M4.1/M4.2/M4.3 checkpoints and separate PR sequencing, distinguishing planning from implementation | Original one-branch M1–M3 policy must not override D21; preserve its historical scope and acceptance |
| designs/governance/guarded-files.md | Register the exact newly approved/locked milestone design and any approved contract sections | Only after Sharon approves that baseline; current shared draft is not automatically a locked design |
| designs/progress.md | Link actual draft/approved/implemented/verified/accepted/merged status with exact PR/revision | Update at the corresponding gate; this opening leaves current implementation status unchanged and does not claim M4 completion |
| designs/README.md, exploration index, Atlas catalog/generated HTML | Reconcile navigation/status with finalized source records | Rebuild from reconciled sources; no manual merge of generated HTML; no draft promotion to Current merely because a PR exists |
| designs/roadmap.md | Review only if stage ordering changes | No ordering change selected now; M4 submilestones do not renumber completed stages |
| designs/refactors/workflow-contract/design.md | Review the previously marked stale PR #40 review-status header (N02), if still present | Separate status-only guarded correction after verifying and explaining it; do not rewrite accepted lifecycle contracts |

These are review tasks, not blanket approval of unseen edits. No guard is removed. D11/D18/D19 are already accepted directions; review their concrete per-file consequences rather than reopening the same high-level choices.

## At each implementation milestone's closeout

- [ ] Refresh main and relevant concurrent PRs; assess shared-file overlap, especially context signatures, configuration/dependencies and Atlas. Do not claim zero conflicts.
- [ ] Map implementation and meaningful tests to the approved design and stable requirement IDs; preserve existing workflow results/errors and sandbox isolation.
- [ ] Record actual checks at their exact revision, plus blocked/unrun checks and local UI acceptance separately. Do not copy research success into application completion.
- [ ] Update official app/docs guides in the same PR when supported behavior/configuration changes; otherwise state the concrete no-impact reason.
- [ ] Reconcile progress, stage summaries, current shared records, relevant guarded changes and Atlas before readiness. Preserve earlier evidence as dated history.
- [ ] After an explicitly authorized merge, inspect the resulting main and update actual merge/acceptance status. Opening or approving a draft is not merge authorization.

M4.1 closeout covers context propagation/isolation. M4.2 adds real root correlation, startup/disabled/outage/shutdown behavior. M4.3 adds actual maintained workflows, masking/startup checks and local server/UI observation coverage. Agent lifecycle, logging, scores and unrelated harness work remain outside these closeouts.
