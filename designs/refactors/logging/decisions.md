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
| LQ01 | Must records persist when Docker/storage stops? Continue, stop, buffer or drop? How is loss visible? | Backend/delivery choice |
| LQ02 | Resolved direction: VictoriaLogs store/UI and direct OTLP; exact artifacts and viewer behavior remain to check | M1/M2 |
| LQ03 | Resolved API shape: explicit context + message through small level helpers; exact accepted context type remains open | M2 |
| LQ04 | Field types, reserved keys, exception treatment, redaction and payload limits? | Implementation |
| LQ05 | Retention, rotation, multi-process writers, shutdown, bounded queues/retries and duplicates? | Delivery acceptance |
| LQ06 | Exact first-increment application/framework coverage and one-time error recording boundary? | Coverage/tests |
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
| LD16 | Explicit user agreement | A CLI run invocation initializes logging once through the runner/composition boundary; workflows and agents do not initialize providers. Flush/shutdown in runner cleanup. No generic startup registry, package distribution or public API work now. |
| LD17 | Explicit user agreement | Small log_info/log_warning/log_error helpers take context and message; optional fields remain possible. Exact context type, field contract and exceptions are deferred design details. Context remains data-only. |
| LD18 | Explicit user clarification | Local self-hosted configuration, documented behavior and pinned versions are sufficient research scope. No source audit or exhaustive network/read/write investigation. Retain accurate distinction between local configuration and absolute host-wide exfiltration guarantees. |
| LD19 | User requested draft | Begin with M1 configuration sanity: minimal component Compose, direct Python export, synthetic context/message and local UI inspection. CLI service management, installer, Langfuse Compose migration and production runner integration are later work. |

The earlier chat's hardcoded endpoint illustrated transport only. Implementation must use existing external configuration ownership (LOG-14 / principle 6), validate a local destination and keep logging exporter settings separate from Langfuse.

M1 proposes an opt-in smoke command that exits after flushing. It is not the production logging outage policy. No durable queue, exactly-once delivery or replay is promised. LQ01 remains open before production runner integration.

Alignment checkpoint: immutable context/native tracing already exist; logging does not. Earlier collector-first recommendations are historical. Official OTLP/Docker/Python sources support the direction; no Docker runtime was available for verification. This draft changes no guarded baseline. Ready to draft M1 design/tests/plan; exact approved revision and implementation authorization are still absent. See [current source notes](research/2026-11-15-direct-otlp.md).
