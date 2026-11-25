# Agent Playbook — Execution Specifications

> **DO NOT MERGE PR #45 — MERGE LAST, AFTER ALL STAGE 04 IMPLEMENTATION PRs.** This is the ongoing design workspace. Keep it open through every milestone; reconcile final documentation after the entire Stage 04 implementation is accepted and merged, then merge this PR only with Sharon's explicit final authorization. Individual design/milestone approval does not authorize merging it.

Revision: 32 · Updated: 2026-11-25 · Owner: Sharon
Companion: [Decision board](decisions.md)

The [milestone table](README.md#canonical-milestone-and-readiness-index) owns current status. The [M1 alignment checkpoint](decisions.md#m1-alignment-checkpoint--2026-11-25) records resumed detailed design in PR #72; D54 below settles construction-time validation. Dated sections below preserve their original revision context.

## Status and authority

This is the working specification for the agent-role and execution integration discussion. It records the agreements recoverable from the supplied conversation, its reconstructed handover, and the repository's approved design. It is not a complete transcript and does not claim to recover every historical decision.

**Approved** means explicitly accepted by Sharon in this discussion. **Inherited baseline** means an existing approved repository constraint. **Open** means unresolved; a suggested implementation is not approval. Desired structure does not mean implemented code.

These two records do not silently override guarded repository documents. Before implementation, reconcile any affected canonical design files through their existing design-change process. D31 now authorizes this draft documentation PR. No runtime change, dependency installation, roadmap edit, merge or adoption of a third-party library is authorized. This package is a future-stage planning workspace, not a locked implementation baseline.

## Agreed goals

| ID | Requirement | Decision |
|---|---|---|
| G1 | Use multiple agent runtimes through an application-owned, typed interface. Roles should work with our predefined events. | D02, D04 |
| G2 | Keep the integration small and isolated. Be able to replace a provider or external normalization library with our own implementation. | D02 |
| G3 | Keep agent roles separate from execution/provider mechanics. | D03 |
| G4 | Learn from existing projects and reuse only what is useful; avoid bringing in a large framework just for translation. | D05 |
| G5 | Begin with a relatively simple event contract; work out settings, permissions, hooks and further capabilities deliberately. | D06 |
| G6 | Preserve decisions, alternatives, reasons, unanswered questions and explicit changes in the two maintained records. | D01, D07 |
| G7 | Deliver a robust, extensible MVP with a small initial feature set. | D11 |
| G8 | Give each behavioral interface its own module; require explicit abstract contracts for adapters, event mappers and application agent roles. | D09, D10, D25, D26 |
| G9 | Include basic settings, permissions, agent support and execution-event logging. | D12 |
| G10 | Scope this delivery to the shared foundation, excluding actual provider adapter implementations. | D13 |

Interchangeability is limited to capabilities an implementation actually supports. Matching event names alone does not establish equal behavior.

## Agreed structural rules and MVP scope

The approved separation remains: application roles under `agents/`, shared execution contracts and models under `execution/`, and provider-specific implementations under `execution/adapters/<provider>/`. Each role keeps its behavior, event handling and output models together.

**2026-11-14 amendment:** Sharon explicitly replaced the single `contracts.py` arrangement with separate files for the behavioral interfaces. Adapters and event mappers must have explicit abstract contracts with required methods. The old single-file layout is retained as history in D03/D09, not as the current target.

**Accepted in revision 4:** Sharon approved the expanded desired structure and the abstract-interface approach shown in the previous response (D14/D15). Python `ABC`/`abstractmethod` is the chosen behavioral contract mechanism. The tree is a design target; the real provider directories remain later integration. Exact parameter/payload schemas and failure policies remain open.

```text
agents/
  agent.py                  # Agent ABC; required handle_event
  coder/
    agent.py
    event_handler.py
    models.py
  reviewer/
    agent.py
    event_handler.py
    models.py

execution/
  harness.py
  contracts/
    execution_adapter.py
    event_mapper.py
    event_handler.py
  events.py
  request.py
  result.py
  settings.py
  permissions.py
  adapters/
    fake.py
    claude/                 # later integration
      adapter.py
      event_mapper.py
    codex/                  # later integration
      adapter.py
      event_mapper.py
```

Adding a required abstract method must make an incomplete adapter, mapper or agent-role subclass non-instantiable through ordinary ABC inheritance. Adding an event type is a different change: keep the interface stable and update relevant mapping/handling logic and checks.

**Separation reaffirmed (D23):** retain each behavioral contract in its own module even if it has only one method. `execution/events.py` holds our shared event types/payload schema; mapper and handler contracts refer to that schema rather than defining provider-specific payloads for roles. Actual event fields remain open.

**Approved role contract (D24/D25):** `agents/agent.py` defines an `Agent` ABC requiring `async handle_event(self, event: AgentEvent) -> None`. Each participating reviewer/coder/other agent role explicitly implements it; a no-op is allowed. The role supplies its bound method to the harness, which composes logging and role delivery and passes the adapter an `EventHandler` callback. `EventHandler` remains the typed asynchronous callback signature in `execution/contracts/event_handler.py`. Provider adapters implement execution; provider mappers translate native messages. They do not implement role-specific event handling. [P11](decisions.md#p11--enforce-handling-on-the-agent-role-pass-a-callback-to-execution) records the accepted arrangement and alternatives. Q32 is answered.

**Three behavioral contracts approved together (D26):**

| ABC | Required method shape | Implemented by |
|---|---|---|
| Agent | async handle_event(self, event: AgentEvent) -> None | Each application agent role; explicit no-op allowed. |
| ExecutionAdapter | async run(self, request: ExecutionRequest, *, on_event: EventHandler) -> ExecutionResult | Each concrete execution adapter. |
| EventMapper[NativeMessage] | map(self, message: NativeMessage) -> list[AgentEvent] | ClaudeEventMapper, CodexEventMapper or the corresponding concrete mapper. |

These are the three ABCs. `EventHandler = Callable[[AgentEvent], Awaitable[None]]` is the callback type, not a fourth ABC. The common harness remains a concrete wrapper. “Provider mapper” means the concrete Claude/Codex event mapper, not an additional component. Related payload types live in the shared data-model modules; their precise fields remain open.

The current required methods are `Agent.handle_event`, `ExecutionAdapter.run` and `EventMapper.map`, on their respective classes. No future permission, system or hook methods are committed by this decision; these remain design questions. An ABC is our abstract class contract, while a provider SDK is an integration library used inside an adapter.

The product scope is a **robust MVP**, not a disposable experiment. Small means fewer supported features, not weaker typing, silent permission failures or untested boundary behavior. Adding events and capabilities should be deliberate and practical; this does not require building every future capability now.

Basic settings, permissions and execution-event logging remain product requirements. D28/D29 now plan a deterministic DemoAgent before real coder/reviewer roles. D27 defers Stage 02 context, Langfuse and actual logging integration from the foundation checkpoints; this does not declare the logging requirement fulfilled. The precise role catalogue, permission fields and logging scope remain to be agreed.

The requested delivery excludes actual provider adapter implementations. The shared interfaces/models and surrounding execution behavior are the intended focus. A deterministic fake is included in the accepted desired structure and design sequence (D14/D20); its exact fixtures and acceptance scenarios remain to be designed. Full Claude/Codex behavior and enforcement cannot be accepted until real adapters are connected and tested. D29 answers Q20: real native mappers are deferred together with their SDK adapters; the fake mapper is part of the planned foundation.

A role supplies an event-handling method typed against our shared events. The accepted shared harness wrapper composes logging and role delivery; it does not replace the native runtime's model/tool loop or CrewAI's workflow scheduling.

This iteration authorizes a draft repository design PR (D31), not runtime Python files, a roadmap rewrite or a merge.

## Autonomous MVP execution

**Approved (D16):** the MVP runs unattended under permissions configured before execution. It has no human approval prompts, approval queue or wait-for-human state. If a permission request cannot be resolved under the configured automatic policy, surface a clear execution failure instead of waiting or silently widening access. Interactive permission/input callbacks remain future scope.

Native policy denial can be tool feedback; whether every denial aborts the whole execution remains Q25. This is separate from the settled requirement that unresolved human approval must never suspend the MVP.

**Approved (D17):** do not add a separate mechanism to police workflow authors' combinations of tools and permissions. Authors own those choices; existing input/configuration validation and accurate reporting of unsupported provider capabilities remain distinct. Native restrictions are not bypassed.

## Permission responsibility clarification

Our policy describes desired access. The adapter translates and validates it against the selected SDK/runtime's controls. The configured runtime enforces supported restrictions; any OS sandbox supplies the process-level limits it actually covers. This design does not call for implementing a second filesystem-permission engine.

For built-in tools, configure the provider's actual tool availability and permission rules. For path restrictions, use its supported file-access rules; if shell execution is enabled and indirect writes must also be blocked, use the supported sandbox controls. Custom/external tools need their own appropriate controls and are not automatically covered by a shell sandbox.

A requested policy that the integration cannot uphold must be rejected or reported as unsupported, not silently weakened. Exact read/write paths, approval behavior and settings remain Q18/Q05. This is a clarification of adapter responsibility, not approval of a concrete security configuration. Sources and the Claude `allowed_tools` distinction are recorded under Q23 in the decision board.

## Inherited architecture constraints

The approved repository design continues to govern the wider application:

- Python remains the application environment; a provider may require a subprocess or another language at its SDK boundary.
- CrewAI Flows owns workflow routing and state. Execution adapters do not become another workflow scheduler.
- Workflows/roles depend on narrow execution contracts; SDK clients and native types stay inside adapters.
- Langfuse is the initial tracing integration. Telemetry is not authoritative workflow state or a workflow controller.
- Runtime configuration is external; credentials are not source-controlled or copied into telemetry.
- Deterministic executors support offline regression checks; live provider checks are explicitly configured.
- Unsupported required capabilities and execution failures must be reported honestly. No implicit guarantee of recovery, exactly-once effects or safe retries is introduced.

The existing workflow ABC lifecycle is a separate contract. The requirement for mandatory abstract adapter/mapper contracts now comes directly from Sharon (D10); exact execution methods and data-model choices remain separate decisions.

## Boundary requiring reconciliation

**C01 — Open.** The approved architecture and structure describe provider-neutral event normalization under observability. The execution exploration refines that into native SDK → shared execution events inside execution, followed by execution events → telemetry inside observability.

Sharon has now accepted the desired role/execution folder structure. This record preserves that acceptance, while flagging that the corresponding canonical wording and dependency direction still need explicit reconciliation before implementation. The earlier files are not edited or declared superseded by this document.

The planned distinction is about ownership: role-facing execution evidence versus telemetry export. Exact schema and control responsibilities are still open.

## What is not yet specified

| Question | Missing decision |
|---|---|
| Q01 | Partly answered by D34: five event names/basic meanings accepted. Payloads, IDs, timing and truthful mapping rules remain open. |
| Q02 | Minimal declaration shapes are accepted (D26). Request/result fields, terminal-event/result relationship and handler-failure behavior remain open. |
| Q03 | Codex transport/SDK and supported version; Claude SDK mode/version. |
| Q04 | Common settings versus provider-specific settings and configuration ownership. |
| Q05 | Answered for MVP: no human interaction (D16). Automatic policy defaults remain open; interactive permission/input callbacks are future scope. |
| Q06 | Hooks, interruption/cancellation, steering and session reuse scope. |
| Q07 | Which reference project's code or dependency, if any, to adopt. |
| Q08 | ABC/callback declarations and frozen event/result dataclasses are settled (D26/D37). D54 settles construction-time schema validation and propagated creation errors. D55 selects TypeError/ValueError with model/field/rule diagnostics. Exact constraints/diagnostic formatting, other model representations, nested-mutation policy and serialization/versioning remain open. |
| Q09 | Correlation and observability integration without duplicating work in the logging/context stream. |
| Q10 | Backpressure, callback exceptions, stream disconnects and retry behavior. |
| Q11 | Any UI requirement and separation from the execution core. |
| Q12 | Reconcile canonical guarded architecture/structure wording (C01). |
| Q17 | What does execution logging include: normalized events, native diagnostics, outputs, storage and failure policy? |
| Q18 | Exact initial role scenario and enforceable read/write policy across tools and subprocesses. |
| Q19 | Answered: expanded structure and common wrapper accepted (D14); detailed method/data semantics remain open. |
| Q20 | Answered by D29: native SDK adapters and their concrete native mappers are deferred; fake adapter and fake mapper belong in the foundation. |
| Q32 | Answered (D24/D25): Agent ABC in agents/agent.py requires handle_event; each role implements it explicitly, and the method is supplied as the execution callback. No separate EventHandler ABC is required. |
| Q33 | Define the role's task invocation/input/result path; handle_event alone does not define how a workflow or script starts its task. |
| Q34 | Clarify each role's event_handler.py helper versus its required handle_event method; avoid duplicate responsibilities without silently changing the approved tree. |

Detailed candidate solutions belong under explicitly labelled proposals in the decision board until Sharon accepts them. A requirement that remains open must not silently become a guarantee in diagrams or code.

## Design sequence and examples

**Approved clarification (D18):** “support both” referred to tool configuration concepts: available tools, automatically allowed tools and disallowed tools. It did not request interactive human approval. Preserve that distinction; the exact initial shared fields, defaults and mapping remain Q26 because Sharon also mentioned starting with only a subset. D16's autonomous MVP scope is unchanged.

**Approved working approach (D19):** design the surrounding execution system incrementally before defining role-specific code or implementing anything. Coder/reviewer are reference examples to keep requirements practical, not a prerequisite for deciding the shared contracts. A reviewer running alone is a possible later acceptance exercise, followed by a coder/reviewer workflow.

The agreed desired tree is already recorded above. The system is ready for detailed design, not yet a complete implementation specification: minimal method declarations are accepted, while event/request/result payloads, tool-policy fields and failure/logging/lifetime semantics remain open.

**Approved design sequence (D20):** [P08](decisions.md#p08--incremental-design-plan) is the agreed six-topic design sequence. Work remains design-only; step 1's ownership/wiring direction and step 2's minimal declarations are accepted (D22/D26). The delivery checkpoints below organize this continuing design work. Approval of the sequence does not finalize event payloads, exact signatures or failure policies.

**Approved simplicity decision (D21):** settings conversion begins as a small function inside the provider integration. No separate SettingsAdapter interface is required now; extract a private module if complexity later warrants it.

**Approved execution wiring (D22):** application configuration selects the provider; application assembly constructs the concrete adapter through a small factory and injects it into the common harness. The role receives the harness and supplies its event handler; the harness invokes the adapter, and the adapter maps native messages and delivers shared events through the supplied callback. The result returns through the harness to the role. The harness owns common setup/validation and event-delivery/logging composition; native configuration, stream handling and provider cleanup stay inside the adapter. [P09](decisions.md#p09--harness-and-adapter-selection) retains the explanation and alternatives. Exact selection scope/defaults, constructors and object/session lifetime remain open.

**Contract checkpoint retained from revision 12: design step 2 reviewed.** D26 explicitly approves all three ABCs and their minimum declaration shapes under [P10](decisions.md#p10--minimal-behavioral-contracts) and P11. Q02/Q08 are partially answered; payloads and result/delivery/failure semantics remain open under Q01/Q02/Q08/Q10. The review found no structural blocker to detailed design. Next is step 3's event schema and completion semantics; settings fields follow in step 4. New role-entry/helper questions are Q33/Q34.


## Current planning checkpoint — revision 13

D27–D32 capture the subsequent discussion and this PR authorization. [milestone-plan.md](milestone-plan.md) owns the delivery boundaries and their change log; [repository-updates.md](repository-updates.md) owns pending canonical reconciliation. This is the active repository specification; the original revision-12 files are preserved under [history](history/README.md) as frozen evidence, not parallel active specifications.

| ID | Agreed requirement / planning direction | Decision |
|---|---|---|
| G11 | Develop the execution design alongside Stage 02; exclude context fields/propagation, Langfuse and a new logger from the first foundation work. Reuse the owning track later. | D27 |
| G12 | Plan the shared foundation, then one deterministic agent, then a maintained CrewAI demonstration before native integration. | D28 |
| G13 | Later native integration includes SDK selection, concrete adapter and mapper, settings/permission translation, lifecycle and native verification. | D29 |
| G14 | The fake must exercise message translation and shared events, reflecting useful native integration behavior without claiming native equivalence. | D30 |
| G15 | Maintain a permanent draft design package/PR; preserve history, decisions, proposals, open questions and learning references; leave roadmap and runtime unchanged. | D31 |
| G16 | Milestone boundary changes start as pending deltas in the milestone plan, are checked against decisions/specification, and are applied consistently only within the required approval. | D32 |

**Draft delivery allocation:** S04.M1 contracts/models; S04.M2 harness + fake adapter/mapper; S04.M3 DemoAgent; S04.M4 maintained CrewAI demonstration. These local IDs are unrelated to Stage 02's M4.1–M4.3. Direction is agreed; detailed boundaries and proposed acceptance cases in the plan await review/lock. There is no assertion that Stage 04 is current, implemented or approved to start coding.

**Desired tree versus first delivery:** the accepted longer-term tree above remains intact. The new first exercise uses a small demo role instead of implementing coder/reviewer. Exact demo/fake-mapper paths and justified helper files will be resolved in milestone design; do not generate unused folders. The Agent ABC belongs with roles even when M1 delivers it alongside execution contracts.

**Independent does not mean dependency-free:** no shared Stage 02 model is duplicated here. Event-local identity, if selected, is not a replacement for workflow/application correlation. Before workflow integration, recheck actual merged context/constructor contracts and standalone invocation needs (Q35). No context placeholder, telemetry broker or new logger is introduced by the harness. The common event-delivery/logging composition responsibility remains; actual logging/export needs separate agreed integration and evidence.

**Still proposed:** the accepted five events' payloads, terminal ownership, model implementation library, exact settings fields/defaults, fake scripts/count/input, optional random variation, demo delay, role task entry, callback/cleanup/failure policies. Deterministic scripted cases are recommended; Sharon's random-event idea remains an option to evaluate. A fake cannot certify live tool permissions or provider parity.

**Roadmap boundary:** the guarded/provisional sequencing remains as checked on main. The suggestion to give Stage 04 this foundation and later native work to Stage 05 is a working planning direction, not an edit to either global stage. Resolve the difference deliberately before locking implementation. The original standalone-reviewer/coder-reviewer ideas remain later examples; they are not removed from history.


## Historical review checkpoint — revision 12

**Assessment, not implementation acceptance:** the architecture is coherent and ready for detailed design. The three ABCs, ownership and callback wiring are accepted; event/request/result schemas, failure rules and configuration semantics are not complete enough to implement against yet.

The decision board's [revision 12 review](decisions.md#three-abc-approval-and-design-review--revision-12) records the full findings. Outstanding work includes the terminal-event/result relationship, callback/logging/transport failure behavior, runtime capability mapping, per-execution context and mutable-state lifetime, the agent task entry point, and whether per-role handler helper files earn their place. No proposed resolution has been silently adopted.

Current canonical architecture/structure/governance were reread. They still label the role/harness details as exploration and reserve observability normalization separately. C01 remains a documented reconciliation step before implementation; no repository or Atlas file was edited. A deterministic foundation can verify local contracts but cannot prove native provider mapping or permission enforcement.


## Accepted initial events — revision 14

D34 records Sharon's explicit acceptance of the five event types and the basic meanings explained in this conversation. This narrows Q01; it does not approve all payload/status/identity/delivery proposals previously collected under P01.

| Event | Accepted meaning |
|---|---|
| ExecutionStarted | Our execution has begun; this does not establish native provider readiness. |
| TextProduced | A completed piece of assistant text; multiple pieces may occur before execution finishes. |
| ToolCallObserved | We observed a reported tool/action call; observation alone does not prove it ran or was approved. |
| ToolResultObserved | We observed the corresponding tool/action result, including failure evidence when reported. |
| ExecutionFinished | Our execution reached a terminal outcome; terminal does not necessarily mean successful. |

All five are shared typed data in `app/src/agent_playbook/execution/events.py`; `AgentEvent` is the shared union consumed by the mapper and callback. They are not five new behavioral ABCs and do not need five separate modules. The already accepted separate-interface rule remains: `agents/agent.py`, `execution/contracts/execution_adapter.py`, `execution/contracts/event_mapper.py` and `execution/contracts/event_handler.py` each retain their own responsibility. Request/result/settings/permissions remain in their separate existing target modules. A real provider's mapper will live with its adapter later; the fake mapper's exact path remains M2 design.

Incremental text/deltas mean small arriving fragments (not necessarily one exact token each); reported reasoning means only explanatory/reasoning material exposed by the provider; usage updates mean accounting such as token counts, and cost where actually available; tool progress means intermediate activity before a final tool result. These are explained future possibilities, not added initial event types. Deferring a live UsageUpdated event does not decide whether optional final usage belongs in ExecutionResult. No native capability/parity claim is made by this explanation.

Next design decisions: essential payload fields, event identity/order if required, who emits local start/finish, and how completion relates to the returned ExecutionResult. Callback failure may prevent terminal delivery; guarantees must be explicitly designed rather than inferred from the event name. No runtime files are created here.

## Historical field-design checkpoint — revision 15

D35 reaffirms our owned, minimal contract informed by reference projects. Sharon endorses the suggested future event categories as future directions, not additions to the initial five. The new [P12 field proposal](decisions.md#p12--minimal-fields-illustrated-by-a-standalone-reviewer) uses a standalone reviewer reading one file as a design example. Exact fields, model representation, result semantics and envelope identity remain open; no new runtime or milestone scope is approved. Stage 02 context/correlation remains with its owner.

## Accepted field shape — revision 16

D36 accepts the P12 field set with tool_call_id replacing call_id. Keep output (Sharon allowed either name). Each variant has a fixed type discriminator. Models remain in execution/events.py and execution/result.py; no new behavioral interfaces or runtime files.

| Event/model | Accepted fields beyond the fixed event type |
|---|---|
| ExecutionStarted | None |
| TextProduced | text_id: str; text: str |
| ToolCallObserved | tool_call_id: str or None; tool_name: str; input: JSON object or None |
| ToolResultObserved | tool_call_id: str or None; output: JSON value (including null); status: succeeded / failed / unknown |
| ExecutionFinished | result: ExecutionResult |
| ExecutionResult | status: completed / failed / cancelled / indeterminate; final_text: str or None; error: str or None. This is a result model, not another event. |

Missing call identity and unknown tool outcome are different cases. Reliable native identity may be normalized, but no speculative pairing algorithm is approved. The missing-ID fallback policy, lifecycle owner, result-delivery guarantees and concrete model/validation choice remain open. A Python dataclass example explains the shape; it does not select the implementation library. Enum values represent statuses; event instances carry data. Workflow/tracing correlation remains deferred to its owning work. Earlier unresolved-field statements are historical to their checkpoints; D36 is the current field baseline.

## Current accepted representation and handling — revision 17

D37 selects frozen Python dataclasses for the shared event/result models; statuses use enums, and AgentEvent remains a union of the five concrete event classes. This supersedes the event/result representation question in earlier checkpoints. Dataclasses can have methods; our events carry data and roles own interpretation. No event behavior ABC, visitor or handler method per event is introduced. The three accepted behavioral ABCs and asynchronous callback remain unchanged.

Role handle_event may use match/case with class patterns and field extraction; roles need only handle relevant events and may explicitly do nothing. isinstance remains suitable for a single relevant event. The [reviewer example](decisions.md#dataclasses-and-role-dispatch-approval--revision-17) illustrates this approved approach without adding a real reviewer to the first foundation milestones. Its print calls are teaching output, not the deferred logging integration.

frozen=True prevents ordinary field reassignment; nested JSON containers are not automatically immutable. init=False keeps a fixed type field out of constructor arguments. Runtime input validation and defensive copying remain detailed-design choices. D38 forbids guessed call/result pairing; nullable identity and unknown outcome are distinct. There is no promised fallback where evidence is absent.

Q08 is now answered for event/result representation and remains open for validation/serialization and other data models. Q01 is answered for initial vocabulary/fields/no-guessing, but invocation identity/order and provider-specific missing-evidence handling remain open. Q02/Q04/Q10/Q26 and C01 retain their unresolved portions. Ready to begin M1 detailed design, not implementation lock.

## Dependency-gated progress — revision 18

D39 requires useful independent milestones and explicit prerequisite gates for dependent integration, allowing progress alongside Stages 02/03. [BC03](milestone-plan.md#bc03--explicit-dependency-gates-for-parallel-delivery) proposes the concrete allocation; D40 now accepts that allocation and its prerequisite gates; no detailed milestone implementation baseline is approved. The independent foundation must not require context construction or placeholder context data. The five accepted event payloads remain unchanged. Deferred behavior must have a named owner, trigger and acceptance evidence before implementation of that integration.

Current main now records basic workflow context as merged and permits independent Stage 04 foundation progress. Existing ExecutionContext.for_agent already derives agent metadata; an additional AgentContext is not selected. Standalone context compatibility and propagation remain Q35, separate from tracing completion. No workflow IDs may be invented for a standalone agent. No Stage 02/03 edits or new context subsystem are authorized by this requirement.

## Current delivery agreement — revision 19

D40 approves the four milestone boundaries and BC03 gates: contracts/models; harness/fake; standalone DemoAgent; workflow integration. M1–M3 are usable without context, workflow invocation or telemetry. M4 reuses specific merged compatible application/workflow/context contracts; whole Stage 02/03 completion is not required by the foundation exception. Detailed milestones still need their own approved design/test/plan and implementation authorization.

D41 requires progressive design: start M1 now and defer dependent later choices until prior contracts/results clarify them. The README owns the canonical milestone readiness/status table; milestone-plan.md owns boundaries and the question/dependency matrix. Each milestone's detailed package will have its own folder under the merged stage-working method. Shared requirements remain here; decisions/research/history stay at stage root. No placeholders, guessed IDs or competing context model are introduced.

Main's roadmap resolves Q37 broad sequencing; C01/Q12 still requires a concrete guarded ownership proposal before M1 implementation lock. Main synchronization preserves the new governance and other stages. Stage Design PR #45 remains draft and merges last only with explicit final authorization.

## Lifecycle ownership and event dispatch — revision 20

D42 — **Approved:** retain the shared event classes and one asynchronous role handle_event callback. The common harness emits ExecutionStarted before invoking ExecutionAdapter.run. On the normal return path, it emits ExecutionFinished carrying the same ExecutionResult that it returns to its caller. The provider adapter and its mapper normalize native content/tool messages; they do not duplicate these local lifecycle notifications. This accepts ownership and the normal-path sequence, not a guarantee of terminal delivery under exceptions.

ExecutionStarted keeps its fixed discriminator and no additional payload now. Its dataclass can gain fields later through an explicit contract change. Optional/defaulted fields can preserve existing construction; required fields or changed meanings require consumer/compatibility review. No prompt, context, timestamp or native turn field is selected here.

The start event describes our local execution boundary. It is not a native Claude pre-turn hook, a permission request, or a veto/control mechanism. An execution may contain multiple native turns. Preparing role-specific instructions belongs before execution; reacting to the notification belongs in the role handler.

Sharon considered separate required onStart/onText/onToolResult methods for visible implementation obligations, then explicitly chose events. Retaining one callback avoids a new mandatory ABC method for every event type and preserves a common observation surface. Roles may delegate to private helpers or ignore irrelevant events; adapters remain role-independent. ABC enforcement requires handle_event, not exhaustive handling of every union variant.

Q01/Q02 are answered for lifecycle emission ownership and normal returned-result consistency. Q10 remains open: callback exceptions, ordering/backpressure, adapter exceptions and terminal delivery on abnormal paths need explicit design. Q06 native hooks/controls remains open. C01 canonical ownership reconciliation is unchanged. This decision fits existing M1 contract/M2 implementation boundaries; no boundary change, runtime implementation or merge is authorized.

## Handler failure and future customization — revision 21

D43 — **Approved MVP policy:** if the agent's handle_event raises an exception, stop local execution processing, perform resource cleanup and propagate the failure to the caller. If ExecutionStarted handling fails, do not invoke the adapter. For later failures, stop consuming/delivering ordinary events and require adapter cleanup. Do not swallow the handler failure or return a successful result. This does not undo already executed tools or guarantee immediate termination of a separate native process; native stop/cleanup mechanics need provider integration evidence.

Sharon selects stop-and-propagate to expose problems during debugging. Continuing after a handler failure risks hiding broken essential role behavior. A configurable policy now adds unnecessary MVP choices. An agent may catch an expected nonessential error within its own handler. Exact exception wrapping, cleanup-error precedence, cancellation and whether to attempt ExecutionFinished through a failed handler remain open; D43 does not silently answer these cases or change adapter-failure semantics.

D44 — **Approved future direction, deferred implementation:** preserve a path to per-agent error behavior. Sharon requests later configuration, potentially via agent context, and possibly an injected error-handler method for code-defined behavior. Context fields, policy names, callback signature and a new Agent ABC method are not selected. Keep current policy ownership in the common execution boundary rather than duplicating it in each provider. This allows later policy injection without changing native event schemas; it is not a promise of zero future contract changes.

Future tracking: revisit configuration versus injected behavior when a concrete agent needs a different failure policy. M1 records the contract and deferred need; M2 implements only D43 after its own design approval. Any future implementation must first receive a milestone-boundary amendment. No additional/final milestone, AgentContext model, placeholder flags or extension framework is added now. This preserves D27/D39/D40 standalone scope and D26's three ABCs.

Q10 is **partly answered** for handler failures by D43; terminal notification after failure, adapter errors, ordering/backpressure, cancellation and cleanup precedence remain open. Q35 context integration is still deferred. Next discussion: whether to attempt ExecutionFinished after the handler fails. No runtime implementation, detailed-design lock or merge is authorized.

## Terminal delivery after handler failure — revision 22

D45 — **Approved:** after handle_event raises, do not invoke that failed handler again with ExecutionFinished. Perform cleanup independently of event delivery and propagate the original handler exception. If the failure occurs while handling ExecutionFinished itself, do not retry it. If ExecutionStarted handling fails, the adapter is never invoked (D43). Completion notification is therefore not guaranteed on a handler-failure path and must not be used as the resource-cleanup mechanism.

Sharon explicitly accepts the recommendation after clarification that this is a Python exception in the role's event-processing code, not an LLM response or a reported tool failure. The alternative was to attempt one final notification through the same handler, which could support role-specific completion behavior but could fail again and complicate error handling. The MVP chooses the simpler original-error path. D44 retains later customization as deferred; no new policy flag or hook is introduced.

ExecutionFinished describes an ended execution with a result, not necessarily a successful result. D42 normal-return delivery is unchanged. Q10 is answered for terminal delivery after handler failure; adapter exceptions with a healthy handler, cancellation, cleanup-error precedence and ordering remain open. Next topic: distinguish adapter exceptions from returned failed execution outcomes. D45 fits existing M1/M2 boundaries and does not authorize implementation, a milestone lock or merging PR #45. Earlier revision-21 open wording is historical and superseded only for this specific question.

## Adapter exception policy — revision 23

D46 — **Approved:** propagate unexpected exceptions from ExecutionAdapter.run after resource cleanup. The common harness must not broadly convert raised adapter exceptions into failed ExecutionResult values. Sharon explicitly accepts the recommendation to propagate. Preserve debugging evidence and distinguish an execution-code/transport exception from an unsuccessful outcome deliberately reported by the runtime.

When the adapter has a supported, explicit runtime-reported unsuccessful outcome, it may return a failed ExecutionResult. D42 then applies: the harness delivers ExecutionFinished with that result and returns it if the handler succeeds. A single failed tool result does not automatically establish failure of the whole execution; the native runtime may recover. Exact provider-specific outcome mapping belongs to later native integration.

Alternative considered: convert every adapter exception to a failed result for one uniform caller return shape. This was not selected because broad conversion risks hiding implementation bugs and losing useful exception diagnostics. The caller must handle both returned outcomes and propagated exceptions. No automatic retries, exception-class hierarchy or new configuration is selected.

Q10 is answered for propagation versus result conversion of unexpected adapter exceptions. Whether a healthy handler receives any terminal notification on this exception path, cleanup-error precedence, cancellation and callback ordering remain open. D45 continues to govern an already-failed handler. Do not infer a synthetic terminal result or new error event from D46. Existing M1 contract/M2 harness boundaries, D44 future customization and guarded ownership reconciliation are unchanged. No runtime implementation, milestone lock or merge is authorized.

## Terminal notification on adapter exceptions — revision 24

D47 — **Approved:** if ExecutionAdapter.run raises, skip ExecutionFinished even when the role handler remains healthy. Run cleanup independently and propagate the adapter exception under D46. Do not fabricate a failed ExecutionResult solely to send a terminal notification. If the adapter returns a result, including a reported failed outcome, D42 normal delivery applies; if the terminal handler then raises, D43/D45 propagate that handler failure without retry.

Sharon explicitly accepts this recommendation. The alternative was to construct and send a failed terminal event before propagating the exception, providing a final notification but introducing result conversion and another potential handler failure. The MVP chooses one simple distinction: returned result permits terminal notification; raised exception propagates without it. Consumers must not assume every ExecutionStarted has a matching ExecutionFinished, and cleanup cannot rely on that event.

Q10 is now answered for terminal notification on adapter exceptions. Cleanup-error precedence, cancellation and ordering remain open. D44 future customization remains deferred. This closes an existing M1/M2 contract question without changing milestone scope, adding a new event or authorizing implementation or merge. Revision-23 terminal-delivery open wording remains historical.

## Cleanup failure precedence — revision 25

D48 — **Approved:** when an execution/handler exception is already propagating and cleanup also raises, preserve the original exception as primary with its original traceback, and retain the cleanup failure as additional inspectable diagnostic information. Do not replace the original failure or silently discard the cleanup failure. If cleanup is the only exception, propagate that cleanup exception normally.

Sharon explicitly accepts the recommendation after clarification that exception propagation and logging are separate. The failures occur in the same execution but this does not prove that one caused the other; diagnostics must not assert false causality. Future logging should expose both failures, but retaining both must work without a logging integration. Exact Python attachment/representation remains a detailed implementation-design choice; no custom exception framework, ExceptionGroup or logging subsystem is selected.

Alternatives considered: an error group exposes both equally but complicates caller handling; propagating only cleanup is simpler but hides the original problem. Keep the primary exception for understandable debugging while making the secondary failure visible. D43–D47 propagation and terminal-delivery decisions remain unchanged. Q10 is answered for cleanup-error precedence; cancellation, delivery ordering and the concrete diagnostic representation remain open. This fits current M1 contract/M2 harness scope, with no new milestone, runtime implementation, design lock or merge authorization. Earlier cleanup-precedence open statements are historical.

## Sequential event delivery — revision 26

D49 — **Approved:** deliver callbacks sequentially within one execution. Await completion of the current handler invocation before delivering the next event. Preserve mapped event order, including the order of events returned by one mapper call. Do not launch event callbacks as independent background tasks. D43 stops further ordinary delivery if a callback raises; D45/D47 govern terminal suppression. Different executions may progress concurrently; no global order or serialization across executions is promised.

Sharon explicitly requests sequential delivery. Concurrent callbacks could process independent work faster but complicate ordering, role state and failure handling. The MVP chooses predictable local delivery without adding a queue, replay or concurrency framework. Awaiting the callback does not guarantee that a separate native runtime pauses or that its buffers are bounded.

The accepted D26 asynchronous handler contract remains unchanged: async handle_event(event) -> None, invoked via await. Async describes how waiting can yield to other tasks; it does not require overlapping callbacks. A handler containing only ordinary synchronous operations can still be async def without an internal await. Blocking I/O or CPU-heavy work inside such a handler can block the event loop; specific offloading belongs to the implementation needing it. Await waits for work performed or awaited by the handler, not untracked background tasks it starts.

Sharon asks whether both sync and async handlers should be supported. Recommendation, not a new approved interface: retain the existing async-only public callback and avoid auto-detecting mixed return types or adding a synchronous overload. An explicit wrapper can be considered later if a concrete synchronous integration requires it. No dual-mode callback contract, handler timeout or cancellation policy is selected by D49.

Q10 is answered for per-execution callback sequencing. Cancellation, slow-handler timeout policy and concrete cleanup diagnostic representation remain open. M1 specifies the contract; M2 verifies it with the fake adapter/mapper. Existing milestone boundaries and prerequisites remain unchanged; no runtime implementation or merge is authorized.

## Open hook-scope evaluation — revision 27

Sharon asks to evaluate runtime-affecting pre-tool callbacks. P13 in the decision board and pending BC04 in the milestone plan compare deferring hooks, designing one optional request/response contract with fake verification, and implementing native hooks now. The recommendation is the middle option, not an approved scope change. Current event-only callback, sequential delivery and native-integration deferral remain unchanged. Fresh Claude SDK source supports the pattern; equivalent Codex effects have not been established. No hook schema, new ABC, timeout policy or implementation is selected.

## Product target and replaceable execution — revision 28

D50 — **Approved requirement:** Sharon prioritizes avoiding strong coupling and a large future rewrite when execution gains capabilities or becomes a separately deployed service. Microservice extraction is a future possibility, not an instruction to build a service now. Continue the small MVP; do not promise zero refactoring, universal SDK parity or a stable network protocol merely from Python ABCs.

D51 — **Approved product acceptance target:** the first useful product must support a coder/reviewer workflow. The coder receives an implementation plan in Markdown and the necessary scoped permissions to edit/create/delete files and implement code/tests. The reviewer receives the design/test plan and produced work and checks coverage/conformance. Workflow code determines the next action; an extra decision agent is only a possibility. Precise permission fields, review output schema, test-execution policy and retry behavior remain to be designed. This refines the product goal beyond a demonstration, not the accepted Stage 04 native-integration boundary.

Stage 04 supplies contracts/harness/fake/standalone demo/workflow integration; native adapters and real roles are still later work. The product target is achieved only after real integration is verified. Coder and reviewer must refer to the same produced workspace/artifact revision. Reviewer write restrictions and whether it executes tests need explicit design; a read-only instruction alone is not enforcement. No new context model or logging dependency is introduced.

The event stream alone is not the entire execution API. Current handle_event returns None and D49 serializes local callback consumption; neither guarantees a pause before the next native model call. The runtime owns its internal loop. A hook reply can affect execution only through a supported native control boundary and adapter response mapping. Current contracts have no selected graceful stop/interrupt API; fail-fast exceptions are not a designed substitute for user-requested cancellation.

P14 in the decision board compares reference designs and proposes observation/control separation and portable data. BC04 remains pending; no hook response, cancellation API, network protocol or new required method is selected.

## Construction-time schema validation — revision 31

D54 — **Approved:** validate M1 data models when they are constructed. Check all agreed schema constraints decidable from the supplied object data, including nested values and any agreed cross-field invariants. Invalid construction raises to its caller without returning a substitute object or silently coercing invalid input. Exact exception types/messages and still-undecided field constraints remain detailed-design choices.

This preserves D37 frozen event/result dataclasses and adds no library choice. Validation at creation does not promise deep immutability after creation. It does not prove provider support, actual permission enforcement, event-sequence correctness or missing tool relationships; those remain with their existing owners and decisions. No custom tool/policy contradiction engine is introduced.

M1 expresses and tests the data contract. M2 later implements the harness/fake and applies D42–D49 if object creation fails during execution. Hooks, cancellation controls, runtime implementation and milestone scope are unchanged. The synchronized [M1 design](m1-contracts-models/design.md#construction-time-validation--approved-d54), acceptance cases and implementation plan remain drafts pending remaining choices and approval at a pinned revision.

## Research status

Reference review from revision 12 is preserved. Revision 15 adds a focused source refresh for P12; other upstream claims retain their historical verification status. The [decision board](decisions.md#design-proposals-and-acceptance-status) contains the native mapping comparison and proposals P01–P07. P02's Protocol recommendation is historical. D14 accepts P07's displayed structure and responsibilities; D25/D26 accept the three ABCs and minimum declaration shapes. Event/result fields and representation are now accepted under D36/D37; validation, lifecycle guarantees and permission settings remain unresolved.

The event schema and future control interfaces remain open; P10/P11's minimal ABC/callback declarations are accepted under D25/D26, while execution data and behavioral details remain unresolved. Research confirms that events can cover more than assistant text and that settings/permission responses are different contract categories. Exact SDK versions, payloads and interactive permission support through the chosen Codex surface still require selection and verification.

## References

Historical record:
- Supplied `agent_playbook_conversation_handover.md`: reconstructed substantive handover, not a verbatim full transcript.
- The original [shared conversation](https://chatgpt.com/share/6af85cc6-8978-83ed-8dc2-0be19f55adc7?ogimg=plain): full contents were not recovered from the share link.
- This conversation: direct evidence for the new approvals.

Repository authority:
- [Approved architecture](https://github.com/SharonLanger/agent-playbook/blob/main/designs/architecture.md)
- [Approved structure](https://github.com/SharonLanger/agent-playbook/blob/main/designs/project-structure.md)
- [Design contract](https://github.com/SharonLanger/agent-playbook/blob/main/designs/governance/design-contract.md)
- [Agent execution exploration](https://github.com/SharonLanger/agent-playbook/tree/main/designs/explorations/agent-execution)
- [Architecture notes](https://github.com/SharonLanger/agent-playbook/blob/main/designs/explorations/agent-execution/architecture-notes.md)
- [Candidate structure](https://github.com/SharonLanger/agent-playbook/blob/main/designs/explorations/agent-execution/candidate-file-structure.md)
- [Atlas](https://github.com/SharonLanger/agent-playbook/tree/main/designs/atlas): a view of approved/current/exploratory material, not another authority.

Reference projects to study, not adopted dependencies:
- [Vercel AI SDK](https://github.com/vercel/ai)
- [Triad Labs Harness SDK](https://github.com/Triad-Labs-Inc/harness-sdk)
- [UnifiedAgentWrapper](https://github.com/PentestGPT-Project/UnifedAgentWrapper)
- [InHarness agent-adapters](https://github.com/inharness/agent-adapters)
- [AgentDock](https://github.com/crossainthero-lab/AgentDock)

## Update procedure — every substantive design iteration

Read this specification, the complete decision board, milestone plan and relevant governing sources before progressing. Apply the [boundary-change protocol](milestone-plan.md#boundary-change-protocol--required-every-iteration): a scope change is first recorded as Pending in the plan, cross-checked for contradictions, then reflected in the board, this specification and affected milestone documents once agreed. Tell Sharon before changing any existing agreement; preserve superseded reasoning and approval evidence.

Maintain both active records in this repository package with matching revision entries. Mark questions Answered, Deferred or Open explicitly. Do not promote a recommendation merely because it appears here. History snapshots retain their original bytes. Future sessions must load the active files and plan; a remembered folder diagram is insufficient.

## Standard validation exceptions — revision 32

D55 — **Approved:** a wrong supplied type raises `TypeError`; a correctly typed value violating an agreed constraint raises `ValueError`. Messages identify the model, field and violated rule. These creation errors propagate under D54. No custom validation exception is selected.

This refines Q08's exception representation only. Exact constraints, diagnostic formatting, multiple-error reporting and nested mutation remain open. Existing frozen dataclasses, lifecycle rules and milestone boundaries are unchanged. The M1 design/test/plan remain drafts pending full approval.

## Revision history

| Revision | Date | Change |
|---|---|---|
| 1 | 2026-11-14 | Created approved working baseline, desired structure, unresolved questions and maintenance rules. Event research pending. |
| 2 | 2026-11-14 | Added research status and links to clearly unapproved P01–P06; approved baseline unchanged. |
| 3 | 2026-11-14 | Recorded robust MVP correction, separate mandatory interface modules, basic settings/permissions/logging and exclusion of real adapters; preserved historical layout and added P07/open questions. |
| 4 | 2026-11-14 | Recorded approval of the expanded desired structure/ABC approach, clarified method-versus-event extension and SDK/runtime-owned permission enforcement. |
| 5 | 2026-11-14 | Recorded autonomous MVP scope, deferred human approval and no separate tool/policy contradiction engine; native-denial outcome policy remains open. |
| 6 | 2026-11-14 | Clarified tool-setting intent (D18), ecosystem-first incremental design (D19), and proposed P08 phased plan/call flow; no implementation. |
| 7 | 2026-11-14 | Accepted design sequence/settings simplicity (D20/D21); added P09 harness explanation and proposed adapter selection, with scope/lifetime open. |
| 8 | 2026-11-14 | Accepted execution wiring/adapter-selection direction (D22); moved to design step 2 and drafted P10 minimal contracts with request/result responsibilities and unresolved semantics clearly marked. |
| 9 | 2026-11-14 | Reaffirmed separate one-method contracts (D23), clarified the schema location, and retained EventHandler ABC versus callable as a targeted open question (Q32). |
| 10 | 2026-11-14 | Recorded mandatory explicit role handle_event implementations (D24), clarified mapper versus handler ownership, and proposed P11 Agent ABC plus callback wiring. |
| 11 | 2026-11-14 | Accepted the Agent ABC and role-side handle_event contract (D25), answered Q32, updated the desired tree, and corrected the earlier misplaced provider/role pushback. Future permission/system methods remain open. |
| 12 | 2026-11-14 | Recorded explicit approval of all three ABCs and minimal declarations (D26); reviewed both records and current canonical boundaries, corrected stale statuses, and logged remaining design gaps without adopting new policies. |
| 13 | 2026-11-14 | Recorded D27–D32, parallel-design/deferred-integration boundaries, deterministic foundation/demo direction and authorized draft PR; introduced plan-first milestone change control and preserved exact revision-12 snapshots. |
| 14 | 2026-11-14 | D33: PR #45 merges last after all Stage 04 implementation. D34: five event names/basic meanings accepted; schema/ownership remain open; placement and optional future event explanations added. |
| 15 | 2026-11-14 | Recorded reference-led direction and future-event endorsement; linked unapproved P12 field proposal and refreshed research status. |
| 16 | 2026-11-14 | Accepted D36 field baseline and tool_call_id naming; retained open fallback/lifecycle/representation questions. |
| 17 | 2026-11-15 | Accepted event/result dataclasses and role match dispatch; recorded no-guessing rule and remaining M1 design questions. |
| 18 | 2026-11-15 | Recorded D39 parallel-delivery requirement, linked proposed dependency gates and distinguished merged context from future integration. |
| 19 | 2026-11-15 | Accepted four gated milestones and progressive detailed design; reconciled main governance and remaining canonical ownership gate. |
| 20 | 2026-11-15 | D42 accepts single-handler lifecycle ownership and normal result reuse; keeps start payload empty and abnormal delivery semantics open. |
| 21 | 2026-11-15 | D43 accepts fail-fast handler errors; D44 defers per-agent configuration/injected error behavior; terminal delivery and remaining failure semantics stay open. |
| 22 | 2026-11-15 | D45 accepts skipping terminal notification after handler failure; cleanup remains independent and original failure propagates. |
| 23 | 2026-11-15 | D46 accepts adapter exception propagation and distinguishes returned unsuccessful runtime outcomes; remaining terminal/cleanup policies stay open. |
| 24 | 2026-11-15 | D47 skips terminal notification on adapter exceptions even with a healthy handler; result-return delivery remains unchanged. |
| 25 | 2026-11-15 | D48 preserves the original exception and cleanup diagnostics; a sole cleanup exception propagates normally. |
| 26 | 2026-11-15 | D49 accepts sequential awaited callbacks per execution; clarifies existing async contract and records dual-mode support as unselected. |
| 27 | 2026-11-16 | Tracks open P13 hook evaluation and pending BC04; accepted specification unchanged. |
| 28 | 2026-11-16 | D50/D51 add explicit low-coupling constraint and coder/reviewer product target; proposed controls remain open. |
| 29 | 2026-11-21 | D52 records Stage 04-only PR scope and the methodology reconciliation. Product decisions and milestone boundaries retain their existing approvals. |
| 30 | 2026-11-21 | D53 authorizes four shared navigation files. Stage requirements and milestone approvals retain their existing status. |
| 31 | 2026-11-25 | D54 requires construction-time schema validation and propagation of creation errors; exact constraints/exception representation remain open; M1 detailed design resumes in #72. |
| 32 | 2026-11-25 | D55 approves standard TypeError/ValueError validation exceptions and model/field/rule diagnostics; matching M1 design/test/plan updated. |
