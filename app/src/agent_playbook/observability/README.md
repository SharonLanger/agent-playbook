# Observability

This package provides workflow tracing through Langfuse and application logging
through OpenTelemetry to VictoriaLogs.

| Location | Responsibility |
|---|---|
| `adapters/langfuse/` | Client setup, explicit project checks and mock observations, native tracing initialization and flush |
| `logging.py` | Context-aware helpers using Python's standard logging |
| `adapters/otel_logging/` | Logging provider/export setup, explicit connection checks and cleanup |

The application runner uses native Langfuse scope and propagation under the
approved integration exception. With tracing enabled, the shipped
`show_framework_events: true` setting enables automatic Flow and executed-step
observations. Explicit `false` retains runner observations but suppresses those
automatic observations with the pinned instrumentor.

Application assembly sets up the integrations; the runner owns the application
logging lifetime, and the CLI attempts tracing flush after observations close.
Context stays data-only and workflow business steps stay provider-free.

See [workflow tracing](../../../docs/workflows.md#native-workflow-tracing),
[application logging](../../../docs/logging.md), and
[configuration](../../../docs/configuration.md). Accepted tracing and logging
status is recorded in [Stage 02](../../../../designs/stages/02-langfuse/README.md)
and the [logging progress record](../../../../designs/refactors/logging/progress.md).

Follow [the guarded project structure](../../../../designs/project-structure.md).
