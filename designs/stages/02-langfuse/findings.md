# Milestone 1 findings

Status: **Implemented on PR #36; awaiting Sharon's acceptance.** Sharon authorized the local UI milestone only. M2–M4 remain unimplemented. The tested implementation revision is `56b70792ac2b0a62834090a3c19c7bc1b971ef8f` on `docs/stage-02-langfuse-setup`, based on `a58bd88`. This evidence-only follow-up changes no deployment files.

## Decision and placement

The charter selects Langfuse; principles require external secrets, local-first operation, evidence and incremental scope. The target architecture separates observation from scheduling. The guarded project structure places checkout-only deployment in `app/tooling/`. `observability/compose.yaml` owns the local stack; `setup.py` creates ignored credentials once. Inputs are local `.env` settings; outputs are a loopback UI and named persistent volumes. Langfuse and its storage services own startup failures. The observability exploration informed the sequence but does not authorize broader event/log proposals. No guarded meaning or ownership boundary changed. Official setup instructions are in `app/docs/langfuse-local.md`; Atlas and progress distinguish this pending PR from accepted work.

## Verification, 2026-11-13

Environment: managed Linux x86_64; Docker Engine 29.9.2; Compose 2.40.3; 17 GiB RAM, 30 GiB free disk. Reference: upstream `langfuse/langfuse` tag `v4.80.0` `docker-compose.yml`. Images: Langfuse web/worker 4.80.0, PostgreSQL 17.7, ClickHouse 26.3.62.3, Redis 7.4.7, MinIO `sha256:96b6cf3e14084d3427ec46de10c2873af61b945ad9272eec266cfc8df551cba5`.

Checks used a copied Compose file, disposable generated credentials, project `agent_playbook_m1_verify`, port 33000 and isolated named volumes. No Sharon-owned service or volume was touched.

| Check | Result | Observation or limit |
|---|---|---|
| `python3 app/tooling/observability/setup.py` in isolated copy | PASS | Private `.env` created; existing file was not replaced. |
| `docker compose --env-file /tmp/langfuse-m1-check/.env -f /tmp/langfuse-m1-check/compose.yaml -p agent_playbook_m1_verify config --quiet` | PASS | Resolved structure inspected without displaying secrets: six pinned services, loopback ports and five named volumes. |
| `docker compose --env-file /tmp/langfuse-m1-check/.env -f /tmp/langfuse-m1-check/compose.yaml -p agent_playbook_m1_verify up -d --quiet-pull` | PASS after fix | First run exposed missing explicit single-node ClickHouse settings and a web migration failure. Adding `CLICKHOUSE_CLUSTER_ENABLED=false` and `CLICKHOUSE_CLUSTER_NAME=default` allowed startup. |
| `curl --noproxy '*' http://127.0.0.1:33000/api/public/health` | PASS | HTTP 200; `{"status":"OK","version":"4.80.0"}`. |
| `curl --noproxy '*' -L http://127.0.0.1:33000/` | PASS | HTTP 200, HTML with Langfuse marker. Page response alone does not verify browser login. |
| Normal `down`, then `up -d`, then health request | PASS | Containers restarted with the same named volumes; health again returned `{"status":"OK","version":"4.80.0"}`. This does not prove application-record persistence. |
| `python3 designs/atlas/build.py --check`, changed Markdown links/fences, `git diff --check` | PASS | Atlas references, hierarchy, guards, sandbox boundary and freshness passed; local links and fences passed. |
| `XDG_DATA_HOME=/tmp/agent-playbook-xdg app/.venv/bin/python app/tooling/checks.py check` | PASS | Pyright 0 errors, Ruff lint and format pass, pytest 119 passed. The default sandbox blocked CrewAI's home-directory write during collection; the same gate passed with approved filesystem access. |
| Account/project creation and persistence | NOT RUN | Sharon's short UI acceptance exercise. Authentication and trace ingestion are unverified. |

Normal stop from the repository root is `docker compose --env-file app/tooling/observability/.env -f app/tooling/observability/compose.yaml down`; `down -v` deletes data and is not the normal operation. Linux verification cannot establish Mac Docker Desktop resource allocation or browser behavior.

## Setup usability review — documentation follow-up

