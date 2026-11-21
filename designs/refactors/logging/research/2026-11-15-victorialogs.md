# VictoriaLogs: configuration-first integration research

Date: 2026-11-15. **Source-verified research / proposed architecture, not a tested deployment or adopted stack.** Addresses R01–R03/R06 and LOG-15–20. Current upstream documentation was read; exact release compatibility and artifacts are not yet pinned.

## Recommended candidate and replacement boundary

Application emits ordinary structured JSONL using structlog plus Python logging. An existing Fluent Bit collector tails a mounted application-log directory and sends JSON lines through its configurable HTTP output. One VictoriaLogs container stores/queries logs and serves its built-in UI. No custom broker, bespoke sender, database, indexing engine or viewer is needed for this candidate.

This is a recommendation inferred from the documented ingestion and collector interfaces, not a completed substitution test. Workflow code imports a backend-independent logger, never a VictoriaLogs SDK. Replace VictoriaLogs by changing collector output/configuration, service image/configuration and UI/check integration. Application log calls and correlation fields remain unchanged. A different backend may require a different supported collector output or collector. Queries/dashboards, old stored data and backend-specific health probes do not automatically migrate.

Importing a provider logger everywhere would not prove replaceability: similar method names do not establish compatible schemas, delivery or lifecycle semantics. A standard JSON boundary provides detachment without an owned broker API.

For today's host Python app, a host log directory bind-mounted read-only into the collector is the simplest candidate. Keep collector state/buffers in a separate writable volume. Later containerizing Python can retain a shared file directory or deliberately switch to structured stdout collection. Do not assume Linux Docker-internal log paths are accessible from macOS; the official demo tails such paths and cannot be copied unchanged for the host app.

## Official examples reviewed

