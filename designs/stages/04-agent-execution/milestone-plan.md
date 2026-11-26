# Agent execution foundation — milestone boundaries

> **DO NOT MERGE PR #45 — MERGE LAST, AFTER ALL STAGE 04 IMPLEMENTATION PRs.** This is the ongoing design workspace. Keep it open through every milestone; reconcile final documentation after the entire Stage 04 implementation is accepted and merged, then merge this PR only with Sharon's explicit final authorization. Individual design/milestone approval does not authorize merging it.

Revision: 15 · 2026-11-26 · Owner: Sharon
Status: **overall milestone boundaries and BC03 gates approved (D40); detailed milestone design/test/plan not yet locked; no implementation authorization.**

[Start here](README.md) · [Specification](specifications.md) · [Decision board](decisions.md) · [Repository reconciliation](repository-updates.md)

Use the [stage README](README.md#canonical-milestone-and-readiness-index) for current milestone status and the [current M1 reconciliation](decisions.md#current-m1-decision-reconciliation--2026-11-26) for current prerequisites. This plan owns boundaries and their change history. Earlier revision checkpoints retain the state known at the time.

## Authority and sequence

Sharon authorized this planning PR, explicit milestone boundaries and a plan-first change process. The shared-foundation → deterministic-agent → CrewAI demonstration direction is accepted in the discussion. D40 approves the four milestone boundaries and BC03 prerequisite gates. Detailed acceptance cases and design/test/plan revisions still require their own approval.

`S04.M1`–`S04.M4` are stable local planning IDs. They are distinct from Stage 02's M4.1/M4.2/M4.3. They do not activate Stage 04, change the roadmap's order, or move real native integration to a newly approved global stage. Each milestone later needs an approved detailed design, scoped implementation authorization and its own evidence. An approved plan is not proof of implementation; passing tests is not user acceptance or merge approval.

P08's six design topics still guide the design work within these delivery checkpoints. Publishing a delivery plan early does not resolve its open schemas and policies.

## Common boundary

**Within this planned foundation:** shared typed contracts/data, a small common execution wrapper, fake native messages translated by a fake mapper, a deterministic application agent, and finally one maintained CrewAI demonstration.

**Outside all four milestones unless deliberately amended:** real Claude/Codex SDKs and concrete native adapters/mappers; real coder/reviewer/verifier roles; new Stage 02 context fields or propagation; Langfuse instrumentation/export; a logging backend/store/viewer; a second context or tracing system; human approval waiting; session pooling/replay; durable queues/event buses; automatic task retries; a custom filesystem-permission or tool-policy contradiction engine; wholesale external-framework/UI adoption; roadmap changes. Existing contracts and logging requirements remain recorded, with integration deferred rather than declared fulfilled.

Different folders reduce textual overlap; shared contracts still create dependencies. Design may proceed in parallel with PR #43. M1–M3 deliver standalone behavior without required context. M4 must recheck the merged application/context signatures and concrete dependency evidence before implementation. No invented workflow IDs or placeholder context ABC are permitted to hide a missing agreement.

## Milestone overview

| ID | Delivers | Stops before | Depends on |
|---|---|---|---|
| S04.M1 | Three ABCs, callback and small typed event/request/result/settings/permission models | Harness, fake implementations, concrete agent or workflow | Detailed data/behavior decisions and canonical reconciliation |
| S04.M2 | Shared harness plus fake adapter and fake native-message mapper | DemoAgent, CrewAI wiring, native integrations, actual log/trace export | Approved/verified M1 contracts and local failure/lifetime policy |
| S04.M3 | One deterministic DemoAgent using the shared path | Coder/reviewer behavior and workflow integration | Approved/verified M2; agreed task entry/result path |
| S04.M4 | One maintained CrewAI flow invokes DemoAgent and reports success/failure | Native providers, richer orchestration, context/logging redesign | Approved/verified M3 and reconciled current workflow/context boundary |

## S04.M1 — behavioral contracts and typed data

**Goal:** make the owned boundary concrete enough that incomplete implementations and incompatible signatures can be detected without introducing a provider.

**In scope:** `Agent.handle_event`, `ExecutionAdapter.run`, `EventMapper.map`, the `EventHandler` callback; the smallest agreed event union, request/result and basic settings/permission data; meaningful boundary validation. Each behavioral interface remains in its separate accepted module. Data classes may share their owner module. Runtime models must not import SDK, CrewAI or Langfuse types.

**Out of scope:** production harness behavior, fake or native adapter/mapper implementations, DemoAgent, role catalogue, workflow registration, context forwarding, logging backend. Tiny test subclasses used to verify the ABC/type contract are test fixtures, not the M2 fake implementation.

**Placement:** proposed runtime files under `app/src/agent_playbook/agents/agent.py` and `execution/{contracts,events.py,request.py,result.py,settings.py,permissions.py}`; tests under maintained `app/tests/` owners. Exact test/model choices belong in the detailed M1 design. No empty coder/reviewer/provider folders are required.

**Entry / decisions to close:** Q01/Q02/Q08 for event/data semantics and result/error representation; Q04/Q26 for the initial configuration subset; Q10 for the contract-level failure promises; C01/Q12 for canonical ownership. Resolve only the portions required by M1, explicitly defer the rest. D34 accepts the five initial event names and basic meanings. D36/D37 subsequently accept event/result fields, status vocabulary and frozen dataclasses. D42–D49 subsequently settle lifecycle ownership, result reuse, sequential delivery and the recorded failure/cleanup policies. D54–D56 settle construction validation, standard exceptions and deep event immutability. Exact request/settings/permission fields/defaults, ID/result invariants, immutable representation/conversion and remaining cleanup/timeout/cancellation details remain open. Do not add required context fields now or silently forbid later context integration.

**Proposed acceptance:** incomplete ordinary subclasses cannot instantiate; a concrete role can explicitly implement a no-op handler; static checking catches incompatible overrides/callbacks; supported data values and genuinely invalid inputs follow the agreed schema; contracts stay independent of native SDKs and roles. Do not write a test solely to assert each filename exists or add a custom metaclass to police every descendant class.

**Exit:** exact schemas and failure declarations reviewed/locked; focused tests and relevant standard quality checks pass at a recorded commit; known limitations and manual review recorded. This milestone does not demonstrate execution or native permission enforcement.

## S04.M2 — common wrapper and deterministic execution

**Goal:** exercise the real application-facing path from request through translation and callbacks to the returned result.

**In scope:** common setup/validation and callback composition, injected adapter selection seam, `FakeAdapter` implementing `run`, a fake mapper implementing `map`, scripted fake native messages, normal and controlled failure outcomes. A test recorder can observe deliveries; it is not a production logging system. Small explicit construction is sufficient; full application YAML/registry wiring belongs to M4 if needed.

**Out of scope:** actual provider SDKs, native mapper implementations, role logic, CrewAI integration, session reuse/pooling, native permission enforcement, tracing/export and log persistence. Logging remains a requirement to integrate with its owning track, not a second subsystem built here.

**Placement:** proposed `execution/harness.py` and `execution/adapters/fake.py`; a separate concrete fake-mapper file is a candidate if that is clearest. Choose its exact path in the detailed design; the mapper ABC already has its own file. Shared fixtures/tests belong in maintained test folders, never personal examples.

**Entry / decisions to close:** Q01/Q02 terminal owner and event/result agreement, Q10 callback/stream failure behavior, Q30 instance and mapper-state lifetime. Q17 must distinguish what can be observed/tested now from actual deferred logging delivery. Native cancellation guarantees and unknown future transports need not be invented to complete the fake.

**Fake fidelity requirement (accepted direction):** fake messages must pass through the concrete mapper; emitting final shared events directly must not be the only path. Use evidence from the preserved native/reference research when choosing representative shapes. This demonstrates local translation mechanics, not equivalence to a live provider.

**Proposed acceptance:** repeatable success, paired simulated tool evidence, zero/one/multiple events per message where agreed, repeated invocations without leaked state, controlled adapter and handler failure, cleanup/result behavior and explicit unsupported-policy handling under the selected contract. Validate terminal-event/result consistency if a terminal event is selected. Prefer fixed scripts; e.g. a request for five simulated calls produces five ordered call/result pairs. Exact scenario input/event count, failure types and optional seeded variation remain Q36. Never run real tools merely to generate a fake tool event.

**Exit:** agreed contract behavior demonstrated without model credentials, SDK downloads, a server or Stage 02 context implementation. This is foundation acceptance, not native capability or full logging acceptance.

## S04.M3 — one deterministic application agent

**Goal:** show that an application agent can use the foundation and implement the mandatory role handler.

**In scope:** one `DemoAgent`, typed task input/output as needed, explicit `handle_event`, harness injection, predictable output and controlled failure; independent invocation outside CrewAI. The role interprets its result while the adapter remains role-agnostic.

**Out of scope:** real reviewer/coder prompts and verdicts; workflow routing; additional Agent ABC methods merely for symmetry; helper files without an actual responsibility; real SDK integrations.

**Placement:** candidate `agents/demo/` with `agent.py` and only justified role data/helper modules, plus maintained tests. This adds a demo for the first exercise; it does not silently delete the accepted longer-term coder/reviewer tree. Q34 still governs role helper organization.

**Entry / decisions to close:** Q33 exact task entry and result ownership; Q34 handler/helper responsibilities; Q35 standalone context integration remains deferred; M3 must work without constructing context or invented workflow IDs. The task method need not become a new mandatory Agent ABC method without approval.

**Proposed acceptance:** a caller receives predictable typed output through DemoAgent → harness → fake adapter → fake mapper → shared callback; the role handler observes agreed events; a controlled failure propagates honestly. If Sharon's suggested visible delay is retained, it is configurable, with short/zero duration in automated checks. Exact delay/default/input is still Q36.

**Exit:** a simple reproducible standalone demonstration with documented expected outcomes, no live provider required, and no claim that a real reviewer/coder exists.

## S04.M4 — maintained CrewAI demonstration

**Goal:** exercise the same path through the application's actual workflow contract and CrewAI Flow.

**In scope:** one small maintained workflow calls DemoAgent through an ordinary step; supported application assembly/configuration selects the deterministic dependency; typed workflow input/output, explicit successful and failed outcomes, focused public instructions when implemented.

**Out of scope:** replacing workflow lifecycle/registry, inventing another scheduler, adding parallel orchestration or recovery, real agents, changing context models, new tracing/logging infrastructure, personal examples.

**Placement:** a named package under maintained `workflows/`, narrowly necessary assembly/configuration integration, independent `app/tests/` fixtures, and official `app/docs/` updates alongside working behavior. Exact workflow ID, source paths and CLI/YAML entry are a later detailed-design choice.

**Entry:** M3 accepted for integration; check the [merged workflow/context contract](../02-langfuse/m4-workflow-integration/README.md) on then-current main. Reconcile constructors/context injection and the synchronous/asynchronous call boundary with the existing Workflow ABC. Raise conflicts first. Stage 02 does not become complete through this exercise and is not redesigned here.

**Proposed acceptance:** a real maintained CrewAI Flow reaches the agent path; success returns validated output through the normal runner/CLI; a controlled agent failure is classified as failure and does not become a success; invalid workflow input follows existing rules; repeated invocations are isolated; ordinary checks need no model/server. Define exact commands, expected values, tests and applicable release checks in its detailed design.

**Exit:** executable instructions and revision-specific evidence; existing workflow behavior preserved; Sharon's review/acceptance recorded separately from technical verification. This establishes deterministic integration only. Native providers require their own later design and acceptance.

## Boundary-change protocol — required every iteration

1. Read this plan, the **entire current specification and decision board**, the relevant history, governing documents and any approved affected milestone design. Check current branch/PR status.
2. For a scope, dependency, deliverable or acceptance-boundary change, **first add a proposed delta here**: affected milestone(s), old/new inclusion or exclusion, reason, impacted decision/spec IDs, dependencies and acceptance effects. Mark it **Pending**. Do not rewrite the effective boundary yet.
3. Cross-check that proposal against all existing decisions/specification and guarded authorities, including other affected milestones. If it contradicts an agreement, explain the conflict and consequences to Sharon **before changing agreed meaning**; preserve the earlier decision. Use existing scoped authorization where it applies. A plan edit itself grants no authorization.
4. After the change is agreed, update the effective milestone boundary, record a new or superseding decision with rationale/alternatives/evidence, and update the specification plus affected detailed designs/acceptance cases **in the same change/PR**. Mark the delta **Accepted and applied**, linking the approval. If rejected or deferred, retain the proposal and reason without changing the effective scope.
5. Check cross-document consistency, links and status; rebuild/check Atlas when affected. Implementation follows only the approved/locked milestone design and actual authorization. Never change code first and retrofit the plan to excuse scope drift.

Changes within a boundary still require a decision/spec consistency check and appropriate record updates. Editorial corrections need not manufacture a scope-change decision. New substantive agreements and answered/deferred questions must remain traceable. No scheduled background editing is implied by “every iteration.”

### Boundary change log

| ID | Milestone / delta | Authority and status | Consistency / consequences |
|---|---|---|---|
| BC01 | Establish this first four-checkpoint draft; explicit inclusions, exclusions, prerequisites and proposed exits | **Draft for review.** Sharon authorized creation of the design PR and bounded milestone planning; no implementation lock. | Preserves D02–D26. D27–D32 record later planning/deferral/process choices. Four allocations and exact acceptance details await review. |

For later deltas use stable BC02, BC03… entries with the fields in the protocol. Do not recycle IDs or delete rejected proposals.

## Next design step

Continue the [S04.M1 draft package](m1-contracts-models/README.md) in PR #72 using the [reconciled remaining-work list](decisions.md#seven-item-remaining-work-list-reconciled). Earlier approvals remain in force. Suggested next topic is the exact request schema, followed by the initial settings/permission subset. Complete meaningful acceptance cases and file-specific canonical amendments before requesting approval of the detailed design/test/plan. The draft package exists; no implementation-ready brief or approved candidate SHA exists.

## Revision 2 checkpoint — 2026-11-14

BC02: **Accepted and applied — process boundary, no runtime scope expansion.** Sharon explicitly requires PR #45 to remain the ongoing design workspace and merge last, after the entire Stage 04 implementation is merged. D33 records this order. Milestone implementation PRs must not merge this design PR as a prerequisite; carry the approved, necessary milestone design/authority amendments into their own reviewable changes, preserve the remaining planning/history here, and reconcile the workspace as implementations merge. Exact branching/cherry-pick choices belong to each implementation handoff; never copy the whole design PR just to bypass this order. Final merge still needs explicit authorization.

D34: **Accepted event catalogue within existing S04.M1 scope.** ExecutionStarted, TextProduced, ToolCallObserved, ToolResultObserved and ExecutionFinished names/basic meanings are approved. Their payloads, emission owner, failure/delivery guarantees and result relationship remain open. This resolves part of Q01, not all of P01. No S04.M1–M4 implementation or changed milestone allocation is authorized.

Current M1 design task sequence: (1) accepted event catalogue → payloads, (2) completion owner and terminal/result relationship, (3) request/result schema, (4) minimal settings/permissions, (5) contract-level failure behavior, (6) detailed design and meaningful acceptance cases before implementation approval. Later steps may expose changes to earlier ones; follow the boundary-change protocol.

## Field-design checkpoint — revision 16

D36 accepts the basic event/result field set, with tool_call_id naming. This closes that portion of M1 data design without changing the milestone boundary. Earlier payload-open statements describe earlier checkpoints; validation, missing-ID fallback, envelope identity, terminal ownership and delivery guarantees remain open. No new BC entry or implementation authorization follows from acceptance within the existing boundary.

## Current design checkpoint — revision 17

D37/D38 approve event/result dataclasses, role match dispatch and no guessed tool pairing within existing M1 scope. The reviewer is an illustration, not a new role deliverable. Begin M1 detailed design now; settle lifecycle ownership/result consistency, callback failure/order, request/settings/permissions and validation there. Before locking, reconcile requirements/decisions with then-current canonical sources and resolve C01. Prepare milestone design, acceptance cases and implementation handoff; no implementation or later-milestone expansion is approved.

## BC03 — explicit dependency gates for parallel delivery

**Accepted and applied under D40 on 2026-11-15.** Historical allocation: M1/M2 independent, M3/M4 recheck context before implementation, with context integration generally deferred. Accepted refinement: M1–M3 demonstrate a genuinely standalone foundation without required context construction/imports; M4 alone connects to actual application/workflow boundaries once its specific dependencies are ready. Preserve M1–M4 IDs and core outcomes. Do not quietly add context propagation or tracing acceptance to an already approved milestone.

| Milestone | Standalone outcome | Approved prerequisite gate | External dependency |
|---|---|---|---|
| S04.M1 | Importable typed contracts/events/result/settings/permission data | Approved and locked M1 design/test/plan, canonical C01 reconciliation as applicable | No Stage 02/03 completion, Langfuse or context object required |
| S04.M2 | Request through fake native messages, mapper and callbacks to a result | M1 accepted and merged; M2 design/test/plan approved | No context construction, tracing service or Stage 03 patterns |
| S04.M3 | DemoAgent runs directly with deterministic success/failure | M2 accepted and merged; M3 task-entry design/test/plan approved | No workflow invocation/IDs or context required for standalone exercise |
| S04.M4 | Same agent path through one maintained CrewAI workflow | M3 accepted/merged; actual workflow/context contracts merged, checked for compatibility and necessary decisions approved; M4 design/test/plan approved | Reuse existing context at the integration boundary only where needed; never fake required IDs |

M1–M3 must be useful and testable without pending integration. Their tests prove their bounded contracts, not future propagation/telemetry. M4 is blocked on missing concrete prerequisites, not automatically on all of Stage 02 or Stage 03. A simple single-agent workflow has no proposed dependency on advanced Stage 03 branching/parallel joins. If selected behavior later needs one, record that exact accepted/merged capability as a gate before coding. Tracing acceptance needs its own explicit scope and prerequisite; no new Langfuse work is added here.

Gate record for each detailed milestone: required capability/document, owner, approved version or merged SHA, verification evidence, Ready/Blocked/Not required status, and the work specifically blocked. Design/research can proceed while implementation of the dependent behavior waits. External prerequisites are rechecked at handoff; do not mark them Ready from this proposal alone.

Deferred slice rule: finish the independent behavior, name the later integration slice and owning milestone/workstream, describe its trigger and completion evidence. Do not create context=None placeholders or duplicate context classes simply to hide a dependency. If an event's actual meaning requires context, defer that event/capability or explicitly split its scope before approval; do not emit an incomplete event and call it complete. The existing five accepted event payloads do not require context. Later mandatory fields/signature changes require explicit impact review, not a promise of zero rework.

BC03 impacts D27/Q35/Q09 and M3/M4 entry wording, not accepted event fields, native ownership or the Stage 05 boundary. Any new agent-context propagation acceptance beyond existing M4 scope must be separately approved here before being assigned. AgentContext is exploratory; first inspect existing ExecutionContext.for_agent and standalone needs. No M5/M7 is created, no Stage 02/03 file is changed, no current implementation baseline is amended.

## Design progression and readiness — D40/D41

The stage README owns the canonical milestone/status index. Boundaries and dependency gates are accepted; no exact implementation contract is locked. Each detailed milestone package will live in its own folder with README.md, design.md, test-cases.md and implementation-plan.md, created together when that milestone enters detailed design. Do not publish speculative later designs as approved or create empty review PASS reports. Existing specifications.md remains the shared requirement owner rather than introducing a competing requirements.md.

| Milestone / future folder | Design readiness | Resolve in that design | Wait for predecessor / avoid now |
|---|---|---|---|
| M1 / m1-contracts-models | Draft in #72; continue remaining choices | Exact request/settings/permissions and ID/result constraints; concrete immutable representation/conversion; remaining diagnostics and scoped timeout/cancellation choices; C01 guarded amendments. D42–D49/D54–D56 are settled | No Stage 02/03 wait. Do not specify real SDK mapping or build harness code |
| M2 / m2-fake-execution | Boundary ready; detailed design waits for M1 contract approval, with review against merged M1 before implementation | Fake scripts/native fixtures, mapper isolation, harness cleanup/failure behavior and observable acceptance | M1 settles field shape, lifecycle and callback promises; do not reopen them speculatively |
| M3 / m3-demo-agent | Boundary ready; detailed design waits for M2 design to settle the executable path; implementation waits for accepted/merged M2 | One simple task/input/result, no-op versus useful handler behavior, optional visible delay, repeated invocation evidence | Use M1 request/result and M2 fake behavior. Do not design reviewer prompts, AgentContext or a role framework |
| M4 / m4-workflow-integration | Boundary/dependencies ready to assess; concrete design waits for M3's invocation contract and current main compatibility review | Workflow input/output and sync/async entry, construction/config selection, context at the integration boundary only where necessary, success/failure CLI evidence | Reuse actual merged context. No Stage 03 parallel/join requirement unless explicitly added; no tracing/logging redesign |

Detailed design may begin after the prior design is approved without waiting for all implementation to finish if the boundary is stable; record any assumptions and recheck actual predecessor acceptance/merge before implementation handoff. Default focus is one milestone at a time. In parallel, collect bounded source evidence or prerequisite status that will still be useful; do not freeze dependent signatures early.

Every milestone entry requires: approved design/test/plan at a pinned SHA; its listed prerequisite capabilities accepted/merged and checked; scoped implementation authorization. Every exit requires meaningful tests, reviewed evidence, explicit acceptance and separate implementation merge. Stage Design PR stays open. These are not yet satisfied by this planning update.

Current next action: continue the existing M1 package from the reconciled residual choices. Preserve approved lifecycle/failure/validation/immutability policy and complete the design/test/plan before lock. Later milestone questions remain with their owners; they do not block M1.

## Lifecycle checkpoint — revision 20

D42 settles harness-owned lifecycle notifications and normal result reuse within M1 contracts/M2 harness boundaries. Retain one role callback and the empty start payload. No milestone boundary changes; abnormal callback/adapter failure behavior remains open before implementation lock.

## Handler failure checkpoint — revision 21

D43 selects stop-and-propagate within existing M1 contract/M2 harness scope. D44 tracks future per-agent policy/context or injected error behavior as deferred, with no new milestone or current implementation acceptance. Next settle terminal notification after handler failure. Any future customization milestone must pass the boundary-change protocol before assignment; standalone prerequisites are unchanged.

## Terminal-delivery checkpoint — revision 22

D45 closes terminal delivery after handler failure within existing M1/M2 scope: no further callback or terminal retry; cleanup is independent. Adapter-exception outcomes, cleanup-error precedence, cancellation and ordering remain open. No milestone boundary or prerequisite changes.

## Adapter exception checkpoint — revision 23

D46 accepts unexpected adapter exception propagation within M1/M2, keeping returned runtime outcomes distinct. Terminal notification to a healthy handler on that path and cleanup-error precedence remain open. No new milestone, implementation scope or prerequisite changes.

## Adapter terminal-delivery checkpoint — revision 24

D47 closes terminal notification on adapter exceptions: skip it and propagate after independent cleanup. M1/M2 scope and prerequisites are unchanged. Cleanup-error precedence, cancellation and ordering remain open.

## Cleanup precedence checkpoint — revision 25

D48 preserves the original exception and cleanup diagnostic evidence, with a sole cleanup exception propagated normally. Concrete representation, cancellation and ordering remain open within M1/M2. No boundary, prerequisite or logging integration change.

## Sequential callback checkpoint — revision 26

D49 accepts per-execution sequential delivery through the existing async callback. M1 contract/M2 verification scope remains unchanged. Dual sync/async callback support is not selected; cancellation and slow-handler policies remain open.

## BC04 — narrow blocking-hook contract (Pending, 2026-11-16)

Trigger: Sharon asks to evaluate hooks that influence the runtime before it continues, such as providing context before tool execution. He has not approved an implementation or scope expansion. P13 records the proposal and evidence.

Proposed delta: M1 designs one optional typed pre-tool request/response contract, registration/capability behavior and failure/timeout/cancellation semantics. M2 adds one fake native checkpoint proving the action waits, the response is applied, and failure cannot silently continue the action. Existing sequential observation events remain unchanged. Native provider wiring and capability verification remain in Stage 05; M3/M4 do not gain new acceptance obligations automatically.

Before acceptance: agree the first hook's actual response effects and confirm matching semantics against selected SDK surfaces. Unsupported requested capabilities should fail clearly rather than be silently ignored (proposal). Fake evidence cannot establish real-provider support. No new required Agent ABC method, mandatory hooks hierarchy, script runner or generic hook engine is proposed. D26/D34/D49 remain unchanged; D13/D29 native deferral is preserved. Q06 is reopened for this concrete use case. Hook failure handling must be designed explicitly rather than copying notification policies blindly.

Owner/trigger/evidence: Stage 04 design owns this pending contract/scope choice; implementation only after explicit BC04 acceptance and a locked milestone design. Stage 05 owns real mappings and provider tests. Required fake evidence would include waiting before side effects, response translation, failure/timeout behavior and no-hook behavior. Cost/risk: small-to-medium design expansion, moderate fake implementation/tests; native integration remains provider-dependent. No day estimate is justified before defining the first response effect. If rejected/deferred, current M1/M2 boundaries remain unchanged.

## Product acceptance and P14 assessment — revision 28

D50/D51 record the explicit low-coupling requirement and coder/reviewer product target. Stage 04 remains the deterministic foundation; native adapters and real roles remain Stage 05. No roadmap renumbering or implicit M4 expansion. A fake demonstration alone does not satisfy the real product MVP. BC04 remains Pending: request for assessment and conditional support for a small response shape does not approve its complete hook/failure/capability design.

P14 proposes keeping observations, optional hook responses and cancellation controls distinct, with serializable boundary data and shared adapter contract tests. These are design recommendations, not new required ABC methods or remote transport implementation. If cancellation or hooks are added to M1/M2 acceptance, first amend BC04 or add a separately reviewed boundary delta. The product scenario should inform minimal request/settings/artifact/result design without importing all later-stage work into M1.

## Documentation reconciliation — 2026-11-26

D57 updates current M1 readiness/question summaries using D42–D49 and D54–D56. The older dated checkpoints retain their historical state. This is editorial reconciliation within the approved M1 boundary; BC03 remains accepted and BC04 Pending. No inclusion, exclusion, prerequisite or acceptance boundary changes, so no new BC proposal is introduced.
