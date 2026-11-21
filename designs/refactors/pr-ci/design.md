# Design

## PR checks

Use one read-only GitHub Actions workflow for PRs targeting main, with a stable job name `PR quality`. Include all paths and draft PRs. A private-repository job condition keeps the runner inactive until public. Never treat a skipped private run as verification. The PR merge candidate is the source tested. Require an up-to-date base once protection is active. The MVP uses the PR trigger, with no duplicate post-merge job or release trigger.

On a fresh standard macOS runner, install the pinned Python and uv, then sync locked development dependencies from app. Use the dependency-setup portion of the existing bootstrap; invoking the whole bootstrap before release would run checks twice. Run the Atlas check and invoke the existing release script or CLI with a new directory under runner temp. Release already runs Pyright, Ruff lint, Ruff format and pytest once, checks TOML against the lock, archives only package inputs, records the commit and SHA-256, installs the wheel with locked dependencies, checks the installed import path and exercises offline workflows. Also invoke the installed console executable from outside the checkout with a copied offline fixture and verify version/source and a known workflow result. Verify the wheel contains the declared entry point and required runtime inputs and excludes checkout-only paths. Report the wheel identity and results in the run log. No retained wheel, persistent cache or published artifact is needed for CI.

Use pull_request with contents read, pinned supported actions, no persisted checkout credentials, no provider keys, and no access to personal examples. Setup may download locked dependencies. Workflow execution uses only deterministic fixtures. Avoid networked runtime checks, service containers, Docker state, modifying user configuration or interacting with existing volumes.

## Main protection

After public activation observe the stable check on a real PR. Apply an active ruleset targeting main, require the PR path with zero human approvals, successful up-to-date `PR quality`, block force pushes and deletion, and select repository admin bypass **For pull requests only**. With zero required approvals there is no stale-approval policy to maintain. Read back the active settings and exercise a red then green test PR. Observe bypass availability without exercising an unauthorized merge. If settings access is unavailable, give Sharon the exact controls and verify readback after his change.

## Local versioning and PR history

Keep bare version read-only and retain the explicit-version tooling input. Extend the checkout-only bump form with minor and major, reusing the pinned uv path and existing version tooling. From 0.2.7, patch gives 0.2.8, minor gives 0.3.0 and major gives 1.0.0. Update project metadata and lock consistently; a failed update must not leave mismatched files. No Git commit, PR, tag, service, upload or implicit build on bump. Build locally from a clean committed revision with the existing release command.

Use root CHANGELOG.md with Unreleased and dated version headings. At a maintainer bump, reconcile the merged PRs between the previous committed version bump and the main revision included in this bump. List each once with number and title, including docs and maintenance PRs. Use the previous version commit and the included main revision as comparison endpoints. Obtain the list from repository history and GitHub merged PRs where necessary; the local bump command itself stays offline. Unreleased entries can be added along the way, with the reconciliation at bump time covering omitted entries. A one-line upgrade note accompanies a breaking change. A version-preparation PR falls in the next interval if its merge follows the recorded cutoff. Never invent pre-baseline release history. Use main’s first 0.2.0 revision, 8895c2dbf6674716656d5b780f8c181a743e44f2 (#54), as the initial lower bound. Its first parent still declares 0.1.4. Through the inspected main revision, the next interval contains #55 and #59. Direct commits are visible in the comparison and are not counted as PRs.

## Scoped amendments for approval

- Root AGENTS.md replaces the current CI exemption with the agreed PR gate while preserving local checks.
- designs/governance/design-contract.md clarifies that Atlas runs in the same required workflow; it needs no separate CI service.
- designs/stages/00-environment/architecture.md and plan.md retain their historical exclusions with dated scope notes. The architecture note also supersedes its stage-based version scheme prospectively.
- designs/project-structure.md records ownership of .github/workflows/ for CI and root CHANGELOG.md for version history. Existing runtime/tooling boundaries stay intact.
- designs/governance/guarded-files.md registers the newly locked package when approved. Update affected navigation, progress and Atlas to reflect evidence at handoff/closeout. Limit public guidance to the affected CLI and checkout workflow.

## Principle assessment

Principles 1, 3, 4, 8, 12 and 15 require pinned approval, implementation review, evidence and accurate status. Principles 2, 7, 10 and 13 govern permissions, deterministic checks, local operation and sandbox exclusion. Principles 9, 11 and 14 preserve scope, historical decisions and public command guidance. Principles 5 and 6 introduce no new integration or configuration contract in this change.
