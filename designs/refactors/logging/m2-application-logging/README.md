# M2 — application logging

**DRAFT concrete design; user choices settled, implementation revision not approved.**

Outcome: normal CLI workflow runs produce correlated application logs in local VictoriaLogs, with useful exceptions and debugging details. Calls stay context + message + optional fields. SDKs own the logging machinery.

Read [design](design.md), [test cases](test-cases.md), [implementation plan](implementation-plan.md), and shared [decisions](../decisions.md). Main inspected: 529fe15895afc8211d833fc2544e98f0d18fb451.

Prerequisites: existing immutable ExecutionContext and native Langfuse integration; M1 local component/smoke available before live acceptance. Offline implementation can be checked without a running service.

Included: thin logging helpers; configuration; scoped runner lifecycle; diagnostic calls; standard exception handling; consistent initialization-only requirement for logging and Langfuse; runtime telemetry failures warn only.

Excluded: custom logger/transport/queue/exception engine, generic broker, automatic Stage 04 events, observation duplication, M3 Compose migration, M4 management CLI, package/distribution redesign and durable replay.

Approval SHA: none. Implementation PR: none. Guarded amendments are [listed](design.md#guarded-amendments-for-review), not applied. Review this package before an implementation handoff; PR #51 stays draft/open.
