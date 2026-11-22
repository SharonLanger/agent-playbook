# Research agenda

**Research agenda with an initial source review.**
See [2026-11-15 VictoriaLogs research](2026-11-15-victorialogs.md) for verified documentation/license evidence and remaining gaps. No runtime experiments or benchmarks performed. Exact artifact pins and bundled-license review remain pending.

## Historical candidate architectures

| Option | Proposed responsibilities | Main question |
|---|---|---|
| A: JSONL + existing viewer | Structlog prepares records; standard logging writes/rotates; existing tool queries/views | Is an Apache-2.0 viewer available with query-before-load? How are concurrent writers handled? |
| B: VictoriaLogs primary | Structlog prepares records; existing delivery mechanism sends to local storage/UI | What happens when Docker is unavailable/slow? Which shipper, queue and custom glue are required? |
| C: JSONL + VictoriaLogs | Local files retain records; existing shipper feeds search/viewing | Does outage resilience justify checkpoint/rotation/replay complexity? What duplicates or losses occur? |
| D: existing embedded SQLite solution | Existing component owns recording/querying/viewing | Investigate only if a maintained Apache-2.0 option exists; do not build a logging database. |

Structlog and VictoriaLogs have different responsibilities and may be combined. These are hypotheses, not verified support or installation recommendations.

## Bounded tasks

| ID | Deliverable | Evidence needed |
|---|---|---|
| R01 | Operating requirements for stopped viewer/storage, disk failure, slow sinks and shutdown | Policy table separating application outcome, record preservation/loss and diagnostics |
| R02 | Compare A/B/C, optionally D | Official docs/licenses for exact artifacts; process/service count, configuration and custom-code inventory |
| R03 | Find suitable existing viewers | Demonstrated workflow/agent/time query-before-load, bounded results and client-side sorting/filtering; license/maintenance evidence |
| R04 | Compare API/context approaches | Isolated nested-helper, sibling, repeated-run and async/thread probes; field collision behavior |
| R05 | Validate selected storage/delivery | Pinned versions; restart, rotation, concurrent writers, disk/queue limits, flushing, replay/duplicate measurements |
| R06 | Trace/event integration if selected | Supported native enrichment/capture; no broker or duplicate records; Stage 04 coordination |

The selected direct-OTLP direction was implemented through M1–M3; see the
[completed logging refactor](../README.md) for current status and remaining work.
The research tasks above retain their original scope; completion of the refactor
does not establish that every research question or live probe was completed.

## Future research record

Create a dated record per executed task: question and LOG/LQ IDs; candidate/version/license; official source URLs/access date; method/commands/environment; actual results; assumptions; operational/custom-code cost; recommendation; limitations/open questions. Distinguish source findings, observations and inference. Use synthetic fixtures outside app/examples.

No runtime PASS results, benchmarks or dependency selections are asserted. Project-level license findings are documented in the source review; full artifact compliance is not certified.

## Current selection

[Direct OTLP findings](2026-11-15-direct-otlp.md) supersede the collector-first recommendation. Python standard logging plus the OpenTelemetry bridge/exporter sends directly to VictoriaLogs. Historical alternatives remain for reference, not parallel implementation work.
