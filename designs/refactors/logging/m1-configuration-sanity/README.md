# M1 — local logging configuration sanity

**Complete. Implementation #54 merged.**

Outcome: start the pinned local VictoriaLogs component and see one synthetic context/message record sent by Python/OpenTelemetry in its built-in UI.

Read [design](design.md), [test cases](test-cases.md), then [implementation plan](implementation-plan.md). Shared [requirements](../requirements.md) and [decisions](../decisions.md) remain authoritative.

Prerequisites: local Docker Engine/Desktop running; source checkout and Python environment; internet only for fetching dependencies/images, not for runtime logging. No Langfuse service is required for this isolated smoke.

Excluded: production runner changes, generalized initialization framework, public API/distribution, log-management CLI, Langfuse Compose migration, exception formatting, durable replay and extensive product/security testing.

Next: review and approve this concrete design/test/plan revision before implementing. The current update prepares the draft only.
