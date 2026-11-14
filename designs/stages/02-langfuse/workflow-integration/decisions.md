# Decisions and open questions

Updated: 2026-11-14, iteration 21. These are **accepted discussion decisions**, not a complete approved/locked implementation design. [Requirements](requirements.md) is the specification; [full history](history/context-discussion.md) preserves reasoning and superseded proposals. Read [the entry point](README.md) before using this record.

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

## Open questions and resolved questions retained

Resolve a question only from explicit agreement or verified evidence, or defer it with its scope/milestone. Do not reopen dataclasses/no-ABC, accepted propagation or no-broker choices without new evidence. The next discussion concerns Q01/Q04–Q07/Q12/Q18; client/export policies follow in runner/CrewAI design. Agent lifetime (Q17) belongs to the separate agent-adapter work.

| ID | Question | Status |
| --- | --- | --- |
| Q01 | What responsibilities and information belong in the initial context? | General context with an observability section selected in iteration 4; further sections and exact fields remain open. |
| Q02 | Is context an ABC interface plus implementation, a Protocol plus implementation, or a concrete typed holder? What contract does the logger expose? | Context representation resolved by D18: ordinary typed dataclasses, no context ABC. Dataclass options are detailed-design items. Broker contract closed by D11; logger contract remains deferred. |
| Q03 | Which methods does application code call on the context's observability access point? | Broker method design closed by D11. Choose the SDK calls/native integration and context-to-attribute mapping needed by each milestone; do not create an equivalent reporting facade. |
| Q04 | At what precise point is context created and injected through runner, factory, workflow ABC and CrewAI flow? How are failures before construction/prepare correlated? | Route accepted by D19: runner creates, factory forwards, constructor receives, workflow retains and supplies Flow. Precise timing, signatures and early-failure correlation remain open. |
| Q05 | Who creates workflow/agent run and trace IDs, how is incoming trace context reused, and what happens when tracing is disabled/unavailable? When is active span identity read? | ID meanings/names decided; D08 now accepts span identity and SDK-managed mechanics. Public span exposure, local LogRecord inclusion, identity lifecycle and disabled-mode policy remain open. |
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