Reviewed PR head `74c3f11` after Sharon requested easier Docker operation,
configurability and removal. The public guide now uses the deployment folder's
short Compose commands and explains installation prerequisites, files, start,
stop, restart versus configuration changes, data location and removal boundaries.
No custom Dockerfile is needed because every service uses a prebuilt image.
The stage README's stale documentation-only status is corrected.

Static review confirms the deployment's isolation from application code in the
PR diff and the one-time setup's exclusive-create behavior. Configurability is
not complete: the MinIO host port is hard-coded to 9090. The implementation brief
records the specific remaining change and lifecycle checks for Codex; this
follow-up deliberately changes documentation only, preserving Sharon's division
between design/review and the implementing agent.

Governance/impact: this follows the existing tooling/docs ownership and principles
2, 5, 6, 8, 10 and 14; no guarded contract, component boundary or runtime code is
changed. Existing earlier principle assessment still applies. Public documentation
is updated in place; Atlas generated fingerprints must be refreshed for changed
sources, without promoting pending implementation to accepted Current. Progress's
M1 pending-acceptance status remains accurate, so no separate progress edit is
needed. The architecture proposal's M2–M4 boundaries are unchanged.

Verification for this documentation follow-up: local isolated setup executed twice
with bytes/permissions checked; 22 relative Markdown links, code fences and whitespace checks passed; Atlas
build and `--check` passed. No application code changed, so the application
quality gate was not rerun for this documentation-only update. Docker commands could not be
rerun here: `docker compose version` and `docker info` both fail with
`docker: command not found`. Earlier Linux runtime evidence above is retained as
prior-agent evidence, not claimed as a new live test. Mac startup and actual
project persistence remain local acceptance checks.

## M1 configurable storage port follow-up — 2026-11-13

Tested implementation commit: `9743c3103d892dce8cd5a5fb26a9cffadabcad83`.

The separate M1 checkpoint `fad8a4f119cab5316529b3ad9239d01b8347368c`
remains reachable for Sharon's original exercise. This follow-up adds
`MINIO_PORT`, default 9090, to generated private settings, the host binding and
the web media URL. Existing `.env` files without it retain port 9090; repeated
setup does not overwrite them. Internal MinIO URLs stay on the Compose network.

On managed Linux x86_64, Docker Engine 29.9.2 / Compose 2.40.3, an isolated
`agent_playbook_port_verify` project passed first and repeated setup (unchanged
file hash, mode 600), quiet Compose validation, resolved loopback ports 33010
and 33011, media endpoint 33011, and backward-compatible 9090 resolution for
an old `.env`. It started with six services and returned Langfuse 4.80.0 health
HTTP 200. Repeated `up -d`, `restart` and normal `down`/`up -d` commands
completed with isolated named volumes retained.

Applying changed ports 33012/33013 via `up -d` is **BLOCKED** here: the Docker
daemon uses `vfs`, and recreating the web/worker images filled its 32 GiB
filesystem (`no space left on device` while copying image files). A later start
after `down` met the same limit. The isolated project and volumes were removed.
The changed-port resolved configuration passed, but live readiness after that
change is unverified. Mac architecture support and Docker Desktop behavior are
also unverified. Sharon's original M1 acceptance remains pending.

The existing application gate passed Pyright (0 errors), Ruff lint and format.
Pytest initially had 26 errors while Docker filled the filesystem; after removing
the disposable stack, `XDG_DATA_HOME=/tmp/agent-playbook-xdg app/.venv/bin/python
-m pytest -xq app/tests` passed 119 tests. No Docker service was needed by those
tests. The follow-up changes no Python dependency or workflow behavior.

## M2 project connection — 2026-11-13

Tested implementation commit: `2278ee9c5742d78076f56fb64116abbadc01111b`.

Sharon authorized M2 while M1 Mac acceptance remains pending. The guarded
charter, architecture, principles and project structure require local-first
configuration, isolated provider details and evidence. The observability
exploration informed the sequence; its event/harness proposals were not adopted.
The existing `config/` loader owns YAML/local/environment precedence and private
key references; `observability/adapters/langfuse/connection.py` owns the SDK,
bounded read-only project request and cleanup; checkout-only
`tooling/observability/check_connection.py` owns exit codes and safe output.
Inputs are application settings and project keys; output is a small status.
No runner, workflow/context or guarded meaning changed.

