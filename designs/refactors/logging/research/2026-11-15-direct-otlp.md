# Direct OpenTelemetry to local VictoriaLogs

Source review: 2026-11-15. Documentation/source evidence only; no end-to-end run.

## Findings

- VictoriaLogs accepts OTLP/HTTP logs at /insert/opentelemetry/v1/logs directly from SDKs. The log body becomes the message; attributes carry context. Resource fields identify service-level streams, so run IDs belong in per-record attributes.
- One VictoriaLogs service owns storage, query and UI (/select/vmui). No Collector is necessary.
- Python LoggingHandler bridges standard logging records. The supported current handler location is opentelemetry.instrumentation.logging.handler; sdk._logs.LoggingHandler is deprecated.
- The HTTP exporter accepts an explicit endpoint and Requests session. A local destination plus disabled environment proxies and redirects avoids accidental external routing for that exporter.
- Docker loopback publishing limits host-port exposure; an internal network prevents ordinary external routing. Internal containers can still contact appropriately configured host services. These settings do not prove host-wide impossibility of data forwarding.
- Pin the locally deployed release; use the upstream documented configuration. No source audit or exhaustive security proof is requested.
- Batch export is not a durable disk spool. Workflow outcomes, dropped records and production exporter failures need an explicit M2 policy.

## Version evidence

VictoriaLogs official quickstart currently uses v1.54.0; use it as the M1 proposed pin, not a proven local compatibility claim. Existing app/uv.lock at main 4ed7a318e25653d481705d9cb40c35de9ab649c7 contains OTel SDK/exporter 1.45.2 and instrumentation family 0.66b2. Logging instrumentation is not yet installed; handler source was verified at v0.66b2. Reuse aligned pins rather than upgrading Langfuse's dependencies incidentally.

VictoriaLogs and OpenTelemetry project licenses provide Apache-2.0. Carry exact version/license links into M1 evidence; this does not certify every bundled/transitive artifact.

## Official references

- [VictoriaLogs OTLP ingestion](https://docs.victoriametrics.com/victorialogs/data-ingestion/opentelemetry/)
- [VictoriaLogs quickstart](https://docs.victoriametrics.com/victorialogs/quickstart/)
- [VictoriaLogs license](https://github.com/VictoriaMetrics/VictoriaLogs/blob/v1.54.0/LICENSE)
- [Python logs example and handler migration](https://opentelemetry-python.readthedocs.io/en/latest/examples/logs/README.html)
- [Pinned logging handler source](https://github.com/open-telemetry/opentelemetry-python-contrib/blob/v0.66b2/instrumentation/opentelemetry-instrumentation-logging/src/opentelemetry/instrumentation/logging/handler.py)
- [Python HTTP exporter](https://opentelemetry-python.readthedocs.io/en/latest/_modules/opentelemetry/exporter/otlp/proto/http/_log_exporter.html)
- [Requests session options](https://requests.readthedocs.io/en/latest/api/)
- [Docker internal networks](https://docs.docker.com/reference/cli/docker/network/create/#network-internal-mode---internal)
- [Docker port publishing](https://docs.docker.com/engine/network/port-publishing/)

## Scope of evidence

The normal ingest/query/UI behavior is documented; M1 repeats a small representative example rather than re-testing the product. Docker is absent in this design environment. Local runtime compatibility, UI behavior and concrete shutdown delivery are NOT RUN. The previous JSONL/Fluent Bit proposal remains historical and unselected.
