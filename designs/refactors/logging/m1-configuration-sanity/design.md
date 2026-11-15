# M1 design — configuration sanity

**Draft.** Maps LOG-08/09/14/19/20/23/24/25 and LD15/18/19. M2 owns LOG-21/22 production integration.

## Outcome and ownership

Use one local VictoriaLogs container, its bundled UI and Python's standard logger bridged by OpenTelemetry. A checkout-only smoke script owns its short lifecycle: initialize once, emit synthetic records, flush, exit. No production runner wiring or permanent application API yet.

Proposed placement within existing tooling ownership:
- app/tooling/logging/compose.yaml — isolated logging service.
- app/tooling/logging/logging_smoke.py — opt-in synthetic emitter.
- app/tooling/logging/README.md — exact commands, pins, local prerequisites and expected UI query.
- app/pyproject.toml and app/uv.lock — only the missing aligned logging instrumentation dependency if required.
- app/docs/configuration.md — a short supported developer-smoke reference when implemented, clearly distinguished from normal workflow logging.

These add ordinary files within existing tooling boundaries, not new runtime components. Runtime code never imports tooling. Do not access app/examples. No guarded amendments are proposed by M1.

## Proposed service configuration

```yaml
services:
  victorialogs:
    image: victoriametrics/victoria-logs:v1.54.0
    command:
      - "-storageDataPath=/victoria-logs-data"
      - "-retentionPeriod=7d"
    ports:
      - "127.0.0.1:9428:9428"
    volumes:
      - logs-data:/victoria-logs-data
    networks:
      - logs-local
    logging:
      driver: local

volumes:
  logs-data:
    driver: local

networks:
  logs-local:
    internal: true
```

Use explicit Compose project identity agent-playbook-logging-smoke consistently. Do not migrate or attach to Langfuse networks/volumes. Do not delete volumes as part of a successful smoke. Seven days is the user-agreed default retention for both the probe and planned application setup (LD25), configurable through the logging component Compose settings.

Use Docker Engine 28+ for loopback publishing semantics documented by Docker (older versions have a same-L2 exposure caveat). Record actual Docker/Desktop and Compose versions, do not invent a tested minimum. Validate that internal networking plus loopback publication works on the actual platform; do not silently remove isolation if it does not.

## Python configuration and record

Reuse the repository's aligned OTel SDK/exporter 1.45.2 and instrumentation 0.66b2 family, subject to current lock consistency. Add opentelemetry-instrumentation-logging at the matching version. No unrelated upgrade.

Use LoggerProvider, BatchLogRecordProcessor, the HTTP OTLPLogExporter and opentelemetry.instrumentation.logging.handler.LoggingHandler. Attach the handler to a dedicated named logger with propagation disabled; do not set the global tracer provider or instrument the root logger. Resource service.name is agent-playbook-logging-smoke; run identities are log attributes.

Supply the endpoint externally through an explicit smoke argument, with a documented local default:
http://127.0.0.1:9428/insert/opentelemetry/v1/logs
Validate the scheme/host/path and restrict this host-run probe to that loopback destination (an optional port may vary). Requests session ignores environment proxies and refuses redirects. Configure bounded export/flush timeouts. No remote fallback or telemetry forwarding.

Emit INFO with message "Logging smoke check" and a synthetic context mapping containing workflow_id, workflow_run_id and correlation_id; use one unique correlation value per probe. No real prompts, business data, secrets or whole configuration objects. The small probe may pass those fields through Python logging extra; it does not finalize the production helper's accepted context type.

Shutdown in finally. Because exporter failures may be handled internally, process exit alone is NOT evidence of successful delivery. Print the unique correlation and local UI URL, with delivery explicitly unconfirmed until the operator finds the record.

## Acceptance and limitations

Open http://127.0.0.1:9428/select/vmui and search the unique correlation_id. Confirm message, severity and context attributes. This single manual round trip is sufficient integration evidence for M1; do not build a query client or general test framework.

Source-backed local configuration and one actual smoke are the scope. No source audit, packet-capture campaign, broad outage matrix or claim that host/browser/backup software cannot forward data. The Docker daemon and volume must be local; do not configure a remote logging driver.

No production application behavior changes. In-memory buffering may lose logs; durable outage behavior is an M2 decision. Service failures are smoke failures, not a change to workflow outcome semantics.

## Future runner boundary

M2 will place SDK setup in an observability adapter, invoke it from assembly/runner once per run, and flush during cleanup. Workflow/agent code will call level helpers with context + message. Exact context type, optional fields and production failure policy remain open; no generic init registry is needed.

## Principles

The shared [all-principle assessment](../repository-updates.md#all-principle-assessment) applies. M1 adds external local endpoint validation (2/6/10), isolated tooling/SDK setup (5/13), pins and bounded smoke evidence (7/8), a single incremental outcome (4/9), and a documented developer entry point (14). No guarded meaning, historical migration or production contracts change (1/3/11). Requirement IDs, draft status and honest NOT RUN evidence cover 12/15.
