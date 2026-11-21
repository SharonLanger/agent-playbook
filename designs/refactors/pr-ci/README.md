# Pull request CI and local version tracking

[Issue #62](https://github.com/SharonLanger/agent-playbook/issues/62) owns coordination. This is one bounded work package under the [refactor working method](../../governance/stage-milestone-workflow.md). The outcome is a checked PR, a verifiable local wheel, and a short history of merged PRs for each maintainer version.

| Scope and status | Record |
|---|---|
| Boundaries and alignment | [Requirements](requirements.md) and [decisions](decisions.md) |
| Approved behavior | [Design](design.md), [acceptance cases](test-cases.md), [implementation plan](implementation-plan.md) |
| Baseline | main at `46e9062d1fbedefbc04240c280d12001cfdea0ac` |
| Approved revision | [`6ce53c2`](https://github.com/SharonLanger/agent-playbook/tree/6ce53c2377dc21541d94ca8a461bd02d66af7655/designs/refactors/pr-ci), [Sharon’s approval](https://github.com/SharonLanger/agent-playbook/pull/63#issuecomment-7062463938) |
| Implementation and verification | [PR #64](https://github.com/SharonLanger/agent-playbook/pull/64), reviewed code `ba9a18a226a76ffd7a704b747dbe517b8731fe74`, published head `0871a1537df087804e2b332e8f5df97925d131ba`. The five later files are review reports. [Round 3 evidence](https://github.com/SharonLanger/agent-playbook/blob/0871a1537df087804e2b332e8f5df97925d131ba/designs/refactors/pr-ci/reviews/status.md) |
| Originating final review | PASS on the third reviewed candidate. All three requested corrections are closed. |
| Acceptance and merge | Sharon accepted #64 and it merged to main at [`19e4f22`](https://github.com/SharonLanger/agent-playbook/commit/19e4f22de6ac637a9487db8129bc8dad56c52f6d). Sharon authorized design PR #63 closeout on 2026-11-21. Public activation and final coordinated first-run evidence remain with [issue #62](https://github.com/SharonLanger/agent-playbook/issues/62). |

### Final review on 2026-11-21

The [round 2 requests](https://github.com/SharonLanger/agent-playbook/pull/64#issuecomment-7062822599) concerned ambient integration settings, retired action runtimes and omitted PRs between version cutoffs. The originating session inspected the five-file correction and both independent verdicts, verified the two exact Node 24 action manifests, and reran the effective configuration and 12-child-environment checks with synthetic overrides. The version guide now uses consecutive included-main cutoffs, with a worked example covering a preparation PR merged after the first cutoff.

The implementation team recorded 483 passing tests on Linux, clean Pyright and Ruff results, Atlas freshness and a clean installation of the 0.2.0 wheel. Wheel SHA-256 was `841e44af89c1c7de5645159a170612b4dc16ba51651d1ab0d5da1bc30d186b68`. The originating session used the team's evidence for the full suite and wheel build.

The coder reported a manual bare Pyright invocation from the repository root that traversed the excluded personal examples and failed. The coder reported no modifications there. The committed workflow runs the release gate from app; its Pyright configuration includes only src, tooling and tests. The incident is retained in the implementation evidence.

GitHub skipped the [candidate job](https://github.com/SharonLanger/agent-playbook/actions/runs/44906356179) and the [published-head job](https://github.com/SharonLanger/agent-playbook/actions/runs/44906501919) while private. Main reported unprotected at this review. After public activation, observe code and docs-only PR runs, configure and read back the agreed PR-only admin bypass and required check, and demonstrate blocked and eligible ordinary merges. Repeat fresh installation and first run against the final coordinated candidate after the selected merges. The next actual maintainer bump will exercise the changelog interval. #62 tracks these outstanding items; #57 owns service acceptance.