- [VictoriaLogs quick start](https://docs.victoriametrics.com/victorialogs/quickstart/): container/binary, JSON ingestion and built-in UI. Single node does not require a separate database/UI service. Current example uses v1.54.0; this is evidence from docs, not our selected pin.
- [Fluent Bit ingestion guide](https://docs.victoriametrics.com/victorialogs/data-ingestion/fluentbit/): existing HTTP output with json_lines and URI field mapping.
- [Official Compose demo](https://github.com/VictoriaMetrics/VictoriaLogs/tree/master/deployment/docker/victorialogs/fluentbit/jsonline), [configuration](https://github.com/VictoriaMetrics/VictoriaLogs/blob/master/deployment/docker/victorialogs/fluentbit/jsonline/fluent-bit.conf), [README](https://github.com/VictoriaMetrics/VictoriaLogs/blob/master/deployment/docker/victorialogs/fluentbit/README.md): reviewed via GitHub. Config blob 9349781fc6acd8b001c6095a5bfbfc885182fa29; README blob d0ab3ef6d20fa08920bf8bdc0f2ab29db6a311ab. Demo includes vlagent, multiple stores, vmauth and metrics: broader than our minimal candidate. Do not adopt its volume-deleting cleanup command.
- [Fluent Bit tail](https://docs.fluentbit.io/manual/data-pipeline/inputs/tail), [JSON parser](https://docs.fluentbit.io/manual/data-pipeline/parsers/json), [HTTP output](https://docs.fluentbit.io/manual/data-pipeline/outputs/http), [buffering](https://docs.fluentbit.io/manual/data-pipeline/buffering): built-in file collection, offset state, parsing, output and configurable disk buffering; these are not settings-free or unlimited-delivery guarantees.
- [vlagent](https://docs.victoriametrics.com/victorialogs/vlagent/): alternative existing collector with file collection, buffering and JSON-line forwarding. Not required in addition to Fluent Bit for our single-node candidate. Bounded buffers can drop oldest records; no blanket lossless claim.

## Illustrative configuration and use — not installed commands

Top-level Compose concept (proposed paths only):

```yaml
include:
  - langfuse/compose.yaml
  - logging/compose.yaml
```

[Docker include](https://docs.docker.com/compose/how-tos/multiple-compose-files/include/) requires Compose 2.20.3+. Each included model resolves paths relative to its own directory; service/resource names must not collide. Preserve the existing Langfuse deployment/volume identity while introducing the umbrella.

Logging component would define two services: victorialogs and fluent-bit, with pinned images, loopback port 9428, persistent store/state volumes and the host log mount. No production-ready Compose file is supplied by this research. Once configured, standard docker compose up -d starts included services. The built-in UI is at http://localhost:9428/select/vmui . No separate UI process or Grafana is required.

Key collector output fragment, adapted to our proposed fields (not a full collector config):

```ini
[OUTPUT]
    Name   http
    Match  app.*
    Host   victorialogs
    Port   9428
    URI    /insert/jsonline?_msg_field=event&_time_field=timestamp&_stream_fields=service
    Format json_lines
```

Input config must additionally select the mounted JSONL files, JSON parser, app.* tag, durable tail-state path and chosen buffering/retry limits. The app record must contain timestamp and service fields. Keep high-cardinality run/correlation IDs as searchable fields rather than blindly making them stream fields. Final field mappings remain a design choice.

Illustrative application call AFTER centralized logger configuration/context binding:

```python
log.info("step_finished", step="validate", result_count=3)
```

The application owns adding workflow/run/correlation and optional agent identity from the existing context. A collector cannot infer them. structlog renders JSON; standard Python logging can handle the destination/rotation. [Structlog standard-library integration](https://www.structlog.org/en/stable/standard-library.html) documents this composition. Default multi-process file rotation must not be assumed safe; choose and test a simple writer/file strategy.

Example UI query for proposed fields: workflow_id:="wf-02" AND level:="error". Select a bounded time window/results. [Querying docs](https://docs.victoriametrics.com/victorialogs/querying/) document LogsQL, HTTP queries, live tail and built-in display modes. The earlier requirement for arbitrary client-side sorting/filtering without another request has NOT been verified in the UI; retain it as an acceptance gap, not a reason to build a viewer silently.

## Out of the box versus our work

| Responsibility | Existing tool | Our work |
|---|---|---|
| Record rendering/levels/exceptions | structlog / Python logging | One centralized setup and selected config |
| Workflow/agent context | Existing ExecutionContext | Small binding bridge; log calls at meaningful boundaries |
| Collection/delivery | Fluent Bit tail/parser/output/buffer | Configuration, mounts and operational limits |
| Store/index/query/UI | VictoriaLogs | Version, retention, disk volume, loopback port and field mapping |
| Start/stop/status/UI | Docker Compose / existing management pattern | Thin CLI command wiring and clear error messages |
| Verify full path | Existing ingestion/query APIs | Small bounded synthetic emit/read-back check |
| Replacement | Standard JSON + configurable collector | Alternate-output proof; backend-specific queries/health handling |

Zero custom logging infrastructure is plausible; zero Python integration is not. We still need context binding, initialization, useful log calls, CLI wiring and meaningful tests. Do not promise a line count before inspecting the integration diff. Redaction is policy/configuration where supported; extra custom processors need a concrete requirement and discussion.

## Licensing evidence and limits

| Candidate | Project license evidence | Conclusion |
|---|---|---|
| VictoriaLogs community | [LICENSE](https://github.com/VictoriaMetrics/VictoriaLogs/blob/master/LICENSE) | Apache-2.0 project; do not substitute enterprise artifacts |
| Fluent Bit | [LICENSE](https://github.com/fluent/fluent-bit/blob/master/LICENSE) | Apache-2.0 project |
| structlog | [License](https://www.structlog.org/en/stable/license.html) | Apache-2.0 OR MIT; Apache option available; not MIT-only |

This checks selected projects, not every bundled/transitive library or image layer. A literal Apache-only dependency tree is not established. Existing Python, Docker Desktop and the accepted Langfuse stack are prerequisites/existing components, not reclassified as Apache-2.0. Review exact image/package notices before adoption; raise any conflict with Sharon rather than declaring all dependencies compliant. No MIT-only substitute is selected.

## Next evidence gates

Pin a minimal candidate and validate on the actual Mac host-file path; emit/query a unique record through collector; check context isolation and field preservation; stop collector/backend and test restart/rotation/bounded-loss semantics; verify UI interactions; demonstrate alternate output without workflow changes; define checks and clear setup flow. No Docker/service/Python probe or benchmark ran in this research.
