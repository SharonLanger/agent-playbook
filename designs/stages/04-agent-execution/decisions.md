# Agent Playbook — Execution Decision Board

> **DO NOT MERGE PR #45 — MERGE LAST, AFTER ALL STAGE 04 IMPLEMENTATION PRs.** This is the ongoing design workspace. Keep it open through every milestone; reconcile final documentation after the entire Stage 04 implementation is accepted and merged, then merge this PR only with Sharon's explicit final authorization. Individual design/milestone approval does not authorize merging it.

Revision: 15 · Updated: 2026-11-14 · Owner: Sharon
Companion: [Specifications](specifications.md)

## How to read this board

Statuses: **Approved**, **Inherited baseline**, **Proposed**, **Open**, **Answered**, **Deferred**, **Superseded**, **Done**. A researched option is not an approved decision. “Not selected” does not mean permanently rejected.

Evidence levels:
- **Direct**: Sharon's visible instruction or approval in this conversation.
- **Repository**: an approved canonical design, not a new approval inferred from a suggestion.
- **Handover/exploration**: historical reconstruction or explicitly exploratory notes.
- **Research**: observed source behavior; no adoption decision.

This board is comprehensive for the recoverable decisions relevant to this design discussion; it is not a claim that an inaccessible original transcript has been read in full. Unknown historical reasons remain unknown.

**Previous checkpoint, revision 13 (updated by D33/D34 below):** D26's three ABCs remain accepted. D27–D32 below record the parallel planning boundary, deterministic delivery direction and authorization for this documentation PR with plan-first scope control. [specifications.md](specifications.md) is the current working specification; [milestone-plan.md](milestone-plan.md) owns proposed delivery boundaries. Discussion approvals do not silently promote a locked canonical stage baseline. Earlier proposals and revision sections retain their historical status.

## Approved decisions in this discussion

| ID | Decision and status | Alternatives and rationale | Evidence / consequences |
|---|---|---|---|
| D01 | **Approved** — Maintain these two records on every substantive iteration. | Conversation-only memory was insufficient to prevent drift. Separate current specification from decision history. | Direct, 2026-11-14. Record decisions, questions, answers, reasons and alternatives. |
| D02 | **Approved** — Small isolated execution integration with an application-owned boundary. | Direct provider coupling and dependence on an entire external framework make replacement harder. Prefer a replaceable provider/library behind our contract. | Direct. Replacement means compatible behavior, not automatic feature parity. |
| D03 | **Approved, amended by D09** — Separate role packages under `agents/` from adapters under `execution/`; the original single `contracts.py` part is superseded. | Mixing reviewer behavior with SDK mechanics obscures ownership and replacement. Earlier more expansive folder candidates remain exploratory. | Direct: “I like it… Mark that as… desired file structure.” Desired layout, no implementation yet. |
| D04 | **Approved direction** — Provider adapters translate into our typed events and call a role-supplied handler. | Historical `CoderMessages.handle(ClaudeSDKMessage)` leaked native types. Merely wrapping a native stream did not solve role coupling. | Direct request plus handover correction. Class/method choices are subsequently accepted under D25/D26; event schema and scheduling/failure details remain Q01/Q02/Q10. |
| D05 | **Approved** — Research the existing projects and take only the useful minimum. | Wholesale framework/UI adoption is not justified by the translation need. Building every feature ourselves is also not the goal. | Direct. No package or copied implementation selected. |
| D06 | **Approved** — Start relatively simple; examine events first and define settings/permissions/hooks deliberately. | A complete harness abstraction with many concern-specific adapters would introduce decisions before requirements. | Direct. No approval yet for a settings-adapter/permission-adapter/hook-adapter hierarchy. |
| D07 | **Approved** — Check contradictions and notify Sharon before changing an agreed decision. | Silent overwrites lose reasoning and can conflict with other components. | Direct. Retain superseded decisions and link their replacements after approval. |
| D08 | **Approved historical scope; PR restriction amended by D31** — Documentation and research now; runtime implementation remains unrequested. | Earlier instruction was “Do not implement anything yet”; this turn authorizes records and research. | Direct. At that checkpoint no code, dependencies, PRs or provider runs. D31 later permits this draft documentation PR only. |
| D09 | **Approved** — Put each behavioral interface in a separate file; replace the single `contracts.py` arrangement. | A single file was the previous arrangement. Sharon explicitly prefers separately visible interfaces, consistent with his Java experience. Separate modules do not require separate packages or services. | Direct, 2026-11-14. Earlier arrangement preserved in D03/H13; exact expanded filenames proposed in P07. |
| D10 | **Approved requirement** — Adapters and event mappers have explicit abstract contracts with required methods. | Earlier P02 suggested structural Protocol. Sharon wants missing required implementations to be caught, so nominal ABC contracts are the current implementation recommendation. | Direct. Initial signatures were open; D26 subsequently accepts the minimal declarations. Mandatory contracts do not guarantee correct behavior by themselves. |
| D11 | **Approved** — Build a robust, extensible MVP with only the basic feature set initially. | Sharon explicitly corrected his earlier “POC” wording; it must not imply quick/disposable implementation. | Direct correction takes precedence. Keep interfaces, typed data, failure semantics and meaningful checks. |
| D12 | **Approved requirement** — Support basic agents, settings, permissions and execution-event logging. | Output-only observation is insufficient for the intended product. Exact fields, policies and logging coverage are not yet selected. | Direct. Coder read/edit and reviewer read were a proposed first scenario, not a complete role or security specification. |
| D13 | **Approved delivery boundary** — Deliver the shared execution foundation; exclude actual provider adapter implementations. | Full native SDK integrations are a later integration deliverable. | Direct. Does not authorize runtime implementation in this design turn. The fake's inclusion is subsequently accepted under D14/D20; Q20 is subsequently answered by D29: native mappers are deferred too. |
| D14 | **Approved desired structure** — Accept the expanded tree shown in the previous response: contracts directory with separate adapter/mapper/callback modules, shared models/settings/permissions, common harness, fake implementation and later native provider directories. | Continues D09–D13. Keeps the foundation explicit and extensible without introducing a separate adapter object for each concern. | Direct: Sharon says he likes the detailed example and agrees with the pushbacks. Approval covers the displayed structure/responsibilities, not every unshown detail in P07 or an instruction to implement. |
| D15 | **Approved** — Use the ABC approach for mandatory adapter/mapper methods; keep adding events distinct from adding required methods. | Sharon clarifies he meant adding a new required method, not adding an enum/event variant. This resolves the earlier misunderstanding. | Direct. Regular ABC inheritance prevents instantiating incomplete subclasses; typed signature checks and semantic tests remain necessary. |

## Inherited approved baseline

| ID | Existing decision | Alternatives / known reason | Source |
|---|---|---|---|
| B01 | Modular Python application with narrow external integration boundaries. | One project/package is sufficient now; multi-package or global domain/application/infrastructure reorganization was deferred in the handover. | Approved architecture/structure; handover for historical alternatives. |
| B02 | CrewAI Flows owns workflow steps/routing/state. | An adapter or tracing UI must not silently become the scheduler. | Approved architecture. |
| B03 | Workflow-facing requests/results are provider-independent; native types stay inside adapters. | Capability differences remain explicit rather than presumed interchangeable. | Approved architecture. |
| B04 | Langfuse is the initial tracing integration; observability does not own workflow truth. | Other logging/storage/export choices are separate work, not decided by this execution design. | Approved architecture. |
| B05 | External runtime YAML and separate secrets; `app/application.yaml` is shared configuration. | A separate `configs/` directory for a single file was not needed in the historical refactor. | Approved structure; handover for rationale. |
| B06 | Deterministic executors and offline workflow checks; live integration checks explicit. | Do not make ordinary regression checks depend on live paid models. | Approved architecture. |
| B07 | Workflow ABC validates lifecycle/input/output; registry resolves configured classes. | This existing workflow decision does not settle the execution Protocol/ABC question. | Workflow-contract design and approved architecture. |
| B08 | Atlas distinguishes Current and Explorations and is a projection of source documents. | A visual depiction is not independent approval of a proposed class or folder. | Approved architecture. |
| B09 | Release building, release discovery/launch and application execution have distinct responsibilities. | Earlier runtime refactor split these responsibilities; no new restructuring is requested here. | Approved structure and historical handover. |

No current PR/merge status is inferred from stale handover prose. The decision records preserve design reasoning, not a duplicated project progress database.

## Historical alternatives and objections retained

| ID | Option | Status and reason |
|---|---|---|
| H01 | Role handler accepts native Claude/Codex messages. | **Superseded direction** by D04: ties role logic to SDKs and defeats replacing the adapter. |
| H02 | Adapter merely wraps the native loop and forwards native messages unchanged. | **Not sufficient** for D02/D04; translation at the owned boundary is necessary. |
| H03 | `Executor.start(request) -> ExecutionHandle` with event iterator/result/close. | **Exploratory alternative** to injected callback, not a rejected design. More explicit lifecycle but more API surface; Q02 remains open. |
| H04 | Broad event catalogue including deltas, snapshots, tool lifecycle, usage, sessions and terminal status. | **Exploratory**, no schema approved. Distinguish real provider evidence from derived lifecycle. |
| H05 | Every backend supports the same timing, permissions, sandbox and controls because names match. | **Not an accepted guarantee**; capability and semantic differences must be explicit. |
| H06 | Event observer can veto a tool action. | **Invalid conflation** in the earlier discussion: post-action observation cannot enforce a pre-action decision. Define a real request/response control boundary if needed. |
| H07 | Verifier needs more evidence, therefore expose all native messages. | **Unselected**. First use role-owned structured outputs; add shared evidence where necessary; reject unsupported requirements. Deterministic application verification may provide stronger evidence. |
| H08 | Separate event/settings/permission/hook adapter classes immediately. | **Partly resolved:** event mapper is accepted; D21 selects a settings conversion function, not a SettingsAdapter. Separate permission/hook interfaces remain unselected future suggestions. |
| H09 | Adopt an existing project's entire desktop UI/runtime. | **Not selected**. UI ideas may be useful separately; importing their full architecture is not necessary for event translation. |
| H10 | Build all harness features ourselves. | **Not selected**. D05 explicitly calls for learning from existing implementations and considering reuse. |
| H11 | Put every event field, recovery guarantee and retry policy into the first contract. | **Deferred**, requirements and native capabilities must establish need before adding these guarantees. |
| H12 | Mandatory generic agent base class, role registry, or a full coder/reviewer/verifier catalogue. | **Partly adopted later:** D25/D26 approve the narrow Agent ABC requiring handle_event. A role registry, full role catalogue and broader agent framework remain exploratory, not approved by that decision. |
| H13 | Single `execution/contracts.py` for all behavioral contracts. | **Superseded** by D09. Former approved tree had reviewer files, `execution/contracts.py`, `events.py` and per-provider `adapter.py`/`event_mapper.py`. Role/provider separation remains approved. |
| H14 | Structural Protocol as the primary adapter mechanism (P02). | **Superseded recommendation** by D10/P07's explicit required abstract contracts. The typed callback is subsequently accepted under D25/D26; detailed ordering/failure policies remain open. |
| H15 | Describing this work as a POC. | **Corrected by Sharon** to robust MVP (D11); do not carry the earlier label forward as the product scope. |

## Questions and resolution log

