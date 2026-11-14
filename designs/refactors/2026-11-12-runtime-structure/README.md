# Runtime structure refactor — review entry point

**Status: Accepted and merged in PR #34** (`96cb1f89c5d2927bbc7be66e1760595ed0ebe8b0`). Verification is revision-specific in [verification.md](verification.md).

This change implemented the current-code cleanup requested on 12 November 2026.
The future system proposal remains separate from the merged subset.

## Read in this order

1. [Proposal](proposal.md): rationale, alternatives, repository research, complete
   future file tree, role/harness/tool ownership and staged migration.
2. [Current project structure](../../project-structure.md): approved current boundaries.
3. [Verification evidence](verification.md): executed checks and remaining limits.

The proposal is preserved as the planning snapshot. Its source inventory describes
main before this refactor; its proposed names are not a claim that future files exist.
The current structure and verification record describe the implemented subset.

## Historical PR scope

The following records what PR #34 included at review time. The temporary verification helper was subsequently removed by PR #35.

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

## Historical PR principle assessment

The table below records the review-time assessment; its pending-approval statements are historical.

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

## Historical acceptance instructions

At review time, Sharon was asked to review the diff, run the verification command and try the shared PyCharm tasks. PR #34 was subsequently accepted and merged; the temporary helper was removed through PR #35. The architecture proposal and verification record remain permanent.
