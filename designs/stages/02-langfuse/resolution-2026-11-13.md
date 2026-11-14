# PR #36 Langfuse review follow-up — 2026-11-13

[Four original findings](review-2026-11-13.md) · [Combined acceptance plan](verification-simplification-plan.md) · [Main reconciliation](main-reconciliation.md)

Historical checkpoint: **Implemented and independently checked on draft PR #36 at the revisions below.** Current local acceptance and the later delivery-readback limitation are recorded in [2026-11-14 acceptance](acceptance-2026-11-14.md). Main `53764abeb9402d596ee26bef19872fc2ebd7d888` was already reconciled under the six approved decisions. This turn refreshed branch `939e4ef671d9803abd1e13ab71b43028562e74d8` by fast-forward, without new conflicts. M4, workflow contexts, real-agent tracing and PR merge are outside this change.

## Findings closed in code

- **R1:** Project preflight now uses the pinned SDK's `LangfuseAPI` with a short-lived HTTP transport, without creating a tracing-disabled resource manager. A same-process loopback fixture receives the real SDK's OTLP POST after successful preflight. Disabled mode remains skipped without a client.
- **R3:** The explicit observation session flushes and uses bounded authenticated trace readback. The playground prints separate mock outcome and delivery state. A rejected OTLP POST with no trace readback reports `unconfirmed` and cannot exit as delivered; a 401/403 readback reports `rejected`. No whole-run retry is introduced. This checks trace visibility, not every observation's durable UI rendering.
- **R4:** Stage architecture/smoke-plan current-status prose and Atlas navigation now distinguish implemented PR code from local acceptance and live verification. Historical proposal and review evidence remains.
- **Operation:** The checkout-only `agent-playbook langfuse` action flags dispatch to one standard-library helper. It preserves Compose's default project identity, pinned images, private `.env` and named volumes. Docker-only direct-script use needs no app environment; project authentication uses the existing checker. Public setup/CLI/connection/troubleshooting guides now describe supported commands.

Placement follows the approved Stage 02 boundaries: Compose and Docker actions remain under tooling/observability; connection and readback remain in the Langfuse adapter; CLI parser, dispatch and source-checkout bridge own public arguments. The observability exploration was consulted for the trace/log distinction and does not authorize event, logging or harness additions. Existing guarded architecture responsibilities, workflow contract and application configuration boundaries are unchanged. The R4 edits are factual status corrections requested in the plan, not changes to the milestone contract.

## Verification and limits

| Gate | Observation |
|---|---|
| Combined maintained gate | PASS on the completed implementation before commit: `app/.venv/bin/python app/tooling/checks.py check` — Pyright 0 errors/warnings, Ruff lint/format PASS, pytest **350 passed**. The release command repeated the 350-test gate at implementation commit `bd48e01d6db7d98d29a798c21c4eb37f57063ff2`; the combined Drive guide is updated to the final tested documentation revision after its gate. |
| Actual SDK | PASS: two real SDK loopback cases, successful same-process preflight/export/readback and HTTP 400 export with unconfirmed readback. Previous review contains the negative controls on the original code. Loopback evidence does not prove real Langfuse persistence. |
| CLI/helper offline | PASS: all six parser dispatches, invalid/help side-effect guards, config/env-file paths with spaces, release rejection, first/repeated start, preserved settings, idempotent stop, ready/non-ready, missing/stopped engine, unhealthy/timeout, redacted logs, follow interruption and browser failure. |
| Requested playground targeted smoke | PASS against an independent local OTLP fixture in three fresh processes: success spans `initialize, add, multiply, finish, mock-wf-02`; add failure spans `initialize, add(ERROR), mock-wf-02(ERROR)`; multiply failure spans `initialize, add, multiply(ERROR), mock-wf-02(ERROR)`. All three sent one POST, exited 0 with `delivery: verified` from fixture readback. The fixture cannot prove the real UI layout. |
| Docker service validation | PASS: Linux Engine **29.9.2** / Compose **2.40.3**, quiet Compose config, stopped status and repeated non-destructive stop on a disposable project. |
| Live six-service stack and actual project/trace/persistence | **BLOCKED:** Linux Docker uses the `vfs` storage driver. The isolated start consumed free disk from 4.4 GiB to 1.2 GiB while only four containers were created. The operation was interrupted before exhaustion; only agent-owned disposable containers and volumes were removed. No project keys/account were created. This is not a Mac result. |
| Mac acceptance | **MANUAL:** Docker Desktop readiness, UI/account/project, project-key check, synthetic trace detail and stop/start persistence await Sharon. |

The loopback smoke's `delivery: verified` is fixture response evidence; it must not be quoted as live server ingestion. The new helper's first-start Linux path was attempted but did not reach health. Private settings for the isolated attempt lived under `/tmp`, separate from the default ignored `.env`; no existing data or configuration was changed. Docker Desktop 4.99.0 / Engine 29.9.3 / Compose 5.7.0 is an upstream candidate awaiting Mac project verification; the official download and release-note URLs returned HTTP 200 on 2026-11-13.

## Release and current local handoff

At implementation commit `bd48e01d6db7d98d29a798c21c4eb37f57063ff2`, `UV_CACHE_DIR=/workspace/.uv-cache .venv/bin/python -m tooling.release` from `app/` passed its repeated 350-test gate, hashed locked dependency installation, 141-package compatibility check, isolated installed built-in/alias/failure/offline verifier and source identity. Wheel SHA-256: `2c835c6c9b6affd77715f6f037b976b76684efa9247a5629fffc710dc5886bd2`. Direct installed `langfuse --status` rejected checkout-only tooling with exit 2. The code is unchanged by the later guide-link documentation commit.

The historical [single combined Drive checklist](https://drive.google.com/file/d/1vxH9napBHThAPX7ELtdTFoO0ONI8jBgE/view?usp=drivesdk) records the earlier Mac exercise. Current credentials and run instructions are in [official application docs](../../../app/docs/langfuse-hands-on.md). The three old milestone guides remain historical and link to it. The final Drive file is pinned to the last gate-tested commit, independent of this document's historical code commit.

