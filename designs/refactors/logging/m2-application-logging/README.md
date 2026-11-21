# M2 — application logging

**Complete. Implementation #55 merged. [Closeout](../progress.md) records the scope of live acceptance.**

Outcome: normal CLI workflow runs produce correlated application logs in local VictoriaLogs, with useful exceptions and debugging details. Calls stay context + message + optional fields. SDKs own the logging machinery.

Read [design](design.md), [test cases](test-cases.md), [implementation plan](implementation-plan.md), and shared [decisions](../decisions.md). Main inspected: 529fe15895afc8211d833fc2544e98f0d18fb451.

Prerequisites: existing immutable ExecutionContext and native Langfuse integration; M1 PR #54 remains unmerged; Sharon saw the local smoke record and matching correlation after the Docker network correction. Offline implementation can be checked without a running service.

Included: thin logging helpers; configuration; scoped runner lifecycle; diagnostic calls; standard exception handling; reusable explicit component health/connection checks and a small verification script; operational initialization/runtime failures warn only.

Excluded: custom logger/transport/queue/exception engine, generic broker, automatic Stage 04 events, observation duplication, M3 Compose migration, M4 management CLI, package/distribution redesign and durable replay.

Guarded amendments LOG-G01–05 are dated append-only updates in their owners; LOG-G06 registers this approved M2 package. Implementation PR: none yet. PR #51 stays draft/open; implementation and merge are separate.
