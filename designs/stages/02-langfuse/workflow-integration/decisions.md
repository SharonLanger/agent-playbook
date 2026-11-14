# Decisions and open questions

Updated: 2026-11-14, iteration 23. The decision register contains **accepted discussion decisions**, not a complete approved/locked implementation design. P02/P03 below are proposals; P03 revises P02's trace-binding recommendation. [Requirements](requirements.md) is the specification; [full history](history/context-discussion.md) preserves reasoning and superseded proposals. Read [the entry point](README.md) before using this record.

## Decision register

| ID | Decision | Current status |
|---|---|---|
| D01 | workflow_id identifies the definition; workflow_run_id identifies an invocation; trace_id identifies the overall trace that may later contain repeated workflow invocations | Accepted; exact types/generation/binding remain open |
| D02 | Future application logging uses a project-owned facade instead of vendor calls spread through workflows | Deferred logging requirement; does not restore a tracing broker |
| D03 | Logging backend and viewer can be replaced independently | Deferred logging requirement |
| D04 | All tracing access must be provider-neutral and Langfuse clients hidden behind that API | Superseded for tracing by D11; safe central configuration retained |
| D05 | Logs and trace observations are distinct and correlated | Accepted; a log-only message does not imply a trace |
| D06 | ExecutionContext, ObservabilityContext, LogRecord, workflow_run_id, agent_run_id | Accepted names; former ObservabilityBroker object removed by D11; EventBroker is not an observability name |
| D07 | One ObservabilityContext inside ExecutionContext; shared values represented once | Accepted; no speculative context sections now |
| D08 | Keep operation/span identity, including separate tool/model operations within an agent invocation | Accepted; use SDK mechanics, no custom span engine; public exposure remains open |
| D09 | Start with Langfuse only; logs/mirroring later | Scope retained; ordinary broker requirement superseded by D11 |
| D10 | Create/inject one ordinary broker during script initialization | Historical, superseded by D11; not an instruction to implement a broker |
| D11 | No observability broker or replacement SDK; use native Langfuse/instrumentation with minimal code | Accepted; pending narrow guarded reconciliation before implementation |
| D12 | Context/tests → runner/tests → CrewAI/tests, then separate logging work | Accepted sequencing |
| D13 | Prefer supported automatic instrumentation before writing per-step hooks | Accepted; actual version/coverage evidence required |
| D14 | Research CrewAI early beside M4.1, with Astra/high effort and a separate report | Delivered as bounded isolated research |
| D15 | Recommend justified upgrades when useful; current pins are not immutable | Accepted research freedom, not dependency adoption |
| D16 | Align preliminary context choices before writing the detailed design | Still active; no detailed context document yet |
| D17 | Start from concrete type placement, construction, propagation and child enrichment | Accepted discussion order |
| D18 | Two ordinary typed dataclasses in one shared definition file outside provider adapters; no Context ABC | Accepted; exact path/options/fields remain open |
| D19 | Runner creates per invocation; factory → constructor → workflow self.context → Flow; derived agent context, same-child helpers, unchanged parent | Accepted route; exact timing/signatures remain open; agent lifetime not selected |
| D20 | Do not open a PR until detailed design starts | Superseded **only in PR timing** by D22; no-implementation boundary remains |
| D21 | Each implementation milestone gets its own design MD and focused PR | Accepted; later implementation follows explicit design approval |
| D22 | Create the shared-records draft PR now; discuss context details before writing 01-context-design.md | Accepted explicitly in iteration 21; no merge or application implementation authorized |
| D23 | Permanent home is designs/stages/02-langfuse/workflow-integration; README holds entry/maintenance rules; requirements is the spec; repository-updates lists later reconciliation | Accepted explicitly in iteration 21; prior saved copies retained as historical snapshots |
| D24 | Once assigned for a workflow invocation, workflow_id, workflow_run_id and trace_id remain fixed throughout that invocation and its agent scopes | Reaffirmed by Sharon in iteration 23; a distinct future child workflow has its own workflow/run identity and can inherit the trace ID |

## P02 — concrete context proposal for discussion, iteration 22

Sharon asks to start the context discussion with a simple explanation of the file, classes and propagation. He has not yet approved the following detailed choices. D18/D19 remain accepted; no new D-number is assigned merely for presenting P02.

