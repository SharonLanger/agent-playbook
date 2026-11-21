# Pull request CI and local version tracking

[Issue #62](https://github.com/SharonLanger/agent-playbook/issues/62) owns coordination. This is one bounded work package under the [refactor working method](../../governance/stage-milestone-workflow.md). The outcome is a checked PR, a verifiable local wheel, and a short history of merged PRs for each maintainer version.

| Scope and status | Record |
|---|---|
| Boundaries and alignment | [Requirements](requirements.md) and [decisions](decisions.md) |
| Approved behavior | [Design](design.md), [acceptance cases](test-cases.md), [implementation plan](implementation-plan.md) |
| Baseline | main at `46e9062d1fbedefbc04240c280d12001cfdea0ac` |
| Approved revision | [`6ce53c2`](https://github.com/SharonLanger/agent-playbook/tree/6ce53c2377dc21541d94ca8a461bd02d66af7655/designs/refactors/pr-ci), [Sharon’s approval](https://github.com/SharonLanger/agent-playbook/pull/63#issuecomment-7062463938) |
| Implementation and verification | [implementation PR #64](https://github.com/SharonLanger/agent-playbook/pull/64), reviewed code `b4ec345`, report-only head `2d0a381`; [two independent reviews and run evidence](https://github.com/SharonLanger/agent-playbook/blob/2d0a38186ecdedbf365731b1bb5505ad2546d2ca/designs/refactors/pr-ci/reviews/status.md) |
| Originating review | Changes requested on the action versions and PR history interval. Round 3 remains available. |
| Acceptance and merge | Both PRs draft and unmerged. Public macOS verification, main enforcement and final coordinated first run pending. |

The round-02 evidence records 480 passing tests on Linux and the verified 0.2.0 wheel. Both GitHub jobs were skipped while private. The nine files added after the reviewed candidate contain only review records.

**Corrections for #64.**

1. Update the two SHA-pinned Actions to supported Node 24 releases. The reviewed pins declare Node 20. GitHub [retired Node 20 on hosted runners](https://github.blog/changelog/2026-09-23-node-20-is-no-longer-available-in-github-actions/). Private skips cannot demonstrate compatibility.
2. In the CLI guide, define each new PR interval as the previous dated entry’s **included main cutoff (exclusive)** through the new included main cutoff (inclusive). The initial 0.2.0 baseline serves as the first lower bound. Starting from the later version-bump commit can lose PRs merged while that bump was under review. Walk through two successive intervals with an intervening PR and the prior version-preparation PR; both belong exactly once. This is a documentation correction, with no need for a new tracking tool.

Next action is the implementation owner's focused correction and remaining review round. #57 owns service-control CLI design and live acceptance. #61 owns the publication README review. #42 and #60 retain the broader guides. Final first-run acceptance follows the selected merges.
