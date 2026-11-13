# Milestone 1 findings

Status: **Implemented on PR #36; awaiting Sharon's acceptance.** Sharon authorized the local UI milestone only. M2–M4 remain unimplemented. These checks apply to the M1 commit on `docs/stage-02-langfuse-setup`, based on `a58bd88`.

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
