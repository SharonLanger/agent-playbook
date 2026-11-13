# Observability exploration pointers

Status: **EXPLORATION**. [Approved architecture](../architecture.md) still selects Langfuse for initial tracing. Alternatives, logs versus traces, local storage/UI and exporter combinations need evaluation; this note does not replace that choice.

See [agent execution notes](agent-execution/architecture-notes.md) for the distinction between semantic execution events and telemetry projections, correlation, redaction and exporter failure policy. Research references there are historical evidence, not proof of current SDK compatibility. Add new comparisons and their sources here as they are evaluated. Update the guarded architecture only after explicit approval.


## First Langfuse milestone draft

The [Stage 02 review package](../stages/02-langfuse/README.md) proposes self-hosted configuration and a mock-trace script before real workflow instrumentation. It incorporates Sharon's intended workflow ABC with per-run context while leaving the pending refactor's exact API open. This is a draft, not implemented behavior or approval of a logging backend.
