# Local Langfuse: first setup and daily use

Langfuse is an **optional local trace UI**. Docker is needed to run its six local services; ordinary Agent Playbook workflows and a hosted Langfuse endpoint do not require local Docker. Work from the repository root (`agent-playbook`) for all commands below.

## Before the first start on a Mac

- Choose the Docker Desktop download for your Mac processor: **Apple silicon** for M-series chips or **Intel** for an Intel Mac.

- Check Docker's current [macOS support requirements](https://docs.docker.com/desktop/setup/install/mac-install/#system-requirements).

- Install [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/).

- Launch Docker Desktop, accept its permissions and wait for the engine to finish starting.

The Docker command being installed does not mean its engine or socket is ready.

- Allocate at least **8 GiB memory** to Docker Desktop.

- Ensure several GiB of free disk and network access for first-time image downloads.

PostgreSQL, ClickHouse, Redis and MinIO are included as containers; install none separately.

- Check that the Docker engine is available from the repository root.

```sh
docker info
```

- Check that the Compose plugin is available.

```sh
docker compose version
```

Docker Desktop includes the Compose plugin; do not install legacy `docker-compose`.

- Create the required external credentials file using the [configuration guide](configuration.md#general-secrets-file). It may be empty until you configure a project. Keep Langfuse disabled in `app/application.local.yaml` until project keys are ready; the supplied shared YAML enables it.

- Prepare the application CLI from the repository root if it is not already installed.

```sh
python3 app/tooling/bootstrap.py
```

Bootstrap needs Python 3.10+ on the host, network for initial provisioning and sufficient disk for the app environment. The app environment uses Python 3.13 and pinned uv 0.13.6.

| Component | Version/evidence |
|---|---|
| Docker Desktop for Mac | 4.99.0 (released 2026-11-09) is an upstream candidate, **awaiting Mac project verification**; an existing working installation need not change. Its listed bundled Engine is 29.9.3 and Compose is 5.7.0. Record the versions reported on your Mac. |
| Docker Engine / Compose | A working `docker info` and `docker compose` plugin are functional prerequisites. The project-tested Linux versions and final results are recorded in [Stage 02 findings](../../designs/stages/02-langfuse/findings.md); they do not certify Mac. |
| Host Python / app | Management script: Python 3.10+ standard library. App bootstrap: host Python 3.10+; app Python 3.13, uv 0.13.6. |
| Langfuse and stores | Pinned [Compose images and digest](../tooling/observability/compose.yaml): Langfuse web/worker 4.80.0, PostgreSQL 17.7, ClickHouse 26.3.62.3, Redis 7.4.7 and pinned MinIO digest. No floating `latest`. |

## Start and open

- Start the local Langfuse service from the repository root.

```sh
app/.venv/bin/agent-playbook langfuse --start
```

Expect `Langfuse ready. UI: http://localhost:3000` (or your configured port).
First image downloads and database startup can take minutes. `--start` creates
ignored, private `app/tooling/observability/.env` only if missing, applies the
pinned Compose configuration, then waits up to five minutes for six services
and HTTP health.

- Check service status.

```sh
app/.venv/bin/agent-playbook langfuse --status
```

The status should say `ready`.

- Open the local Langfuse UI.

```sh
app/.venv/bin/agent-playbook langfuse --open
```

`--open` prints the URL and opens your default browser.

## Create a local account and project

- Create a local account on the first visit if you do not already have one.

- Create or select the organization for this local instance.

- Create a Langfuse project in that organization the first time you set up this instance.

The project starts with an empty trace list until you run the synthetic example.
Use the same account, organization and project on later starts; you do not need
to create them again. Continue with the [connection guide](langfuse-connection.md)
to configure project keys and run the authentication check.

## UI-only setup before app bootstrap

The management script uses host Python 3.10+, Docker and Compose, but no CrewAI
or Langfuse Python SDK. The project connection `--check` requires the bootstrapped
app environment.

- Start the UI-only stack from the repository root.

```sh
python3 app/tooling/observability/manage.py --start
```

- Check its status.

```sh
python3 app/tooling/observability/manage.py --status
```

- Open its UI.

```sh
python3 app/tooling/observability/manage.py --open
```

## Everyday commands

### View logs

- View recent service logs from the repository root.

```sh
app/.venv/bin/agent-playbook langfuse --logs
```

### Follow logs

- Follow service logs in a separate terminal.

```sh
app/.venv/bin/agent-playbook langfuse --logs --follow
```

Press Ctrl-C in that terminal to end log streaming; the containers keep running.

### Stop

- Stop the local stack.

```sh
app/.venv/bin/agent-playbook langfuse --stop
```

### Restart

- Start the local stack again.

```sh
app/.venv/bin/agent-playbook langfuse --start
```

`--stop` removes this stack's containers but retains the `.env` and named data
volumes. Repeated starts, an already-stopped stop, and start after stop are safe.
Docker Desktop and unrelated containers stay untouched. Keep service logs private.

## Private service settings

The deployment file is [compose.yaml](../tooling/observability/compose.yaml);
[setup.py](../tooling/observability/setup.py) generates Docker service secrets once.

- Change the local UI port by editing `LANGFUSE_PORT` in the ignored Docker `.env`.

Its default is 3000.

- Change the MinIO port by editing `MINIO_PORT` in the ignored Docker `.env`.

Its default is 9090. An older `.env` without `MINIO_PORT` also defaults to 9090.

- Apply Docker `.env` port changes by starting the local stack.

```sh
app/.venv/bin/agent-playbook langfuse --start
```

Shell environment variables override Docker `.env` values. Remove stale overrides
if a URL or port differs unexpectedly.

Use `--env-file /absolute/path/to/private.env` on **every local action** to select
a separately prepared Docker service file. A first `--start --env-file PATH`
creates the file if its parent directory exists. Keep the file and project
directory stable: Compose's project identity is `observability`, so its five
named volumes stay associated with the same data. The UI and MinIO bind to
loopback. This is a local learning deployment, not a backup or production setup.

Project API keys used by [connection checking](langfuse-connection.md) belong
in the external `~/.config/agent-playbook/secrets.env` file selected by the general `secrets.file` setting in `app/application.yaml`. They are separate from Docker's `.env` deployment
secrets. Follow the connection guide to configure YAML and run
`agent-playbook langfuse --check` before using the [Langfuse hands-on guide](langfuse-hands-on.md).
The check can address a hosted endpoint without local Docker. Workflows remain
uninstrumented; the playground explicitly creates synthetic traces.

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
