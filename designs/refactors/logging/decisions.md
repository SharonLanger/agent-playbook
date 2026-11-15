# Decisions and open questions

**DRAFT register.** Sharon owns scope/policy approval; the designer supplies evidence. No implementation authorization.

| ID | State | Direction |
|---|---|---|
| LD01 | Current instruction | Separate logging design workspace/PR in designs/refactors/logging, related to Stage 02; no runtime work. |
| LD02 | Existing approved baseline | Reuse immutable data-only context and agent derivation; no clients/SDK handles in context. |
| LD03 | Existing approved baseline | Native Langfuse stays. Earlier unified logging/tracing broker is superseded; a logging-only wrapper remains open. |
| LD04 | Historical; superseded by LD15 | Structlog prepares records; JSONL was initially preferred. No detailed API or final stack locked. |
| LD05 | Reopened by handover | Superseded in part by LD10: Docker services accepted; VictoriaLogs is now the selected design direction under LD15 and outage policy unresolved. |
| LD06 | Inherited requirements | Viewer independence and separation of diagnostic severity from workflow outcome. |
| LD07 | Inherited constraints | Local operation, Apache 2.0 for new selections, existing open source and minimal replaceable integration. |
| LD08 | Deferred | Automatic observation duplication and execution-event integration need explicit scope/evidence. |
| LD09 | Proposal | Research outage requirements and candidate storage/viewer combinations before choosing API and delivery details. |

| ID | Open question | Gate |
|---|---|---|
| LQ01 | Resolved policy under LD21: required initialization by default; runtime and cleanup failures warn only. Durable replay not selected. | M2 implementation detail |
| LQ02 | Resolved direction: VictoriaLogs store/UI and direct OTLP; exact artifacts and viewer behavior remain to check | M1/M2 |
| LQ03 | Resolved API shape: explicit context + message through small level helpers; accepted context is ExecutionContext (LD22) | M2 |
| LQ04 | Field types, reserved keys, exception treatment, redaction and payload limits? | Implementation |
| LQ05 | Retention, rotation, multi-process writers, shutdown, bounded queues/retries and duplicates? | Delivery acceptance |
| LQ06 | Coverage direction agreed under LD23: workflow lifecycle plus surrounding application infrastructure; exact placement and error ownership to specify in M2 | Coverage/tests |
| LQ07 | Optional SDK trace/span enrichment and disabled-tracing behavior? | Enrichment |
| LQ08 | Built-in VictoriaLogs UI included in M1 sanity check; advanced filtering acceptance later | M1/M2 |
| LQ09 | Does an existing embedded SQLite solution simplify matters? | Optional research |
| LQ10 | Which Stage 04 event contract is ready for consumption without coupling to its drafts? | Later event integration |

Preserve dated history and record sources/versions/limitations with findings. Proposals become approved only through Sharon's explicit decision at a concrete revision; identify guarded amendments before editing. Research/approval does not authorize a merge.

Alignment: ready for the M1 draft; no concrete milestone revision approved for implementation. See [history](history/2026-11-15-kickoff.md).

## Follow-up decisions — 2026-11-15

| ID | State | Decision |
|---|---|---|
| LD10 | Explicit user direction | Docker service dependence is acceptable; component Compose definitions and one umbrella entry point; does not decide loss/durability during outage |
| LD11 | Explicit golden rule | Backend replacement must be easy and demonstrated; no provider logger imports scattered through workflows; broker not mandated |
| LD12 | Explicit user requirement | Clear prerequisites/setup/version guidance, component/all-services entry point, logs CLI mirroring langfuse flags and working-path checks |
| LD13 | Explicit user constraint | Configuration-first; use existing logging infrastructure; discuss any necessary extra custom code; Apache-2.0 option required, not MIT-only |
| LD14 | Superseded recommendation; never adopted | Structlog/standard logging emits JSONL; Fluent Bit tails/ships; single-node VictoriaLogs supplies store/query/UI. No custom broker or extra vlagent required for this candidate |

[Research findings](research/2026-11-15-victorialogs.md) support the configuration boundary but do not prove runtime replacement or certify all transitive licenses. [Action items](action-items.md) track Compose/setup/CLI work. LQ01 now concerns service outages, not whether Docker services are allowed. Exact CLI install/smoke semantics and license-policy scope for bundled dependencies remain to settle before implementation.

## Runner lifecycle and direct OTLP — 2026-11-15

