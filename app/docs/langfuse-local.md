# Local Langfuse

This guide starts a self-hosted Langfuse UI on your machine. Milestone 1 does
not connect Agent Playbook or send traces; the trace list will be empty.

## First setup on a Mac

1. Install and start [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/), choosing the download for your Mac's processor. It includes Docker Compose. Allow at least 8 GiB of memory for the stack.
2. Check that Docker is running and Python 3 is available:

```sh
docker info
docker compose version
python3 --version
```

3. From the repository root, enter the deployment folder and initialize it:

```sh
cd app/tooling/observability
python3 setup.py
docker compose config --quiet
docker compose up -d
```

All commands below run **inside `app/tooling/observability`**. In a new terminal,
enter that folder again. Compose reads its `compose.yaml` and `.env` automatically.

Setup creates private, Git-ignored credentials once. Running it again leaves the
existing `.env` unchanged. Keep that file: replacing database credentials or
Langfuse encryption settings can prevent access to existing data.

The first start downloads prebuilt images and initializes the databases; allow
several minutes. No custom Dockerfile, image build or local database installation
is required. Langfuse runs as six services, managed together by Compose.

## Open the UI

Check service state and HTTP readiness:

```sh
docker compose ps
curl --fail --silent --show-error http://localhost:3000/api/public/health
```

Retry the health request for up to five minutes during first startup. Then open
<http://localhost:3000>, create your account/project and open its empty trace list.
If you configured a different UI port, use that port in both URLs.

The health endpoint checks service readiness. It does not prove successful login,
project persistence or trace ingestion. Confirm your project survives a normal
stop/start in the UI.

## Everyday commands

| What you want | Command |
|---|---|
| Start for the first time or run again | `docker compose up -d` |
| Stop and remove containers, keeping stored data | `docker compose down` |
| Restart existing containers with their current settings | `docker compose restart` |
| Apply an edited configuration | `docker compose up -d` |
| Check service status | `docker compose ps` |
| Read recent UI service logs | `docker compose logs --tail=80 langfuse-web` |
| Validate configuration without printing secrets | `docker compose config --quiet` |

`restart` does not apply changed environment settings; use `up -d` after edits.
Restarting or recreating containers does not reset the database. Never use
`down -v` for an ordinary stop: it deletes persistent volumes.

## Files and configuration

| File | Purpose |
|---|---|
| [compose.yaml](../tooling/observability/compose.yaml) | Pinned service images, network ports, health checks and persistent volumes |
| [setup.py](../tooling/observability/setup.py) | One-time generation of local credentials |
| [.env.example](../tooling/observability/.env.example) | Settings reference; generated `.env` holds your private values |

Edit `LANGFUSE_PORT` in `.env` to change the UI port, then run `docker compose
up -d`. Do not rotate the generated secrets merely to change a port. The current
MinIO browser-access port is fixed at **9090** in Compose; it has no `.env`
setting yet. Image versions are pinned in Compose, not automatically upgraded.

For a separately prepared private settings file, Compose supports
`docker compose --env-file /absolute/path/to/private.env up -d`; use the same
file for every lifecycle command. Setup currently creates only the adjacent
`.env`. Shell variables can override file values, so remove stale overrides when
troubleshooting unexpected settings.

Keep the Compose project identity stable. By default it comes from this folder's
name (`observability`); changing it selects a different set of volumes and can
make the UI appear empty. A separate instance needs its own project name, free
ports and private settings. Do not change identity to repair an existing instance.

## Data and independence from Agent Playbook

Docker-managed named volumes store PostgreSQL, ClickHouse, Redis and MinIO data
(and ClickHouse logs). The browser UI is not the data store. On Docker Desktop,
these volumes live in Docker's managed Linux environment, not in this checkout.
Preserving volumes is not a backup.

The deployment lives entirely under `app/tooling/observability/`. Milestone 1
adds no SDK dependency, workflow import or startup hook to Agent Playbook.
You can run the application while this stack is stopped. To stop using local
Langfuse, run `docker compose down` and keep `.env` and volumes if you want to
return later. Removing the checkout does not itself remove Docker volumes; stop
its containers first and retain the configuration needed to reopen the data.

Connecting the application, selecting a remote endpoint and switching to
Langfuse Cloud belong to later integration milestones. They are not supported
application configuration in milestone 1. Moving historical data is a separate
operation from changing a future endpoint.

## Troubleshooting

- Cannot connect to Docker: start Docker Desktop and wait until `docker info` succeeds.
- Port already allocated: choose a free UI port in `.env`; for the currently fixed port 9090, stop the conflicting service before starting this stack.
- Startup stays unhealthy: inspect `docker compose ps` and the failed service's logs, for example `docker compose logs --tail=80 clickhouse`. Check Docker's allocated memory and free disk space.
- UI looks empty after moving the deployment: check the project identity and retained volumes before creating new data or resetting anything.
- Keep logs private; do not share credentials or full resolved Compose output.

This setup is for local learning. The UI and MinIO API bind only to loopback;
this guide does not configure internet access or production backups.
[Image versions and upstream reference](../tooling/observability/README.md).
[Docker environment settings](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/)
and [restart behavior](https://docs.docker.com/reference/cli/docker/compose/restart/).
