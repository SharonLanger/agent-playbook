# Design agent handover — S04.M1

Start with [README.md](README.md) and its complete reading order. This brief is a navigation aid. The Stage 04 specification and decision board are the authoritative record of what Sharon accepted. Read them in full before editing. Do not infer approval from earlier examples or this draft.

## Objective

Design a small, enforceable typed contract that lets application agents consume shared events and lets later fake, Claude and Codex adapters implement a common execution boundary. M1 implements contracts and data only. The application already has Python workflow infrastructure, CrewAI Flows, context, tracing and logging. Reuse those contracts where M1 actually needs them. M1 is independently testable without constructing workflow context, a model, native provider, logging service or CrewAI Flow.

## Accepted starting points

- D25/D26 accept three separate ABCs, `Agent.handle_event(event)`, `ExecutionAdapter.run(request, *, on_event)` and `EventMapper.map(native_message)`. `EventHandler` is a typed async callable. Roles handle their own events, adapters stay role agnostic.
- D34/D36–D38 accept five initial event classes, the agreed event/result field baseline, frozen dataclasses, a union type for `AgentEvent`, status enums, match dispatch, and no invented tool-call/result pairing.
- D42–D49 settle normal lifecycle ownership, sequential awaited event delivery, fail-fast callback/adapter exceptions, terminal notification suppression on those exception paths, and preservation of a primary exception with secondary cleanup evidence.
- D39–D41/BC03 keep M1–M3 standalone and gate M4 on its actual workflow/context dependencies. D50/D51 set replaceability and eventual coder/reviewer use as the product target. They do not expand M1 into a real provider or role workflow.

## Required design work

1. Make the accepted interfaces, event fields, result and statuses precise. Resolve only remaining field meaning, validation, identity and serialization choices needed to build M1.
2. Specify the smallest useful `ExecutionRequest`, settings and permission data. Distinguish available tools, automatic approval and disallowed tools where applicable. State the outcome when a requested setting cannot be guaranteed by an adapter. Sharon has not approved an exact field/default schema.
3. Define contract-level error and cleanup promises consistent with D42–D49. Assign harness implementation to M2. Do not claim that M1 has working execution or provider enforcement.
4. For C01/Q12, show Sharon the exact proposed changes to guarded [architecture](../../../architecture.md) and [project structure](../../../project-structure.md) before changing their approved meaning. Native message mapping belongs to execution, while observability has its own telemetry role.
5. Tie every M1 requirement and decision to behavior in [design.md](design.md), meaningful assertions in [test-cases.md](test-cases.md) and a bounded [implementation-plan.md](implementation-plan.md). Show open choices and any necessary scope change explicitly before a lock.

## Decisions to bring to Sharon

Q01/Q02/Q08 for still-open data and validation semantics, Q04/Q26 for settings and permissions, Q10 for any unresolved contract-level failure promises, and C01/Q12 for guarded ownership. Check the latest decision entries before presenting a question since earlier Q summaries predate D42–D49. P13/BC04 blocking hooks and P14 cancellation/control ideas remain proposals. If adding them to M1, use the pending boundary-change process and obtain explicit approval.

## Success criterion for this design PR

A reviewable M1 design, tests and implementation plan that agree on scope, failure behavior, ownership, paths and acceptance evidence. Record the exact approved commit only after Sharon approves these documents. Preserve alternatives and reasons in the Stage 04 decision board. Subsequent implementation is a separately scoped PR. This focused PR targets the Stage Design branch as an explicit user-requested review checkpoint. PR #45 remains the ongoing stage authority and merges last.
