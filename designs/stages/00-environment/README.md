# Stage 00 — Development environment

Stage 00 established the reproducible Python environment, application CLI, local quality checks, isolated Wheel release and shared PyCharm tasks. Sharon accepted the stage after the IDE tasks were delivered in [PR #26](https://github.com/SharonLanger/agent-playbook/pull/26). The [repository progress record](../../progress.md#current-status-after-the-pr-36-merge) records the acceptance and merge.

## Canonical milestone index

The recorded substages retain their original IDs, shown as `0.1`–`0.7` in the [approved stage plan](plan.md#substages). The stage-wide design is recorded in [PR #15](https://github.com/SharonLanger/agent-playbook/pull/15) and the [guarded architecture](architecture.md). The stage predates per-milestone design, test and plan pins.

| Substage and outcome | Design and approval | Implementation PR | Verification evidence | Acceptance | Merge |
|---|---|---|---|---|---|
| 00.1 — Python environment and runnable main | [Stage plan](plan.md#01--python-environment-and-runnable-main) | [#17](https://github.com/SharonLanger/agent-playbook/pull/17) | [Bootstrap and run findings](findings.md#2026-11-11-stage-001-bootstrap-and-runnable-main) | Sharon ran main and approved continuation | Merged |
| 00.2 — Application CLI | [Stage plan](plan.md#02--application-cli) | [#18](https://github.com/SharonLanger/agent-playbook/pull/18) | [CLI checks](findings.md#2026-11-11-stage-001-acceptance-and-stage-002-cli) | Sharon ran help and run | Merged |
| 00.3 — Pyright strict typing | [Stage plan](plan.md#03--pyright-strict-typing) | [#19](https://github.com/SharonLanger/agent-playbook/pull/19) | [Typing checks](findings.md#003--pyright-strict-2026-11-11) | Sharon observed a type error in PyCharm | Merged |
| 00.4 — pytest | [Stage plan](plan.md#04--pytest) | [#20](https://github.com/SharonLanger/agent-playbook/pull/20) | [Test checks](findings.md#004--pytest-2026-11-11) | Sharon reported four passing tests in PyCharm | Merged |
| 00.5 — Ruff | [Stage plan](plan.md#05--ruff) | [#21](https://github.com/SharonLanger/agent-playbook/pull/21) | [Lint and format checks](findings.md#005--ruff-2026-11-11) | Included in accepted Stage 00 | Merged |
| 00.6 — Unified quality gate | [Stage plan](plan.md#06--unified-quality-gate) | [#22](https://github.com/SharonLanger/agent-playbook/pull/22) | [Unified gate and output checks](findings.md#006--unified-gate-2026-11-11) | Sharon accepted the improved check output | Merged |
| 00.7 — Versioned Wheel release | [Stage plan](plan.md#07--versioned-wheel-release) | [#23](https://github.com/SharonLanger/agent-playbook/pull/23) | [Isolated-release checks](findings.md#007--versioned-wheel-release-2026-11-11) | Sharon built a release and accepted 00.7 | Merged |

The [retained progress checkpoints](../../progress.md#langfuse-branch-detail-earlier-integration-checkpoint) record each substage's merge and Sharon's observed results.

## Next action

Stage 00 is closed. For a tooling refresher, follow the [Python environment lesson](learning/00-1-python-environment.md) through [the Wheel release lesson](learning/00-7-wheel-release.md), then see [Stage 01](../01-crewai-flows/README.md) for the first workflows.

The historical architecture and plan retain their original status headings. The [progress record](../../progress.md#architecture-documentation) records their later approval and the outstanding historical discrepancy between the CrewAI import acceptance item and the Stage 00 scope exclusion.
