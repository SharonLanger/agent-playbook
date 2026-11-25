# S04.M1 design — draft

This is a design working document. [Stage-wide approved choices](../decisions.md) and the [M1 boundary](../milestone-plan.md#s04m1--behavioral-contracts-and-typed-data) govern it. Specific schema and validation choices below remain open until reviewed with Sharon.

## Goal and ownership

M1 makes incomplete concrete implementations detectable and makes event/request/result data importable independently of CrewAI, Langfuse and native SDKs. The application agent implements `Agent.handle_event`. A concrete adapter later implements `ExecutionAdapter.run`, and a concrete mapper later implements `EventMapper.map`. A common harness will compose their behavior in M2. Native provider types remain inside adapters.

| Approved contract | M1 responsibility | Source |
|---|---|---|
| `Agent.handle_event(event: AgentEvent) -> None` | Required async role method. An explicit no-op is permitted. | D24–D26 |
| `ExecutionAdapter.run(request: ExecutionRequest, *, on_event: EventHandler) -> ExecutionResult` | Required async adapter method. | D26 |
| `EventMapper.map(native_message) -> list[AgentEvent]` | Required mapper method, generic over native message type. | D26 |
| `EventHandler` | `Callable[[AgentEvent], Awaitable[None]]` signature. | D25/D26 |

The [specification](../specifications.md) records the initial five classes and fields. `ExecutionStarted` has no additional payload. `TextProduced` has `text_id` and `text`. `ToolCallObserved` has nullable `tool_call_id`, `tool_name` and optional input. `ToolResultObserved` has nullable `tool_call_id`, `output` and `status` of succeeded/failed/unknown. `ExecutionFinished` carries `ExecutionResult`. Result data has status, final text and error as accepted in D36. D37 selects frozen dataclasses for shared event/result data, status enums, and a five-class union. D38 forbids fabricating a missing tool relationship.

D42–D49 constrain the later harness contract. It emits start before adapter invocation and finish on normal return, carries the same returned result, awaits event handlers sequentially, and propagates callback/adapter exceptions with the documented terminal and cleanup rules. M1 expresses only the contracts needed for M2 to fulfill those promises.

## Boundary and proposed placement

The [milestone plan](../milestone-plan.md#s04m1--behavioral-contracts-and-typed-data) suggests `app/src/agent_playbook/agents/agent.py` and separate `execution/` contract and model files. The design agent will confirm precise module paths against current code and [project structure](../../../project-structure.md). Keep each behavioral ABC in its own file. Shared data classes may share an owner file. Focused tests belong in `app/tests/`.

M1 does not construct a harness, fake/provider adapter, demo role, workflow or runtime telemetry. Test-only concrete subclasses may exercise ABC signatures. M2 owns the working harness and fake adapter, M3 the demo role, M4 the CrewAI invocation, and Stage 05 native providers.

## Open contract choices

| Question | Decision required before design lock |
|---|---|
| Request/result details | Exact required/optional fields, outcome distinctions, defaults and invalid input behavior. Respect D36/D42. |
| Settings and permissions | Available, allowed and disallowed tool semantics, policy enforcement responsibility, unsupported capability behavior and defaults. Preserve honest provider-specific differences. |
| Identity and validation | Nullable IDs, JSON value boundaries, frozen data with nested mutation, event-local identity, and whether a portable representation is needed now. |
| Error expression | Contract-level behavior for missing evidence, slow handlers, cleanup diagnostics and cancellation where necessary. D43–D49 already settle the documented primary failure and event order. |
| Guarded ownership | Exact amendment to architecture and project structure for execution-owned mapping and role placement. Present the logical diff to Sharon first. |

Blocking hooks, control responses, service transport, logging export, real coder/reviewer, tool execution and provider parity remain outside M1. Research references are architecture inputs, not adopted libraries or evidence of parity.
