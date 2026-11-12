# Runtime structure refactor — review entry point

Status: **Draft for Sharon's review; not accepted or merged.**

This change implements the current-code cleanup requested on 12 November 2026.
The proposed completed system is documented separately from what exists today.

## Read in this order

1. [Proposal](proposal.md): rationale, alternatives, repository research, complete
   future file tree, role/harness/tool ownership and staged migration.
2. [Current project structure](../../project-structure.md): actual boundaries on
   this branch. Changes to guarded documents are part of the review diff.
3. [Review commands](../../../app/docs/refactor-review.md): automated checks and
   the short PyCharm checklist.
4. [Verification evidence](verification.md): executed checks and remaining limits.

The proposal is preserved as the planning snapshot. Its source inventory describes
main before this refactor; its proposed names are not a claim that future files exist.
The current structure and review guide describe the implemented subset.

## Included now

- Split release discovery and process launch; move terminal messages into the CLI.
- Split application assembly, workflow construction and workflow execution.
- Extract argument parsing from command dispatch/presentation.
- Move shared YAML to `app/application.yaml`; detect an old local override before
  it could be silently ignored.
- Align imports, tests, current documentation and shared IDE verification tasks.
- Provide a removable review script with source and isolated-release checks.

The future `agents/`, harness policies, SDK adapters and agent tools remain proposals.
There is no new model integration, workflow behavior, dependency, CI service or
application-version change. Existing examples and historical sandbox files are retained.

## Principle assessment

| Principle | Evidence / application |
|---|---|
| 1. Explicit approvals | Sharon explicitly requested implementing these changes in an unmerged PR for later review. Guarded-document changes remain proposed in the diff; this document does not declare them accepted. |
| 2. Security from the start | Active/local YAML stays outside wheels; local files remain ignored; verification uses the dedicated offline fixture and reports no secret values. |
| 3. No design drift | CrewAI still schedules workflow steps; current flow algorithms, input models and result semantics are unchanged. Proposed future ownership is explicitly labeled. |
| 4. Learning first | Stage lessons, diagrams and all eight independent examples remain; reading maps point to the extracted owners. |
| 5. Isolated integrations | Assembly configures CrewAI before the factory imports a selected flow. No new provider integration is introduced. |
| 6. External configuration | Shared/local YAML lives directly under app; explicit/environment selectors and validation remain, with a migration guard. |
| 7. Reproducible quality gates | Existing pinned uv environment and Pyright/Ruff/pytest gate; review script adds CLI, wheel and installed-release checks. |
| 8. Evidence over claims | Actual results and limits are in verification.md; macOS/PyCharm acceptance remains with Sharon. |
| 9. Incremental scope | Only existing responsibilities are extracted. The full future tree is an ownership proposal, not implementation instructions or frozen contracts for future stages. |
| 10. Local-first | CLI, bootstrap and local releases remain the operating model; offline checks are explicitly scoped to the fixture. |
| 11. No silent migration | sandbox is unchanged; old local YAML triggers instructions instead of being ignored or overwritten; no releases are deleted. |

## Acceptance

Review the diff, run the verification command, and try the shared PyCharm tasks.
Approval and merge are separate future actions. The helper can be removed after
acceptance; the architecture proposal and verification record are permanent.
