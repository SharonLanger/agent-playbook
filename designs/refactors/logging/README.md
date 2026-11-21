# Application logging

**Complete and merged.** This independent Stage 02 follow-on delivers context-based Python logging over OpenTelemetry to local VictoriaLogs. Langfuse traces and application logs share a correlation ID.

| Milestone | Delivered | Merged PR |
|---|---|---|
| [M1](m1-configuration-sanity/README.md) | Local VictoriaLogs and a synthetic smoke record | #54 |
| [M2](m2-application-logging/README.md) | Runner-owned logging with execution context, message and optional fields | #55 |
| [M3](m3-service-composition/README.md) | Individual and aggregate service commands | #65 implementation and #57 design |

Sharon accepted the Mac workflow sanity check for closeout. [Progress and follow-ups](progress.md) records its scope. Guided setup is deferred. The [CLI doctor issue](https://github.com/SharonLanger/agent-playbook/issues/37) owns the user-facing health check.

[Requirements](requirements.md) · [Decision history](decisions.md) · [Research](research/README.md) · [Repository impact](repository-updates.md)