| ID | Question | Status | Answer / next evidence |
|---|---|---|---|
| Q00 | Where do role logic and provider execution belong? | **Answered** | D03; approved desired folder structure in specifications. |
| Q01 | Which events and payloads are necessary first? | **Partly answered by D34** | Five names/basic meanings accepted; payloads, identity/order, detailed evidence and lifecycle ownership remain open. |
| Q02 | What execution/callback interface, class mechanism and delivery semantics? | **Partly answered (D26)** | Minimal ABC/callback declaration shapes accepted. Request/result fields, terminal-event/result relationship, delivery and failure semantics remain open. |
| Q03 | Which Codex integration surface and Claude SDK mode/version? | **Open** | SDK versus app-server affects streaming, permissions and controls. |
| Q04 | Which settings are common and which stay provider-specific? | **Open** | Define a small request/settings model; do not pretend permission/sandbox equivalence. |
| Q05 | Are interactive permissions and user questions needed in the first scope? | **Answered for MVP; future interaction deferred** | D16: configured automatic policy or clear failure, with no human prompt or approval wait. |
| Q06 | Which hooks, cancellation, steering and session controls are required? | **Open** | Capability evidence and concrete first use case needed. |
| Q07 | Reuse a dependency, copy permitted components, or write thin native wrappers? | **Open** | Study the five projects and licenses; no adoption yet. |
| Q08 | Mandatory behavioral interfaces, payload models and serialization/versioning needs? | **Partly answered** | D09/D10/D14/D15/D25/D26 settle all three ABCs and minimal method/callback declarations. Payload models, validation, serialization and behavioral details remain open. |
| Q09 | How do events connect to run/step context and observability? | **Open** | Coordinate with existing context/logging work; resolve C01. |
| Q10 | What happens on slow/failed handlers, disconnects or partial evidence? | **Open** | Define ordered delivery and explicit failure policy before implementation. |
| Q11 | Is a UI needed; which actions may it issue? | **Open / later** | UI references are not a committed UI requirement. |
| Q12 | How should canonical ownership wording be reconciled? | **Open** | C01; explain precise canonical changes before implementation. |
| Q13 | Can these two records replace guarded repository authority silently? | **Answered** | No; D07 and inherited design contract. They record the new working agreement and pending reconciliation. |

When a question is answered, retain its row, add the answer and decision ID, and record any prior rejected or superseded alternatives. Do not delete the question.

Additional research questions resolved in revision 2:

| ID | Question | Status | Answer / source |
|---|---|---|---|
| Q14 | Are events only assistant messages? | **Answered — research** | No: tool/action evidence, usage and lifecycle can also be observed. Initial scope remains Q01. |
| Q15 | Must a Python application add a JavaScript bridge for Codex? | **Answered — research** | No inherent requirement: official Python SDK over app-server exists. Exact controls/version remain Q03/Q05. |
| Q16 | Can AgentDock currently be assumed to grant open-source code reuse? | **Answered — research** | No: its README says no license and rights reserved. No adoption selected. |

New questions from the MVP clarification:

| ID | Question | Status | Answer / next evidence |
|---|---|---|---|
| Q17 | What exactly must the harness log, and through which existing integration? | **Open** | D12 requires logging. Propose normalized execution events/results first; CLI-equivalent raw diagnostics, retention and export-failure policy need scope. |
| Q18 | Is coder read/edit plus reviewer read the initial scenario, and what enforces it? | **Open** | Example supplied by Sharon. Define workspace boundary and indirect writes through tools/subprocesses before claiming enforcement. |
| Q19 | Accept the expanded tree and shared harness wrapper? | **Answered** | D14 accepts the displayed tree and module responsibilities. Exact call/error/payload semantics remain open. |
| Q20 | Are concrete native event mappers deferred along with real adapters? | **Answered by D29** | Native SDK integration includes its concrete adapter and mapper later; the fake mapper belongs to the foundation. Earlier open status is retained in historical sections/snapshots. |
| Q21 | Does TextProduced mean the end of a turn/execution? | **Answered — proposed semantics clarified** | No. It represents a completed text unit; several may occur around tool calls before ExecutionFinished. P01 remains an unapproved event schema. |
| Q22 | Can Python reject a subclass missing a newly required abstract method? | **Answered — language behavior** | Ordinary ABC subclasses cannot be instantiated until required methods are implemented. Signature compatibility and semantic coverage require static checks/tests; adding an event type is not adding an abstract method. |
| Q23 | Does our adapter implement permission enforcement itself? | **Answered — responsibility clarification** | Configure and validate the provider's supported controls; the SDK/runtime and relevant sandbox enforce them. No duplicate filesystem-security engine is proposed. Exact policy mapping and native acceptance tests remain open. |

## Conflict register

| ID | Conflict / tension | Status | Required handling |
|---|---|---|---|
| C01 | Approved observability normalization wording versus proposed execution-owned native-message mapping; new `agents/` role boundary is absent from current guarded folder table. | **Open; flagged to Sharon** | Preserve both sources. Before implementation, explain affected canonical ownership/dependency changes and reconcile them explicitly. No canonical file changed here. |
| C02 | “Minimal” integration versus settings/permissions/hooks/controls requested for investigation. | **Partly resolved** | D11/D12 establish robust MVP with basic settings/permissions/logging; advanced hooks and controls still need scope. |
| C03 | Previous single-contract-file arrangement versus separate mandatory interfaces. | **Resolved** | D09 explicitly authorizes the change. Flagged before updating records; original arrangement retained under D03/H13. |

## Actions

| ID | Action | Status |
|---|---|---|
| A01 | Create the specifications and decision board. | **Done** — revision 1. |
| A02 | Verify reference projects and current native event/control surfaces. | **Done at revision 2** — historical source/doc review below; live parity and selected-version checks remain future work. |
| A03 | Propose minimal typed events, callback/interface and internal mapper responsibilities. | **Done** — P01–P06 and later refinements. D25/D26 accept ABC/callback declarations; the event schema and remaining behavioral policies still need decisions. |
| A04 | Obtain Sharon's design choice on the initial contract after showing the proposal. | **Done for initial declarations** — D25/D26 accept all three ABCs and callback wiring. Detailed data and behavior contracts remain open. |
| A05 | Reconcile affected canonical architecture before runtime implementation. | **Open; depends on design choices** |
| A06 | Maintain the two active specification/decision records on each substantive iteration. | **Ongoing; D31 moves their active home to this repository package.** Original revision-12 files remain frozen snapshots. |
| A07 | Review the complete working records for discrepancies and design readiness. | **Done for revision 12** — findings F01–F09 below; no runtime tests or implementation. |

## Reference register