- Proposed definition file: `app/src/agent_playbook/context/models.py`, with a minimal package `__init__.py`. Both classes are in models.py; no implementation/interface hierarchy. This is a new shared responsibility to record in the guarded structure before implementation, not an already existing path.
- Proposed representation: `@dataclass(frozen=True, kw_only=True)` for both classes. ExecutionContext has the one required `observability: ObservabilityContext` field. ObservabilityContext has required `workflow_id: str`, `workflow_run_id: str`, and optional `trace_id: str | None = None`, `agent_type: str | None = None`, `agent_run_id: str | None = None`. No mutable metadata bag, extra context classes or SDK clients in this initial data schema. Agent labels are strings here; this does not select the separate agent-role registry/enum contract.
- Proposed identity source: configured workflow ID; a fresh UUID string per workflow invocation; a fresh agent invocation ID when that future invocation is made. Actual generation helper, validation and agent API remain detailed items. Helpers inside an invocation reuse its identity.
- Proposed M4.1 creation point: after configuration and workflow selection, immediately before factory construction. The runner supplies one context through `construct_workflow` and the existing constructors, including `create_workflow` callers where needed. Workflow retains it and explicitly passes it to its own CrewAI Flow subclass constructor. The Flow holds it outside NumberState/other serialized business state; reading `self.context` does not itself export telemetry. Precise signatures and policy for failures before selection remain open.
- Historical P02 trace-binding option, revised by P03: leave trace_id=None for M4.1/disabled mode, then obtain a real scope's ID before constructing the workflow-bound context in M4.2. This was one proposed sequencing choice, not a Langfuse limitation or an approved requirement. Preallocation is also supported; use the P03 recommendation for the next discussion.
- Derivation uses nested `dataclasses.replace`: create a changed ObservabilityContext, then a changed ExecutionContext containing it. The workflow retains the original; helpers can share the child. With the proposed immutable scalar fields there is no nested mutable container to leak. Frozen fields alone would not freeze a future dictionary. No client/resource deep copy or automatic SDK span activation occurs.
- Keep D08 span identity. Do not store a root span ID under a misleading fixed `current_span_id` field; CrewAI changes active operations without replacing the workflow context. Read the active SDK span at reporting time when needed. Exact future correlation accessor and cross-process transfer remain out of scope for this initial explanation.
- Existing settings/configuration stay on their current path; do not duplicate credentials or complete settings in the context. Imports in the proposed context module are standard-library/data-only. No broker, local logging, exporter or agent runtime is implemented by M4.1.

Focused acceptance direction: separate workflow invocation IDs, exact context forwarding into real wrappers/Flows, isolated A/B/A derived scopes and helper access, unchanged workflow outputs/errors, and operation without a tracing backend. Test integration contracts rather than Python's generated dataclass constructor. The formal test plan follows alignment.

This proposal refines Q01/Q04–Q07/Q12/Q18, but does not mark them resolved. No contradiction with the accepted context route or no-broker direction was found; exact placement still requires the known guarded reconciliation.

## P03 — allocate trace identity before context construction, iteration 23

Sharon asks why trace_id must be None, who creates it, and whether we can create it up front and keep it fixed. He prefers creation up front if there is no technical reason against it. The evidence supports that direction. The previous None-first proposal was a milestone convenience, not an SDK restriction; the optional field type in P02 is therefore still review material rather than a settled contract.

Recommended ordering: at a new top-level runner boundary, allocate a valid trace ID locally using the existing SDK's static `Langfuse.create_trace_id()` helper, pass it into the context constructor, and later start the runner scope with `trace_context={"trace_id": context.observability.trace_id}`. Default SDK behavior can instead generate an ID on starting a root operation; both are supported. The backend does not need to be contacted to allocate an ID. The helper uses random generation without a seed, or a deterministic hash with a seed. Do not use Python hash() or workflow_id alone: repeated workflow runs must not accidentally collapse into one trace.

If deliberately continuing an existing trace, reuse its ID and preserve its active parent/span context instead of generating a fresh ID or unconditionally overriding parentage. Do not generate a new trace ID inside every generic context/child constructor. This preserves D01 and allows eventual nested workflows to have separate workflow_run_id values within one trace. No distributed/nested-workflow implementation is added now.

The candidate schema can make trace_id a required string, supplied once before the context is shared. This also permits a reserved ID when export is disabled or M4.1 has no exporting pipeline. A reserved ID does not assert that a span exists, that it is active, or that Langfuse has stored anything. A later enabled integration must use this exact ID. This proposed disabled-mode/schema policy still needs final alignment; D24's fixed-identity invariant is already clear. Offline delivery errors and sampling policy remain separate runner concerns.

Keep SDK imports and ID allocation at the integration/runner boundary, not inside the shared dataclass definition. Generating an ID does not require initializing a client, connecting to a server or implementing an exporter. Scope activation and flush/ingestion remain later integration work.

