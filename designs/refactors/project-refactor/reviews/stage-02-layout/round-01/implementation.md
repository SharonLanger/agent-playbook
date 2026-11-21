<!-- Permanent evidence for PR #67; candidate ab94509cedf9f01eedaa32a4546ecdfafcc879e5; round 01. -->

# Stage 02 documentation layout migration

**Coder outcome: PASS.** Candidate frozen locally for publication and independent review. Baseline `13bebb0d824cf9b2d1794a0cbff2311fbd99489c`, tree `e95da0c49ea01dab4cbc3edc3c9f445884405806`. Sharon approved the complete file map and a separate draft PR. The reviewed SHA and final PR state belong to the orchestrator's publication record.

## Change summary

The approved mapping retains four root documents, relocates 63 files and adds the M1–M3 package README. All 67 originals have one destination. Of these, 44 are byte-identical and 23 have link or navigation changes. Current stage navigation starts at a single canonical milestone table. The M4.R research, M4.1 context and combined M4.2 + M4.3 tracing retain their original IDs, exact URL pins, protected contracts and review evidence.

The relocation uses the existing stage-level rules for canonical status, protected contracts, document retention and project-status roll-up. D23, the stage alignment record, the logging amendments and old review reports retain historical path references as provenance. New navigation points to current paths. The dated alignment note records the scope of Sharon's location approval. The guard register lists all six current protected milestone paths and keeps the original approval URLs. No product behavior, dependency integration, test contract, release configuration or personal sandbox activity is involved. The maintained local Langfuse guide has one evidence-link repair.

## Verification

| Criterion | Evidence |
|---|---|
| S2L-01 | Exact `inputs/metadata.json` source-to-destination inventory, original Git blob verification, no collisions, unexpected deletions or additions. |
| S2L-02 | The joint M1–M3 package and M4 package navigation retain milestone IDs and historical package names. The stage README owns the canonical table. |
| S2L-03 | All original absolute URLs and stable ID occurrences preserved. All non-README Stage 02 text compares exactly after the mapped link replacements and two explicit relative path repairs. Retained prose and heading aliases verified for the four updated READMEs. Six guard locations reconciled without a change to approved meanings. |
| S2L-04 | All 13 research/probe files match their original Git blob hashes. The research note also moved byte-for-byte. |
| S2L-05 | Applied 162 recorded inline link rewrites across 31 files. The audit checked 420 relative Markdown references, comprising 386 repository path resolutions, 33 local anchors and one unchanged out-of-scope Stage 00 link validated for tracked path only. No path or in-scope anchor errors. Original README anchors survive the heading changes. |
| S2L-06 | `python3 designs/atlas/build.py` regenerated the index. `python3 designs/atlas/build.py --check` reported PASS for references, hierarchy, guards, sandbox boundary and freshness. Candidate Atlas entries link to the new local package and describe completed M4 and historical research/reconciliation consistently with closeout. |
| S2L-07 | Eleven outside paths changed. All other available files compare byte-for-byte. No other stage changes. No application source/configuration/tests/dependencies, CI, shared governance rules or README outside Stage 02 and specified navigation changed. |
| S2L-08 | Current entry points lead to completed Stage 02 and the approved M4 packages. Dated prior instructions and statuses are retained below historical headings. Local `verify-layout.py` passed, including a check for introduced trailing whitespace. |

The unchanged Stage 00 `plan.md#substages` fragment is outside the migration. Its file is tracked, and the verifier skips the Stage 00 heading check. Application and probe execution were outside this documentation-only verification. No examples were read. The partial snapshot was supplemented with the pinned repository tree for targets. No blockers found.

## Changed paths

The full 67-file inventory is `inputs/metadata.json`. The only new file is `designs/stages/02-langfuse/m1-3-local-langfuse/README.md`. The following mapped destination files changed content beyond their relocation.

