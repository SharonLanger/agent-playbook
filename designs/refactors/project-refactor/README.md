# Project refactor

**Status — draft PR.** [Project refactor PR #59](https://github.com/SharonLanger/agent-playbook/pull/59) contains the approved [stage and milestone structure](stage-structure.md), the [existing-stage alignment](stage-alignment.md), and the authorized [shared-learning and root-sandbox migration](learning-sandbox-migration.md). The migration is applied on the draft branch. Its independent review has a separate evidence record.

Sharon agreed to the structure and retention direction in the 2026-11-18 project-structure discussion. On 2026-11-19 Sharon authorized the shared-learning and root-sandbox migration using the proposed destinations and archive, with the two guarded navigation and ownership amendments recorded in the [migration record](learning-sandbox-migration.md).

## Historical proposal and baseline inventory

The proposal below records the original design and pre-implementation verification. Its proposed paths describe the original inventory, inspected on [main at `cdbc06c2e9a9b87910b5145ac116aeb8a81e06e4`](https://github.com/SharonLanger/agent-playbook/commit/cdbc06c2e9a9b87910b5145ac116aeb8a81e06e4). The migration record links the applied dispositions and the exact pre-migration PR revision.

## Goal and scope

Make system-wide design easier to find, keep stage learning and evidence with their owners, and restart the root `sandbox/` as a small collection of useful references and ideas. Keep the existing repository and its history. Preserve complete design records, useful learning, stable identifiers and revision-specific evidence.

The migration covers two groups of files, `designs/learning/` and root `sandbox/`, plus their documentation and navigation dependencies. Runtime code, tests, configuration, tooling, releases, official product behavior, renumbering or relocating stage and milestone records, and the personal `app/examples/` sandbox are outside its scope. The publication exposure audit follow-up runs independently. Publication readiness is determined through that audit and the separate publication review.

## Ownership

| Location | Responsibility |
| --- | --- |
| `app/` | Executable application, tests, configuration and development tooling |
| `app/docs/` | Maintained user guides for supported product behavior |
| `designs/` | Overall architecture, principles, structure, roadmap and progress |
| `designs/governance/` | Procedures and rules governing repository work |
| `designs/stages/<stage>/` | Stage designs, decisions, milestones, reviews and learning. Milestone-specific evidence stays with its milestone. |
| `designs/refactors/` | Refactor proposals, rationale and verification records |
| `designs/explorations/` | Non-binding research and alternatives |
| `designs/atlas/` and `designs/diagrams/` | Visual navigation and shared architecture diagrams |
| `sandbox/` | Curated reference material and draft ideas, outside runtime and governance |

### Learning and walkthroughs

| Baseline path | Planned disposition |
| --- | --- |
| `designs/learning/architecture-walkthrough.md` | Move to `designs/architecture-walkthrough.md`, beside the architecture it explains. Update its execution SVG and diagram-viewer links to `diagrams/02-execution.svg` and `diagrams/index.html`. Preserve its status as an illustration of the target. |
| `designs/learning/README.md` | Fold its useful navigation into `designs/README.md`, including the distinction between the system walkthrough and stage tutorials. Retire this index after repairing inbound navigation. |

This is the complete shared learning folder at the baseline. Stage-specific learning belongs in `designs/stages/<stage>/learning/`. Stages 00 and 01 already use that structure. Stage design, milestone acceptance and review evidence continue to follow the [stage and milestone method](../../governance/stage-milestone-workflow.md). Link to the owning explanation when another document needs it. Existing refactor-specific lessons and milestone evidence stay with their own records.

## Root sandbox restart

All 17 tracked root sandbox files at the baseline are Markdown. Each file was read to assign its disposition. Six are useful retained documents, seven are placeholders or illustrative examples, two describe a separate historical project, and two provide maintenance and navigation. The count matches the earlier inventory.

The archive is proposed under this refactor's directory, with the source project's internal layout intact so its PR 46 requirements can still link to the adjacent feature design through the existing relative path. The retained filenames under `references/` and `ideas/` are also proposed. Before implementing, refresh the inventory and account for any newly added files before retiring paths.

| Baseline path | Planned disposition | Evidence and adaptation |
| --- | --- | --- |
| `sandbox/agents/reviewer.md` | Retain as `sandbox/references/reviewer.md` | Historical reviewer scope, approval/evidence checks and the Drive handoff protocol. Keep the reasoning. Label example invocation, routing and write permissions as historical, including the `system-one-harness` hardcoding in destination resolution. |
| `sandbox/agents/designer.md` | Retain as `sandbox/references/designer.md` | Historical requirements and design approval process. Label its playbook-root `projects/` lookup, numbering and save flow as the earlier convention. |
| `sandbox/verification/reviewer-handoff.md` | Retain as `sandbox/references/reviewer-handoff.md` | Historical delivery and fresh-session checklist, including manifests, hashes and readback. Preserve the distinction between planned checks and observed evidence. |
| `sandbox/projects/agent-playbook/features/f-01-reviewer-trial/design.md` | Retain as `sandbox/ideas/reviewer-trial.md` | Draft `f-01-reviewer-trial` uses System One Harness PR 46 as the first trial. Preserve the evaluation criteria and point to the archived requirements with their draft context. |
| `sandbox/projects/agent-playbook/features/f-02-implementer-handoff/design.md` | Retain as `sandbox/ideas/implementer-handoff.md` | Draft `f-02-implementer-handoff` proposes bounded writer/reviewer delivery and explicit outcomes. Treat the code-writer placeholder and old filename as historical references. |
| `sandbox/projects/agent-playbook/features/f-03-design-deviations/design.md` | Retain as `sandbox/ideas/design-deviations.md` | Draft `f-03-design-deviations` describes numbered deviations, authority and a closeout record. Keep its link to the implementer idea and historical planner rationale. |
| `sandbox/agents/code-writer.md` | Retire from the working tree | `UNIMPLEMENTED` stop placeholder. Keep its historical reference in the implementer idea. |
| `sandbox/agents/orchestrator.md` | Retire from the working tree | `UNIMPLEMENTED` role and routing placeholder pointing to the old README. |
| `sandbox/agents/replanner.md` | Retire from the working tree | `UNIMPLEMENTED` deferred role. The deviation idea retains the planner-based alternative. |
| `sandbox/agents/tester.md` | Retire from the working tree | `UNIMPLEMENTED` deferred role. |
| `sandbox/workflows/implement-change.md` | Retire from the working tree | `UNIMPLEMENTED` workflow without steps, routes or limits. |
| `sandbox/projects/project-a/review-rules.md` | Retire from the working tree | Example template with no project requirements. |
| `sandbox/projects/project-a/reviews/pr-14.md` | Retire from the working tree | Example naming placeholder with no PR-specific requirements. |
| `sandbox/projects/system-one-harness/features/f-01-offline-test-suite/design.md` | Archive as `designs/refactors/project-refactor/archive/system-one-harness/features/f-01-offline-test-suite/design.md` | Preserve the complete draft, its `f-01-offline-test-suite` ID, source repository, test design and approval caveat. The quoted former design location remains historical provenance. |
| `sandbox/projects/system-one-harness/reviews/pr-46.md` | Archive as `designs/refactors/project-refactor/archive/system-one-harness/reviews/pr-46.md` | Preserve the complete review requirements, the relative design link and the external PR 45 and 46 references. |
| `sandbox/README.md` | Rewrite at `sandbox/README.md` | Replace the old role-launch and per-project navigation with the sandbox purpose and links to the six retained documents. Preserve the historical guide in Git and carry forward any needed provenance. |
| `sandbox/AGENTS.md` | Rewrite at `sandbox/AGENTS.md` | Replace the old `agents/`, `workflows/` and `projects/` maintenance structure with concise reference and idea maintenance rules under the repository's root instructions. |

Label the retained reference documents as historical and the three ideas as drafts. Preserve original IDs, approval caveats, source revisions and evidence in the moved records. Link to the baseline when an old invocation or retired path matters to understanding the history. Keep source and external PR citations pinned where a revision is already recorded.

## Dependencies verified at the baseline

| Surface | Observed dependency and planned handling |
| --- | --- |
| [Design index](../../README.md) | Its `learning/README.md` link is the live entry to shared learning. Link directly to `architecture-walkthrough.md`, keep the stage-learning pointers findable, and update the wording for the existing `../sandbox/` link. |
| [Target architecture](../../architecture.md) and the moved walk-through | The target links to `learning/architecture-walkthrough.md`. Change that link after guarded approval. The walk-through's `../diagrams/` references need a one-level adjustment at the new location. |
| [Project structure](../../project-structure.md), [root instructions](../../../AGENTS.md) and [design instructions](../../AGENTS.md) | Project structure defines `sandbox/` as historical experiments and `designs/` as the home for architecture and learning. Root instructions treat the sandbox as historical with separately scoped edits. The design instructions already distinguish stage records, refactors and explorations. Align the current descriptions with the approved migration and retain the existing edit-scope rules. |
| [Atlas catalog](../../atlas/catalog.json), [generated viewer](../../atlas/index.html) and [viewer guide](../../atlas/README.md) | Current and Explorations inventories both list the two shared learning files. Their repository blocks both refer to root `sandbox/`, and the historical Explorations inventory lists all 17 original sandbox files. Update Current to the moved walk-through and curated sandbox boundary, without adding sandbox internals to Current. Keep historical rows attributable to their original snapshot. Review their display so old names are clearly historical. Rebuild from the catalog and check both views. The builder validates explicit source references, guards, hierarchy and freshness. Its inventory entries are display records, so separately review their status and path accuracy. |
| [Historical candidate inventory](../../explorations/agent-execution/candidate-file-structure.md) and [earlier runtime proposal](../2026-11-12-runtime-structure/proposal.md) | The candidate inventory prints the old learning and sandbox paths as a PR baseline. The runtime proposal includes an earlier tree and [an immutable walk-through citation](https://github.com/SharonLanger/agent-playbook/blob/6f16508d9f36da66edec04ddb055d8954f0f7c70/designs/learning/architecture-walkthrough.md). Preserve those historical references and distinguish them from live navigation. |
| Sandbox cross-references | The old README links the checklist and feature drafts. The reviewer links the checklist and uses the old `projects/` lookup. The checklist relies on the old launch example. The three ideas cite the earlier roles, files or PR 46 rules. Repair navigation to retained and archived destinations. Preserve old procedures as dated examples and avoid implying that historical settings authorize any new review or Drive actions. |

The baseline text search covered the relevant tracked Markdown, configs, source and generated Atlas output, excluding `app/examples/`. It found no live references to the moving paths in `app/docs/` or application code. Before a migration, repeat the targeted search on its actual base and inspect any affected branch or open PR references and known external links. Preserve immutable citations and validate live links from the new locations. Historical research inventories should remain understandable as snapshots even after old live paths leave `main`.

### Guarded amendments for the migration phase

| Guarded file | Proposed logical change for Sharon to review |
| --- | --- |
| `designs/project-structure.md` | Replace the root sandbox ownership description with curated references and ideas. Record stage-local learning, system-level walkthrough placement and the historical records location under the owning refactor. This changes documentation ownership and lookup locations. |
| `designs/architecture.md` | Update the single live walk-through target. This is a navigation change within the guarded architecture. |
| `designs/charter.md` | Its historical-experiment separation rule is compatible with the proposal when the archive stays separate from application work. If the line is updated to describe the curated root sandbox and the historical archive explicitly, present that exact wording as a guarded change. |
| `designs/principles.md` | Principle 11 already calls for reviewed preservation of historical playbook material. Retain the guard and show how archival, durable links and ordinary Git history meet it. If implementation requires changing its wording, obtain approval for the exact logical amendment first. |

The [design contract](../../governance/design-contract.md) and [guarded-file register](../../governance/guarded-files.md) govern approval and retention. Baseline inspection identified no moved file in the register. Protection also follows any previously approved content, so recheck before editing. Treat any later change to explicitly guarded text, including protected portions of instructions or diagrams, under the same approval rule.

## Later implementation and verification

1. Refresh `main`, existing PR dependencies and the 17-path inventory. Confirm destination names and archive ownership. Record the migration base and the required per-file approvals before any guarded edit.
2. Move the walk-through, the six retained files and the two complete archive records within Git. Keep renames reviewable. Preserve historical content and add status/provenance framing to the six retained documents. Keep the archive pair's relative layout and link to it from the refactor record.
3. Update live navigation, including the walk-through's diagram links and sandbox cross-links, and apply approved authority edits. Rewrite the two sandbox maintenance files. After live references resolve, retire the old learning index and seven placeholders. Preserve pinpoint access through the migration-base commit for any old material that still explains a retained decision.
4. Update Atlas metadata, run `python3 designs/atlas/build.py` and `python3 designs/atlas/build.py --check`, and review the Current and Explorations views. Use the verified status records for any status change. Record the actual migration separately from the draft proposal.
5. Verify the final diff against the mapping and scan for unresolved old live paths. Resolve relative links and anchors, open the SVG and HTML viewer links, and check historical citations against their referenced commits. Confirm all three idea IDs and both archive records retain their provenance and that the archived PR rules resolve to the archived design. Confirm the scope by comparing application paths, stage records and existing guards to the base. Keep the actual results attached to the migration revision.
6. If needed after merge, revert the migration in ordinary Git commits, with the matching navigation and Atlas output. Verify restored links against the recorded base and account for intervening edits. Preserve commit history.

## Proposal verification and approval basis

This note belongs under `designs/refactors/` because it records a proposed change to repository documentation structure and its eventual verification. The governing sources are the [charter](../../charter.md), [principles](../../principles.md), [project structure](../../project-structure.md) and [design contract](../../governance/design-contract.md). The [agent execution exploration](../../explorations/agent-execution/README.md) provides the historical role and path inventory. The [harness exploration](../../explorations/harness.md) provides context for keeping harness ideas separate from approved application responsibilities.

- Principles 1, 3, 4, 8, 9, 11, 12, 13, 14 and 15 apply through explicit guarded approval, unchanged approved boundaries, learning ownership, revision-specific evidence, bounded scope, retention, provenance, personal-sandbox isolation, official-guide assessment and explicit draft status.
- Principle 2 applies to keeping historical configuration and links as provenance while leaving access and publication assessment with the authorized owners. Principles 5, 6, 7 and 10 concern implementation, configuration, runtime gates and deployment. The PR records this proposal and removes private Drive URLs from current tracked Markdown; it changes no executable behavior.
- The structural proposal leaves current status, official guides and Atlas inputs unaffected. The separately authorized Drive-link cleanup preserves status/verification claims and records private checklist titles without their URLs. The current Atlas should not present the proposed structure as implemented.
- Baseline verification read all 17 sandbox files and checked the path dependencies. The existing Atlas builder completed its input checks, but `--check` reported a pre-existing freshness failure against `main` at the recorded SHA. All 76 input and output files used by the check matched their baseline Git blobs. Regeneration differed in the embedded diagrams, source fingerprint and final newline. The draft records that discrepancy for later reconciliation.

## Publication-link decision and applied cleanup — 2026-11-18

Sharon requested removal of Google Drive links from current repository files and explicitly accepted leaving their older commit-history occurrences unchanged. This authorized the URL cleanup in this PR. The folder migration was still proposed at the time of that decision.

The cleanup removes 10 Markdown link targets from these five files while retaining checklist names, historical verification claims, and repository-local guidance:

- `designs/progress.md`
- `designs/stages/02-langfuse/resolution-2026-11-13.md`
- `designs/stages/02-langfuse/user-verification.md`
- `designs/stages/02-langfuse/verification-simplification-plan.md`
- `sandbox/agents/reviewer.md`

The reviewer guide now requires an explicitly supplied Drive destination instead of configuring a personal folder in the repository. Destination discovery and delivery must still be verified; no external document or sharing setting is changed by this cleanup.

Scope and verification: the preceding exposure audit located these links in current tracked content at the unchanged main baseline above; this branch previously added only this proposal. The five affected files and this proposal were checked for remaining Drive URLs and copied destination IDs after editing. The Markdown table labels and local navigation remain intact. Historical links are accepted by the owner and are not removed through a history rewrite. This decision resolves the intended treatment of audit item F-002; main still requires the PR to be merged before its current files reflect the cleanup. Other audit items, metadata-email decisions and coverage limits remain open.

## Remaining decisions

The migration's independent review and Sharon's disposition are recorded separately from this proposal. PR #59 remains draft and unmerged.

## Refactor process clarification — 2026-11-19

Sharon requested that identifying work as a refactor automatically selects the same requirements, decisions, design, approval and bounded-review process as stages, with research/learning when needed and milestones only when useful. The shared [working method](../../governance/stage-milestone-workflow.md#independent-refactors) now defines that startup procedure, root-package alternative and Refactor Design PR lifecycle. Root/design agent instructions make discovery mandatory. The guarded project structure defines placement; the guarded design contract extends authority/registration to approved refactor baselines; the guarded handover rules cover root packages and identify the refactor PR in both handoff directions. Stage sequencing and existing protection remain intact.

This applies the user's explicit request within draft PR #59, without migrating active logging/stage contracts or changing runtime behavior. Architecture/charter/principles and public product guides need no changes: this is a shared development procedure and adds no supported application capability. Atlas navigation reflects the expanded working method. Existing stage-standard/alignment/migration review reports apply to their recorded candidates; this follow-up does not claim those independent reviews cover these new edits.

Verification for this clarification: Atlas regeneration and `python3 designs/atlas/build.py --check` passed; 94 relative Markdown links and their local anchors resolved against the checked repository inventory; changed Markdown passed whitespace and Drive-URL checks. The diff is limited to the two agent instruction files, four shared governance/ownership documents, design/refactor indexes and Atlas catalog/generated view. No application tests were run for this procedure-only change. These are originating-session checks, not a new independent implementation-review round.
