# M2 design — application logging

**Behavior and LOG-G01–06 approved by Sharon on 2026-11-16; implementation handoff revision to be pinned.** Shared LD15–26 and LOG-01–15/20–24/26–32 govern. No implementation approved.

## 1. Minimal integration

Reuse Python logging for levels/records and OpenTelemetry's released LoggingHandler, LoggerProvider, BatchLogRecordProcessor and HTTP OTLPLogExporter. VictoriaLogs supplies storage/query/UI. No custom logger class, serializer, exception tree, queue, collector, retry loop or observability broker.

Our code has four jobs:
1. Extract selected ExecutionContext fields into logging extra.
2. Read and validate integration settings through the existing loader.
3. Configure/close the SDK pipeline at the runner boundary.
4. Keep telemetry infrastructure failures from replacing workflow outcomes, with safe terminal diagnostics.

## 2. Public application calls

```python
log_debug(context, "Workflow selected", fields={"component": "runner"})
log_info(context, "Workflow started")
log_warning(context, "Retrying operation", fields={"attempt": 2})
log_error(context, "Operation failed", exception=error)
```

Use the existing ExecutionContext type, a string message and optional keyword-only fields. Add standard critical level only as a thin level alias if needed; no new level taxonomy. All helpers delegate to one private implementation and Python logging. They return None and do not return an SDK object.

Always extract correlation_id plus observability.workflow_id/workflow_run_id and, when present, agent_type/agent_run_id. Omit absent agent attributes. Never serialize the full context or mutate it. A derived agent context is passed explicitly; no second implicit context store or logger bound into the context.

Proposed fields contract for the first increment: Mapping[str, str | bool | int | float], finite numbers only. No arbitrary object repr, nested JSON encoder or recursive traversal. Optional None values may be omitted rather than serialized. Reserve the context identity names, Python LogRecord keys, exception.* and trace/span identity keys. Omit conflicting/unsupported optional entries with a fixed safe terminal warning; keep the message and valid context. Do not allow a logging field mistake to interrupt an otherwise valid workflow. Incorrect context/message types are developer misuse, not a claim of runtime type coercion.

Use Python logging extra, exc_info (when exception is supplied) and stacklevel to retain the caller. Configure the existing handler with code attributes if supported by the pinned version. Default level DEBUG; support standard DEBUG/INFO/WARNING/ERROR/CRITICAL names. No global root-level DEBUG or automatic collection of all SDK/library logs.

## 3. Standard exception capture

Pass exception instances through Python logging's exc_info support. The pinned OTel handler supplies exception.type, exception.message and exception.stacktrace using Python traceback.format_exception; this preserves ordinary explicit/implicit cause formatting and Python's suppression semantics. SDK representation is the wire contract. No separate hand-built chain or manual stack formatting.

At the runner, record one failed outcome at the final ownership boundary, including the preserved exception/cause chain where safe. Inner layers that simply propagate do not add duplicate ERROR records. A recovered operational failure is logged by its handler and does not turn later success into failure. ERROR is a diagnostic level, not a control signal.

Do not capture locals, entire settings, resolved credentials or workflow input/output payloads merely because DEBUG is enabled. Known configuration/authentication failures keep the existing fixed safe diagnostics; do not attach credential-bearing SDK exceptions or their causes to a record. Other approved application exceptions use native details. Native formatting cannot recognize arbitrary secrets in user-written messages or exception text. Verify real exported records with synthetic configuration-secret sentinels; resolve any concrete leak using existing safe boundaries/supported controls, not a speculative generic redactor. Logging must not change Langfuse's separately approved native input/output capture.

## 4. Configuration

Proposed fields, under the existing integrations owner:

```yaml
integrations:
  langfuse:
    enabled: true
    # Existing base_url, environment and key references remain.
  logging:
    enabled: true
    level: DEBUG
    endpoint: http://127.0.0.1:9428/insert/opentelemetry/v1/logs
```

The checked-in application YAML enables logging. For compatibility with older configuration files, an absent logging section means disabled; when supplied, document enabled explicitly. There is no required_start setting; level defaults DEBUG. Existing Langfuse defaults/keys remain intact. The enabled flag controls whether SDK setup is attempted.

Extend the existing loader/models rather than adding another configuration system. Use its shared YAML → local overlay → documented environment override precedence. Proposed overrides: AGENT_PLAYBOOK_LOGGING_ENABLED, AGENT_PLAYBOOK_LOGGING_LEVEL, AGENT_PLAYBOOK_LOGGING_ENDPOINT. Never repurpose global OTEL_EXPORTER_OTLP_ENDPOINT or trace settings.

This milestone runs Python on the local host: require an HTTP loopback-IP endpoint with path /insert/opentelemetry/v1/logs, a valid explicit port and no credentials/query/fragment. Configure Requests session to ignore environment proxies and refuse redirects, as in M1. Future container-hostname/alternate OTLP backend configuration is a deliberate deployment extension, not a workflow-code change. Invalid application configuration remains a ConfigurationError. Backend unavailability and operational SDK initialization failures warn and allow workflow execution; malformed YAML or missing required credential references are not service-health failures.