| ID | State | Decision |
|---|---|---|
| LD15 | User-selected design direction | Python standard logging bridged by OpenTelemetry directly to local VictoriaLogs; built-in store/query/UI. No mandatory structlog, JSONL files, Fluent Bit, Collector or broker. Exact milestone contracts remain draft. |
| LD16 | Explicit user agreement | A CLI run invocation initializes logging once through the runner/composition boundary; workflows and agents do not initialize providers. Use a Python context manager (Java try-with-resources equivalent) for bounded flush/shutdown on normal exit and exception unwinding. No generic startup registry, package distribution or public API work now. |
| LD17 | Explicit user agreement | Small log_info/log_warning/log_error helpers take context and message; optional event-specific fields are required as an optional argument. ExecutionContext is selected under LD22; detailed field contract and exceptions remain to design. Context remains data-only. |
| LD18 | Explicit user clarification | Local self-hosted configuration, documented behavior and pinned versions are sufficient research scope. No source audit or exhaustive network/read/write investigation. Retain accurate distinction between local configuration and absolute host-wide exfiltration guarantees. |
| LD19 | User requested draft | Begin with M1 configuration sanity: minimal component Compose, direct Python export, synthetic context/message and local UI inspection. CLI service management, installer, Langfuse Compose migration and production runner integration are later work. |

The earlier chat's hardcoded endpoint illustrated transport only. Implementation must use existing external configuration ownership (LOG-14 / principle 6), validate a local destination and keep logging exporter settings separate from Langfuse.

M1 proposes an opt-in smoke command that exits after flushing. It is not the production logging outage policy. No durable queue, exactly-once delivery or replay is promised. LQ01 remains open before production runner integration.

Alignment checkpoint: immutable context/native tracing already exist; logging does not. Earlier collector-first recommendations are historical. Official OTLP/Docker/Python sources support the direction; no Docker runtime was available for verification. This draft changes no guarded baseline. Ready to draft M1 design/tests/plan; exact approved revision and implementation authorization are still absent. See [current source notes](research/2026-11-15-direct-otlp.md).

## Context-manager cleanup and milestone outline — 2026-11-15

Sharon explicitly requested scoped resource management: initialize on entering the runner's logging scope, then attempt bounded flush/shutdown when leaving it, including exceptions. Preserve the original workflow exception; do not suppress it or replace it with a cleanup failure. This is not guaranteed delivery: forced process termination, interpreter crash or power loss cannot guarantee cleanup, and an unavailable destination cannot guarantee export.

Context + message are required; optional event-specific fields are supported. Correlation/workflow/agent identity comes from context, not caller repetition or optional-field overrides. Exact optional-field syntax/types remain M2 design work.

Sharon requested the complete milestone outline before reviewing M1. M1 alone has a concrete draft. M2 remains proposed; M3 (component/umbrella Compose) and M4 (setup and management CLI) are now explicit proposals for discussion, not accepted scope or approved implementation. Automatic observation/event capture stays deferred without a milestone commitment.

## Milestone sequencing clarification — 2026-11-15

Sharon agreed to keep the four-part outline for now and requested sequential discussion of open questions before completing the designs together. This is planning direction, not approval of detailed contracts or implementation.

- M1 creates logging as a separate component Compose file from the beginning.
- M2 adds application logging and runner lifecycle integration.
- M3 adds the main Compose entry point referencing component Compose files, adapting the existing Langfuse definition only as needed while preserving data/project identity. It does not first combine services and then split them.
- M4 covers setup and management through the CLI; exact commands remain to discuss.

Create the remaining design/test/plan documents as answers settle their contracts, keeping shared decisions canonical. First unresolved production question: what happens when VictoriaLogs is unavailable at run start or during a run? Present a concrete simple policy for discussion; do not silently assume reliable delivery or fail-open/fail-closed behavior.

## Superseded strict-logging interpretation — 2026-11-15

LD20 — Superseded by LD21. Earlier interpretation was broader than Sharon intended: application YAML owns a boolean strict_logging setting (final nesting to follow the existing configuration model). true makes detected logging unavailability/failure fail the run; false permits continued workflow execution. Best-effort diagnostics use the terminal so they do not depend on the unavailable backend. Default remains to ask; no hardcoded default selected.

Apply this policy to startup and runtime/export/cleanup failures. M2 must explicitly design how asynchronous batch-export failures reach the runner, when failure is detected and how the CLI reports a non-success outcome. Do not assume an SDK worker exception automatically propagates to workflow code. Strict mode is not a guarantee that no work occurs after a backend outage or that every record is durable.

