# Local Langfuse UI

Milestone 1 runs a self-hosted Langfuse UI. It does not connect Agent Playbook to
Langfuse or send traces. The expected trace list is empty.

From the repository root, with Docker Engine and Docker Compose installed:

```sh
python3 app/tooling/observability/setup.py
docker compose --env-file app/tooling/observability/.env -f app/tooling/observability/compose.yaml up -d
```

Setup creates a private, Git-ignored `.env` once. It leaves an existing file
unchanged. Keep it: changing these credentials after data has been created can
prevent services from reopening their stored data. The first image download and
database migration can take several minutes. Allow at least 8 GiB of memory.

Wait for readiness, then open <http://localhost:3000>:

```sh
curl --fail --silent --show-error http://localhost:3000/api/public/health
```

If the request fails during initial startup, retry for up to five minutes.
Create your account and project in the UI and open its empty trace list. The
health request establishes HTTP service readiness only; it does not verify
login, project persistence or trace ingestion. These remain your UI checks.

Stop safely without deleting data:

```sh
docker compose --env-file app/tooling/observability/.env -f app/tooling/observability/compose.yaml down
```

Repeat `up -d` to restart. The named PostgreSQL, ClickHouse, Redis and MinIO
volumes survive `down`. Verify the project still appears after restarting.
Never use `down -v` for a normal stop; it deletes the stored data. To use a
different UI port, edit `LANGFUSE_PORT` in `.env` before startup. Ensure the
chosen port is free. The stack publishes the UI and MinIO API on loopback only.

## Troubleshooting

- `docker compose version` and `docker info` check Docker availability.
- `docker compose --env-file app/tooling/observability/.env -f app/tooling/observability/compose.yaml ps` shows service state. A failed database or storage health check prevents the UI from starting.
- `docker compose --env-file app/tooling/observability/.env -f app/tooling/observability/compose.yaml logs --tail=80 langfuse-web` shows startup failures. Treat logs as private: do not paste credentials or full resolved Compose output into reports.
- If port 3000 or 9090 is already used, stop the conflicting local service. Port 3000 can also be changed in `.env`; MinIO uses 9090 for browser media access.

The deployment is for local learning, not internet exposure or production
backup/availability. Its pinned images and upstream reference are documented in
the [tooling directory](../tooling/observability/README.md).