Retention remains seven days in Compose, not duplicated in application YAML. No generic exporter-selection framework. Different compatible local OTLP backends need an adapter/config change, not changes to application log calls; query/UI/data migration is outside that interchangeability.

## 5. Lifecycle and failure ownership

The runner owns one logging scope per CLI run invocation; assembly owns settings and concrete setup. Use contextlib.contextmanager and SDK lifecycle operations. No generalized startup registry, custom client pool or public application API redesign.

Configure a dedicated application logger and a local LoggerProvider; pass it explicitly to the handler. Do not replace the global TracerProvider or Langfuse configuration. Install a NullHandler for disabled application logging to avoid Python lastResort printing an unconfigured error. Keep propagation disabled for this dedicated logging channel; operational stderr diagnostics use a separate path.

Order:
1. Load/validate existing configuration. Pre-configuration failures retain current terminal output.
2. Enter logging runtime scope and initialize enabled integrations before workflow execution.
3. Select workflow and create its existing ExecutionContext at the current boundary; do not move run-ID ownership.
4. Emit records while executing the existing runner/ABC lifecycle and native tracing scopes.
5. Close observation scopes, then attempt SDK log flush/shutdown and existing trace flush, even on exceptions. Remove only our installed logging handler; do not shut down the shared Langfuse tracer provider.

If initialization is partially complete, release resources already acquired. Operational initialization failure yields a warning and disables the failed integration for that invocation; it does not block workflow execution. Keep "configured enabled" separate from "successfully initialized" in ordinary runtime state, not ExecutionContext. No backend ping, auth check or synthetic ingestion is added to normal run initialization. SDK initialization succeeding is not proof the server is reachable.

Once workflow execution begins, logging/tracing failures only warn, including flush/close errors. Catch Exception only around telemetry operations; never put a broad suppressing catch around workflow execution. Do not rerun the workflow, hide a business exception or replace it with an exit-scope failure. Native tracing scope entry/attribute update/exit must honor this policy; if native APIs cannot satisfy it with narrow containment, report the concrete design gap before building a facade. Existing automatic instrumentation needs a focused regression check rather than a new interception layer.

Use the SDK's batch queue, retries and delivery timeout. Proposed HTTP request timeout 5 seconds, force-flush budget 10 seconds; SDK queue defaults otherwise. SDK shutdown can have its own limits: record actual observed behavior on the pinned SDK, and do not call a force_flush timeout a hard whole-process shutdown guarantee. No watchdog thread or custom flush scheduler. Export failure diagnostics use SDK/standard logging facilities plus fixed safe terminal messages for caught application-boundary failures. Avoid routing exporter diagnostics back into the exporter. Queue overflow/crash can lose logs; no spool/replay or exactly-once promise.

Sequential CLI invocations must not duplicate handlers or mix contexts. Simultaneous independent runner lifecycles within one interpreter are not introduced by this milestone; parallel branches within one run use explicit context and normal SDK thread safety.

## 6. Initial diagnostic placements

| Owner / stage | Record |
|---|---|
| Configuration / integration setup before context exists | Existing safe terminal diagnostics; do not invent identity or buffer/replay early records |
| Runner after context creation | INFO Workflow started; DEBUG selected implementation and completed setup (safe identifiers only) |
| Construction / prepare | DEBUG before/after useful phases, with phase/component attributes |
| Execute / validate / serialize | DEBUG phase progress; INFO Workflow completed only after valid final output/serialization |
| Runner-owned failing lifecycle | ERROR Workflow failed once, phase plus safe native exception details; preserve existing error classification/cause |
| Handled operational failure | ERROR at recovery owner; no duplicate ERROR while merely propagating |
| Telemetry failure | Safe terminal warning; workflow outcome preserved |
| Agent/helper code using derived context | Same helpers; no new automatic Stage 04 events |

Workflow failure records include workflow identity only; do not infer an agent identity not present in the supplied context. No logging sweep of personal examples or historical sandbox. Choose useful placements in maintained application code; do not add noise for every function.

## 7. Placement

Paths relative to app/src/agent_playbook/:

| Path | Responsibility |
|---|---|
| observability/logging.py (new) | Thin level helpers, identity/extra mapping, Python standard logging only |
| observability/adapters/otel_logging/runtime.py (new) | Configure dedicated provider/handler/exporter; scoped cleanup; no workflow logic |
| config/models.py and config/loader.py | Settings and existing override path |
| application/assembly.py | Integration setup under the agreed initialization policy |
| application/workflow_runner.py | Logging lifetime, lifecycle records and narrow telemetry-failure containment |
| observability/adapters/langfuse/runtime.py | Existing native setup/flush, best-effort initialization and fixed failure diagnostics |
| cli/commands.py | Preserve output/exit mapping; avoid double flush ownership |
| context/models.py | Unchanged; no clients or logging behavior |

Tests belong under app/tests/observability, application and config with independent fixtures. Public configuration/usage/troubleshooting guides and their discovery links must accompany implementation. Do not change app/examples or use its contents as fixtures.

## 8. Acceptance, dependencies and exclusions

