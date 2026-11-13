# Observability exploration pointers

Status: **EXPLORATION**. [Approved architecture](../architecture.md) still selects Langfuse for initial tracing. Alternatives, logs versus traces, local storage/UI and exporter combinations need evaluation; this note does not replace that choice.

See [agent execution notes](agent-execution/architecture-notes.md) for the distinction between semantic execution events and telemetry projections, correlation, redaction and exporter failure policy. Research references there are historical evidence, not proof of current SDK compatibility. Add new comparisons and their sources here as they are evaluated. Update the guarded architecture only after explicit approval.