Evidence: official trace-ID documentation and installed Langfuse 5.2.0 source were checked. A focused real-SDK in-memory check preserved the preallocated ID on one root and one child, verified the child parent, and observed zero Python socket/DNS attempts. This is two-span SDK evidence only; it does not rerun or extend the eight-case CrewAI acceptance claim, nor test a live server/UI.

## Open questions and resolved questions retained

Resolve a question only from explicit agreement or verified evidence, or defer it with its scope/milestone. Do not reopen dataclasses/no-ABC, accepted propagation or no-broker choices without new evidence. The next discussion concerns Q01/Q04–Q07/Q12/Q18; client/export policies follow in runner/CrewAI design. Agent lifetime (Q17) belongs to the separate agent-adapter work.

| ID | Question | Status |
| --- | --- | --- |
| Q01 | What responsibilities and information belong in the initial context? | General context with an observability section selected in iteration 4; further sections and exact fields remain open. |
| Q02 | Is context an ABC interface plus implementation, a Protocol plus implementation, or a concrete typed holder? What contract does the logger expose? | Context representation resolved by D18: ordinary typed dataclasses, no context ABC. Dataclass options are detailed-design items. Broker contract closed by D11; logger contract remains deferred. |
| Q03 | Which methods does application code call on the context's observability access point? | Broker method design closed by D11. Choose the SDK calls/native integration and context-to-attribute mapping needed by each milestone; do not create an equivalent reporting facade. |
| Q04 | At what precise point is context created and injected through runner, factory, workflow ABC and CrewAI flow? How are failures before construction/prepare correlated? | Route accepted by D19: runner creates, factory forwards, constructor receives, workflow retains and supplies Flow. Precise timing, signatures and early-failure correlation remain open. |
| Q05 | Who creates workflow/agent run and trace IDs, how is incoming trace context reused, and what happens when tracing is disabled/unavailable? When is active span identity read? | D24 fixes identity within an invocation. P03 recommends SDK-assisted local preallocation or incoming-trace inheritance before construction; allocation need not contact Langfuse. Final required-field/disabled-mode policy, parent selection and span exposure remain to align. |
| Q06 | How do steps and agents inherit correlation and add agent/step information without leaking it into parents, siblings or other runs? | D19 reconfirms derived agent contexts, same-child helper propagation and unchanged parent on return. Standard dataclass replacement is the proposed small mechanism; explain its shallow semantics. Nested mutability, exact helper API and cross-execution boundaries remain to specify. |
| Q07 | Which configuration is accessible? How are credentials, private values and mutable data excluded from logging/tracing payloads? | Open. |
| Q08 | How do workers receive context across async tasks, threads and processes? Which crossings are in the first version? | Open; scope must be explicit. A workflow invocation is not inherently a new OS process; in-process calls must also isolate scopes. See N10. |
| Q09 | What is the lifetime/owner of logging sinks and tracing clients? Who initializes, flushes and closes them? | Open for configured SDK client ownership, initialization and flush/shutdown. D10 broker construction is superseded; no new service or per-step client creation. Preserve existing connection behavior. |
| Q10 | Which errors are logged locally and represented in Langfuse, through what API, and once at which boundary? How are cause chains preserved safely? | Outcome semantics accepted through R17–R19. Central wrapper placement, detail ownership, exact summary/deduplication APIs remain proposed. Defer further mechanics discussion while defining context shape; resolve necessary behavior before implementation. |
| Q11 | What are the telemetry outage, disabled mode, buffering and shutdown policies? What happens if local writes fail? | Open; must preserve R08 and current workflow error semantics. |
| Q12 | What are the record schema, field types, reserved fields and extension rules? | workflow_run_id and agent_run_id names selected. Types/generation, span exposure, step fields and schema remain open; no final schema approved. |
| Q13 | Final logger, storage, rotation/retention and viewer choices; query-before-load versus bounded in-memory viewing? | Open; viewer may be separately deferred. |
| Q14 | Which framework logs are captured, and how is context injected with the pinned project versions? Is stdout/subprocess capture needed initially? | Open. |
| Q15 | What belongs in the first context PR versus later logging, UI and real-agent work? What are its concrete acceptance scenarios? | Resolved at sequencing level by D12: context/tests, runner tracing/tests, then CrewAI/tests. Local logging is a separate later PR. Exact PR acceptance details remain to refine; PR #36 merge prerequisite is satisfied. |
| Q16 | What minimal context data/API preparation keeps scores, evaluations, sessions, model usage and prompt-version correlation possible later? | Iteration 6 scan and proposed field inventory in specification sections 15–16. No advanced feature, session ID or final optional-field schema selected. |
| Q17 | Does an agent object represent a reusable runtime or one invocation? Where is per-invocation context held? | IMPORTANT DEFERRED coordination action, iteration 8. Resolve with agent-adapter design before its execution API is finalized; not a prerequisite to discussing the observability schema now. Do not choose a lifetime or invocation-holder mechanism here. |
| Q18 | What are the final context/broker/record names and their owning source modules? | D18 accepts both context dataclasses together in one shared definition file outside provider adapters. Exact path/package and SDK import locations remain for detailed design. No broker; LogRecord deferred. |
| Q19 | What local record(s) correspond to a traced operation, and how does automatic SDK/framework tracing receive the same routing policy? | Deferred under D09. Revisit R25 only when local logging is resumed; no mirroring mechanism in the current scope. |
| Q20 | Which runtime/native integration supplies per-model-call and tool lifecycle data, and which layer maps it to Langfuse without duplicate observations or costs? | Open, iteration 15. Compare supported integrations with a small native-event mapping. Define tool-request versus execution evidence, call correlation, delta versus cumulative usage, missing data, cost rollups and SDK/platform compatibility before claiming complete coverage. Coordinate with the separate agent-adapter design. |
| Q21 | Does current Langfuse-only scope need an ObservabilityBroker, or should instrumentation use the SDK with narrow application helpers? | Resolved by D11 in iteration 17: no tracing broker. Use supported Langfuse APIs/integrations with minimal project code. Do not reopen replacement abstractions without a concrete new requirement. |
| Q22 | Which released CrewAI/Langfuse/instrumentor combination covers all existing Flow, start, listen and router paths? | M4.R research delivered, iteration 18. Recommend OpenInference CrewAI instrumentor 1.1.25 with existing CrewAI 1.15.40/Langfuse 5.2.0; eight isolated real-SDK cases passed with 44 exported spans. Actual application integration, disabled/startup behavior and local UI ingestion remain acceptance work. No dependency change approved solely by research. |
| Q23 | Which repository baseline statements need a tracing-specific exception/revision after D11? | Reconcile principles item 5, architecture observability/provider rules and project-structure dependency rules, plus affected stage/Atlas notes before implementation. No blanket change to agent provider isolation; pending reconciliation is listed in repository-updates.md. |
| Q24 | Where do current session documents live, and when is the PR opened? | Resolved by D22/D23: permanent Stage 02 draft PR now; detailed context design remains unwritten until preliminary alignment. Prior saved copies become dated snapshots. |