Use real OTel in-memory log export for schema/exception/filtering assertions. Test our wiring and failure containment, not SDK internals. Perform one explicit local VictoriaLogs run after M1 and inspect records; offline quality checks do not require Docker. Test native Langfuse coexistence without a broker or external services for the offline cases.

M1 owns installation/pins and a baseline local smoke. M2 uses those aligned dependencies; do not independently upgrade Langfuse or add a second exporter implementation. M3/M4 operations remain deferred. No routine external data transmission for logging, no custom UI, durable queue, disk-pressure campaign or automatic event duplication.

## Guarded amendments for review

Sharon approved these logical amendments on 2026-11-16 after the logging behavior was explained. They are recorded as dated follow-ons in their guarded owners; earlier approved Stage 02 history is preserved:

| ID | File | Proposed change / consequence |
|---|---|---|
| LOG-G01 | designs/architecture.md | Add the small context logging boundary and OTLP adapter; replace logging-deferred wording only for this scope; specify best-effort initialization/runtime warning policy. Native tracing and workflow control remain intact. |
| LOG-G02 | designs/project-structure.md | Activate observability logging helpers and concrete OTLP adapter within existing ownership; record runner lifetime and no SDK-bearing context. |
| LOG-G03 | designs/stages/02-langfuse/workflow-integration/m2-3-workflow-tracing/design.md | Append a dated M2 amendment for Langfuse best-effort initialization and narrow runtime telemetry failure containment, preserving the historical approved contract, native capabilities and exception semantics. |
| LOG-G04 | designs/stages/02-langfuse/workflow-integration/m2-3-workflow-tracing/test-cases.md | Append the new initialization/runtime failure cases by reference to LG-05/06/08; retain existing RUN acceptance history. |
| LOG-G05 | designs/stages/02-langfuse/workflow-integration/m2-3-workflow-tracing/implementation-plan.md | Add a dated follow-on pointer to logging M2, not a rewrite of the completed implementation. |
| LOG-G06 | designs/governance/guarded-files.md | Register M2 design/test/plan only when a concrete revision is approved. |

The user's behavioral agreement authorizes drafting these proposals, not silent amendment of locked historical files. No change to charter/principles or generic tracing-broker permission is proposed.

## 9. Principle assessment

| Principles | Application |
|---|---|
| 1/3 Approval and drift | Settled choices distinguished from unapproved concrete design; LOG-G amendments listed |
| 2 Security | Selected fields; safe startup/SDK errors; no whole config/locals; sentinel verification |
| 4 Learning | Document SDK usage and a small local debugging example |
| 5 Isolation | Helpers use standard logging; OTLP provider stays in adapter; native Langfuse exception retained |
| 6 Configuration | Existing loader/YAML/overrides; no separate loader |
| 7 Quality | Aligned uv pins, typing/lint/format and focused real-SDK checks |
| 8 Evidence | Source review is not runtime PASS; local integration can remain NOT RUN |
| 9 Scope | M2 outcome only; M3/M4/event work excluded |
| 10 Local | Local endpoint/storage; no global trace destination changes |
| 11 History | Preserve earlier contracts and superseded decisions |
| 12 Traceability | LOG/LD IDs to LG acceptance cases |
| 13 Sandbox | No personal examples access/dependency |
| 14 Docs | Configuration, usage and troubleshooting updated with implementation |
| 15 Status | Draft package; no approved SHA/implementation/acceptance claim |

## 10. Explicit reusable component checks (LD27)

No required_start setting, automatic connection check or doctor call in the workflow path. Users run explicit diagnostics and repair services before later workflow runs. The future coordinator/doctor is deferred, not a registry or orchestration class to build now.

Reuse observability/adapters/langfuse/connection.py check_connection(settings): validates project access through the existing read-only authenticated request. Add the analogous check_connection(settings) under observability/adapters/otel_logging/connection.py for the selected VictoriaLogs local deployment. Use the existing validated settings/loader; no second YAML parser. A small plain result can report component, status and safe reason; reuse the existing result conventions where practical, with no provider/plugin hierarchy. Disabled integration returns skipped.

Each check is bounded and read-only: validate applicable settings, reach the configured local service, use its documented health/readiness endpoint and verify authentication/access when the configured deployment has authentication. VictoriaLogs' direct local deployment currently has no credentials: report authentication not applicable, not tested or proven. Verify the pinned release's endpoint/response before implementation. A healthy HTTP response does not establish successful OTLP ingestion, disk durability or full service functionality. Preserve explicit M1 smoke testing for that distinction.

Exercise both methods through one small opt-in tooling script plus focused tests (LG-12). The script uses existing configuration, prints per-component results and exits nonzero for a failed enabled component; no writes, auto-start, repair or service changes. Configuration errors are reported safely before network access. No automatic health polling. Future CLI doctor can call these same methods directly. This increment prepares reusable functions, not the doctor command.

HTTP checks retain timeouts and local endpoint/proxy/redirect safeguards where applicable. Avoid exposing credentials, response bodies or raw authentication exceptions. Update public diagnostics instructions when the script is implemented.
