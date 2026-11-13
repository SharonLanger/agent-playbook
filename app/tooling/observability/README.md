# Langfuse local deployment

This checkout-only deployment implements Stage 02 milestone 1. Follow the
[official setup and troubleshooting guide](../../docs/langfuse-local.md).

The Compose services follow the required web, worker, PostgreSQL, ClickHouse,
Redis and MinIO topology in [upstream Langfuse v4.80.0 Compose](https://github.com/langfuse/langfuse/blob/v4.80.0/docker-compose.yml).
The optional AI gateway, service debug ports and remote exposure are omitted.
Images are pinned in `compose.yaml`; `.env` is generated once and ignored.

The explicitly invoked [project connection check](../../docs/langfuse-connection.md)
belongs here. It uses installed application configuration and Langfuse SDK 5.2.0;
the Docker-only M1 commands do not require a Python dependency installation.
