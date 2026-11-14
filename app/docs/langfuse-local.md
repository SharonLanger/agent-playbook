# Local Langfuse: first setup and daily use

Langfuse is an **optional local trace UI**. Docker is needed to run its six local services; ordinary Agent Playbook workflows and a hosted Langfuse endpoint do not require local Docker. Work from the repository root (`agent-playbook`) for all commands below.

## Before the first start on a Mac

1. Download [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/). Choose **Apple silicon** for M-series chips or **Intel** for an Intel Mac. Check Docker's current [macOS support requirements](https://docs.docker.com/desktop/setup/install/mac-install/#system-requirements) for your machine. Install it, launch Docker Desktop once, accept its permissions, and wait for the engine to finish starting. The Docker command being installed does not mean its engine or socket is ready.
2. Allow **at least 8 GiB memory** for the stack, several GiB of free disk, and network access for first-time image downloads. PostgreSQL, ClickHouse, Redis and MinIO are included as containers; install none separately.
3. Check `docker info` and `docker compose version`. Both must succeed. Docker Desktop includes the Compose plugin; do not install legacy `docker-compose`.
4. In the repository root, run `python3 app/tooling/bootstrap.py` to prepare the application CLI. This needs Python 3.10+ on the host, network for initial provisioning and sufficient disk for the app environment. The app environment uses Python 3.13 and pinned uv 0.13.6.

| Component | Version/evidence |
|---|---|
| Docker Desktop for Mac | 4.99.0 (released 2026-11-09) is an upstream candidate, **awaiting Mac project verification**; an existing working installation need not change. Its listed bundled Engine is 29.9.3 and Compose is 5.7.0. Record the versions reported on your Mac. |
| Docker Engine / Compose | A working `docker info` and `docker compose` plugin are functional prerequisites. The project-tested Linux versions and final results are recorded in [Stage 02 findings](../../designs/stages/02-langfuse/findings.md); they do not certify Mac. |
| Host Python / app | Management script: Python 3.10+ standard library. App bootstrap: host Python 3.10+; app Python 3.13, uv 0.13.6. |
| Langfuse and stores | Pinned [Compose images and digest](../tooling/observability/compose.yaml): Langfuse web/worker 4.80.0, PostgreSQL 17.7, ClickHouse 26.3.62.3, Redis 7.4.7 and pinned MinIO digest. No floating `latest`. |

## Start and open

From the repository root:

```sh
app/.venv/bin/agent-playbook langfuse --start
app/.venv/bin/agent-playbook langfuse --status
app/.venv/bin/agent-playbook langfuse --open
```

`--start` creates ignored, private `app/tooling/observability/.env` only if missing, applies the pinned Compose configuration, then waits up to five minutes for six services and HTTP health. Expect `Langfuse ready. UI: http://localhost:3000` (or your configured port). First download and database startup can take minutes. `--status` should say `ready`. `--open` prints the URL and opens your default browser. Create a local account and project if this is a new installation; on an existing M1 stack, sign in to the same account/project. A new project has an empty trace list.

For **UI-only setup before app bootstrap**, use the same implementation directly:

```sh
python3 app/tooling/observability/manage.py --start
python3 app/tooling/observability/manage.py --status
python3 app/tooling/observability/manage.py --open
```

This fallback needs host Python 3.10+, Docker and Compose, but no CrewAI or Langfuse Python SDK. The project connection `--check` requires the bootstrapped app environment.

## Everyday commands and private settings

```sh
app/.venv/bin/agent-playbook langfuse --logs
app/.venv/bin/agent-playbook langfuse --logs --follow
app/.venv/bin/agent-playbook langfuse --stop
app/.venv/bin/agent-playbook langfuse --start
```

`--logs` shows the recent Docker service log tail; Ctrl-C ends `--follow` without stopping containers. `--stop` removes this stack's containers but retains the `.env` and named data volumes. Repeated `--start`, an already-stopped `--stop`, and start after stop are safe. Docker Desktop and unrelated containers stay untouched. Do not rotate `.env` secrets or delete the volumes to troubleshoot. Keep service logs private.

The deployment file is [compose.yaml](../tooling/observability/compose.yaml); [setup.py](../tooling/observability/setup.py) generates secrets once. Edit `LANGFUSE_PORT` (default 3000) and `MINIO_PORT` (default 9090) in the ignored `.env` to change loopback ports, then run `--start` to apply. An older `.env` without `MINIO_PORT` still defaults to 9090. Shell environment variables override file values; remove stale overrides if the URL or port differs unexpectedly. Use `--env-file /absolute/path/to/private.env` on **every local action** for a separately prepared private file. A first `--start --env-file PATH` creates it if its parent directory exists. Keep the file and project directory stable: Compose's project identity is `observability`, so its five named volumes remain associated with the same data. The UI and MinIO bind to loopback. This is a local learning deployment, not a backup or production setup.

The project API keys used by [connection checking](langfuse-connection.md) belong in the external `~/.config/agent-playbook/secrets.env` file selected with `AGENT_PLAYBOOK_SECRETS_FILE`. They are separate from Docker's `.env` deployment secrets. Follow the connection guide to configure the selector and run `agent-playbook langfuse --check` before using the [Langfuse hands-on guide](langfuse-hands-on.md). `--check` can address a hosted endpoint without local Docker. Workflows remain uninstrumented; the playground explicitly creates synthetic traces.

## Troubleshooting

| Symptom | Try this |
|---|---|
| `docker: command not found` or no Compose plugin | Install Docker Desktop for your Mac processor, launch it once, then reopen the terminal. Check `docker compose version`. |
| Docker socket/engine unavailable | Open Docker Desktop and wait for its engine indicator; finish first-launch permissions. Run `docker info`, then retry `--start`. |
| First start times out or download fails | Check network and free disk space; run `--status` and `--logs`, then retry `--start`. Existing settings/data are retained. |
| Port already allocated | Choose free `LANGFUSE_PORT` and `MINIO_PORT` in the private `.env`, then run `--start`. Keep old secrets unchanged. |
| Service unhealthy or UI not ready | Run `--status` and `--logs`; check Docker's memory allocation (at least 8 GiB) and disk. Do not delete volumes. |
| UI appears empty after an earlier successful install | Check that the same `.env`, `--env-file` selection, Docker context and `observability` project/volumes are in use before making a new project. |
| Browser does not open | Copy the URL printed by `--open` into your browser. `--open` does not start services. |

See [Docker's official installation guide](https://docs.docker.com/desktop/setup/install/mac-install/), [Docker Desktop release notes](https://docs.docker.com/desktop/release-notes/#4990), and [Langfuse's Compose guide](https://langfuse.com/self-hosting/deployment/docker-compose).
