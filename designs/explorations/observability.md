# Observability exploration pointers

Status: **EXPLORATION**. [Approved architecture](../architecture.md) still selects Langfuse for initial tracing. Alternatives, logs versus traces, local storage/UI and exporter combinations need evaluation; this note does not replace that choice.

See [agent execution notes](agent-execution/architecture-notes.md) for the distinction between semantic execution events and telemetry projections, correlation, redaction and exporter failure policy. Research references there are historical evidence, not proof of current SDK compatibility. Add new comparisons and their sources here as they are evaluated. Update the guarded architecture only after explicit approval.


## Langfuse milestones

The [Stage 02 review package](../stages/02-langfuse/README.md) now separates local UI setup, a connection check, a personal mock-data playground and later real workflow integration. Milestones 1–3 require no workflow/context changes; only milestone 4 waits for the refactor. Sharon requested the editable playground under app/examples/langfuse; maintained tests remain independent of it. The milestone direction is agreed, but detailed implementation is still a draft and no capability is implemented by this documentation change. [Doctor #37](https://github.com/SharonLanger/agent-playbook/issues/37) is a separate feature request.
