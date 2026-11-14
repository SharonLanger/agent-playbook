# Agent execution foundation — milestone boundaries

> **DO NOT MERGE PR #45 — MERGE LAST, AFTER ALL STAGE 04 IMPLEMENTATION PRs.** This is the ongoing design workspace. Keep it open through every milestone; reconcile final documentation after the entire Stage 04 implementation is accepted and merged, then merge this PR only with Sharon's explicit final authorization. Individual design/milestone approval does not authorize merging it.

Revision: 2 · 2026-11-14 · Owner: Sharon
Status: **draft plan for review; no locked implementation baseline or implementation authorization.**

[Start here](README.md) · [Specification](specifications.md) · [Decision board](decisions.md) · [Repository reconciliation](repository-updates.md)

## Authority and sequence

Sharon authorized this planning PR, explicit milestone boundaries and a plan-first change process. The shared-foundation → deterministic-agent → CrewAI demonstration direction is accepted in the discussion. The detailed allocations and acceptance criteria below are proposed for review, not automatically approved by publication.

`S04.M1`–`S04.M4` are stable local planning IDs. They are distinct from Stage 02's M4.1/M4.2/M4.3. They do not activate Stage 04, change the roadmap's order, or move real native integration to a newly approved global stage. Each milestone later needs an approved detailed design, scoped implementation authorization and its own evidence. An approved plan is not proof of implementation; passing tests is not user acceptance or merge approval.

P08's six design topics still guide the design work within these delivery checkpoints. Publishing a delivery plan early does not resolve its open schemas and policies.

## Common boundary

**Within this planned foundation:** shared typed contracts/data, a small common execution wrapper, fake native messages translated by a fake mapper, a deterministic application agent, and finally one maintained CrewAI demonstration.

**Outside all four milestones unless deliberately amended:** real Claude/Codex SDKs and concrete native adapters/mappers; real coder/reviewer/verifier roles; new Stage 02 context fields or propagation; Langfuse instrumentation/export; a logging backend/store/viewer; a second context or tracing system; human approval waiting; session pooling/replay; durable queues/event buses; automatic task retries; a custom filesystem-permission or tool-policy contradiction engine; wholesale external-framework/UI adoption; roadmap changes. Existing contracts and logging requirements remain recorded, with integration deferred rather than declared fulfilled.

Different folders reduce textual overlap; shared contracts still create dependencies. Design may proceed in parallel with PR #43. M1/M2 can be designed independently of context implementation. M3/M4 must recheck the merged application/context signatures before implementation. No invented workflow IDs or placeholder context ABC are permitted to hide a missing agreement.

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

**Entry / decisions to close:** Q01/Q02/Q08 for event/data semantics and result/error representation; Q04/Q26 for the initial configuration subset; Q10 for the contract-level failure promises; C01/Q12 for canonical ownership. Resolve only the portions required by M1, explicitly defer the rest. D34 accepts the five initial event names and basic meanings. Dataclasses/Pydantic, payload fields, IDs, result status names and terminal-event ownership remain open. Do not add required context fields now or silently forbid later context integration.

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

**Entry / decisions to close:** Q33 exact task entry and result ownership; Q34 handler/helper responsibilities; Q35 standalone context boundary if context has since become mandatory. The task method need not become a new mandatory Agent ABC method without approval.

**Proposed acceptance:** a caller receives predictable typed output through DemoAgent → harness → fake adapter → fake mapper → shared callback; the role handler observes agreed events; a controlled failure propagates honestly. If Sharon's suggested visible delay is retained, it is configurable, with short/zero duration in automated checks. Exact delay/default/input is still Q36.

**Exit:** a simple reproducible standalone demonstration with documented expected outcomes, no live provider required, and no claim that a real reviewer/coder exists.

## S04.M4 — maintained CrewAI demonstration

**Goal:** exercise the same path through the application's actual workflow contract and CrewAI Flow.

**In scope:** one small maintained workflow calls DemoAgent through an ordinary step; supported application assembly/configuration selects the deterministic dependency; typed workflow input/output, explicit successful and failed outcomes, focused public instructions when implemented.

**Out of scope:** replacing workflow lifecycle/registry, inventing another scheduler, adding parallel orchestration or recovery, real agents, changing context models, new tracing/logging infrastructure, personal examples.

**Placement:** a named package under maintained `workflows/`, narrowly necessary assembly/configuration integration, independent `app/tests/` fixtures, and official `app/docs/` updates alongside working behavior. Exact workflow ID, source paths and CLI/YAML entry are a later detailed-design choice.

**Entry:** M3 accepted for integration; inspect then-current main and the actual merged state of PR #43 or its implementation successor. Reconcile constructors/context injection and the synchronous/asynchronous call boundary with the existing Workflow ABC. Raise conflicts first. Stage 02 does not become complete through this exercise and is not redesigned here.

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

Review these boundaries, then develop **S04.M1** one decision at a time: the payloads for the accepted five event types, request/result data and completion ownership first, followed by the basic settings/permission subset. Prepare its detailed design, meaningful acceptance cases and file-specific canonical amendments before asking to lock or implement it. No detailed M1 design or executable implementation brief is claimed to exist yet.

## Revision 2 checkpoint — 2026-11-14

BC02: **Accepted and applied — process boundary, no runtime scope expansion.** Sharon explicitly requires PR #45 to remain the ongoing design workspace and merge last, after the entire Stage 04 implementation is merged. D33 records this order. Milestone implementation PRs must not merge this design PR as a prerequisite; carry the approved, necessary milestone design/authority amendments into their own reviewable changes, preserve the remaining planning/history here, and reconcile the workspace as implementations merge. Exact branching/cherry-pick choices belong to each implementation handoff; never copy the whole design PR just to bypass this order. Final merge still needs explicit authorization.

D34: **Accepted event catalogue within existing S04.M1 scope.** ExecutionStarted, TextProduced, ToolCallObserved, ToolResultObserved and ExecutionFinished names/basic meanings are approved. Their payloads, emission owner, failure/delivery guarantees and result relationship remain open. This resolves part of Q01, not all of P01. No S04.M1–M4 implementation or changed milestone allocation is authorized.

Current M1 design task sequence: (1) accepted event catalogue → payloads, (2) completion owner and terminal/result relationship, (3) request/result schema, (4) minimal settings/permissions, (5) contract-level failure behavior, (6) detailed design and meaningful acceptance cases before implementation approval. Later steps may expose changes to earlier ones; follow the boundary-change protocol.
