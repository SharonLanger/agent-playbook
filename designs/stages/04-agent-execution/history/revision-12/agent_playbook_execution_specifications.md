# Agent Playbook — Execution Specifications

Revision: 12 · Updated: 2026-11-14 · Owner: Sharon
Companion: [Decision board](agent_playbook_execution_decision_board.md)

## Status and authority

This is the working specification for the agent-role and execution integration discussion. It records the agreements recoverable from the supplied conversation, its reconstructed handover, and the repository's approved design. It is not a complete transcript and does not claim to recover every historical decision.

**Approved** means explicitly accepted by Sharon in this discussion. **Inherited baseline** means an existing approved repository constraint. **Open** means unresolved; a suggested implementation is not approval. Desired structure does not mean implemented code.

These two records do not silently override guarded repository documents. Before implementation, reconcile any affected canonical design files through their existing design-change process. No runtime change, dependency installation, PR, or adoption of a third-party library is authorized by creating these records.

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

**Approved role contract (D24/D25):** `agents/agent.py` defines an `Agent` ABC requiring `async handle_event(self, event: AgentEvent) -> None`. Each participating reviewer/coder/other agent role explicitly implements it; a no-op is allowed. The role supplies its bound method to the harness, which composes logging and role delivery and passes the adapter an `EventHandler` callback. `EventHandler` remains the typed asynchronous callback signature in `execution/contracts/event_handler.py`. Provider adapters implement execution; provider mappers translate native messages. They do not implement role-specific event handling. [P11](agent_playbook_execution_decision_board.md#p11--enforce-handling-on-the-agent-role-pass-a-callback-to-execution) records the accepted arrangement and alternatives. Q32 is answered.

**Three behavioral contracts approved together (D26):**

| ABC | Required method shape | Implemented by |
|---|---|---|
| Agent | async handle_event(self, event: AgentEvent) -> None | Each application agent role; explicit no-op allowed. |
| ExecutionAdapter | async run(self, request: ExecutionRequest, *, on_event: EventHandler) -> ExecutionResult | Each concrete execution adapter. |
| EventMapper[NativeMessage] | map(self, message: NativeMessage) -> list[AgentEvent] | ClaudeEventMapper, CodexEventMapper or the corresponding concrete mapper. |

These are the three ABCs. `EventHandler = Callable[[AgentEvent], Awaitable[None]]` is the callback type, not a fourth ABC. The common harness remains a concrete wrapper. “Provider mapper” means the concrete Claude/Codex event mapper, not an additional component. Related payload types live in the shared data-model modules; their precise fields remain open.

The current required methods are `Agent.handle_event`, `ExecutionAdapter.run` and `EventMapper.map`, on their respective classes. No future permission, system or hook methods are committed by this decision; these remain design questions. An ABC is our abstract class contract, while a provider SDK is an integration library used inside an adapter.

The product scope is a **robust MVP**, not a disposable experiment. Small means fewer supported features, not weaker typing, silent permission failures or untested boundary behavior. Adding events and capabilities should be deliberate and practical; this does not require building every future capability now.

Basic settings, permissions and execution-event logging are required. A coder that can read/edit and a reviewer that can read were suggested as a first scenario; the precise role catalogue, permission fields and logging scope remain to be agreed.

The requested delivery excludes actual provider adapter implementations. The shared interfaces/models and surrounding execution behavior are the intended focus. A deterministic fake is included in the accepted desired structure and design sequence (D14/D20); its exact fixtures and acceptance scenarios remain to be designed. Full Claude/Codex behavior and enforcement cannot be accepted until real adapters are connected and tested. Concrete native mapper implementation scope remains Q20.

A role supplies an event-handling method typed against our shared events. The accepted shared harness wrapper composes logging and role delivery; it does not replace the native runtime's model/tool loop or CrewAI's workflow scheduling.

This iteration still authorizes design and the two maintained records, not creation of runtime Python files or a PR.

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
| Q01 | Initial event vocabulary, payloads, IDs, timing and truthful mapping rules. |
| Q02 | Minimal declaration shapes are accepted (D26). Request/result fields, terminal-event/result relationship and handler-failure behavior remain open. |
| Q03 | Codex transport/SDK and supported version; Claude SDK mode/version. |
| Q04 | Common settings versus provider-specific settings and configuration ownership. |
| Q05 | Answered for MVP: no human interaction (D16). Automatic policy defaults remain open; interactive permission/input callbacks are future scope. |
| Q06 | Hooks, interruption/cancellation, steering and session reuse scope. |
| Q07 | Which reference project's code or dependency, if any, to adopt. |
| Q08 | All three ABCs and minimal method/callback declarations are settled (D25/D26); payload models, validation and serialization/versioning needs remain open. |
| Q09 | Correlation and observability integration without duplicating work in the logging/context stream. |
| Q10 | Backpressure, callback exceptions, stream disconnects and retry behavior. |
| Q11 | Any UI requirement and separation from the execution core. |
| Q12 | Reconcile canonical guarded architecture/structure wording (C01). |
| Q17 | What does execution logging include: normalized events, native diagnostics, outputs, storage and failure policy? |
| Q18 | Exact initial role scenario and enforceable read/write policy across tools and subprocesses. |
| Q19 | Answered: expanded structure and common wrapper accepted (D14); detailed method/data semantics remain open. |
| Q20 | Confirm exclusion of concrete native mappers alongside real provider adapters; the deterministic foundation's inclusion is already accepted (D14/D20). |
| Q32 | Answered (D24/D25): Agent ABC in agents/agent.py requires handle_event; each role implements it explicitly, and the method is supplied as the execution callback. No separate EventHandler ABC is required. |
| Q33 | Define the role's task invocation/input/result path; handle_event alone does not define how a workflow or script starts its task. |
| Q34 | Clarify each role's event_handler.py helper versus its required handle_event method; avoid duplicate responsibilities without silently changing the approved tree. |

Detailed candidate solutions belong under explicitly labelled proposals in the decision board until Sharon accepts them. A requirement that remains open must not silently become a guarantee in diagrams or code.

## Design sequence and examples

**Approved clarification (D18):** “support both” referred to tool configuration concepts: available tools, automatically allowed tools and disallowed tools. It did not request interactive human approval. Preserve that distinction; the exact initial shared fields, defaults and mapping remain Q26 because Sharon also mentioned starting with only a subset. D16's autonomous MVP scope is unchanged.

**Approved working approach (D19):** design the surrounding execution system incrementally before defining role-specific code or implementing anything. Coder/reviewer are reference examples to keep requirements practical, not a prerequisite for deciding the shared contracts. A reviewer running alone is a possible later acceptance exercise, followed by a coder/reviewer workflow.

The agreed desired tree is already recorded above. The system is ready for detailed design, not yet a complete implementation specification: minimal method declarations are accepted, while event/request/result payloads, tool-policy fields and failure/logging/lifetime semantics remain open.

**Approved design sequence (D20):** [P08](agent_playbook_execution_decision_board.md#p08--incremental-design-plan) is now the agreed six-step plan. Work remains design-only; step 1's ownership/wiring direction is accepted (D22) and step 2 is active. Approval of the sequence does not finalize event payloads, exact signatures or failure policies.

**Approved simplicity decision (D21):** settings conversion begins as a small function inside the provider integration. No separate SettingsAdapter interface is required now; extract a private module if complexity later warrants it.

**Approved execution wiring (D22):** application configuration selects the provider; application assembly constructs the concrete adapter through a small factory and injects it into the common harness. The role receives the harness and supplies its event handler; the harness invokes the adapter, and the adapter maps native messages and delivers shared events through the supplied callback. The result returns through the harness to the role. The harness owns common setup/validation and event-delivery/logging composition; native configuration, stream handling and provider cleanup stay inside the adapter. [P09](agent_playbook_execution_decision_board.md#p09--harness-and-adapter-selection) retains the explanation and alternatives. Exact selection scope/defaults, constructors and object/session lifetime remain open.

**Current work: design step 2 reviewed.** D26 explicitly approves all three ABCs and their minimum declaration shapes under [P10](agent_playbook_execution_decision_board.md#p10--minimal-behavioral-contracts) and P11. Q02/Q08 are partially answered; payloads and result/delivery/failure semantics remain open under Q01/Q02/Q08/Q10. The review found no structural blocker to detailed design. Next is step 3's event schema and completion semantics; settings fields follow in step 4. New role-entry/helper questions are Q33/Q34.

## Review checkpoint — revision 12

**Assessment, not implementation acceptance:** the architecture is coherent and ready for detailed design. The three ABCs, ownership and callback wiring are accepted; event/request/result schemas, failure rules and configuration semantics are not complete enough to implement against yet.

The decision board's [revision 12 review](agent_playbook_execution_decision_board.md#three-abc-approval-and-design-review--revision-12) records the full findings. Outstanding work includes the terminal-event/result relationship, callback/logging/transport failure behavior, runtime capability mapping, per-execution context and mutable-state lifetime, the agent task entry point, and whether per-role handler helper files earn their place. No proposed resolution has been silently adopted.

Current canonical architecture/structure/governance were reread. They still label the role/harness details as exploration and reserve observability normalization separately. C01 remains a documented reconciliation step before implementation; no repository or Atlas file was edited. A deterministic foundation can verify local contracts but cannot prove native provider mapping or permission enforcement.

## Research status

Reference review is complete for this iteration. The [decision board](agent_playbook_execution_decision_board.md#design-proposals-and-acceptance-status) contains the native mapping comparison and proposals P01–P07. P02's Protocol recommendation is historical. D14 accepts P07's displayed structure and responsibilities; D25/D26 accept the three ABCs and minimum declaration shapes. Event payloads and permission settings remain unresolved.

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

1. Read the current versions of both files and affected canonical design documents.
2. Check the proposed change against existing decisions, open questions and component ownership.
3. If it contradicts an agreement, tell Sharon which decision would change and its consequences **before changing that agreement**. Preserve the previous decision as superseded only after approval.
4. Add the decision, source of approval, alternatives, rationale and consequences to the board. Do not invent an unspoken reason.
5. Mark answered questions Answered and link the answer/decision; retain their history. Mark deferred items explicitly with a reason.
6. Update this specification only with approved changes; leave open questions visible. Keep research and proposals clearly separate.
7. Update both revision logs and save new versions of the same two files. Verify links and consistency.
8. A future session must load both files; memory or a folder diagram alone is not the authority.

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