| ID | Source | Why study it | Adoption |
|---|---|---|---|
| R01 | [Vercel AI SDK harnesses](https://github.com/vercel/ai/tree/main/content/docs/03-ai-sdk-harnesses) | Common application-facing streams over agent runtimes. | None |
| R02 | [Triad Labs Harness SDK](https://github.com/Triad-Labs-Inc/harness-sdk) | Adapters, capabilities, reverse permission/input paths and shared tests. | None |
| R03 | [UnifiedAgentWrapper](https://github.com/PentestGPT-Project/UnifedAgentWrapper) | Python request/event/result mapping. | None |
| R04 | [InHarness agent-adapters](https://github.com/inharness/agent-adapters) | Unified iterable events and explicit provider differences. | None |
| R05 | [AgentDock](https://github.com/crossainthero-lab/AgentDock) | Adapter ownership and a separate UI consumer. Licensing must be checked before reuse. | None |
| R06 | [Claude Agent SDK Python](https://github.com/anthropics/claude-agent-sdk-python) | Authoritative native message, option, permission and hook types. | Integration under investigation |
| R07 | [Codex source](https://github.com/openai/codex) / [app-server](https://developers.openai.com/codex/app-server) | Authoritative SDK and protocol differences. | Integration under investigation |


## Research findings — 2026-11-14

**Evidence, not approval.** Relevant documentation and source types/mappers were inspected. No project was installed or run, no feature-parity test was performed, and no version has been selected for Agent Playbook. Upstream default-branch source and published SDK releases can differ. Pin and verify a concrete SDK/runtime pair before implementation.

### What to learn from the five projects

| Reference | Verified useful pattern | What to take as a design reference | What not to adopt automatically |
|---|---|---|---|
| R01 — Vercel | A harness abstraction separate from ordinary model providers; runtime output projects into compatible application streams. Its harness packages are explicitly experimental. | Preserve the native runtime and own a stable consumer boundary. | The entire TypeScript framework, sandbox/session stack, or an assumption that its experimental harness API is stable. |
| R02 — Triad | Actual `ProviderAdapterV1`/`ProviderRuntime` types separate event output from permission/input responses; capabilities and shared adapter contract tests are explicit. | A narrow behavior contract, truthful capabilities, reverse translation for decisions, and a shared fixture suite. | SQLite history, persistent session management, queues, replay and its full public event catalogue before our requirements justify them. |
| R03 — UnifiedAgentWrapper | Python frozen dataclass event union; separate Claude/Codex normalization; current Codex backend uses the official Python SDK over app-server. | Python organization and concrete message-to-event mapping examples. | Its raw-event escape hatch in role logic, zero defaults for missing usage, or treating its similarly named sandbox policies as equivalent enforcement. README describes no interactive permission prompts or mid-turn controls. License/reuse terms remain to verify before copying/adoption. |
| R04 — InHarness | Typed `AsyncIterable<UnifiedEvent>`; capability differences documented. Its Codex TypeScript SDK path describes synthesized full-text “deltas” and a fixed approval policy. | Explicit capability descriptions and distinguishing native timing from synthesized output. | Treating its Codex limitations as limitations of app-server; silently dropping required settings; importing its whole catalogue. |
| R05 — AgentDock | Adapter owns launch, event translation, interaction-response mechanics and stop/resume semantics; UI consumes common types. | Clear ownership and UI separation. | The Electron application, Pro orchestration, or assuming its chosen Codex transport defines all Codex capabilities. Its README currently says there is no license and rights are reserved: use as a design reference; code reuse is not selected. |

The Python wrapper is the closest structural example, and Triad provides the strongest reference for bidirectional controls. Vercel confirms the larger pattern. These are research conclusions, not production-quality or adoption endorsements.

### Native surfaces: what can be translated

| Information | Claude Agent SDK Python | Codex app-server / Python SDK | Initial proposal |
|---|---|---|---|
| Completed assistant text | `AssistantMessage` with `TextBlock`; current docs describe completed blocks, potentially several under one message ID. | `item/completed` for an `agentMessage`. | `TextProduced`, keyed by a locally normalized text-unit ID. |
| Incremental text | `StreamEvent` carrying `content_block_delta/text_delta` when partial messages are enabled. | `item/agentMessage/delta`. | Optional `TextDelta` later; do not double-append the final completed text. |
| Observed tool/action call | `ToolUseBlock` gives call ID/name/input. | Relevant `item/started` or completed item evidence for commands, MCP tools and file changes. | `ToolCallObserved`; explicitly not proof of approval or actual execution start. |
| Observed result | `ToolResultBlock` associates output/error evidence with a tool-use ID. | Relevant `item/completed`; command exit/output, MCP result/error, file-change status. | `ToolResultObserved`; preserve unknown status and typed evidence where available. |
| Terminal outcome | `ResultMessage` subtype, error flag, terminal reason and result; transport exceptions are separate. | `turn/completed` with its status; transport failures remain separate. | `ExecutionFinished`; “completed event received” alone does not mean success. |
| Usage | Result usage, optional cost and model usage. | Token-usage notifications / collected turn result. | Put optional scoped usage in the final result first. Missing is not zero; thread totals are not per-execution increments. |
| Reported reasoning | Thinking blocks or supported partial updates. | Reasoning items/summary updates. | Later, only what the runtime exposes; do not promise all internal reasoning or equal timing. |
| Command output / changed files | Tool-specific result evidence; arbitrary text is not a reliable command/file schema. | Structured command/file items and supported output updates. | Later typed evidence if a verifier actually needs it; no fabricated parity. |
| Session identity / compaction / subagent activity | Init/system/task messages and supported hooks, varying by version and SDK. | Thread/item/other protocol notifications, varying by version and surface. | Capability-specific later extensions, not required for the first five events. |
| Permissions / user questions | `can_use_tool` and supported hooks; callbacks return provider-specific decisions. | Server-initiated approval/input requests with matching responses. | Separate control contracts if needed; not just one-way events. |

The official Codex Python SDK now controls app-server, exposes typed notifications via a turn handle's `stream()`, and documents steer/interrupt methods. This is a viable candidate for the Python application without a TypeScript bridge. The reviewed high-level Python documentation did not establish a complete application-owned interactive approval response bridge; verify that exact requirement against the selected SDK/version or use a direct app-server control adapter. **Protocol capability does not prove every SDK exposes it.**

Keep the other Codex surface separate: TypeScript `@openai/codex-sdk` has `thread.started`, `turn.started/completed/failed`, `item.started/updated/completed` and `error` events with typed items. Its event schema is not the app-server notification schema. InHarness's synthesized text behavior is specific to its selected integration.

Claude's current Python type definitions include hooks such as PreToolUse, PostToolUse, PostToolUseFailure, UserPromptSubmit, Stop, SubagentStart/Stop, PreCompact, Notification and PermissionRequest. Hook availability differs even between Claude's Python and TypeScript SDKs. An observer receiving our `ToolCallObserved` is not a substitute for an enforceable pre-tool hook.

### Source snapshot

These are **blob SHAs of the inspected files**, not repository commits or pinned dependency releases. Links point to upstream default branches and may change.

| Source | Inspected path | Blob SHA |
|---|---|---|
| Vercel | [Harness overview](https://github.com/vercel/ai/blob/main/content/docs/03-ai-sdk-harnesses/01-overview.mdx) | f4b6cf1db6487f4c1a847dfc8ee2b0d610c271ef |
| Triad | [Provider interface](https://github.com/Triad-Labs-Inc/harness-sdk/blob/main/packages/core/src/provider.ts) | c9a622ceae96e03410c5f7bae7c1cadb0afab4d8 |
| Triad | [Shared types](https://github.com/Triad-Labs-Inc/harness-sdk/blob/main/packages/core/src/types.ts) | 2d9c8ce64ac86460cfa73dc6468534a6700fd54d |
| Triad | [Adapter design](https://github.com/Triad-Labs-Inc/harness-sdk/blob/main/docs/provider-adapters.md) | aa418ece1fe63a585958fde0be851dbc839c3edb |
| Python wrapper | [Events](https://github.com/PentestGPT-Project/UnifedAgentWrapper/blob/main/unified_agent/events.py) | 4ddc3154f6d4484e9623924d6b1a5f7964478550 |
| Python wrapper | [Codex mapper](https://github.com/PentestGPT-Project/UnifedAgentWrapper/blob/main/unified_agent/backends/codex.py) | 9c38b5a4680dda63025711269af87a2b15c4fb45 |
| Python wrapper | [Claude mapper](https://github.com/PentestGPT-Project/UnifedAgentWrapper/blob/main/unified_agent/backends/claude_code.py) | 88c9bec956f3a1c6e93d0420568b27f451a9e8b8 |
| InHarness | [README/event and capability tables](https://github.com/inharness/agent-adapters/blob/main/README.md) | c8b08a96a85768f534c46f203902ea03d43f7498 |
| AgentDock | [README/license statement](https://github.com/crossainthero-lab/AgentDock/blob/main/README.md) | 8b130ba5afa0bbf035e2ac6c0da401a321adc1b4 |
| Claude | [Python message/options/hook types](https://github.com/anthropics/claude-agent-sdk-python/blob/main/src/claude_agent_sdk/types.py) | 5a8358e95141f717f86be2012c49597f7cad54d4 |
| Codex | [TypeScript events](https://github.com/openai/codex/blob/main/sdk/typescript/src/events.ts) | f6ad902779bee05ab0fb9b9cc6a2bca59d52c136 |
| Codex | [Python API reference](https://github.com/openai/codex/blob/main/sdk/python/docs/api-reference.md) | 09031318a4fabfff98529ee9c7057e059742314b |

Additional official documentation checked: [Codex SDK](https://developers.openai.com/codex/sdk), [app-server](https://developers.openai.com/codex/app-server), [Claude streaming](https://code.claude.com/docs/en/agent-sdk/streaming-output), [Claude permissions](https://code.claude.com/docs/en/agent-sdk/permissions), [Claude hooks](https://code.claude.com/docs/en/agent-sdk/hooks), [AgentDock adapters](https://docs.agdc.dev/developer/agent-adapters).

Caution from source comparison: Claude's streaming prose and current Python types differ on some metadata fields, and Triad's adapter design still includes forward-looking declaration wording while source declarations exist. Use selected version source and fixtures to settle exact field availability; do not merge inconsistent snapshots into an imagined API.

## Design proposals and acceptance status

P01–P07 retain their historical proposals and explicit acceptance status. D14/D15 now approve the displayed P07 tree, module responsibilities and ABC approach. Other event/control details remain proposals. P02's Protocol recommendation and the single-contract-file arrangement are historical.

### P01 — Five initial event types (Q01)

**Revision 14 amendment:** D34 accepts the five names and basic meanings only. The table's payload/status details and rules below retain their proposal status unless separately approved; do not interpret catalogue acceptance as wholesale P01 approval.

| Proposed class | Meaning / minimal payload | Reason |
|---|---|---|
| `ExecutionStarted` | Local execution ID and observation time. Emitted once after request validation, before starting provider work. | Common lifecycle marker; it describes the local invocation, not native session readiness. |
| `TextProduced` | Normalized text-unit ID and completed text. | Useful across providers without imposing token streaming on the first version. |
| `ToolCallObserved` | Call ID, action kind/name and available structured input. | Distinguishes observing an intended/represented action from proving it ran. |
| `ToolResultObserved` | Matching call ID, available output and explicit outcome evidence; status may be unknown. | Allows reviewer/verifier logic without importing provider types. |
| `ExecutionFinished` | One `ExecutionResult`: completed/failed/cancelled/indeterminate, final output, optional scoped usage, structured output and error details. | One terminal representation rather than separate overlapping success/error events. |

Proposed common fields: `execution_id`, a sequence number within that invocation and `observed_at`. Exact run/step context integration remains Q09; do not build a second context system. Source-native IDs may be retained internally; application IDs must not be assumed to be native session IDs.

Proposed rules:
- One execution means one bounded task submission through its native internal tool loop. Multi-turn interactive sessions are separate future scope.
- Map zero, one or multiple shared events from one native message. Keep mapping state local to an execution when needed for IDs, complete blocks or result correlation.
- Tool evidence may arrive only when an action completes. Emit call-observed then result-observed if sufficient evidence exists; do not backdate a start time or invent missing input.
- Preserve “unknown” when the native record lacks a success flag, exit code, usage or cost. A textual “tests passed” is not deterministic verification.
- Map shell/MCP/file activities to a small shared action-kind field if required by scope. Provider tool names may be descriptive values, but shared behavior must not depend on native SDK classes or an untyped raw event.
- Complete text units and deltas have different semantics. If deltas are added, give them IDs and distinguish append from completed-snapshot replacement.
- Successful normal delivery has one terminal event and one returned result with identical content. A callback that has failed cannot be promised delivery of a terminal event; expose that failure to the caller (P02).
- Unexpected stream loss is indeterminate unless there is stronger terminal evidence. A cancel request is not proof that side effects stopped. Do not automatically replay an accepted task.
- Do not add an event bus, durable event store, replay protocol or schema migration framework for this initial in-process contract.

Candidate later extensions: `TextDelta`, `ToolProgress`, `UsageUpdated`, typed command/file evidence, diagnostic notices, reported reasoning, compaction and subagent activity. Add only for a concrete consumer need. Final usage can live in the result initially.

Alternative considered: start with all events from one reference library. Not recommended because that imports UI/session/monitoring assumptions and weakens D06. Alternative: use only final results. Simpler, but does not satisfy Sharon's requested event-handling boundary.

### P02 — Historical Protocol proposal and callback rationale (Q02, Q08, Q10)

**Revision 3 status:** the Protocol recommendation is superseded by Sharon's requirement for explicit mandatory abstract contracts (D10/P07). The original rationale below is retained as history. The callback shape is subsequently accepted under D25/D26; callback order, result handling and failure policy still need decisions.

Use a Python `Protocol` for behavior and small frozen dataclasses for event payloads. This uses the standard library and does not force an inheritance hierarchy. Existing project validation models could be reused if runtime validation/serialization is needed; choosing Pydantic is a separate payload-model decision, not the opposite of choosing Protocol.

Illustrative signature only, not implemented code:

```python
EventHandler = Callable[[AgentEvent], Awaitable[None]]

class ExecutionAdapter(Protocol):
    async def run(
        self,
        request: ExecutionRequest,
        *,
        on_event: EventHandler,
    ) -> ExecutionResult: ...

async def handle_event(event: AgentEvent) -> None:
    # Dispatch by our concrete event type.
    ...

result = await adapter.run(request, on_event=handle_event)
```

`AgentEvent` is a union of the five typed event classes. Each concrete adapter satisfies the same contract. The adapter translates native data, then calls the injected callback; it does not require modifying the provider's internal loop.

Default proposal: await callbacks sequentially for one invocation, preserving order and bounded delivery without a background queue. Slow handlers therefore slow observation; handlers should remain short. On a handler exception, surface an explicit delivery failure and attempt provider cleanup/cancellation rather than silently swallowing it. Cancellation effectiveness and any uncertain side effects must be reported. Exact timeout/cancellation behavior remains to settle before implementation.

Use one final result model for both `ExecutionFinished` and the return value. A role's structured reviewer verdict remains its own model, validated by role/workflow logic; transport completion does not validate that verdict.

Alternatives:
- **ABC (original evaluation, corrected in revision 3):** shared default behavior is one reason to use an ABC, but not a prerequisite. Enforcing mandatory methods on ordinary subclasses is also a valid reason, and matches D10.
- **Async iterator:** clean consumer-controlled alternative; an application wrapper can call the same handler. Keep it available if callback delivery becomes awkward.
- **ExecutionHandle:** useful for explicit steer/interrupt/session controls; defer until those capabilities are required.
- **Handler class with one method per event:** more interface churn each time an event is added. One typed entry point is enough initially; internal type dispatch remains possible.

### P03 — Keep settings, control requests and observations distinct (Q04–Q06)

**Revision 5:** D16 excludes human permission/input interaction from the MVP. The corresponding callback rows below describe future extensions.

| Concern | Suggested contract | Provider responsibility | Status |
|---|---|---|---|
| Task input | `ExecutionRequest`: task/instructions and required output contract. | Translate to provider prompt/instruction/output-schema fields. | Proposed |
| Launch/settings | `ExecutionSettings`: only genuinely shared settings such as working directory, timeout and selected model; exact fields still open. | Validate supported settings and translate explicitly; keep provider-only configuration at assembly/adapter boundary. | Proposed |
| Observations | Awaited callback accepting AgentEvent and returning no value. | Map evidence into our events. | Callback shape accepted under D25/D26; failure semantics open |
| Permission decision | `on_permission(PermissionRequest) -> PermissionDecision`. | Map native request into ours; translate the answer back before proceeding. | Optional, unapproved first-version scope |
| User question | `on_input(InputRequest) -> InputResponse`. | Preserve question/request IDs and pending native response correlation. | Optional, unapproved first-version scope |
| Pre-action hook | A named supported control operation, if required, with an explicit result. | Register a real provider interception point; reject unsupported requirements. | Investigate later |
| Interrupt / steer / resume | Explicit operations or handle methods. | Implement only supported lifecycle semantics. | Investigate later |

System instructions are input configuration, not a special outgoing event. Static approval/sandbox settings are policy inputs, not permission request events. An event may report a pending/resolved interaction for display, but it cannot replace the response mechanism.

Do not flatten provider security settings into one misleading “safe” switch. Likewise, a shared `effort` name does not imply equal allowed values, token budgets or model behavior. Decide how provider-native configuration loads from the environment/project; do not inherit it accidentally.

### P04 — One provider adapter; split helpers only when justified (Q04–Q06)

**Revision 3:** D12 now requires basic settings/permissions/logging; P07 proposes their modules. The earlier deferral below is historical. Avoiding a hierarchy of concern-specific adapters remains the recommendation.

Retain the approved two files per provider: `adapter.py` plus `event_mapper.py`. Initially, small request/settings conversion functions can stay in `adapter.py`.

If requirements grow, proposed additions are:
- Shared `execution/settings.py`: owned settings types.
- Shared `execution/interactions.py`: permission/input request and response types.
- Provider-local `settings_mapper.py` or `interaction_mapper.py`: translation helpers.

**Status amendment:** settings.py is subsequently part of the accepted desired tree under D14. interactions.py and provider-local mapper helpers remain future possibilities; D21 keeps initial settings conversion as a function. Do not introduce an EventAdapter + SettingsAdapter + PermissionAdapter + HooksAdapter object hierarchy. Different concerns need clear semantics; they do not each require an independently injected adapter object.

### P05 — Initial reuse approach (Q03, Q07)

Prefer our tiny owned contract with thin integrations to the official Claude Python SDK and, subject to the required control surface, the official Codex Python SDK. Learn mappings from the Python wrapper, capability/control patterns from Triad and boundary organization from AgentDock.

If the Python wrapper later satisfies our chosen contract, version support and reuse terms, it can sit behind our adapter instead. Consumers must still depend on our types. This keeps adoption reversible without committing to writing all harness functionality ourselves.

No library is selected, no license-dependent code is copied and no production maturity is assumed. Do not implement a provider's model/tool loop: let the existing runtime own it.

### P06 — Acceptance evidence when implementation is authorized

Use a small shared fixture suite for the same adapter contract: ordered events, correctly paired tool results, no duplicate completed text, known/unknown outcomes, failure/stream-loss handling and callback failure. Add permission round trips and capability rejection only if those features enter scope. Real provider checks should be explicit and separately configured.

This is future validation planning, not a claim that these checks ran. No tests are needed merely to create these Markdown records.


### P07 — Updated MVP structure and enforcement

**Status, revision 4, amended by D26:** D14/D15 approve the tree and module responsibilities displayed to Sharon, including the ABC approach. D26 subsequently accepts minimal method declarations; logging/error policies and concrete settings remain open. This supersedes the Protocol recommendation and single-file organization while retaining role/provider separation. No Python files have been created.

Paths are relative to `app/src/agent_playbook/`. This is the revision 4 snapshot; the current specification additionally includes agents/agent.py under D25. The two real-provider directories below illustrate later integration, not this deliverable.

```text
agents/
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

| Module | Accepted responsibility / open detail |
|---|---|
| `contracts/execution_adapter.py` | `ExecutionAdapter(ABC)` with required `run(request, *, on_event)`. Exact return/error/cancellation semantics still Q02/Q10. |
| `contracts/event_mapper.py` | Generic `EventMapper[NativeMessage](ABC)` with required `map(native_message)` returning zero or more `AgentEvent` values. Native type bindings stay inside concrete provider code. |
| `contracts/event_handler.py` | Typed `EventHandler` callable signature; no stateful handler base class required. |
| `events.py` | Shared event payload classes/union. Related event data can share one file; separate behavioral interfaces do not imply one file per field/class. |
| `request.py`, `result.py` | Owned task request and execution outcome; role verdict models remain with the role. |
| `settings.py` | Model selection, workspace, timeout and other approved launch settings. Instructions belong in the request. Exact fields open. |
| `permissions.py` | Typed policy data for supported access, initially workspace read-only versus read/edit as a candidate. Separate static policy from any later interactive decision callback. |
| `harness.py` | Shared wrapper prepares/validates request/settings and composes event logging with the role callback, then invokes the chosen adapter. Reuse the existing observability boundary; no new logging framework. |
| `adapters/fake.py` | Deterministic fixture implementation for validating contracts, delivery and failure behavior without a live model. It does not establish native permission enforcement. |

The common harness passes a composed callback into the adapter. That callback sends normalized evidence to the existing logging/observation integration and to the role handler. This preserves the typed callback boundary without duplicating common logging in each provider adapter. Delivery order and logging failure behavior remain Q09/Q10/Q17. The wrapper does not replace CrewAI scheduling or implement a new model/tool loop.

**Enforcement:** use regular subclassing with `ABC` and `@abstractmethod`. On normal application reload, adding a required abstract method makes an otherwise incomplete concrete subclass non-instantiable. An inherited concrete implementation also satisfies that method. Python does not provide Java-style compilation or verify behavior from method names; use the project's static checker for typed override compatibility and a shared contract suite for semantics. Source: [Python abc documentation](https://docs.python.org/3/library/abc.html).

**Pushback on extension strategy:** adding an event class should ordinarily leave `run`, `map` and `handle_event` signatures unchanged. Add mapper cases and tests for each backend that claims the capability. New event types do not automatically cause ABC errors when a mapper forgets a case. Reserve new mandatory abstract methods for behavior every adapter must provide; optional capabilities should not force fake no-op implementations.

**Permissions:** setting `read_only` in our model expresses intent. The real adapter must configure its provider's supported controls so the runtime enforces the policy, and reject requirements that configuration cannot uphold. It does not implement a separate filesystem-security engine. Working directory alone is not confinement; a reviewer that can write via shell is not read-only merely because an edit tool is disabled. Exact permitted roots, external access and shell/network policies are still Q18.

**Logging:** “log everything” is a product goal to scope, not an already-achieved lossless native transcript guarantee. Recommend recording each normalized event, terminal outcome and failure with correlation. Native diagnostic capture and storage/redaction policy require an explicit decision; do not leak native SDK objects into role handlers to obtain logs. Existing logging/context work remains its own integration.

**Delivery reality:** with actual provider adapters excluded, this increment delivers a reusable, tested foundation. Real Claude/Codex runs and their enforced permission behavior become an integration acceptance step. Proposed default is to defer their native mapper implementations too (Q20), while delivering the shared mapper contract now.

**Deferred unless needed:** generic hook registry, per-setting adapters, permission-adapter hierarchy, dependency-injection container, durable event bus, UI, session replay, multi-turn controls. Keep the separation of concerns so these can be introduced deliberately; do not build placeholders for them now.

### Permission clarification evidence — revision 4

The provider's permission system is the enforcement mechanism for supported tool operations. The adapter owns translating our intent into that system and verifying coverage. Additional custom enforcement is not automatically required.

Claude distinguishes tool availability from auto-approval: `tools` configures the built-in tool set; `allowed_tools` pre-approves listed tools and does not itself remove the others; `disallowed_tools` blocks tools/rules. An allow rule alone is not proof of exclusive folder access.

Path-scoped file rules can govern built-in file operations. If shell commands/scripts are available, process-level filesystem limits need the supported sandbox configuration. Claude's shell sandbox covers shell commands and children, while built-in file tools follow permission rules and external tools/processes have their own coverage. Do not claim a sandbox covers every tool automatically.

Illustrative responsibility split, not a finalized configuration:

| Our requested policy | Adapter work | Runtime work |
|---|---|---|
| Reviewer may read approved project files and may not edit | Select appropriate tools and path/permission rules; remove or constrain other enabled routes | Reject unavailable/disallowed operations under those controls |
| Coder may read one directory and write another | Translate allowed roots into supported native controls; reject unsupported scope | Apply file-tool rules and any required process sandbox |

For the simplest reviewer scope, a truly restricted read-tool set can be sufficient for the enabled tools; no custom edit-blocking engine is inherently necessary. Do not confuse this with `allowed_tools=["Read"]`, which has different semantics.

Sources checked 2026-11-14: [Claude Python options](https://code.claude.com/docs/en/agent-sdk/python), [permission rules and paths](https://code.claude.com/docs/en/agent-sdk/permissions), [sandbox coverage](https://code.claude.com/docs/en/sandboxing). No native integration was run. Specific policy fields and configurations remain open.

## Autonomous MVP decision — revision 5

| ID | Decision | Status and rationale |
|---|---|---|
| D16 | Execute autonomously under configured permissions; no human approval prompts or wait-for-human state. | **Approved.** Sharon wants autonomous execution or failure. If an approval cannot be resolved automatically under the configured policy, fail clearly; human responses through CLI/UI are future scope. |
| D17 | Do not introduce a separate tool/policy contradiction engine that blocks authors' workflow choices. | **Approved.** Authors own their combinations. Typed input/configuration checks and accurate provider capability reporting remain distinct; this does not bypass native permissions. |

| ID | Question | Status / answer |
|---|---|---|
| Q24 | Should the MVP wait for a human to answer an SDK permission request? | **Answered:** no (D16). Later, an adapter may route such a request to CLI/UI and return the person's decision to the runtime. |
| Q25 | Does every automatic native permission denial fail the entire execution? | **Open:** a native denial may be tool feedback allowing an alternative action. Define this outcome policy separately; unresolved human approval must not wait. |

## Design direction clarification — revision 6

| ID | Decision | Status / rationale |
|---|---|---|
| D18 | “Both” refers to tool configuration categories, not automatic versus human approval. | **Approved clarification.** Sharon names tools, allowed tools and disallowed tools. Do not artificially conflate those meanings; exact initial fields/defaults remain Q26 because using only a subset was also mentioned. D16 remains unchanged. |
| D19 | Design the shared execution system in small steps before role-specific implementation. | **Approved approach.** Coder/reviewer are grounding examples. A standalone reviewer and later a combined workflow may validate the design, but neither should redirect the immediate discussion into role implementation. |

| ID | Question | Status / next step |
|---|---|---|
| Q26 | Which of available-tools, automatic-allow and disallow controls belong in the initial shared settings, with what defaults? | **Open.** Preserve distinct meanings and extension room; user clarified the topic but did not fix an exact schema. |
| Q27 | What is the order of the remaining design work? | **Answered:** P08's six-step sequence accepted under D20. Step 1's ownership/wiring direction is accepted (D22); step 2 is active and later details remain open. |
| Q28 | Are the contracts all methods called by the adapter? | **Answered.** Harness calls ExecutionAdapter.run; adapter calls its concrete EventMapper.map and the injected callback. Minimal declarations are accepted under D26; detailed failure semantics remain open. |

### P08 — Incremental design plan

**Status: Design sequence approved (D20), revision 7.** The six-step order is accepted. Minimal declarations are subsequently accepted under D26; event/request/result payloads, settings and failure policies remain unresolved. The plan does not authorize implementation or select a concrete provider SDK. Step 1's ownership/wiring direction is accepted under D22; step 2's declarations are accepted and its remaining behavioral details carry into steps 3–5.

| Step | Design topic | Concrete output / completion condition |
|---|---|---|
| 1 | Ownership and one execution's call flow | Agree who creates the request, who invokes the adapter, who maps native output, who delivers/logs events and who returns the result. Confirm the standalone-agent entry path. |
| 2 | Behavioral contracts and request/result boundary | Define the minimum ExecutionAdapter ABC, EventMapper ABC and EventHandler signature, plus the request/result roles. Add required methods only when behavior demands them. |
| 3 | Shared events | Settle the initial event names and essential payloads, correlation/ordering, text versus final completion, tool evidence and the relationship between terminal events and returned results. P01 is the starting candidate, not an approved schema. |
| 4 | Settings, tools and permissions | Define basic configuration and keep available tools, automatic approval and denial distinct. Specify provider translation and unsupported-setting behavior; no new contradiction engine or human approval scope. |
| 5 | Failure handling and logging | Settle execution lifetime, delivery failures, cancellation/timeout behavior where required, terminal status, logging scope and observability failure handling. Clarify a denied tool versus a failed execution. |
| 6 | Acceptance criteria and implementation increments | Write a bounded future build plan and shared contract checks, reconcile affected canonical designs (C01), and identify the separate native integration stage. Start with a deterministic adapter, then a standalone role exercise, then a combined workflow when real integrations are available. |

Each step should close its own questions and update the two records. Return to an earlier step when later evidence exposes a conflict; notify Sharon before changing an agreed decision. Avoid picking all fields, defaults and edge-case policies now.

**Step 1 call-flow direction (accepted under D22; minimum declarations accepted under D26, failure details still open):**

1. A caller invokes an agent role with a task; the caller can be a standalone script or, later, a workflow.
2. The role calls the shared harness with an execution request and its event handler.
3. The harness performs its agreed setup/validation and calls the chosen adapter's `run`, supplying a callback that connects logging and role delivery.
4. The provider adapter starts/uses the native runtime. As native messages arrive, it calls its event mapper; each mapped event is delivered through the supplied callback.
5. The adapter returns the execution result through the harness to the role. The role interprets/validates its own domain output, such as a reviewer verdict. CrewAI retains workflow-level routing.

The sequence describes ownership, not a final failure-handling algorithm. Logging order, exception policy and exact data fields remain in later design steps. The native runtime retains its own model/tool loop; the adapter consumes its output.

| Contract | Implemented/provided by | Called by |
|---|---|---|
| ExecutionAdapter ABC | Concrete provider adapter; deterministic implementation for tests | Shared harness |
| EventMapper ABC | Provider-specific event mapper | Its provider adapter |
| EventHandler callable | Caller/role, composed with logging by the harness | Adapter receives and invokes the supplied callback |

**Settings translation pushback:** do not add a SettingsAdapter interface simply because there is an `ExecutionSettings` model. Translation belongs inside the provider integration and can begin as a small function; split a private mapper module if its complexity later justifies it. Separate behavioral interfaces remain appropriate for replaceable execution and event mapping. No new class hierarchy or generic mapper framework is required by this plan.

**Use-case discipline:** keep coder read/edit and reviewer read as examples when evaluating a proposed capability. Do not specify their prompts, full verdict schemas, routing or orchestration before the shared boundaries. “Reviewer first” is a later validation sequence, not permission to implement a reviewer now.

**Delivery boundary:** real Claude/Codex adapters are still excluded from the current foundation delivery. A fake adapter can validate contract behavior, not real provider capabilities or permission enforcement. An actual reviewer powered by Claude/Codex necessarily depends on a later native integration step; the design plan must label that dependency rather than imply a working live workflow already exists.

## Plan acceptance and adapter-selection discussion — revision 7

| ID | Decision | Status / evidence |
|---|---|---|
| D20 | Accept P08's six-step design sequence and proceed with execution ownership/call flow first. | **Approved.** Sharon explicitly agrees with the design plan and says to move forward. This authorizes continued design, not runtime implementation or implicit acceptance of unresolved schemas. |
| D21 | Keep settings conversion inside the provider integration as a small function; grow the organization if complexity warrants it. | **Approved.** Sharon explicitly agrees with the pushback. No separate SettingsAdapter interface now. |

| ID | Question | Status / next step |
|---|---|---|
| Q29 | Is a separate SettingsAdapter interface needed now? | **Answered:** no (D21); basic provider-specific conversion belongs within the existing adapter boundary. |
| Q30 | Where and how is a concrete adapter selected? | **Answered at mechanism level (D22).** Configuration names a provider; application assembly uses a small factory and injects the adapter into the shared harness. Exact selection scope/defaults, constructors and lifetime remain open. |
| Q31 | What does our harness mean and own? | **Answered at responsibility level (D22).** Common setup/validation, event logging/delivery composition, adapter invocation and result return; native model/tool loop stays in the provider runtime. Detailed lifecycle/error policy remains unresolved. |

### P09 — Harness and adapter selection

**Status: Selection/wiring direction approved under D22, revision 8.** Sharon accepted the harness/selection explanation and requested progression to the contract. Exact YAML fields, constructor parameters, selection scope/defaults and object/session lifetime remain open. The illustrative code is not implementation or approval of every detail.

The harness is an ordinary Python object in the application process. It holds the small shared work around agent execution: agreed request preparation/validation, connecting event logging and role delivery, invoking the adapter, and returning the result. It does not choose model/tool actions, replace a provider's native loop, or schedule workflow steps.

The provider adapter owns SDK configuration translation, native invocation and stream handling, provider event mapping, and provider-specific cleanup. Common behavior belongs in the wrapper only when it is actually shared; provider details must not migrate into the wrapper. No new server, dependency-injection framework or observability broker is implied.

**Accepted selection mechanism (D22), with example labels still illustrative:**

1. Application configuration provides a simple provider choice, such as `claude`, `codex` or `fake`. These are illustrative labels, not an approved YAML schema.
2. Existing application assembly reads the selection. A small explicit factory function constructs an implementation of `ExecutionAdapter`; it can begin within assembly rather than a new registry framework.
3. Assembly passes the selected adapter object into `Harness`, then passes that harness into the agent role.
4. The role calls the same execution API regardless of provider. The harness delegates to the injected adapter without importing/selecting concrete providers in its execution method.
5. Unsupported provider names or required capabilities produce a clear configuration error rather than silent fallback.

Illustrative Python construction only; these runtime classes are not implemented:

```python
# Application setup; provider choice comes from configuration.
adapter = create_adapter(provider="claude")
harness = Harness(adapter=adapter)
reviewer = Reviewer(execution=harness)

# Later, inside the reviewer:
result = await self.execution.run(
    request,
    on_event=self.handle_event,
)
```

`create_adapter` would return `ClaudeAdapter`, `CodexAdapter` or the deterministic implementation according to the configured choice. Exact constructor parameters and where each settings value belongs are decisions for steps 2/4, not settled by this illustration.

**Alternatives and rationale:**

| Option | Assessment |
|---|---|
| Role imports and constructs ClaudeAdapter/CodexAdapter | Not recommended: binds role logic to provider construction and makes replacement/test injection harder. |
| Harness.run switches on provider names and imports SDK implementations | Not recommended: mixes common execution behavior with application assembly/provider selection. |
| Configuration + small assembly factory + injected adapter | Chosen direction (D22): follows the existing assembly boundary and keeps provider choice explicit. |
| Plugin discovery/container or dynamic provider routing on every event | Not needed for the current requirements; adds lifecycle and configuration complexity. |

**Selection scope remains open.** A single application default is the smallest configuration. Per-role choices would allow, for example, a reviewer using one provider and a coder using another without changing role code; each can receive a separately configured harness. A global singleton is not proposed. Decide actual adapter instance/session reuse separately—this example does not promise that adapters are reusable, concurrent or session-sharing.

**First increment:** select the deterministic adapter while developing the shared foundation. The concrete Claude/Codex choices become executable only in the separate native integration stage.

## Execution wiring acceptance and contract draft — revision 8

| ID | Decision | Status / evidence |
|---|---|---|
| D22 | Accept the execution ownership/call-flow direction and configuration-selected adapter injection described in P08/P09. | **Approved direction.** After the harness/selection explanation Sharon said it was good, that he understood, and asked to progress to defining the contract. This accepts the relationship between assembly, role, harness, adapter and mapper; it does not settle exact constructors, YAML fields, default/per-role selection, instance/session lifetime or the new P10 signatures. |

Step 1 is sufficiently agreed to proceed to step 2. Its unresolved lifecycle and configuration details remain assigned to steps 4/5 rather than being treated as implementation decisions.

### P10 — Minimal behavioral contracts

**Status: Minimal declarations accepted under D26, revision 12; not implemented.** D23 confirms separation; D24/D25 settle the mandatory role handler and Agent ABC. D26 accepts the adapter run, mapper map and callback shapes below alongside that role contract. Request/result/event payloads and detailed delivery/failure/lifetime policies remain open; publishing suggestions below is not their approval. No runtime Python files are created.

**1. `execution/contracts/execution_adapter.py`**

```python
from abc import ABC, abstractmethod

from ..request import ExecutionRequest
from ..result import ExecutionResult
from .event_handler import EventHandler


class ExecutionAdapter(ABC):
    @abstractmethod
    async def run(
        self,
        request: ExecutionRequest,
        *,
        on_event: EventHandler,
    ) -> ExecutionResult:
        ...
```

The harness calls this method once for one execution. The adapter translates the request/settings into native configuration, consumes the native runtime's output, invokes its mapper, awaits delivery of mapped events, and produces one shared result on normal return. The provider continues to own its model/tool loop. Provider resources acquired for the invocation must be cleaned up on exit; exact failure/cancellation semantics and any longer-lived session ownership remain step 5.

No separate required `start`, `configure`, `stop`, `resume` or `close` methods are proposed now. A future concrete requirement may justify extending the contract; this draft does not rule out those capabilities.

**2. `execution/contracts/event_mapper.py`**

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ..events import AgentEvent

NativeMessage = TypeVar("NativeMessage")


class EventMapper(ABC, Generic[NativeMessage]):
    @abstractmethod
    def map(self, message: NativeMessage) -> list[AgentEvent]:
        ...
```

A provider supplies its own native message type to this generic interface. Claude types remain in the Claude integration and Codex types in the Codex integration; the role sees only `AgentEvent`.

Mapping is synchronous local translation, not an SDK call, tool execution or logging operation. One native message may produce zero, one or several shared events. Empty output is permitted for irrelevant native notifications; failures or missing evidence must not be hidden as success. A mapper may keep correlation/assembly state scoped to one execution. It must not mix state between executions. Exact treatment of unknown native messages and end-of-stream evidence remains steps 3/5; do not invent a mandatory flush method without a concrete need.

**3. `execution/contracts/event_handler.py`**

```python
from collections.abc import Awaitable, Callable

from ..events import AgentEvent

EventHandler = Callable[[AgentEvent], Awaitable[None]]
```

Any matching asynchronous function or bound method can serve as the handler, for example `async def handle_event(self, event: AgentEvent) -> None`. The callback is typed against our schema and returns no control decision. Tool approvals, tool results supplied back to the runtime, steering and cancellation are separate responsibilities; an observation callback must not silently become that control channel.

The role passes its handler to the harness. The harness supplies the adapter with a composed callback that connects common logging and role delivery. The proposed MVP delivery policy is to await each callback before delivering the next event from that execution; this gives a simple ordered local delivery path. It can slow our event consumption, but does not guarantee that the native runtime pauses or that its buffering is bounded. It does not imply a queue, replay, exactly-once delivery, or global ordering across concurrent executions. Callback exception/timeout policy and the order/failure behavior of logging versus role handling remain Q10/Q17, to settle in step 5.

**Call-direction illustration inside an adapter, not a real provider implementation:**

```python
for event in mapper.map(native_message):
    await on_event(event)
```

The harness can expose the same `run(request, *, on_event) -> ExecutionResult` shape to roles. It is a concrete common wrapper, not another proposed interface hierarchy. Shared setup/validation stays there; native configuration and native message handling stay in the provider adapter. Synthetic application lifecycle events need not come from a native mapper: step 3 must assign their owner and prevent duplicate terminal events.

**Request/result boundary — proposed responsibility, not a frozen field schema:**

| Shared model | Carries | Deliberately unresolved |
|---|---|---|
| ExecutionRequest | Task/instructions and typed execution configuration needed for one invocation. | Exact prompt/context fields, settings nesting, IDs, serialization and provider-specific options. |
| ExecutionResult | The execution's final shared outcome, with output and diagnostic/usage evidence where available. | Status vocabulary, field names, nullable values, exception-versus-result rules and relationship to a terminal event. |
| AgentEvent | An observation emitted during execution, expressed in our types. | Initial event union and payload schemas; P01 is still a candidate. |

A result returns once when `run` returns normally; events can be delivered many times before it. This does not promise a final result under every exception/cancellation. A reviewer verdict or coder-specific output remains the role's interpretation/validation of execution output, not a required field of every provider adapter.

**Alternatives and rationale:**

| Choice | Reason for this proposal |
|---|---|
| Awaited typed callback | Matches Sharon's requested injected method and accommodates asynchronous event handling without a second consumer API. |
| Async event iterator | Viable alternative, not chosen in this draft: would also require settling how the caller obtains the final result and how wrapper delivery is composed. Revisit if multiple consumers or stream composition become a concrete need. |
| Event-handler ABC | Original P10 recommendation: a typed callable suffices for injection. D24 adds a separate role obligation; D25 accepts P11's Agent ABC to enforce it. Callback typing alone does not enforce that role obligation. |
| Synchronous mapper returning a small list | Keeps translation separate from I/O and handles zero/one/many output events with one required method. |
| Separate settings/permission mapper interfaces | Not introduced: D21 keeps settings conversion within each provider integration. |
| Many speculative lifecycle methods | Deferred until a required capability establishes their semantics; preserves a small initial contract. |

**Question updates:** D26 partially answers Q02/Q08 by approving the minimal declaration shapes. Q10's detailed ordered-delivery/failure policy remains open. Event payloads and terminal-result ownership are the next detailed-design step. The chosen SDK/version and real provider integrations remain outside this iteration.

## Separation clarification — revision 9

| ID | Decision | Status / evidence |
|---|---|---|
| D23 | Keep behavioral contracts separated even when each currently has one required method. | **Approved.** Sharon explicitly asks to retain the separation despite the one-method interfaces. Existing adapter/mapper ABCs and their separate modules remain the target; no extra methods are required merely to justify a class. |

**Schema location:** `execution/events.py` is the already accepted home for the application-owned event types and payload schema (`AgentEvent` and concrete events). The mapper contract imports that schema; each provider implementation translates its native types into it; the handler consumes it. The file's role is settled, but its actual event vocabulary/payloads remain Q01 and are not implemented.

**Scope of the earlier pushback:** the suggestion to use a typed callable instead of another ABC referred specifically to `EventHandler`, already in its own `execution/contracts/event_handler.py` module. It did not propose merging any modules or removing the adapter/mapper ABCs.

| ID | Question | Status / next step |
|---|---|---|
| Q32 | Does Sharon also want EventHandler itself to be an ABC with a required handle_event method, rather than the proposed typed callable in its own file? | **Answered under D24/D25, revision 11.** Agent ABC in agents/agent.py requires handle_event; each role explicitly implements it, even as a no-op. EventHandler is the typed callback passed through the harness. No separate EventHandler ABC is required. |

P10 remains the concrete execution contract draft. D23 confirms separation and the existing adapter/mapper ABC direction; D24 clarifies Q32's role obligation, with P11 accepted under D25 as the mechanism. Detailed lifecycle/failure policies remain open. No new runtime files, event schemas or interface implementations are created in this iteration.

## Mandatory role handler clarification — revision 10

| ID | Decision | Status / evidence |
|---|---|---|
| D24 | Every application agent role participating in this execution boundary must explicitly implement handle_event; an explicit no-op implementation is allowed. | **Approved requirement.** Sharon identifies reviewer/coder/implementer as the implementers and explicitly says every agent must implement the method, even if empty. Provider adapters implement their native event mappers and invoke the supplied callback; they do not implement the role's domain event handling. |

**Q32 resolution:** the intent is a mandatory method on agent roles, not a requirement that each provider adapter implement an EventHandler subclass. The Agent ABC and callback arrangement under P11 are now accepted by D25 (revision 11). The callback can still be passed to `run`; requiring a method on a class and passing that bound method as a callback are compatible.

### P11 — Enforce handling on the agent role; pass a callback to execution

**Status: Accepted design under D25, revision 11; not implemented.** The Agent ABC in agents/agent.py and its required async handle_event(event: AgentEvent) -> None are accepted, with the bound method supplied as a typed callback. This adds one small role-side ABC to the desired design. It does not alter native adapter/mapper responsibilities or finalize P10's remaining execution semantics.

**Accepted arrangement:** `agents/agent.py` defines an `Agent` ABC with the required asynchronous `handle_event` method. All application agent roles in this execution design inherit from it. The existing `execution/contracts/event_handler.py` keeps the typed callback signature. This separates enforcement of the role obligation from execution-side callback delivery.

Illustrative code only (each class would live in its own relevant module):

```python
from abc import ABC, abstractmethod

from ..execution.events import AgentEvent


class Agent(ABC):
    @abstractmethod
    async def handle_event(self, event: AgentEvent) -> None:
        ...
```

Example role implementation, deliberately a no-op:

```python
class Reviewer(Agent):
    async def handle_event(self, event: AgentEvent) -> None:
        pass
```

At the existing execution call site inside the role:

```python
result = await self.execution.run(
    request,
    on_event=self.handle_event,
)
```

The harness composes common logging and role delivery and supplies the adapter with a callback of the same signature. The adapter continues to invoke `await on_event(event)`; it does not require knowledge of the Reviewer or Agent class. `self.handle_event` is the bound method passed as a value; `run` neither defines nor implements that method.

The accepted callback shape connecting the role to execution is:

```python
EventHandler = Callable[[AgentEvent], Awaitable[None]]
```

Here `Awaitable[None]` means that the callback is awaited and supplies no result value. The role-side method uses `async def ... -> None`. An ordinary Agent subclass missing the abstract method cannot be instantiated. ABC enforcement does not verify that a handler performs useful work or that overriding parameter types match; explicit no-op is allowed by D24 and signature compatibility needs static checking.

**No new methods solely for symmetry:** this contract adds only the requested role obligation. It does not define an agent lifecycle, role task schema, workflow scheduler, session API or a generic agent framework.

| Alternative | Assessment / reason |
|---|---|
| Agent ABC requires handle_event; execution receives the bound method as a callback | Chosen under D25: directly enforces the requirement on every participating agent role while preserving the existing callback flow. |
| EventHandler ABC implemented by reviewer/coder roles | Valid alternative, not selected under D25. The Agent ABC already expresses the required role method; an additional handler ABC is unnecessary for the current contract. |
| Typed callback only, with no role-side abstract requirement | Insufficient by itself for D24: describes the supplied function but does not require every agent class to define a handler. |
| Non-abstract inherited no-op handler | Convenient, but does not satisfy Sharon's explicit requirement that each role implement the method itself. |
| Provider adapter implements the role handler | Assistant-mentioned boundary caution, never proposed by Sharon. Sharon explicitly confirmed role/provider separation; the assistant acknowledged that this pushback was misplaced. It is not a rejected user proposal. |

**Pushback:** requiring the method guarantees an explicit implementation point, not useful event processing. Allowing a no-op is consistent with roles that use only the final result. Do not force roles to add logging or fake handling just to satisfy the contract.

**Structure status:** D25 accepts agents/agent.py as an addition to the desired tree in the working specification. The existing role/execution split and separate contracts remain intact. This does not change canonical repository files: C01 reconciliation is still required before implementation. No conflict with native-loop ownership or autonomous-permission decisions was identified.

## Agent ABC acceptance and ownership correction — revision 11

| ID | Decision | Status / evidence |
|---|---|---|
| D25 | Accept P11's Agent ABC in agents/agent.py with required async handle_event(event: AgentEvent) -> None; each participating role explicitly implements it, and execution receives a typed callback. | **Approved design.** Sharon asks whether reviewer/coder must implement the method, says this is needed, and explicitly says to proceed and update both records. This accepts the small role-side contract, including the explicit no-op allowed under D24. It authorizes documentation, not runtime implementation, a repository commit or a PR. |

**Terminology:** an ABC is our Python abstract base class defining required methods. A provider SDK is an external integration library used inside a provider adapter. `Agent` is our application role contract; this discussion is not adopting a new agent SDK.

**Correction to the intervening exchange:** Sharon explicitly rejected the suggestion that provider adapters should implement role-specific handling and stated that the adapter should implement its own execution interface. He had never proposed moving role behavior into providers. The assistant's earlier pushback introduced a problem that was not being proposed; it must not be recorded as a rejected user design. This clarification preserves D03/D04/D22/D24 rather than changing them.

| Component | Required method in the current design | Implementer / caller |
|---|---|---|
| Agent ABC | handle_event(event) | Implemented by each reviewer/coder/other application agent role; supplied through the harness as a callback. |
| ExecutionAdapter ABC | run(request, *, on_event) | Implemented by the selected provider adapter or deterministic implementation; called by the harness. |
| EventMapper ABC | map(native_message) | Implemented by each provider's mapper; called by that provider's adapter. |
| EventHandler callback type | No class method to implement | Describes the asynchronous function/bound method passed as on_event; the adapter awaits the supplied callback. |

The role's requirement to implement `handle_event` does not add `map` or the execution-adapter `run` method to that role. Concrete agents will need their own task behavior, but its shared interface is not specified by this decision.

**Reason and alternatives:** the small Agent ABC directly enforces Sharon's explicit role-method requirement. Callback-only typing cannot enforce that requirement on agent classes. A separate EventHandler ABC could express a handling capability, but adds no required behavior beyond the accepted Agent contract here. An inherited default no-op would remove the explicit implementation requirement and is therefore not the selected design.

**Pushback and extension boundary:** the Agent ABC is justified by the current mandatory method; future permissions, system behavior or hooks do not need placeholder methods now. Sharon's mention of those future capabilities is exploratory. Add a required role method only when its behavior, owner and use case are defined, and explain the effect on existing role implementations before changing the contract. Configuration values can remain typed data rather than becoming methods. Existing native permission enforcement and the unattended MVP remain unchanged; this is not approval of an interactive permission handler.

**State of the design:** Q32 is answered under D25. The role-side contract and its callback connection are accepted. P10's exact execution request/result fields, event payloads, delivery/failure semantics and native SDK choices remain open. The next design topic is the shared event schema, after resolving any remaining contract questions. No implementation has started.

## Three-ABC approval and design review — revision 12

| ID | Decision | Status / evidence |
|---|---|---|
| D26 | Approve all three ABCs together: Agent.handle_event, ExecutionAdapter.run and EventMapper.map, with the minimal declaration shapes in P10/P11 and the typed callback wiring. | **Approved design.** Sharon explicitly says he agrees with the previous explanation and likes all three ABCs, and asks to add that approval to both records. This settles the interface choices; it does not implicitly select P01's event catalogue, unresolved payload fields, statuses, failure policies or SDK versions. No implementation is authorized. |

**Naming clarification retained:** a “provider mapper” is the concrete ClaudeEventMapper or CodexEventMapper implementing EventMapper. It is not a new layer. Prefer the explicit names in explanations. EventHandler is the callback type, not a fourth ABC; Harness is the existing concrete shared wrapper.

**Review coverage and limits:** both working records were reread in full, together with the visible conversation and the current canonical architecture, project structure and design contract. The original inaccessible shared transcript remains unavailable; the earlier handover is a reconstruction. This was a design/document review, not a runtime test, provider parity check or fresh verification of every upstream library claim.

### Review findings

| Finding | Evidence / consequence | Status and recommendation |
|---|---|---|
| F01 — Stale approval labels | H12 still called the generic agent base exploratory; P02/P03 still treated the callback as proposed; H08/P04 obscured the later settings decisions; Q02/Q08 and A04 lagged current contract approvals. The fake's inclusion was approved in D14/D20 while some prose still called all of it proposed. | **Corrected documentation drift.** Preserve historical rationale and distinguish the now-approved narrow choices from still-unselected registries, role catalogues, advanced controls and native mapper scope. |
| F02 — Completion has more than one representation | P01 proposes ExecutionFinished carrying ExecutionResult, while run returns a result. Lifecycle ownership and behavior on callback/transport failure are not finalized. | **Open: Q01/Q02/Q10.** Before implementation, assign one owner for local lifecycle/terminal emission and define result/event agreement. Recommendation for step 3: consider harness-owned local start/finish around adapter execution, while adapter/mapper report native evidence. This ownership detail is a proposal, not approved by this review. |
| F03 — Awaiting delivery does not control the native runtime | Callback invocation is awaited, but a native process may continue producing messages or performing actions. Error, cancellation and buffering behavior depend on integration details. | **Open: Q10/Q06/Q30.** Ordered local delivery is not a native pause, safety gate, bounded native buffer or exactly-once guarantee. Define what happens when a role handler, logger or native stream fails; do not add a queue or retry framework by default. |
| F04 — Permissions/settings have direction but not an executable schema | Available tools, automatic allow rules and deny rules have distinct meanings; SDK/version and capability coverage are unselected. D16 settles unattended execution, not every native tool-denial outcome. | **Open: Q03/Q04/Q18/Q25/Q26.** Pick a small initial policy and per-provider compatibility rules. Preserve unsupported-policy reporting and native enforcement. No second permission engine or human approval wait is introduced. |
| F05 — Working design and canonical records have different approval status | Current architecture acknowledges the execution-event refinement as exploratory; current structure has no accepted agents folder and still labels role/harness details exploratory. | **Open: C01/Q12.** This is a pending canonical promotion/reconciliation, not evidence of broken runtime code. Present the exact logical updates and obtain the scoped guarded-document approval before editing those records. No guarded file, code or Atlas change made here. |
| F06 — Agent's task entry point is not specified | Agent.handle_event enforces observation handling; it does not define how a workflow or script supplies the task and receives a role result. P08's flow presumes such a call. | **Open: Q33.** Define that entry path during detailed design. It may be a role-specific method; do not add a second Agent ABC method purely for symmetry. |
| F07 — Role helper files may duplicate a small method | The accepted tree includes both a role's agent.py and event_handler.py, while the role class must implement handle_event. No delegation responsibility has been specified. | **Open: Q34.** Keep the approved tree unchanged in this review. Recommendation: let handle_event delegate to a helper only if there is real logic to separate; avoid two competing handler contracts or empty scaffolding. Any removal/change to the accepted structure must be presented first. |
| F08 — A fake establishes only local contract behavior | D13 excludes real native adapters; D14/D20 include a deterministic foundation. Native mapping and enforcement cannot be verified by fake events alone. | **Scope clarified, not expanded.** Shared-contract acceptance and real-provider integration acceptance must remain separate. Q20 still covers concrete native-mapper delivery; use representative native fixtures and explicit live validation when native integration is authorized. |
| F09 — Logging/context and mutable state need an agreed connection | The harness composes logging and role callbacks; IDs, context propagation, adapter/role reuse and mapper state lifetime are not fully declared. Separate logging/context work already exists. | **Open: Q09/Q17/Q30.** Reuse that work rather than define another context or tracing system here. Decide invocation-level state/correlation before concurrent reuse; do not infer safety from an async method or shared event names. |

**Interface enforcement limitation retained:** ABCs prevent instantiation when an abstract method remains unimplemented. An inherited concrete method can satisfy an ABC; the requirement for each concrete role to explicitly implement handle_event is also a project convention, not automatic proof supplied by Python for every descendant class. No-op is deliberately valid. Static checking covers compatible signatures, and behavioral acceptance covers mapping/results; an ABC alone proves none of those semantics. No custom metaclass or inheritance policing is proposed.

### Additional open questions identified in review

| ID | Question | Status / next step |
|---|---|---|
| Q33 | How does a workflow or standalone caller invoke an agent task and receive its role-specific result? | **Open.** Define the entry path and inputs/output ownership. Keep separate from execution-adapter run; a new generic Agent method is not automatically required. |
| Q34 | What does each role's event_handler.py own beyond the role's required handle_event method? | **Open.** Clarify delegation versus unnecessary empty/duplicated files; accepted tree unchanged pending that decision. |

### Assessment and next design boundary

**Assessment: good architecture foundation; ready for detailed design; not ready for runtime implementation.** The split is consistent: roles own their task interpretation, adapters own provider execution, event mappers translate native evidence, the harness shares local wiring, and CrewAI retains workflow scheduling. One-method ABCs are justified by the explicit interface requirements. This design does not need another abstraction hierarchy.

The main work now is semantics rather than more folders/classes. Continue the accepted sequence with one representative invocation and the initial shared event schema, including terminal-result ownership (F02). Then settle basic settings/permissions and failure/logging/lifetime rules. Close the role entry-point question and perform canonical reconciliation before an implementation plan is declared ready. Long-term session control, UI, queues/replay and richer hooks need not be designed to complete this MVP.

**Review recommendations are not new approved decisions.** D26 is the new approval. F02–F09 remain findings/open items unless already governed by an earlier decision. This review neither selects an external library nor starts an implementation.

### Canonical source snapshot for this review

Read from the repository default branch on 2026-11-14. These are file blob SHAs, not implementation commits or release pins.

| Source | Blob SHA | Review use |
|---|---|---|
| [architecture.md](https://github.com/SharonLanger/agent-playbook/blob/main/designs/architecture.md) | e017cfc0389390654fe5283ad34882c1df0a89ba | Confirms ownership, native-boundary rules, failure reporting and exploratory event refinement. |
| [project-structure.md](https://github.com/SharonLanger/agent-playbook/blob/main/designs/project-structure.md) | 8f7f8422e9a5352d201d4c4cb00c56bb5f598e26 | Confirms canonical folder ownership and pending role/harness promotion. |
| [design-contract.md](https://github.com/SharonLanger/agent-playbook/blob/main/designs/governance/design-contract.md) | af403b5c993820fa7ca333b310762f409bc64e54 | Confirms approval/state distinctions and canonical reconciliation process. |


## Parallel milestone planning and PR authorization — revision 13

These entries record the subsequent discussion, separately from the detailed recommendations drafted for review. The historical D08 ban on creating a PR is amended only for this documentation PR; no runtime or merge approval follows.

| ID | Decision / status | Evidence, rationale and alternatives | Consequences |
|---|---|---|---|
| D27 | **Approved planning boundary:** pursue execution design in parallel with Stage 02; defer its context/Langfuse concerns from the first foundation work. | Sharon explicitly wants parallel designs and says to ignore context/Langfuse-related additions for now, assuming later support. Waiting for all observability work would unnecessarily block independent contracts; creating substitute context/tracing infrastructure would compete with that work. | Keep shared seams open; do not add context fields, tracing/export or a new logger here. Recheck actual application contracts before workflow integration. This does not repeal D12's logging requirement. |
| D28 | **Accepted direction:** plan shared execution foundation, then a simple deterministic agent, ending with invocation through maintained CrewAI infrastructure. | Sharon proposes everything around native integrations first and a simple deterministic agent; accepts progressing with a design PR. A real reviewer/coder first would force SDK and role details before the shared boundary. | Four checkpoints are now drafted as S04.M1–M4; their exact allocation/acceptance criteria await review. They organize D20's design topics rather than claiming those questions are already answered. |
| D29 | **Approved exclusion/clarification:** later native integration includes SDK plus actual provider adapter, concrete event mapper, settings/permissions translation and lifecycle verification. | Sharon agrees that the later work is not merely calling an SDK and explicitly keeps actual adapters outside the foundation. No extra global stage is required by this clarification. | Q20 answered. Keep the roadmap unchanged as explicitly requested. Stage 04/05 reassignment remains a working suggestion requiring later sequencing review. |
| D30 | **Accepted fake fidelity requirement:** exercise mapping and shared event delivery with useful representative behavior. | Sharon explicitly agrees the fake must reflect real integration and test the mapper. He suggests a count of tools and random numbers selecting events. Fixed scripts are recommended for reproducibility; random variation is still exploratory. | Fake native messages → fake mapper → shared events must be covered. Exact script/input/event counts, random generation and timing are Q36. A fake cannot prove native permissions or parity. |
| D31 | **Authorized now:** create a draft repository design PR with permanent organized records, milestones, history/references and drift prevention. | Sharon explicitly says to create it after discussing the PR modeled on #43. Earlier standalone files must not become competing active specifications. | This package becomes the active home; preserve original revision-12 bytes as history. No roadmap/guarded-meaning change, runtime implementation, dependency adoption or merge. D08's earlier no-PR restriction is amended for this scope only. |
| D32 | **Approved process:** milestone boundary changes originate in the milestone plan and are verified against existing decisions/specification before application. | Sharon's latest instruction explicitly adds milestone boundaries and plan-first checking. Changing implementation first and retrospectively adjusting records would defeat drift prevention. | Use the plan's Pending → conflict/approval check → coordinated application protocol. Read the full active spec/board before each iteration. A pending proposal does not authorize itself. Preserve superseded decisions and reasons; update all affected current records together. |

### New questions and deferred dependencies

| ID | Question | Status / owner / next step |
|---|---|---|
| Q35 | How does independent agent execution connect to the shared context model, especially without a workflow invocation? | **Deferred to context/execution coordination before integration.** Stage 02 owns context data/propagation; this track owns agent runtime lifetime. Do not invent workflow identifiers or a duplicate context model. Reinspect the actual merged contract before S04.M3/M4 needs it. |
| Q36 | What exact fake scripts, task input/count, demo delay and optional variation should the first exercise expose? | **Open — S04.M2/M3 design.** Fixed scripts and zero/short test delay are recommendations. Random event selection and a visible half-minute delay were examples, not approved defaults. |
| Q37 | When and how should the global Stage 04/05 descriptions be reconciled with this foundation-first direction? | **Deferred — deliberate roadmap review before implementation lock.** Sharon explicitly instructed that the roadmap stay unchanged now. No added stage or sequencing amendment is approved here. |
| Q38 | Where does actual execution-event logging join this path, and what counts as acceptance? | **Deferred integration requirement; detailed policy open (Q09/Q17).** D12 stays required. A test event recorder establishes local delivery only, not persisted/correlated logs or successful export. Coordinate with the separate logging/context track; no new backend in these checkpoints. |

Q01/Q02/Q04/Q08/Q10/Q26 remain open in the portions needed for S04.M1. Q33/Q34 remain for the demo entry/helper design. Q03/Q07 and concrete native security behavior can wait for native integration. At revision 13 P01 was proposed. D34 now accepts the names/basic meanings; its payload and outcome policies remain proposed.

### Parallel-work assessment and PR #43 reference

Main inspected: d12b5fc2867d3646b6fab2eb71f1447ff177d8c1. [PR #43](https://github.com/SharonLanger/agent-playbook/pull/43) was open, draft and unmerged at head 11bba581291c1b166973848ea8db6a9e2a142413. Its [entry point at that revision](https://github.com/SharonLanger/agent-playbook/blob/11bba581291c1b166973848ea8db6a9e2a142413/designs/stages/02-langfuse/workflow-integration/README.md) now describes the detailed context/test/implementation-review draft. This package borrows its organization and explicit evidence/status separation; it does not adopt that other track's review-agent procedure or context schema as this track's locked design.

Independent folders support parallel design, not automatic merge or semantic independence. Shared assembly, workflow constructors, configuration, documentation navigation and generated Atlas will require reconciliation. PR #43's data-only context and rejected tracing-broker direction must not be replaced by an execution-owned observability system. Recheck the other PR when those dependencies become relevant.

### Consistency result and limits

- D02–D26's narrow interfaces, role/provider separation, native loop ownership, autonomous execution and minimal adoption remain intact.
- D08's PR restriction is deliberately amended by D31, while its runtime restriction remains.
- D12's logging requirement is retained and scheduled outside the initial foundation integration under D27/Q38.
- Native mappers are explicitly deferred under D29; fake mapping remains included under D30.
- The longer-term role tree is preserved; a demo is the first exercise, not an approved removal of role responsibilities.
- C01 remains open. Q37 tracks the roadmap tension. Neither conflict is resolved by changing a draft's status label.
- Exact milestones, new acceptance suggestions and fake semantics are review proposals. This PR is not implementation acceptance.

The plan's BC01 is the initial draft boundary entry. Later scope changes must first create a Pending BC entry and follow D32. Research findings above are preserved at their original inspection snapshots, not freshly reverified upstream claims.



## Merge-last rule and event catalogue approval — revision 14

| ID | Decision / status | Evidence, alternatives and consequences |
|---|---|---|
| D33 | **Approved: PR #45 remains open and merges last, only after the entire Stage 04 implementation is accepted and merged.** | Sharon explicitly requests this merge order and ongoing design-document workspace. Earlier generic no-merge-without-approval statements did not define this ordering; this adds it. Do not merge at design approval, a milestone checkpoint or as an implementation prerequisite. Keep the README, milestone plan, PR title/body and current records explicit. Final reconciliation and Sharon's explicit merge authorization are still required. |
| D34 | **Approved: initial five event names and basic meanings — ExecutionStarted, TextProduced, ToolCallObserved, ToolResultObserved, ExecutionFinished.** | Sharon reviews the preceding five-event explanation and says the event types are fine. This accepts that catalogue, not all earlier P01 fields/statuses/rules. Q01 is partly answered. A broader initial stream catalogue remains unnecessary for the current agreed baseline; final usage in a result is still an independent open design choice. |

Schema placement is the previously agreed execution/events.py, with AgentEvent consumed by the mapper/callback. Separate behavioral interfaces remain separate files. The shared event payloads do not each need an ABC. Native provider mappings remain later integration; the fake mapper's exact path is still to be designed.

The user also asks what optional incremental text, reported reasoning, usage updates and tool progress mean. The specification now explains these as future possibilities; that request is not approval to add them. No library/model implementation, payload fields, local lifecycle emitter or delivery guarantee was selected. No runtime or merge action is authorized.

Consistency: D33 supplements D31/D32 and is recorded as BC02 in the milestone plan. D34 narrows Q01/P01 within existing M1 scope. D02–D32, native runtime ownership, autonomous permissions, deferred logging and historical alternatives remain intact. Roadmap reconciliation belongs to the separate owner; no other branch is edited.

## Reference-led field proposal — revision 15

D35 — **Approved direction:** Sharon endorses the future-event suggestions, asks to learn event vocabulary from reference projects and keep our owned implementation, and requests one workflow to ground a field proposal. Future categories remain future; no exact field schema, dependency adoption or runtime implementation is approved. This reaffirms D02/D05/D11 and leaves D33 intact.

### P12 — Minimal fields illustrated by a standalone reviewer

**Proposed, not accepted.** Within S04.M1's existing event/data design scope; no milestone boundary change. Reviewer reads one supplied file and returns findings. This is a design example, not a new M3 role deliverable or replacement for DemoAgent.

Each event has a fixed `type` discriminator matching its variant. Its other fields are typed per variant, not an arbitrary common dictionary. `AgentEvent` remains the union in execution/events.py. Immutable data is recommended; dataclass versus Pydantic remains Q08.

| Event | Proposed fields beyond type | Meaning |
|---|---|---|
| ExecutionStarted | None yet | Local execution begins; invocation metadata is not repeated in its payload. |
| TextProduced | text_id: str; text: str | One completed text unit. Stable local text ID leaves room to associate future deltas with the completed snapshot. |
| ToolCallObserved | call_id: str or None; tool_name: str; input: JSON object or None | A reported call and available arguments. None means unavailable, not empty arguments. Provider names are descriptive; generic consumers must not infer capabilities from spelling. |
| ToolResultObserved | call_id: str or None; output: JSON value or None; status: succeeded / failed / unknown | Same call ID when pairing is established. Output can carry reported error details. Unknown must not default to success. JSON null/unavailable output is not distinguished in this minimal draft. |
| ExecutionFinished | result: ExecutionResult | Reuse the result model instead of separate terminal status/output copies. Exact result/delivery relationship still requires approval. |

Proposed smallest result shape for this example: status (completed / failed / cancelled / indeterminate), final_text (str or None), error (str or None). Completed means runtime completion, not an approved reviewer verdict. Role findings stay role-owned. Optional structured output and final usage remain separate design choices; no token/cost zero defaults. Cancellation controls and callback-exception guarantees are not implied by the status enum. These names are candidates carried forward from P01, not newly approved behavior.

Example observations: ExecutionStarted; ToolCallObserved(call_id='call-1', tool_name='read_file', input={'path':'calculator.py'}); ToolResultObserved(call_id='call-1', output='<file contents>', status='succeeded'); TextProduced(text_id='text-1', text='Possible division by zero.'); ExecutionFinished(result with status='completed', final_text='Possible division by zero.', error=None). Tool name and IDs are illustrative. A reviewer finding a bug is not an execution failure.

Pairing rules proposed: normalize an evidence-backed native call identity; keep any mapper state local to one invocation. If native evidence supplies no usable pairing key, preserve None rather than guess using tool name or arrival order. Locally generated IDs can label known entities but cannot prove a relationship. Text IDs identify text units within this invocation; duplicate/final-delta handling remains to specify when streaming enters scope.

No workflow ID, correlation ID, Langfuse ID or context placeholder is added. Execution envelope identity, sequence/time and invocation scoping remain Q01/Q09/Q35, to resolve before concurrent consumption/integration; callback association alone is not a global identity guarantee. P01's proposed envelope is retained as an alternative, not silently adopted or rejected. This field discussion deliberately does not implement a second context system under D27.

Alternatives: copying an entire reference catalogue brings session/history/UI requirements; anonymous tool results lose pairing; bool success with a default of false or true loses unknown evidence; one untyped payload loses per-event field checking; duplicating terminal output/status apart from the returned result risks disagreement. Reuse reference patterns selectively. Model/tool loop and permissions remain native-owned.

### Focused source review for P12

Inspected upstream source/docs on 2026-11-14; not installed or run; no version pin or parity certification.

- [UnifiedAgentWrapper event source](https://github.com/PentestGPT-Project/UnifedAgentWrapper/blob/main/unified_agent/events.py): frozen dataclasses and a union; separate text delta/completed text/reasoning, call name/input/optional ID, result output/error, progress and completion. We use its small Python shapes as reference, but recommend unknown-aware result status rather than adopting its default is_error=False.
- [Vercel streamText reference](https://ai-sdk.dev/docs/reference/ai-sdk-core/stream-text): typed text/tool events, tool-call IDs on calls and results, input/output fields and finish/usage information. This is the shared stream reference, not a claim that every harness emits every field.
- [Triad shared types](https://github.com/Triad-Labs-Inc/harness-sdk/blob/main/packages/core/src/types.ts): event union with session/turn identity, sequence, timestamp and history/subscription surfaces. Useful distinction between content and an event envelope; do not import its persistence/session machinery for our callback contract.
- [Vercel harness architecture](https://github.com/vercel/ai/blob/main/architecture/harness-abstraction.md): adapter is the native-runtime translation boundary. No framework or sandbox infrastructure adopted.

InHarness package/source retrieval failed during this focused refresh; its earlier research remains historical and was not freshly verified. No new claims about its current schema are needed for P12.

Q01/Q02/Q08/Q09/Q10 remain open for exact payload acceptance, result semantics, identity/delivery and model representation. Next review can settle these fields before lifecycle emission ownership. The research and proposal do not resolve C01 or authorize implementation.

## Maintenance rule

Read both files before progressing the design. Update this board with evidence and explicit status; update the specification only for accepted decisions. Detect conflicts before edits. Tell Sharon before changing any agreement; retain superseded entries and rationale. Maintain the two active repository records, keeping cross-links and revision numbers consistent; original saved files are history. Boundary changes must first be proposed in [milestone-plan.md](milestone-plan.md), then applied under D32 across all affected records. Do not turn a recommendation into “Approved” because it appears in a file.

## Revision history

| Revision | Date | Change |
|---|---|---|
| 1 | 2026-11-14 | Created recoverable decisions, alternatives, open/answered questions, conflict register and research actions. |
| 2 | 2026-11-14 | Added verified native/reference findings, source snapshots and P01–P06; answered Q14–Q16, completed A02/A03. All new design choices remain Proposed. |
| 3 | 2026-11-14 | Recorded D09–D13 and MVP correction; resolved C03, preserved superseded arrangements, clarified text/ABC behavior, proposed P07 and tracked permissions/logging/native-integration limits. |
| 4 | 2026-11-14 | Added D14/D15 acceptance, answered Q19/Q23, clarified native permission enforcement and tool availability versus auto-approval; no runtime implementation. |
| 5 | 2026-11-14 | Recorded autonomous MVP scope, deferred human approval and no separate tool/policy contradiction engine; native-denial outcome policy remains open. |
| 6 | 2026-11-14 | Clarified tool-setting intent (D18), ecosystem-first incremental design (D19), and proposed P08 phased plan/call flow; no implementation. |
| 7 | 2026-11-14 | Accepted design sequence/settings simplicity (D20/D21); added P09 harness explanation and proposed adapter selection, with scope/lifetime open. |
| 8 | 2026-11-14 | Accepted execution wiring/adapter-selection direction (D22); moved to design step 2 and drafted P10 minimal contracts with request/result responsibilities and unresolved semantics clearly marked. |
| 9 | 2026-11-14 | Reaffirmed separate one-method contracts (D23), clarified the schema location, and retained EventHandler ABC versus callable as a targeted open question (Q32). |
| 10 | 2026-11-14 | Recorded mandatory explicit role handle_event implementations (D24), clarified mapper versus handler ownership, and proposed P11 Agent ABC plus callback wiring. |
| 11 | 2026-11-14 | Accepted the Agent ABC and role-side handle_event contract (D25), answered Q32, updated the desired tree, and corrected the earlier misplaced provider/role pushback. Future permission/system methods remain open. |
| 12 | 2026-11-14 | Recorded explicit approval of all three ABCs and minimal declarations (D26); reviewed both records and current canonical boundaries, corrected stale statuses, and logged remaining design gaps without adopting new policies. |
| 13 | 2026-11-14 | Recorded D27–D32 and Q35–Q38; answered Q20; preserved original records; authorized draft design PR and introduced explicit plan-first milestone boundaries without changing roadmap or implementation. |
| 14 | 2026-11-14 | Added D33 merge-last rule and D34 five-event approval; partially answered Q01, clarified P01 remaining proposals and payload placement; no runtime changes. |
| 15 | 2026-11-14 | D35 records reference-led direction and future-category endorsement; P12 proposes reviewer-grounded fields with fresh source references; no field approval or implementation. |
