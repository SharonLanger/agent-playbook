# Application logging

Application diagnostics use Python logging through OpenTelemetry to local VictoriaLogs. Start, inspect and stop it explicitly from a bootstrapped source checkout. The checked-in YAML enables logging at DEBUG; older configuration without a logging section leaves it disabled.

```yaml
integrations:
  logging:
    enabled: true
    level: DEBUG
    endpoint: http://127.0.0.1:9428/insert/opentelemetry/v1/logs
```

```sh
app/.venv/bin/agent-playbook logs --start
app/.venv/bin/agent-playbook logs --status
app/.venv/bin/agent-playbook logs --stop
```

These commands manage `agent-playbook-logging-smoke` separately from Langfuse.
`logs --start` works even when workflow logging is disabled and leaves
configuration files unchanged. `services --start` selects by both workflow
integration flags. The local service always uses `127.0.0.1:9428` and retains
`agent-playbook-logging-smoke_logs-data` on stop. See the
[CLI guide](cli.md#local-services) for options and exit codes, and the
[logging smoke](../tooling/logging/README.md) for ingestion verification.

Shared YAML, optional local YAML, the selected secrets file and process environment overrides apply in that order. `AGENT_PLAYBOOK_LOGGING_ENABLED`, `AGENT_PLAYBOOK_LOGGING_LEVEL` and `AGENT_PLAYBOOK_LOGGING_ENDPOINT` override those values. Levels are DEBUG, INFO, WARNING, ERROR and CRITICAL. The destination must use HTTP, a loopback IP, an explicit port and the exact OTLP logs path shown above, without credentials, query or fragment. Requests ignore proxy environment settings and reject redirects. Logging never changes the Langfuse destination.

Maintained workflow runs emit started/completed/failed records and DEBUG phase progress. Search the local UI at http://127.0.0.1:9428/select/vmui for `correlation_id`, `workflow_id` or `workflow_run_id`. Logging level describes diagnostics; it does not determine workflow success.

Application code can use the same helpers with the existing immutable context:

```python
from agent_playbook.observability.logging import log_info, log_error

log_info(context, "Operation started", fields={"attempt": 1})
# In an exception handler:
log_error(context, "Operation failed", exception=error)
```

Pass derived agent contexts explicitly. Helpers extract identity without serializing the context. Optional fields accept flat scalar strings, booleans and finite numbers; None is omitted. Reserved identity/LogRecord/exception/trace fields and unsupported values are omitted with a safe warning. Exceptions use native Python/OTel chained traceback formatting without locals. Avoid secrets in messages and exceptions; arbitrary user-written secrets cannot be recognized automatically. DEBUG never authorizes dumping settings or workflow payloads. Langfuse retains its separate approved native capture.

Operational logging/tracing initialization and runtime failures warn and preserve the workflow outcome. Invalid YAML/settings and missing required credential references still fail configuration validation. No automatic health check runs before a workflow. To check services explicitly from the app directory:

```bash
.venv/bin/python tooling/logging/check_services.py --config application.yaml
```

The read-only script prints each component's status and exits nonzero when an enabled component fails. VictoriaLogs `/health` checks connectivity/health; authentication is not applicable to the selected direct local deployment. Langfuse checks authenticated project access. Neither proves ingestion or durability; run the explicit smoke and inspect its record for that evidence.

One SDK batch pipeline belongs to each run. Observation scopes close before cleanup; SDK force-flush is requested with 10 seconds and HTTP export uses a 5-second request timeout. In pinned SDK 1.45.2 the batch force-flush timeout is ignored and shutdown has its own 30-second worker limit, so these are not whole-process deadlines. Logs may be lost on overflow, outage or abrupt termination. There is no disk spool/replay or exactly-once guarantee. Sequential invocations remove their own handlers; simultaneous independent runner lifecycles in one interpreter are outside scope.

The same helper schema works with an SDK in-memory exporter (covered by maintained tests). Replacing storage requires adapter/configuration work; this is not a tested database migration promise. Retention is seven days in Compose. Post-load UI ordering and live M2 ingestion require local acceptance; no custom viewer is provided.
