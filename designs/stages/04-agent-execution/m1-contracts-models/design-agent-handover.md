# Design agent handover — S04.M1

Start with [README.md](README.md) and its complete reading order. This brief is a navigation aid. The Stage 04 specification and decision board are the authoritative record of what Sharon accepted. Read them in full before editing. Do not infer approval from earlier examples or this draft.

## Current continuation point — 2026-11-26

Read the [current M1 decision reconciliation](../decisions.md#current-m1-decision-reconciliation--2026-11-26) before turning an older question table into new questions for Sharon. It maps all seven reported open-item categories to settled choices, precise remaining work and owners. Earlier dated checkpoints retain history; later explicit decisions govern their answered portions.

The current package includes D54 construction-time validation, D55 standard validation exceptions and D56 deeply immutable events. Preserve these alongside D24–D49. Sharon authorized consolidating the history and suggested continuing M1 in the originating conversation; a new session is optional. The repository records remain the continuation source whichever session works next.

M1 is ready for further detailed design, not implementation. No whole-package approval SHA or active implementation handoff exists. Keep #72 and #45 draft/open; #72 targets #45's branch, and #45 merges last.

## Objective

Design a small, enforceable typed contract that lets application agents consume shared events and lets later fake, Claude and Codex adapters implement a common execution boundary. M1 implements contracts and data only. The application already has Python workflow infrastructure, CrewAI Flows, context, tracing and logging. Reuse those contracts where M1 actually needs them. M1 is independently testable without constructing workflow context, a model, native provider, logging service or CrewAI Flow.

## Accepted starting points

- D25/D26 accept three separate ABCs, `Agent.handle_event(event)`, `ExecutionAdapter.run(request, *, on_event)` and `EventMapper.map(native_message)`. `EventHandler` is a typed async callable. Roles handle their own events, adapters stay role agnostic.
- D34/D36–D38 accept five initial event classes, the agreed event/result field baseline, frozen dataclasses, a union type for `AgentEvent`, status enums, match dispatch, and no invented tool-call/result pairing.
- D42–D49 settle normal lifecycle ownership, sequential awaited event delivery, fail-fast callback/adapter exceptions, terminal notification suppression on those exception paths, and preservation of a primary exception with secondary cleanup evidence.
- D39–D41/BC03 keep M1–M3 standalone and gate M4 on its actual workflow/context dependencies. D50/D51 set replaceability and eventual coder/reviewer use as the product target. They do not expand M1 into a real provider or role workflow.
- D16–D18/D21 distinguish tool availability, automatic approval and denial; require autonomous operation or clear failure, native enforcement through supported controls and simple provider-local settings conversion. The initial field/default schema remains open.
- D54/D55 require all locally decidable agreed schema validation at construction, propagated TypeError/ValueError, no substitute object or silent coercion, and diagnostics identifying model/field/rule.
- D56 requires deep immutable event snapshots, including isolation from producer aliases and nested consumer mutation. Exact containers/conversion remain open. New fields/new instances and later hook responses remain possible without approving hooks now.

## Required design work

1. Make the accepted interfaces, event fields, result and statuses precise. Resolve only remaining field meaning, validation, identity and serialization choices needed to build M1.
2. Specify the smallest useful `ExecutionRequest`, settings and permission data. Distinguish available tools, automatic approval and disallowed tools where applicable. State the outcome when a requested setting cannot be guaranteed by an adapter. Sharon has not approved an exact field/default schema.
3. Define contract-level error and cleanup promises consistent with D42–D49. Assign harness implementation to M2. Do not claim that M1 has working execution or provider enforcement.
4. For C01/Q12, show Sharon the exact proposed changes to guarded [architecture](../../../architecture.md) and [project structure](../../../project-structure.md) before changing their approved meaning. Native message mapping belongs to execution, while observability has its own telemetry role.
5. Tie every M1 requirement and decision to behavior in [design.md](design.md), meaningful assertions in [test-cases.md](test-cases.md) and a bounded [implementation-plan.md](implementation-plan.md). Show open choices and any necessary scope change explicitly before a lock.

## Decisions to bring to Sharon

Use the exact residual questions in the [seven-item reconciliation](../decisions.md#seven-item-remaining-work-list-reconciled). Q01/Q02 concern remaining ID/result/request constraints; Q04/Q26 concern initial settings/permissions; Q08 concerns concrete representation/conversion and remaining validation details; Q10 concerns remaining cleanup diagnostics and the necessary timeout/cancellation scope; C01/Q12 concerns precise guarded amendments. Do not reopen event fields/status vocabularies, ABC/callback choices, propagation/terminal/ordering policy, validation timing/exception classes or deep event immutability.

Propose concrete minimal choices with reasons and alternatives, one topic at a time. Start with ExecutionRequest as a suggested next topic. Explain a newly discovered contradiction before changing an approval. Detailed paths, meaningful tests, checks and traceability are work for the design agent to prepare; they are not seven new product decisions for Sharon. P13/BC04 blocking hooks and P14 cancellation/control ideas remain proposals. If adding them to M1, use the pending boundary-change process and obtain explicit approval.

## Success criterion for this design PR

A reviewable M1 design, tests and implementation plan that agree on scope, failure behavior, ownership, paths and acceptance evidence. Record the exact approved commit only after Sharon approves these documents. Preserve alternatives and reasons in the Stage 04 decision board. Subsequent implementation is a separately scoped PR. This focused PR targets the Stage Design branch as an explicit user-requested review checkpoint. PR #45 remains the ongoing stage authority and merges last.