## Drift and reconciliation markers

- D22 deliberately changes the PR timing; it does not approve an unseen context design. D23 resolves the earlier temporary-versus-permanent placement question.
- The guarded provider-isolation wording conflicts with D11's tracing direction. See [the exact affected documents](repository-updates.md); do not weaken separate agent-execution adapters or claim these baselines already changed.
- N02: the earlier workflow-contract design header still needs a status-only review; verify current text before proposing a guarded correction. Its deferral does not block this new draft.
- Full N01–N22 explanations remain in history. In particular, invocation does not imply a new OS process; per-invocation isolation must hold in one process too.
- dataclasses.replace is shallow copy-with-changes, not deep copy. A changed inner ObservabilityContext and changed outer ExecutionContext must both be distinct; untouched nested mutable objects would still be shared. Detailed mutability policy remains open.
- A context copy does not activate a span. A stored root span ID cannot masquerade as the current step's span. Use the existing SDK for active scope and restoration.
- CrewAI start/listen/router and the other named probe cases have evidence. Other decorators, persistence/resume, retries, loops, cancellation, real agent/tool/generation usage and arbitrary concurrency are not implicitly verified.
- Research completion does not prove application/local-UI acceptance. No source pins have changed. Preserve blocked PyPI update-check and raw flow_inputs/masking caveats in the report.

## Assessment rubric

| Class | Meaning | Treatment |
|---|---|---|
| A | Essential for the selected block to work at all | Required in that block's first working version |
| B | Essential for Agent Playbook correctness or agreed requirements | Required for project acceptance |
| C | Small preparation for a specific credible future need | Include only with explicit present cost and cost-of-deferral rationale |
| D | Useful later, safely deferrable or uncertain | Defer with a named trigger/open question |

For a capability, record whether it applies to tracing, logging or both; outcome and omission consequence; class/status/rationale; implementation/testing/maintenance effort; runtime/operational risk; cost of postponement; and an observable acceptance case. Locality, no-required-logging-service and licensing constraints are pass/fail, not scores to average away. This rubric does not revive a deferred feature.
