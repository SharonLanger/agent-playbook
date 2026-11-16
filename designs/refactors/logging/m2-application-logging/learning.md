# M2: follow one diagnostic through the SDK

The application helper extracts five selected identity fields from immutable
ExecutionContext into Python logging `extra`. The context remains a value object:
`parent.for_agent(...)` returns a derived value; passing parent again restores
workflow-only identity without an implicit context store.

Python logging owns severity filtering, caller location and `exc_info`. The released
OpenTelemetry LoggingHandler turns the LogRecord into an OTel log. With an exception
instance, native traceback formatting retains explicit/implicit causes and suppression
semantics. No custom chain walker or serializer is involved. The adapter enables
supported code attributes so the exported caller points to the application call.

A local LoggerProvider holds the SDK batch processor and HTTP OTLP exporter. It is
passed directly into LoggingHandler rather than replacing any global trace provider.
Tests replace export with the SDK's in-memory exporter through the same handler;
application calls and identity schema stay unchanged. A different database still
needs compatible adapter/configuration and separate ingestion/migration validation.

The runner opens this pipeline once per invocation. Observation scopes enclose the
existing lifecycle; then trace/log delivery and cleanup are attempted. Narrow catches
surround telemetry operations only. Business exceptions retain their classification
and causes, and the workflow is never retried for telemetry failure. The final owner
emits one failed record; propagating inner layers do not duplicate it.

The batch queue is bounded and volatile. A requested force-flush budget is not a
whole-process deadline: pinned SDK 1.45.2 ignores that batch timeout and has a separate
shutdown worker timeout. HTTP requests use five seconds. Outage, overflow or abrupt
termination can lose records. Health, ingestion, persistence and UI inspection are
separate pieces of evidence; the explicit read-only service check establishes only
the first. Live M2 ingestion and UI sorting remain local acceptance work.