- `designs/stages/02-langfuse/README.md`
- `designs/stages/02-langfuse/architecture.md`
- `designs/stages/02-langfuse/closeout.md`
- `designs/stages/02-langfuse/m1-3-local-langfuse/history/connection-playground-handoff.md`
- `designs/stages/02-langfuse/m1-3-local-langfuse/history/implementation-handoff.md`
- `designs/stages/02-langfuse/milestones.md`
- `designs/stages/02-langfuse/m1-3-local-langfuse/reviews/resolution-2026-11-13.md`
- `designs/stages/02-langfuse/m1-3-local-langfuse/reviews/review-2026-11-13.md`
- `designs/stages/02-langfuse/m1-3-local-langfuse/smoke-plan.md`
- `designs/stages/02-langfuse/m1-3-local-langfuse/user-verification.md`
- `designs/stages/02-langfuse/m1-3-local-langfuse/history/verification-simplification-plan.md`
- `designs/stages/02-langfuse/m1-3-local-langfuse/verification.md`
- `designs/stages/02-langfuse/m4-workflow-integration/README.md`
- `designs/stages/02-langfuse/m4-workflow-integration/decisions.md`
- `designs/stages/02-langfuse/m4-workflow-integration/history/runner-design-discussion.md`
- `designs/stages/02-langfuse/m4-workflow-integration/m4-2-3-workflow-tracing/reviews/tracing-final-review.md`
- `designs/stages/02-langfuse/m4-workflow-integration/m4-1-context/README.md`
- `designs/stages/02-langfuse/m4-workflow-integration/m4-1-context/implementation-plan.md`
- `designs/stages/02-langfuse/m4-workflow-integration/m4-1-context/reviews/status.md`
- `designs/stages/02-langfuse/m4-workflow-integration/m4-2-3-workflow-tracing/README.md`
- `designs/stages/02-langfuse/m4-workflow-integration/m4-2-3-workflow-tracing/follow-ups.md`
- `designs/stages/02-langfuse/m4-workflow-integration/history/repository-updates.md`
- `designs/stages/02-langfuse/m4-workflow-integration/requirements.md`

The only edits outside Stage 02 are listed below.

- `app/docs/langfuse-local.md`
- `designs/atlas/catalog.json`
- `designs/atlas/index.html`
- `designs/explorations/README.md`
- `designs/governance/guarded-files.md`
- `designs/progress.md`
- `designs/refactors/project-refactor/stage-alignment.md`
- `designs/refactors/project-refactor/stage-structure.md`
- `designs/refactors/workflow-contract/design.md`
- `designs/refactors/workflow-contract/file-structure.md`
- `designs/refactors/workflow-contract/test-plan.md`


## Published candidate and reproducibility

