# S04.M1 design — draft

This is a design working document. [Stage-wide approved choices](../decisions.md) and the [M1 boundary](../milestone-plan.md#s04m1--behavioral-contracts-and-typed-data) govern it. D54 approves construction-time schema validation and creation-error propagation. D55 selects standard validation exceptions with model/field/rule diagnostics. D56 approves deeply immutable event snapshots. Specific field constraints, concrete representation and remaining diagnostic details remain open. The [current decision reconciliation](../decisions.md#current-m1-decision-reconciliation--2026-11-26) distinguishes inherited approvals from the residual work.

## Goal and ownership

M1 makes incomplete concrete implementations detectable and makes event/request/result data importable independently of CrewAI, Langfuse and native SDKs. The application agent implements `Agent.handle_event`. A concrete adapter later implements `ExecutionAdapter.run`, and a concrete mapper later implements `EventMapper.map`. A common harness will compose their behavior in M2. Native provider types remain inside adapters.

| Approved contract | M1 responsibility | Source |
|---|---|---|
| `Agent.handle_event(event: AgentEvent) -> None` | Required async role method. An explicit no-op is permitted. | D24–D26 |
| `ExecutionAdapter.run(request: ExecutionRequest, *, on_event: EventHandler) -> ExecutionResult` | Required async adapter method. | D26 |
| `EventMapper.map(native_message) -> list[AgentEvent]` | Required mapper method, generic over native message type. | D26 |
| `EventHandler` | `Callable[[AgentEvent], Awaitable[None]]` signature. | D25/D26 |

The [specification](../specifications.md) records the initial five classes and fields. `ExecutionStarted` has no additional payload. `TextProduced` has `text_id` and `text`. `ToolCallObserved` has nullable `tool_call_id`, `tool_name` and optional input. `ToolResultObserved` has nullable `tool_call_id`, `output` and `status` of succeeded/failed/unknown. `ExecutionFinished` carries `ExecutionResult`. Result data has status of completed/failed/cancelled/indeterminate, final_text: str or None, and error: str or None as accepted in D36. D37 selects frozen dataclasses for shared event/result data, status enums, and a five-class union. D38 forbids fabricating a missing tool relationship.

D42–D49 constrain the later harness contract. It emits start before adapter invocation and finish on normal return, carries the same returned result, awaits event handlers sequentially, and propagates callback/adapter exceptions with the documented terminal and cleanup rules. M1 expresses only the contracts needed for M2 to fulfill those promises.

## Construction-time validation — approved D54

Every M1 data model validates its agreed schema during object construction. Validate all constraints decidable from the supplied data at that point: required/type rules, nested JSON values and any agreed value or cross-field invariants. Do not defer these checks until a harness or provider happens to use the object. Invalid construction raises to the caller; no invalid object or substitute result is returned and no silent coercion repairs the input.

For the already accepted fields, this means rejecting examples such as `TextProduced(text_id="text-1", text=42)`, a list supplied as `ToolCallObserved.input` (which requires a JSON object or None), or a native/non-JSON object nested in tool data. These are invalid-input test scenarios, not newly supported input types. Valid nullable values and `unknown` status retain D36/D38's meanings.

The eventual request/settings/permission schemas must follow the same construction-time rule once their fields are agreed. This decision does not invent field constraints, require filesystem/network/provider access during construction, or add D17's excluded tool/policy contradiction engine. Provider support and permission enforcement require later execution/integration evidence. Cross-event relationships cannot be validated from one object, and missing relationships must not be guessed.

Frozen event/result dataclasses remain approved; no new dependency or validation framework is selected. D56 adds deep snapshot immutability for events; exact container representation remains open. D55 selects TypeError for wrong types and ValueError for correctly typed values violating an agreed constraint. Messages identify the model, field and violated rule; caller-visible failure propagates. No custom validation exception is introduced. Exact formatting and multiple-error reporting remain open. M2 owns applying the existing D43–D49 execution/cleanup rules when creation errors escape an adapter or handler.

Traceability: G7/G8 and Q08 → D37/D54/D55 → construction-time rejection/propagation → M1-T05/T08/T09 → implementation step 3 and focused contract tests. Those tests remain planned, not executed.

### Validation exception examples — approved D55

A `TextProduced` constructed with `text=42` raises `TypeError`; its diagnostic identifies `TextProduced`, `text` and the requirement for a string. A correctly typed value violating a subsequently agreed constraint raises `ValueError`; the test matrix must use an actually agreed constraint, not invent a nonempty-string rule. Nested invalid data follows the same type/value distinction. Constructors do not wrap these errors in a custom schema exception.

## Immutable event snapshots — approved D56

All five event variants are immutable after successful construction, including nested tool input/output and the existing immutable result carried by ExecutionFinished. Construction must detach mutable input containers so later producer edits cannot alter the event. Consumers cannot add, replace or remove nested content through supported operations. This is an application data contract, not a security boundary against deliberate Python runtime bypasses.

Meaningful examples: construct an event from a dictionary containing a nested list and dictionary, then modify each original container; the event retains its original values. Attempts to modify the event's nested object/array fail and leave the snapshot unchanged. JSON meaning, array order, null and unknown evidence are preserved. Exact read-only container types, mutation-error details, accepted constructor container types and JSON conversion API remain to be designed before lock. D54/D55 still reject invalid data; freezing valid containers is not permission to coerce invalid input.

Schema evolution remains possible through reviewed fields and newly constructed instances. A future hook may read an immutable request and return a separate new response with additional context. That illustrates extension compatibility, not M1 hook behavior or a promise about any native SDK. Current EventHandler returns None; BC04 remains Pending and no hook fixtures or implementation are added.

Traceability: D37/D54/D56 → immutable validated snapshots → M1-T09/T10/T11 → implementation steps 3–4. Scope is event data; other model representations remain open.

## Boundary and proposed placement

The [milestone plan](../milestone-plan.md#s04m1--behavioral-contracts-and-typed-data) suggests `app/src/agent_playbook/agents/agent.py` and separate `execution/` contract and model files. The design agent will confirm precise module paths against current code and [project structure](../../../project-structure.md). Keep each behavioral ABC in its own file. Shared data classes may share an owner file. Focused tests belong in `app/tests/`.

M1 does not construct a harness, fake/provider adapter, demo role, workflow or runtime telemetry. Test-only concrete subclasses may exercise ABC signatures. M2 owns the working harness and fake adapter, M3 the demo role, M4 the CrewAI invocation, and Stage 05 native providers.

## Open contract choices

This table lists residual choices only. The [decision board](../decisions.md#seven-item-remaining-work-list-reconciled) preserves the approved foundations, alternatives and owners. No closed policy is reopened.

| Item | Remaining work before design lock |
|---|---|
| Request data | Exact task/instruction/settings fields, required/optional/default rules and agreed constraints. Apply D54/D55 validation without reopening its timing or exception policy. |
| Settings and permissions | Initial supported tool/policy/settings subset, defaults and explicit unsupported-request outcome. Preserve D16–D18/D21 and native enforcement responsibility; no custom contradiction engine. |
| Identity and result invariants | Scope/constraints of text_id and tool_call_id, remaining value constraints, valid combinations of status/final_text/error. Keep D36 fields/status vocabularies, D38 no guessing and D42 terminal/result identity. |
| Immutable representation | Exact read-only containers and accepted JSON/container inputs, freezing/copying and conversion to JSON-compatible data. D56's deep immutability is settled; other model representations still require an explicit choice. |
| Failure details | Concrete secondary-cleanup diagnostic representation; identify the minimum necessary slow-handler/cancellation decisions and explicitly defer the remainder. D43–D49 already settle fail-fast propagation, terminal suppression, cleanup precedence and delivery order. M2 implements/verifies the harness. |
| Guarded ownership | Present exact C01/Q12 logical amendments for execution-owned mapping, roles and dependency rules in architecture.md and project-structure.md. Preserve already agreed responsibilities. |
| Approval package | Complete meaningful assertions, exact implementation paths/steps/checks and traceability; present a concrete candidate SHA and remaining blockers for approval. This preparation is the design owner's responsibility. |

Blocking hooks, control responses, service transport, logging export, real coder/reviewer, tool execution and provider parity remain outside M1. Research references are architecture inputs, not adopted libraries or evidence of parity.
