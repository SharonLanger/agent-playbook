# M2 — application logging

**Complete. Implementation #55 merged. [Closeout](../progress.md) records the scope of live acceptance.**

Outcome: normal CLI workflow runs produce correlated application logs in local VictoriaLogs, with useful exceptions and debugging details. Calls stay context + message + optional fields. SDKs own the logging machinery.

Read [design](design.md), [test cases](test-cases.md), [implementation plan](implementation-plan.md), and shared [decisions](../decisions.md). The original design inspected main at 529fe15895afc8211d833fc2544e98f0d18fb451.

Prerequisites: existing immutable ExecutionContext and native Langfuse integration, plus M1 delivered through merged PR #54. Sharon saw the local smoke record and matching correlation after the Docker network correction. Offline implementation can be checked without a running service.

Included: thin logging helpers; configuration; scoped runner lifecycle; diagnostic calls; standard exception handling; reusable explicit component health/connection checks and a small verification script; operational initialization/runtime failures warn only.

Excluded: custom logger/transport/queue/exception engine, generic broker, automatic Stage 04 events, observation duplication, M3 Compose migration, M4 management CLI, package/distribution redesign and durable replay.

Guarded amendments LOG-G01–05 are dated append-only updates in their owners; LOG-G06 registers this approved M2 package. Implementation PR #55 and overall logging design PR #51 are merged. The [closeout record](../progress.md) distinguishes accepted Mac sanity checks from detailed live checks that remain unverified.

## Historical design checkpoint

At the original design checkpoint, M1 PR #54 was unmerged, no M2 implementation
PR existed, and design PR #51 remained draft/open. Those statuses are superseded
by the merges above; the approved M2 scope and guarded amendments are unchanged.