Langfuse Python SDK 5.2.0 and its directly used HTTPX transport 0.28.1 are
pinned in `pyproject.toml` and `uv.lock` for the previously pinned server 4.80.0.
Wheel metadata includes both exact requirements. M1's Docker commands need no Python
install. Official instructions are in `app/docs/langfuse-connection.md`;
older YAML without Langfuse stays disabled.

M2 verification on managed Linux x86_64, Python 3.13.5:

| Check | Result | Observation or limit |
|---|---|---|
| `uv lock --directory app --check`, `uv build --directory app --out-dir /tmp/m2-dist` | PASS | 150 locked packages; wheel built with exact Langfuse SDK dependency. |
| Focused `pytest` in `app/tests/observability/test_langfuse_connection.py` | PASS | Old YAML, precedence, malformed/missing references, private errors, disabled/no-client behavior, auth/network/other results, cleanup, timeout/no instrumentation and checker exit codes. |
| Explicit checker disabled, missing-key and unreachable endpoint invocations | PASS | Exit codes 3, 2 and 1 with sanitized output; no trace write call. |
| Full `app/.venv/bin/python app/tooling/checks.py check` | PASS | Pyright 0 errors; Ruff lint/format pass; pytest 132 passed. |
| Valid/rejected keys against real Langfuse project | BLOCKED | Docker `vfs` exhausted the managed 32 GiB filesystem while recreating the isolated stack. No personal credentials or volumes were used. Live authentication and absence of live traces remain unverified. |

The checker performs only SDK project GET and sets tracing disabled. This and
offline tests support intended no-write behavior, not a live ingestion proof.
Sharon's M2 acceptance is to supply project keys and run the checker once after
his M1 account/project creation. M2 is implemented but not accepted.

## M3 editable mock playground — 2026-11-13

Sharon authorized creating and manually running only the new
`app/examples/langfuse/` personal playground. The existing adapter boundary
owns Langfuse span creation and cleanup; the personal script owns arithmetic
inputs, intentional failure choice and user-facing output. Inputs are external
M2 settings and editable mock numbers; output is a new trace ID/link plus small
synthetic observations. The observability exploration and stage smoke plan
informed nesting and error behavior. No workflow/context, real CrewAI execution,
global instrumentation or guarded meaning changed. Official navigation links
the personal README; maintained tests use independent fixtures.

M3 verification on managed Linux x86_64, Python 3.13.5, SDK 5.2.0:

| Check | Result | Observation or limit |
|---|---|---|
| `app/.venv/bin/python -m pytest -q app/tests/observability/test_langfuse_connection.py app/tests/observability/test_langfuse_observations.py` | PASS | 14 independent tests; adapter root/child calls, error level, trace identity, flush and shutdown. No test accesses examples. |
| Explicit Ruff lint/format on the new `app/examples/langfuse/run.py` | PASS | Personal script checked once for initial delivery; excluded from the normal gate. |
| Direct disabled `app/.venv/bin/python app/examples/langfuse/run.py` | PASS | Exited 1 with skipped-connection message; emitted no observation. |
| Targeted manual script smoke, success/add failure/multiply failure, using an in-memory session substitute | PASS | Default result 20 and all four steps; add failure stopped before multiply/finish; multiply failure stopped before finish; failed root/step, distinct IDs, printed matching links, flush/close. This is an offline code-path check, not Langfuse ingestion. |
| Live observation readback, hierarchy, values and links | BLOCKED | Managed Docker `vfs` disk exhaustion prevented recreating an isolated server/project. No claim of persisted ingestion or browser display. |
| Full `app/.venv/bin/python app/tooling/checks.py check` | PASS | Pyright 0 errors; Ruff lint/format pass; pytest 133 passed. Normal gate excludes personal examples and needs no Docker. |
| `python3 designs/atlas/build.py --check`, changed Markdown links/fences and `git diff --check` | PASS | Atlas hierarchy/references/guards/freshness and documentation checks passed. |
| `uv build --directory app --out-dir /tmp/m3-dist` and wheel inspection | PASS | New runtime observation module is packaged; personal examples are excluded. |

Sharon's M3 acceptance is to run the script with his local project keys, open
the printed trace, edit inputs, try add/multiply failures and confirm prior
traces survive a normal service restart. M3 is implemented but not accepted.
