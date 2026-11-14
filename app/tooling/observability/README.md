# Langfuse local deployment

This checkout-only deployment supplies the optional local Langfuse stack. `manage.py` is its standard-library lifecycle/browser helper and the direct-script fallback; it reuses `setup.py` for one-time private settings creation and `compose.yaml` for Docker operations. The CLI dispatches to the same helper. Follow the
[official setup and troubleshooting guide](../../docs/langfuse-local.md).

The Compose services follow the required web, worker, PostgreSQL, ClickHouse,
Redis and MinIO topology in [upstream Langfuse v4.80.0 Compose](https://github.com/langfuse/langfuse/blob/v4.80.0/docker-compose.yml).
The optional AI gateway, service debug ports and remote exposure are omitted.
Images are pinned in `compose.yaml`; `.env` is generated once and ignored.

The explicitly invoked [project connection check](../../docs/langfuse-connection.md)
belongs here. It uses installed application configuration and Langfuse SDK 5.2.0;
UI-only direct-script commands do not require the application environment. The authenticated `--check` does.