Coder model configured: `gpt-6.2-sol`. This report describes [candidate ab94509cedf9f01eedaa32a4546ecdfafcc879e5](https://github.com/SharonLanger/agent-playbook/commit/ab94509cedf9f01eedaa32a4546ecdfafcc879e5). The local snapshot, metadata and migration-audit helpers mentioned above were isolated review artifacts, not application dependencies or permanent operating instructions. The exact approved move map is retained in [round 1 implementation evidence](../round-01/implementation.md#complete-relocation-map); the source and resulting files are available at the pinned commits. The audit checked original Git blob identities, mapped path coverage, allowed scope, original IDs/URLs/prose, relative targets and fragments, and Atlas freshness. Reproduce the maintained Atlas check with `python3 designs/atlas/build.py --check` from the reviewed checkout. No application test or probe run is claimed.


## Complete relocation map

Paths below are relative to `designs/stages/02-langfuse/`. Every original file is represented once; unchanged destinations are retained root records.

| Original path | Destination path |
|---|---|
| `README.md` | `README.md` |
| `acceptance-2026-11-14.md` | `m1-3-local-langfuse/reviews/acceptance-2026-11-14.md` |
| `architecture.md` | `architecture.md` |
| `closeout.md` | `closeout.md` |
| `connection-playground-handoff.md` | `m1-3-local-langfuse/history/connection-playground-handoff.md` |
| `findings.md` | `m1-3-local-langfuse/reviews/findings.md` |
| `implementation-handoff.md` | `m1-3-local-langfuse/history/implementation-handoff.md` |
| `main-reconciliation.md` | `m1-3-local-langfuse/history/main-reconciliation.md` |
| `milestones.md` | `milestones.md` |
| `resolution-2026-11-13.md` | `m1-3-local-langfuse/reviews/resolution-2026-11-13.md` |
| `review-2026-11-13.md` | `m1-3-local-langfuse/reviews/review-2026-11-13.md` |
| `smoke-plan.md` | `m1-3-local-langfuse/smoke-plan.md` |
| `user-verification.md` | `m1-3-local-langfuse/user-verification.md` |
| `verification-simplification-plan.md` | `m1-3-local-langfuse/history/verification-simplification-plan.md` |
| `verification.md` | `m1-3-local-langfuse/verification.md` |
| `workflow-integration/README.md` | `m4-workflow-integration/README.md` |
| `workflow-integration/decisions.md` | `m4-workflow-integration/decisions.md` |
| `workflow-integration/history/context-discussion.md` | `m4-workflow-integration/history/context-discussion.md` |
| `workflow-integration/history/context-final-review.md` | `m4-workflow-integration/m4-1-context/reviews/context-final-review.md` |
| `workflow-integration/history/observability-spec-v0.14.md` | `m4-workflow-integration/history/observability-spec-v0.14.md` |
| `workflow-integration/history/runner-design-discussion.md` | `m4-workflow-integration/history/runner-design-discussion.md` |
| `workflow-integration/history/tracing-final-review.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/reviews/tracing-final-review.md` |
| `workflow-integration/m1-context/README.md` | `m4-workflow-integration/m4-1-context/README.md` |
| `workflow-integration/m1-context/design.md` | `m4-workflow-integration/m4-1-context/design.md` |
| `workflow-integration/m1-context/implementation-plan.md` | `m4-workflow-integration/m4-1-context/implementation-plan.md` |
| `workflow-integration/m1-context/reviews/round-01/design-drift.md` | `m4-workflow-integration/m4-1-context/reviews/round-01/design-drift.md` |
| `workflow-integration/m1-context/reviews/round-01/implementation.md` | `m4-workflow-integration/m4-1-context/reviews/round-01/implementation.md` |
| `workflow-integration/m1-context/reviews/round-01/orchestrator.md` | `m4-workflow-integration/m4-1-context/reviews/round-01/orchestrator.md` |
| `workflow-integration/m1-context/reviews/round-01/test-gap.md` | `m4-workflow-integration/m4-1-context/reviews/round-01/test-gap.md` |
| `workflow-integration/m1-context/reviews/round-02/design-drift.md` | `m4-workflow-integration/m4-1-context/reviews/round-02/design-drift.md` |
| `workflow-integration/m1-context/reviews/round-02/implementation.md` | `m4-workflow-integration/m4-1-context/reviews/round-02/implementation.md` |
| `workflow-integration/m1-context/reviews/round-02/orchestrator.md` | `m4-workflow-integration/m4-1-context/reviews/round-02/orchestrator.md` |
| `workflow-integration/m1-context/reviews/round-02/test-gap.md` | `m4-workflow-integration/m4-1-context/reviews/round-02/test-gap.md` |
| `workflow-integration/m1-context/reviews/status.md` | `m4-workflow-integration/m4-1-context/reviews/status.md` |
| `workflow-integration/m1-context/test-cases.md` | `m4-workflow-integration/m4-1-context/test-cases.md` |
| `workflow-integration/m2-3-workflow-tracing/README.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/README.md` |
| `workflow-integration/m2-3-workflow-tracing/design.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/design.md` |
| `workflow-integration/m2-3-workflow-tracing/follow-ups.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/follow-ups.md` |
| `workflow-integration/m2-3-workflow-tracing/implementation-plan.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/implementation-plan.md` |
| `workflow-integration/m2-3-workflow-tracing/reviews/local-acceptance.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/reviews/local-acceptance.md` |
| `workflow-integration/m2-3-workflow-tracing/reviews/round-01/design-drift.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/reviews/round-01/design-drift.md` |
| `workflow-integration/m2-3-workflow-tracing/reviews/round-01/implementation.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/reviews/round-01/implementation.md` |
| `workflow-integration/m2-3-workflow-tracing/reviews/round-01/orchestrator.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/reviews/round-01/orchestrator.md` |
| `workflow-integration/m2-3-workflow-tracing/reviews/round-01/test-gap.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/reviews/round-01/test-gap.md` |
| `workflow-integration/m2-3-workflow-tracing/reviews/round-02/design-drift.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/reviews/round-02/design-drift.md` |
| `workflow-integration/m2-3-workflow-tracing/reviews/round-02/implementation.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/reviews/round-02/implementation.md` |
| `workflow-integration/m2-3-workflow-tracing/reviews/round-02/orchestrator.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/reviews/round-02/orchestrator.md` |
| `workflow-integration/m2-3-workflow-tracing/reviews/round-02/test-gap.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/reviews/round-02/test-gap.md` |
| `workflow-integration/m2-3-workflow-tracing/reviews/status.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/reviews/status.md` |
| `workflow-integration/m2-3-workflow-tracing/round-02-revision.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/round-02-revision.md` |
| `workflow-integration/m2-3-workflow-tracing/test-cases.md` | `m4-workflow-integration/m4-2-3-workflow-tracing/test-cases.md` |
| `workflow-integration/repository-updates.md` | `m4-workflow-integration/history/repository-updates.md` |
| `workflow-integration/requirements.md` | `m4-workflow-integration/requirements.md` |
| `workflow-integration/research/crewai-langfuse.md` | `m4-workflow-integration/research/crewai-langfuse.md` |
| `workflow-integration/research/probe/README.md` | `m4-workflow-integration/research/probe/README.md` |
| `workflow-integration/research/probe/agent_playbook/workflows/wf_01_step_sequence/flow.py` | `m4-workflow-integration/research/probe/agent_playbook/workflows/wf_01_step_sequence/flow.py` |
| `workflow-integration/research/probe/agent_playbook/workflows/wf_01_step_sequence/steps.py` | `m4-workflow-integration/research/probe/agent_playbook/workflows/wf_01_step_sequence/steps.py` |
| `workflow-integration/research/probe/agent_playbook/workflows/wf_02_shared_state/flow.py` | `m4-workflow-integration/research/probe/agent_playbook/workflows/wf_02_shared_state/flow.py` |
| `workflow-integration/research/probe/agent_playbook/workflows/wf_02_shared_state/state.py` | `m4-workflow-integration/research/probe/agent_playbook/workflows/wf_02_shared_state/state.py` |
| `workflow-integration/research/probe/agent_playbook/workflows/wf_02_shared_state/steps.py` | `m4-workflow-integration/research/probe/agent_playbook/workflows/wf_02_shared_state/steps.py` |
| `workflow-integration/research/probe/agent_playbook/workflows/wf_03_conditional_route/flow.py` | `m4-workflow-integration/research/probe/agent_playbook/workflows/wf_03_conditional_route/flow.py` |
| `workflow-integration/research/probe/agent_playbook/workflows/wf_03_conditional_route/state.py` | `m4-workflow-integration/research/probe/agent_playbook/workflows/wf_03_conditional_route/state.py` |
| `workflow-integration/research/probe/agent_playbook/workflows/wf_03_conditional_route/steps.py` | `m4-workflow-integration/research/probe/agent_playbook/workflows/wf_03_conditional_route/steps.py` |
| `workflow-integration/research/probe/probe.py` | `m4-workflow-integration/research/probe/probe.py` |
| `workflow-integration/research/probe/requirements.txt` | `m4-workflow-integration/research/probe/requirements.txt` |
| `workflow-integration/research/probe/results.json` | `m4-workflow-integration/research/probe/results.json` |
| `workflow-integration/research/probe/source-manifest.json` | `m4-workflow-integration/research/probe/source-manifest.json` |