Keep workflow/business errors distinct from logging infrastructure failures. If the workflow already failed, retain its original exception and report the logging failure separately. No remote fallback; disk spool/replay remains unselected. This decision settles policy selection, not the still-draft transport/error implementation.

## Initialization requirement only — 2026-11-15

LD21 — Explicit user clarification, superseding LD20: each integration owns required_start alongside enabled in its existing application YAML settings. Default required_start is true. For Langfuse this belongs under integrations.langfuse; logging uses its own integration settings. No top-level logging/tracing policy block, strict_logging flag or configurable runtime-failure mode.

When an integration is enabled, required_start=true prevents workflow execution if that integration's initialization fails. required_start=false permits proceeding with a terminal warning if initialization fails. Disabled integrations do not initialize or block startup. This latter false/disabled behavior follows the setting's scope.

After workflow execution begins, logging/tracing infrastructure failures only warn; they must not stop the workflow or change its outcome. Cleanup/flush failures also only warn, preserving any original workflow exception. SDK setup, scope/update and export boundaries must be covered by the implementation design without swallowing business/workflow exceptions.

required_start means successful initialization, as clarified by Sharon. It does not add a mandatory network readiness/authentication/ingestion round trip. SDK construction may succeed while a backend is unreachable, so this setting alone cannot promise service availability or delivery. Operational connectivity checks remain separate.

Langfuse currently lacks this consistent policy. Aligning it is requested design scope for M2, not an already implemented behavior. Identify any necessary amendments to its guarded baseline before implementation; this update changes only the logging design record.

## ExecutionContext selected — 2026-11-15

LD22 — Sharon explicitly agreed to use the existing ExecutionContext as the required context argument for log_info/log_warning/log_error and other agreed level helpers. Extract correlation_id from ExecutionContext and workflow_id, workflow_run_id, agent_type and agent_run_id from its observability member. Reuse existing agent-context derivation; no new context type, mutation or SDK/client handle in context.

Context and message are required. Event-specific fields remain optional and cannot overwrite context identity. Extract selected logging attributes rather than serializing the entire context. Exact optional-field syntax/types and collision diagnostics remain detailed M2 design work.

## Application-wide diagnostic coverage — 2026-11-15

LD23 — Sharon accepted automatic workflow started/completed/failed records and delegated useful placement beyond workflow/agent business code, emphasizing debugging the surrounding application infrastructure. "Automatic" means explicit calls in shared runner/infrastructure code, not magic interception or blanket duplication of Langfuse observations.

M2 should cover useful configuration/setup, workflow selection/construction, lifecycle and integration diagnostics, with detailed DEBUG records where they explain execution. ERROR records describe operational exceptions at the handling/reporting boundary. Avoid repeatedly logging the same propagated exception at every layer; caught/recovered operational failures still need a diagnostic without changing workflow outcome. Expected control-flow exceptions are not automatically failures. No global exception hook or capture of every SDK internal exception is selected.

Keep extraction distinct from emission: helpers read the selected identity fields from ExecutionContext; owning application code decides when to emit. No whole-context/configuration serialization. Agent identity comes from the supplied derived context; this does not authorize Stage 04 event capture.

Before ExecutionContext or the logging pipeline exists, use safe terminal diagnostics without invented workflow/agent IDs. The context-based helper contract remains required for execution logs. Initialization/export/cleanup failures follow LD21; diagnostics must not recurse through the failing exporter. Exact startup diagnostic transport, level filtering, sanitized error details and stack-trace treatment remain M2 design details.

These are coverage requirements and delegated placement decisions, not approval of a completed M2 implementation contract.

## Standard severity filtering — 2026-11-15

LD24 — Sharon accepted standard logging levels and a configurable minimum level at integrations.logging.level, default DEBUG for the current development phase. INFO excludes DEBUG; WARNING/ERROR represent progressively more severe diagnostics. Apply this setting to application logging, not a global change to every third-party SDK logger. DEBUG does not authorize dumping secrets, entire contexts/configuration or arbitrary inputs/outputs. Routine SDK mechanics remain implementation design details rather than additional product-policy questions.

## Seven-day retention — 2026-11-15

LD25 — Sharon accepted seven days as the default VictoriaLogs log retention. Configure through the logging component's Compose settings using the existing retentionPeriod option; VictoriaLogs manages expiration of older records. This now applies to the planned application setup as well as the M1 probe. It does not select disk-size limits, backup or durable delivery guarantees.
