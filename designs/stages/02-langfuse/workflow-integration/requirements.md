# Agent Playbook — execution context and native Langfuse integration

Version: 0.28 · 2026-11-15 · Sharon
Status: **M4.1 implemented, independently reviewed and accepted by Sharon; merged via PR #44 at 942e59344c429454263319e783ea76ad297b7ea6. Combined M4.2 + M4.3 detailed design authorized in iteration 40; implementation awaits revised-contract approval. Logging remains deferred.**

## 1. Current goal and authority

Add real workflow observability to the existing local Langfuse stack using its supported SDK and integrations with as little custom code as practical. Keep ExecutionContext containing one ObservabilityContext. Use the completed CrewAI integration research while detailing the agreed context structure, then implement/test the context, add minimal runner-level tracing, and immediately integrate automatic CrewAI observations once those foundations are verified. Local application logging is a separate later PR; scores/evaluation and other advanced features follow later.

The [decision record](decisions.md) owns decisions and open questions. This active specification supersedes the broker-oriented plan in v0.14. That version is retained in [the historical appendix](history/observability-spec-v0.14.md) for reasoning/provenance; its broker requirements, APIs and unresolved removal question are no longer active. The milestone sequence is accepted; detailed acceptance cases and recommendations below remain design refinements until finalized.

## 2. Accepted decisions and constraints

| Decision | Current effect |
| --- | --- |
| D11: no observability broker | Use supported Langfuse SDK capabilities at deliberate instrumentation points. No neutral facade, broker interface, plugin framework or context forwarding API that recreates the same abstraction. |
| D12: incremental delivery | Context and tests → runner tracing and tests → CrewAI tracing and tests. Keep changes reviewable; logging has a separate later PR. |
| D14: early research | M4.R runs alongside M4.1 preliminary discussion; Astra/high effort investigates released versions, exact integration and coverage in a separate MD. |
| D15: version flexibility | Recommend needed upgrades with concrete benefit, compatibility and regression evidence; do not treat current pins as mandatory research limits. No actual upgrade in this planning turn. |
| D16: agree before formal design | Preliminary discussion led to D28 authorization to draft M4.1; approval still precedes application implementation. |
| D17 / R29: concrete structure and easy evolution | Pass one typed context so ordinary field additions do not require editing every forwarding signature. Preserve unspecified values during child derivation; telemetry fields stay explicitly selected. |
| D18: shared concrete dataclasses | ExecutionContext and ObservabilityContext are ordinary typed dataclasses together in one shared definition file outside provider adapters. No context ABC. Exact path/options/schema are pinned by the M4.1 handoff at 11bba58. |
| D19: creation and propagation | Runner creates per invocation; existing workflow factory forwards into constructor; workflow retains self.context and supplies its Flow; agent invocation gets a derived child, helpers reuse it, parent remains unchanged. |
| D21 / D22 / D23 / D28: design and PR timing | Permanent PR #43 now contains the authorized detailed M4.1 draft plus separate test cases and implementation/review plan. Sharon has sent the M4.1 authorization at 11bba58; each implementation milestone retains its own focused PR. |
| D13: reuse existing instrumentation | Prefer supported CrewAI instrumentation and SDK scopes/events/updates. Add manual instrumentation only for a demonstrated coverage gap or application boundary. |
| D07 / AD-01: context composition and isolation | One ExecutionContext contains one ObservabilityContext. Child metadata additions do not mutate the parent/siblings; returning uses the unchanged parent. |
| D01 / D08: identity | workflow_id identifies a definition; workflow_run_id one invocation; trace_id the actual distributed trace; span identity distinguishes observed operations. The SDK owns tracing mechanics. |
| D24 / D25: identity and SDK reuse | Workflow/run identity stays fixed within an invocation. The SDK creates/inherits trace identity and manages active scope. Do not add manual ID allocation or propagation to the normal path. A stored application trace-ID field is not required by correlation semantics. |
| D26: initial application-only fields | Omit stored trace/span IDs and live SDK/client/observation objects from the initial context. Use native propagate_attributes for selected application fields in the later tracing milestone. A stored trace reference can be added later for a concrete consumer; future log correlation remains required. |
| D27 / R30: application correlation | Add a constructor-created stable correlation_id independently of SDK identity. The implemented contract uses ExecutionContext ownership, preserving it in derived scopes and allowing explicit reuse for related work. |
| D30 / R31: shared observation/log correlation | Every workflow-associated Langfuse observation carries the existing application correlation_id as metadata. Later local records carry it independently of optional SDK IDs. Use native propagation and test coverage, not an extra broker. |
| D29: implementation review process | One coder plus two independent reviewers: design drift and test gaps. At most three total rounds with permanent reports; unresolved findings after round three stop implementation. |
| R16 / R24: agent scope | Distinguish agent invocations and retain their identity in nested helpers. Do not prescribe agent lifecycle, pooling or SDK recreation. |
| R17–R19: outcomes | Failures can be observed at their current scope. A failed child remains visible when its parent recovers successfully. Local diagnostic severity does not automatically define operation failure. |
| External settings and local deployment | Reuse existing settings/client initialization. Credentials stay out of telemetry. Use the existing local Langfuse endpoint; no added collector/server or cloud service is required. |

D04's mandatory provider-neutral tracing access, broker-specific D09/D10 and R15, the ObservabilityBroker implementation name, and AD-04/AD-05 broker contracts are superseded for this phase. Central configuration, cleanup and safe telemetry are retained. This does not change the separate agent-execution adapter design.

Preserve workflow ABC lifecycle guards, input/output validation, error classification, CrewAI routing, lazy import/configuration ordering and strict typing. Runtime handles stay outside recoverable workflow business state. Context data is not automatically safe to serialize into telemetry; project only necessary allowed fields.

The A–D rubric remains: A essential to operate; B essential to this project; C small justified preparation; D later. Current milestones prioritize A/B, add C only for a named use case, and defer D. No generic future provider-replacement framework qualifies merely because a replacement might exist someday.

## 3. Verified starting point

- PR #36 merged on 2026-11-14 as 44d69194f6add6f646795b14f7c3f43c656baeda. Main records local setup/mock acceptance, with real workflow/context integration still deferred.
- At the verified PR #36 baseline, app/pyproject.toml specifies app 0.1.3, Python >=3.13,<3.14, crewai==1.15.40 and langfuse==5.2.0. No CrewAI auto-instrumentor is declared there.
- Existing connection.py owns typed-settings-to-client creation and a separate authentication check. Preserve its distinction between checking credentials and creating an exporting SDK client.
- observations.py contains LangfuseSession/Observation for explicit mock root/child spans, update/end, flush/shutdown and bounded delivery readback. It does not install framework instrumentation or establish automatic active scopes. Existing mock UI children are not evidence of real Flow/step tracing.
- WF-02 is a real deterministic CrewAI Flow with initialize/add/multiply/finish methods using @start/@listen. Those steps provide a useful initial integration exercise without real agents/models.
- Existing readback can say unconfirmed despite visible ingestion. A printed trace ID/URL or completed flush alone is not an ingestion assertion. This limitation is preserved, not silently fixed by the new plan.

These repository findings are read-only. Prior application tests remain attached to their tested revisions; no application suite or live Langfuse acceptance was run for this document update. The separate M4.R research ran an isolated real-SDK/Flow probe, recorded below. Do not inspect or depend on app/examples/ for implementation/tests.

## 4. Milestones and proposed acceptance evidence

These are the integration milestones under Stage 02's previously deferred M4. Existing setup M1–M3 remain completed. M4.R research has already established the tested feasibility before application Langfuse integration. Its SDK/propagation findings inform the context details. D21 confirms one focused PR and design MD per implementation milestone; D22 authorized the opening documentation PR; D28 now authorizes the detailed M4.1 package for review, without application implementation.

| Milestone | Starting point | Goal / evidence | Status |
| --- | --- | --- | --- |
| M4.R — CrewAI/Langfuse research | Merged PR #36 pins and maintained Flow definitions; automatic coverage not established. | Released compatible integration and reproducible coverage evidence before application tracing work. | Delivered: eight isolated cases/44 spans; application/local-UI acceptance not yet established. |
| M4.1 — context | Existing runner/factory/Workflow ABC, no general context; D18/D19 structure agreed. | Typed context, constructor propagation and parent/child isolation; focused tests without backend export. | [Design](m1-context/design.md), [test cases](m1-context/test-cases.md) and [implementation plan](m1-context/implementation-plan.md) approved at 11bba58; candidate 16c1580 passed both reviews and final review, accepted by Sharon; merged via PR #44 at 942e59344c429454263319e783ea76ad297b7ea6. |
| M4.2 + M4.3 — combined tracing | Accepted M4.1 context and tested M4.R integration. | Native runner scope and automatic Flow/start/listen/router observations, exact correlation, lifecycle/disabled/failure behavior and local UI acceptance. | One implementation milestone/PR; native SDK and instrumentor, no custom step-tracing layer. |
| Later — logs and advanced features | Working correlated tracing. | Local application logs in a separate PR; scores/evaluations incrementally. | Deferred; local/no-service/Apache and replacement requirements retained. |

### M4.R — CrewAI-to-Langfuse research alongside milestone 1

Deliverable: [agent-playbook-crewai-langfuse-research.md](research/crewai-langfuse.md), containing both the research brief and findings. Sharon explicitly selected Astra with high reasoning effort. Research authorization alone never implied code/pin changes. Detailed M4.1 drafting is now separately authorized by D28.

Determine the least custom code needed to observe every existing workflow's actual @start, @listen and @router operations in the existing local Langfuse stack. Verify whether branch decisions/results and selected branch methods are visible and whether skipped branches are correctly absent. Target one workflow trace with nested observations, not independent traces per method. Do not treat every arbitrary Python utility or nonexistent model call as a tracing requirement.

Required evidence: exact released package versions and source/wheel coverage; Python/framework/SDK compatibility; Apache-2.0 license fit for newly selected components; justified current-pin versus upgrade recommendation; initialization/export/active-scope recipe; correlation field propagation; failures, repeated runs, async behavior and duplicate prevention; local-only destination and payload handling. Prefer a small real-SDK/real-Flow in-memory or loopback probe where feasible, clearly distinguished from actual local Langfuse ingestion. Record unverified cases and commands to verify them later.

Current versions are the starting point, not a prohibition on upgrades. Recommend changing versions if the gain warrants it and document regression/migration cost. Recommend against an option if it adds too much complexity or does not deliver the desired coverage. No custom broker, agent harness, new collector or unbounded provisioning effort. Real Claude/Codex implementation remains outside scope.

Exit: a concrete adopt/current-pins, adopt/upgrade, defer, or unsuitable recommendation with sources, exact version evidence, tested versus untested behavior and a minimal next-step plan. Findings inform context/runner integration; they do not silently approve a class design or dependency change.

**Research result:** recommend released openinference-instrumentation-crewai==1.1.25 in default wrapper mode, retaining CrewAI 1.15.40 and Langfuse 5.2.0. Python 3.13.5, normal dependency checking and all existing locked package versions passed the bounded probe. Eight cases exported 44 spans through the real Langfuse SDK's default processor/filter: maintained WF-01/02/03, both WF-03 branches, repeat/failure, direct async kickoff and an independent AND/OR fixture. Runner → Flow → executed method parentage, actual IDs and inherited workflow/run metadata were asserted. This is an isolated research result, not application assembly or live local UI acceptance; the tested candidate is not claimed to be the latest release.

The report and [probe evidence](research/probe/README.md) contain the exact recipe, pins, hashes and limits. CrewAI's Flow-start console/version checker attempted eight blocked PyPI DNS lookups, distinct from telemetry export; the fixture bypassed the configured application runner/display path. Verify normal startup before claiming zero external attempts or a regression. Other remaining checks include disabled/repeated initialization, recovered-child outcome, masking including raw flow_inputs, actual application lifecycle and local Langfuse ingestion. M4.R is delivered as research; M4.2/M4.3 own integration acceptance.


### M4.1 — Execution context

**M4.1 implemented and accepted.** The approved design/test/plan at 11bba581 and G01–G08 were implemented in PR #44; candidate 16c1580 passed two independent reviews and final review. See [permanent status](m1-context/reviews/status.md). Its data-only contract is unchanged by documentation reconciliation.

Implement the agreed ordinary typed ExecutionContext and nested ObservabilityContext together in one shared file. Runner creates one context per invocation; the existing factory forwards it into the workflow constructor. Workflow retains self.context and supplies its CrewAI Flow. M4.1 includes this actual wiring and parent/sibling isolation, not only class definitions. No Langfuse export yet.

D27 adds application correlation_id; the draft places it on ExecutionContext, generates it only when absent and preserves it in derived children. workflow_run_id still distinguishes workflow invocations. Explicitly sharing a correlation value is a data capability, not a child-workflow launcher, incoming CLI flag or trace-parentage mechanism.

Follow D25/D26: omit stored trace/span IDs, placeholder trace_id=None and live span/client objects. A plain context does not activate an OpenTelemetry scope. Keep application context separate from CrewAI's own execution_context field and serialized business state. No generic mutable metadata bag, configuration copy, outputs, usage, costs or scores in the initial schema.

Exit: Sharon approves the concrete contract and listed guarded amendments; implementation satisfies CTX-01–17, both independent reviews and relevant project gates while preserving current workflow behavior. D29 caps implementation/review at three total rounds and preserves all reports. Drafting the contract is not its implementation or test acceptance.

### Combined milestone: runner acceptance (formerly M4.2)

Use the real Langfuse SDK around the selected workflow execution boundary, with the configured local client and M4.1 context. Record correlation_id from ExecutionContext plus workflow_id and workflow_run_id as consistent safe metadata; obtain the actual trace ID from the SDK-created/joined trace. Retain access to that ID for correlation. Final native result/presentation changes require an explicit contract, not an incidental CLI-output rewrite.

Define which lifecycle phases are inside the root scope and how failures before scope creation are reported. Use SDK-managed active scope so future framework children can attach correctly. Reuse client setup rather than evolving the mock span wrapper into a general broker. Specify initialization, disabled mode, failure/outage behavior and flush/shutdown ownership for short-lived CLI and Python callers. Keep telemetry failure separate from the actual workflow result; the final policy remains to decide.

Proposed tests: exact correlation/workflow/run metadata and actual trace identity on an exported SDK root and all emitted children/events, starting with the earliest observation; repeated invocations do not cross-contaminate; success and unrecovered workflow failure retain their existing application outcomes; tracing-disabled execution does not initialize an exporter or contact services; SDK active scope is restored and cleanup occurs on normal/error exits. Use actual SDK in-memory/loopback export where suitable rather than testing only a fake broker. Add one explicitly configured local integration/acceptance check that confirms root visibility and expected fields. Ordinary unit tests do not require Docker.

Exit: real runner-created workflow traces visible in local Langfuse with correct correlation and outcome, deterministic integration tests pass, lifecycle/outage policy is reviewed, and no duplicate root is created by the mock helper.

#### M4.2 preliminary design baseline — iteration 29

R31 is a must-have for tracing and later logging. Use the exact context.correlation_id value as metadata key correlation_id. Native propagate_attributes sets the active root and future observations in scope; enter it immediately at root creation before child work. Preserve it through all workflow-associated span/agent/tool/generation/event observations, including errors and automatic framework observations when enabled. Keep as_baggage=False for this in-process/local design. No new trace-ID allocation, SDK object in context, manual per-step metadata boilerplate or replacement broker.

Observations are not every possible Langfuse entity: scores, datasets and other future APIs may need their own explicit metadata/linking. Preserve the requested correlation capability when those are introduced; do not claim they all inherit observation scope automatically. Background/thread/process transport likewise needs its own reviewed mechanism. This limitation does not weaken correlation on all observations in the supported workflow path.

Required evidence in M4.2/M4.3: exact matching correlation value on root and every emitted observation, native event coverage, success/error and independent-run isolation, cleanup after scope exit, automatic CrewAI coverage, plus local UI/API visibility and filtering. Check behavior against the actual pinned SDK/server; do not infer ingestion from in-memory export. Missing correlation on a supported emitted observation is an acceptance failure. A propagation scope does not retroactively repair earlier completed observations.

Future context-associated logs carry correlation_id even with tracing disabled or before/after the active SDK span. trace_id/span_id may be captured from the SDK when available, but are not prerequisites for recording logs. Looking up a trace's correlation_id can retrieve all related logs; if one correlation group spans several traces, this may be broader than that single trace. Optional SDK IDs or narrower application run IDs provide finer filtering. Do not promise a one-to-one mapping or add automatic backfilling.

Next decisions: root lifetime across constructor/input/prepare/execute/validation/serialization; client initialization/reuse and CLI flush versus shutdown; disabled/outage/error behavior; selected metadata and acceptance tests. Discuss these before the detailed 02-runner-design.md. Plan against pinned M4.1 and reconcile its actual implementation before tracing code. Logging and agent lifecycle remain deferred.

### Combined milestone: CrewAI acceptance (formerly M4.3)

Enable a compatible existing in-process CrewAI instrumentor once at the appropriate initialization boundary. Run actual maintained workflows under the runner's active Langfuse scope. Prefer automatic Flow/step observations over adding tracing calls to every @start/@listen method. Preserve framework routing and existing outputs.

The official Langfuse guide uses openinference-instrumentation-crewai. M4.R verified the released 1.1.25 wrappers for Flow.kickoff, Flow.kickoff_async and Flow._execute_method and executed the maintained Flow cases with the current CrewAI/Langfuse versions. Adopt the recommendation only through the reviewed implementation and focused acceptance checks; research alone does not change dependency declarations. Do not disable dependency checks as a compatibility strategy. The private _execute_method hook makes upgrade regression coverage important.

Proposed tests: all existing WF-01/02/03 runs yield runner → Flow → relevant start/listen/router observations within the intended trace; correlation_id and workflow/run fields reach every emitted descendant, including automatic observations; both WF-03 branches report the router and only the selected path; failure visibility and a recovered-child scenario preserve actual parent outcome; no duplicate kickoff/method spans; multiple runs do not leak active scope/metadata; disabled mode remains offline. Validate local destination/export and use independent maintained fixtures. Custom SDK decorators/events are fallback additions for documented gaps, not the default implementation.

Agent/tool/generation/event types are available capabilities to use when such operations exist. Current deterministic flows must not emit fictional LLM generations or fabricated token costs. Adding real Claude/Codex agents, their execution controls or an agent pool is outside this milestone. Later native usage capture should attach to actual model calls and avoid duplicate costs.

Exit: actual CrewAI Flow/step hierarchy is inspectable below the runner with correct context, tested version pins, known coverage limits and a small local UI acceptance exercise. No claim of universal automatic instrumentation.

## 5. Native capabilities and scope

| Capability | Use in this plan |
| --- | --- |
| span / suitable workflow observation | Runner and meaningful non-model operations. |
| agent | Actual agent invocation when agent integration arrives. |
| generation | Actual model request, with reported model/usage where available. |
| tool | Actual tool execution, including duration and outcome. |
| event | Useful point-in-time fact within the current trace; not a local log replacement. |
| scores / evaluations | Later addition using retained trace/observation identity; no evaluator machinery now. |

Supported native SDK context managers, decorators, explicit observation lifecycle and integrations can be combined. No owned method-per-type wrapper is required. Automatic instrumentation owns only the calls it actually covers; use native SDK reporting for meaningful missing application observations without duplicating existing instrumentation.

## 6. Context contract — pinned M4.1 handoff

The [M4.1 detailed design](m1-context/design.md) is the single current proposal for exact fields, types/defaults, package location, dataclass flags, constructor signatures, derivation and Flow storage. D18/D19's composition/route, D24's stable identity, D25/D26's SDK-managed tracing and D27's application correlation are accepted discussion choices. D28 originally authorized drafting; iteration 29 records Sharon forwarding the subsequent explicit implementation authorization at 11bba58.

Implemented source: app/src/agent_playbook/context/models.py. ExecutionContext holds correlation_id and observability. ObservabilityContext holds workflow_id, workflow_run_id and optional agent_type/agent_run_id. Frozen keyword-only fields and scalar/frozen nested values avoid parent mutation. No Context ABC, broker, live SDK object, mutable extension dict or empty future context sections.

The for_agent helper uses dataclasses.replace on both the inner and outer objects. replace creates a new instance through its constructor and preserves unspecified ordinary fields/references; it is not a deep copy. The workflow retains its original reference and helpers within an agent can receive the child's reference. No cleanup/copy-back on return and no new client or runtime are required. This does not remove SDK scope cleanup in later milestones.

R29 remains: pass one context through intermediary signatures; field definitions and actual producers/consumers evolve without manually rebuilding all inherited fields. New required semantics may still require callers to provide a value. Review any future mutable fields explicitly. Telemetry projection stays selective, not automatic asdict export.

The separate [test-cases contract](m1-context/test-cases.md) covers identity, derivation, actual maintained Flow access, state separation, existing behavior, typing/offline checks and installed packaging. The [orchestration plan](m1-context/implementation-plan.md) governs the delegated M4.1 implementation, not an application agent feature.

## 7. Deferred requirements retained

- Local application logging is a separate later PR. Python in-process recording, local storage and no required collector/database server remain mandatory. Logs work without Langfuse or a running viewer.
- New logging/viewer components need Apache 2.0 licensing. JSONL is welcome; SQLite and an optional local viewer remain candidates. No backend/viewer selected.
- The future logger and viewer remain independently replaceable. Removing the tracing broker does not select a logging facade implementation or remove that boundary requirement.
- R25 remains deferred: a trace report should also produce corresponding local records, while local log-only calls should not automatically trace. Decide coverage of native instrumentation and avoid duplicates when logging returns; do not build dual-output plumbing now.
- Scores/evaluations, sessions, prompt/version links, advanced analytics/cost reporting, child workflows and cross-process propagation remain later. Preserve meaningful operation identity, not speculative frameworks.
- Another session owns agent adapters, lifecycle, tool permissions and event/control design. This work supplies correlation without imposing a new execution wrapper or runtime lifecycle.

## 8. Repository reconciliation and scope

The exact data-only M4.1 amendments are G01–G08 in [design section 9](m1-context/design.md#9-guarded-logical-amendments-to-approve-with-this-design). They cover context placement, constructor/Flow routing, dated amendments to the existing workflow contract, M4 submilestones and registration of the approved baseline. These are authorized by the forwarded M4.1 instruction and are to be applied by its implementing Codex; this planning update does not apply them or claim them completed.

The no-broker/native-SDK direction remains accepted. Its tracing-specific exception to existing provider-isolation wording must be reconciled before M4.2, not before data-only M4.1. Do not weaken agent-execution adapter isolation. [repository-updates.md](repository-updates.md) separates those gates and their concrete affected files.

This update adds the detailed design/test/implementation drafts, accepted correlation/process decisions and truthful navigation/progress/Atlas status. No guarded baseline, application source, dependency or supported product behavior is changed. Research evidence and historical decisions remain attached to their original revisions.

## 9. Immediate actions

1. Preserve completed M4.1 and CTX evidence.
2. Review the version-2 combined design/test/plan, retain accepted PAYLOAD-01 and approve exact contract/guarded amendments before implementation.
3. Prepare the filled Codex handoff under the standing rules, implement one combined PR, and verify automatic observations through the actual runner and local UI. Documentation PR #47 merges last.

Q25 is resolved at the application-ID level by D27; ownership and constructor details are proposed concretely in M4.1. Q01/Q02/Q04/Q06/Q12/Q15/Q18 have reviewable M4.1 answers in that draft; their later-feature parts stay deferred. Q21 remains closed: no broker. Agent lifecycle and local logger/viewer questions remain outside M4.1. Follow the [README maintenance rules](README.md#rules-that-prevent-design-drift).

## 10. Evidence and limits

- [M4.R report](research/crewai-langfuse.md) and [reproducibility ZIP](research/probe/README.md): released-wheel and isolated runtime evidence for 1.1.25 with current pins; eight cases/44 spans, normal dependency checks. No application runner, live server/UI or full release-gate claim.
- [PR #36](https://github.com/SharonLanger/agent-playbook/pull/36), dependency pins at the research baseline, maintained client/mock adapter, WF-02 Flow, progress and applicable design documents inspected on 2026-11-14.
- [Langfuse CrewAI integration](https://langfuse.com/integrations/frameworks/crewai) documents OpenInference setup and interoperability with native SDK scopes.
- [OpenInference CrewAI documentation](https://arize-ai.github.io/openinference/python/instrumentation/openinference-instrumentation-crewai/) distinguishes the normal wrapper path from its optional event-listener mode.
- [Upstream instrumentor source](https://github.com/Arize-ai/openinference/blob/main/python/instrumentation/openinference-instrumentation-crewai/src/openinference/instrumentation/crewai/__init__.py), blob 2242c19afef574c0a0e7ecac1db36611739fa08b, includes Flow startup/method wrappers. Latest source is not proof of a released compatible pin or runtime success.
- [CrewAI built-in tracing](https://docs.crewai.com/en/observability/tracing) is a separate AMP-oriented facility; do not equate enabling it with the local Langfuse integration or enable external export under this local-only plan.


## 11. Stable requirement register

These identifiers are retained from the discussion for design/test traceability. Current milestones and explicit deferrals above govern delivery; R15 is superseded, not an active broker requirement. Exact M4.1 details are pinned by the authorized handoff at 11bba58; later-feature questions remain open as indicated.

- **R01 — Per invocation:** create a fresh run context when starting each workflow invocation, regardless of entry through CLI, a Python method or a future API. Do not create the per-run context at module import.
- **R02 — Workflow access:** the workflow holds the context. D19 accepts runner → workflow factory → workflow constructor → self.context → CrewAI Flow propagation. The existing workflow ABC is the integration point; exact signature and construction timing are proposed in the M4.1 design for approval.
- **R03 — Propagation:** steps and eventual agents must have access to the appropriate execution context without repeatedly reconstructing workflow/run identity at each log call.
- **R04 — Agent enrichment:** an agent needs the inherited workflow/run correlation plus its own information, such as agent type. The M4.1 draft proposes a small for_agent helper using inner/outer dataclass replacement; unrelated or concurrent runs must not contaminate one another. Sharon explicitly requires agent fields to apply throughout the agent's nested method calls, then stop applying when control returns to the workflow. Agent B must receive its own agent fields without leftovers from agent A.
- **R05 — Configuration:** supply relevant configuration and observability information through the context. Exactly which configuration is exposed remains open. Never include credentials or complete private configuration in telemetry.
- **R06 — No required service:** new Python application logging runs within Agent Playbook. Recording logs must not require a separately started collector, database server or logging backend.
- **R07 — Local only:** new logging storage and processing stay local. No cloud logging service or remote logging dependency.
- **R08 — Independence:** logs remain recordable when a viewer is closed or was never started, and without a live tracing backend. Saved records can be inspected later.
- **R09 — Licensing:** newly selected logging and viewer components must offer Apache 2.0 licensing. Langfuse is an explicitly accepted exception; do not reopen its different license as a blocker.
- **R10 — Existing open source:** prefer an existing library/tool over writing a logging engine, storage engine or viewer ourselves. Keep application logging extremely simple.
- **R11 — Storage flexibility:** JSONL is preferred/welcome, not mandatory. An existing simple embedded SQLite solution is acceptable. Neither storage choice is final.
- **R12 — Viewer:** a small UI is desired. A separately launched local viewer, including CLI or Docker invocation, is acceptable; fewer moving parts are preferred.
- **R13 — Framework logs:** support our Python code and, where practical, library/framework logs such as CrewAI. Capturing printed or subprocess output is a separate integration question.
- **R14 — Operation failures in both:** Sharon wants failed-operation information available through local logging and Langfuse. This does not apply automatically to every error-level diagnostic log; see R18. The call pattern, export policy, sanitization and duplicate-report handling need discussion.
- **R15 — Unified tracing/logging broker superseded by D11; historical requirement from 2026-11-14:** Sharon wants one application-owned broker/access boundary between runner/workflow/agent code and logging/observability, including Langfuse. Logging implementation remains independently replaceable. R25 now specifies trace-plus-local-log versus log-only routing. One class versus several interfaces, distinct record representations, exact method names and binding remain open.
- **R16 — Agent invocation identity, confirmed iteration 4:** three reviewer invocations must be distinguishable. Helpers within one invocation retain its identity. Real agent execution remains later; support for this identity must not be designed out of the context/record contract. Whether the ID has an independent value or reuses a suitable observation identity remains open; it must remain useful for local logging when tracing is disabled.
- **R17 — Error reporting at the current scope, confirmed iteration 4:** an agent, workflow or relevant nested operation can report its own failure without delegating reporting to the workflow first. In the example, agent A finishes successfully; agent B records its failure; the workflow then reports that it failed because of B. Preserve the operation hierarchy and available exception details so the user can follow the cause. Exact automatic/manual API and duplicate policy remain open.
- **R18 — Diagnostic logging does not imply trace failure, confirmed iteration 5:** a small/handled problem may be recorded only in local application logs, even at error severity. That logging call must not automatically create an error observation, change the agent/workflow outcome or duplicate the message in Langfuse. Operation failure reporting is a separate semantic action. This distinction survives removal of the tracing broker; logging remains deferred.
- **R19 — Independent child and workflow outcomes, confirmed iteration 6:** an observed block/agent can fail while its calling workflow successfully recovers through a fallback. Keep that failed child visible and record the workflow's own final outcome accurately. This accepts the behavior in AD-02, not a general automatic retry/recovery engine or every proposed exception-handling mechanism.
- **R20 — Future Langfuse compatibility, iteration 6:** check that the context/Langfuse integration can later support useful Langfuse capabilities, particularly scores/evaluation. Preserve suitable identity, hierarchy and extension boundaries; do not implement all future features now. Exact field/API choices remain review material.
- **R21 — Reusable agent versus invocation, iteration 7:** compare constructing an agent for each invocation with reusing an agent/runtime. Every invocation, including A → B → A, must have fresh agent invocation context/identity regardless of whether a Python object, provider client or CLI runtime is reused. Support the design possibilities without silently choosing an agent lifecycle or implementing agents now.
- **R22 — Future-feature priorities, iteration 7:** scores and evaluations are welcome; token usage is an explicitly desired capability. Sessions and dashboard/view work are deferred. Delivery timing for token usage/evaluation is not selected, and deferring dashboards does not remove structured correlation/filter fields required by existing logging requirements.
- **R23 — General execution context, iteration 7:** retain one general context and one shared observability section for Langfuse now and local logging later. Future agent/event-handler needs may include non-telemetry information. Do not assume the whole context should be logged or create unused sections now. Execution identity may be useful outside observability and must have one source of truth.
- **R24 — Agent-lifecycle neutrality, clarified iteration 8:** deriving a reporting context must not recreate an LLM SDK client or require a new agent runtime/process. Keep compatibility with per-workflow runtimes, reuse, later pooling and different per-invocation prompts/tools. The agent-adapter design session owns those execution choices; this session must not prescribe an AgentExecution wrapper, constructor-injection pattern, pool, concurrency or conversation-reset contract. Per-invocation correlation and isolation remain required independently of runtime lifetime.
- **R25 — Asymmetric routing, stated iteration 10; deferred by D09 in iteration 11:** when logging is resumed, a trace operation/report also produces corresponding local logging; a log-only operation produces local logs without a Langfuse observation. Application code should not have to call both destinations manually for the trace path. Exact lifecycle-to-record mapping, payload detail, automatic instrumentation coverage and API spelling remain open. No assumption of identical log/span schemas or successful atomic delivery to both destinations is introduced. None of this is required in the current Langfuse-only scope.
- **R26 — In-trace point reporting, iteration 15:** support recording meaningful happenings inside an agent execution, such as a tool-request notification, without requiring every report to be a user-managed timed block. Distinguish a Langfuse event from deferred local application logs and the separately designed agent event system. Use supported SDK APIs under D11; exact integration coverage remains open.
- **R27 — Fine-grained model usage/cost, iteration 15:** later inspection must be able to show individual model calls/turns and relevant tool activity, rather than only one final aggregate agent cost. Preserve per-call observations, model identity, source usage and invocation linkage. Availability/granularity of runtime data must be verified; do not fabricate per-call costs from a run total. Native agent adapters and feature delivery remain separately scoped.
- **R28 — Prioritize automatic existing-workflow coverage, iteration 18:** all maintained workflows' real @start/@listen/@router executions and relevant branch results should be inspectable in local Langfuse as soon as the runner/context foundation supports them. Validate WF-01, WF-02 and both WF-03 paths. Do not interpret this as a new independent trace per method or tracing every utility function; one workflow trace contains its executed observations. Absent branches are not completed operations. Desired coverage is not a claim it already works.
- **R29 — Easy field evolution, iteration 19:** adding a context field should normally require changing its typed definition and the code that supplies/uses it, without changing unrelated runner/workflow/helper forwarding signatures or dropping the field during child derivation. This is a maintainability requirement, not permission for untyped arbitrary state, automatic full-context telemetry export or a guarantee that new required semantics need no caller changes.

- **R30 — Stable application correlation, accepted iteration 27:** add correlation_id when the initial ExecutionContext is constructed and preserve it unchanged in descendants. Keep it independent of SDK trace/span IDs and distinct from per-workflow invocation identity. The detailed draft recommends top-level ExecutionContext ownership, UUID4 generation only when omitted and explicit reuse for related work. Do not regenerate when deriving a child, duplicate it inside observability or add a new CLI/process/tracing mechanism merely to carry it.

- **R31 — Correlation on all workflow observations and future logs, accepted iteration 29:** every workflow-associated Langfuse observation we emit, including root/child spans, native events and automatic CrewAI observations, must carry metadata.correlation_id equal to ExecutionContext.correlation_id. Propagate from the earliest runner scope with native SDK support; do not regenerate or backfill it later. Future context-associated local logs must carry the same key without requiring trace_id. Optional SDK IDs remain useful for precise trace/span filtering because a correlation group can include multiple traces. Coverage of future scores/other entity APIs and process boundaries must be designed when introduced, not assumed automatic. No tracing or logger implementation is added to M4.1.

## 12. Inspection and evolution requirements

Later local logs must support inspection by workflow_id across runs, narrowing to workflow_run_id/trace_id, and combining workflow and agent-type filters. Preserve structured timestamps, severity, messages and safe error details. Indexing is not required from the logging library itself; query-then-load UI remains an unselected possibility. No logger/store/viewer is selected now.

The accepted A–D classification and assessment rubric is retained in [decisions.md](decisions.md#assessment-rubric). Milestone design proposals must record applicability (tracing/logging/both), observable outcome, omission consequence, effort/maintenance, operational risk, cost of deferral and an acceptance example.

## Iteration 35 closeout clarification

M4.1 draft-era proposals above are implemented under the approved three-file contract; G01–G08 are applied. Final review passed with an independent 43-test rerun; the implementation reports the full 380-test/release gates. M4.2 and M4.3 proposals remain unapproved. No application behavior is changed in this reconciliation.

## Iteration 40 — accepted consolidation and reusable handover rules

On 2026-11-15 Sharon accepted combining M4.2 and M4.3 into one implementation milestone and authorized the simplified detailed design. Use native Langfuse plus the released OpenInference CrewAI instrumentor for existing workflows; no broker, manual per-step instrumentation, custom SDK lifecycle or new agent runtime. Earlier separate-milestone sequencing is historical. This accepts scope and drafting, not an unseen detailed contract or application implementation.

The reusable [Codex handover rules](../../../governance/codex-handover-rules.md) now govern every handoff: pinned design/test/plan, one coder, two independent reviewers, three rounds maximum, permanent evidence and exact outgoing/return copyable messages. PR #47 remains MERGE LAST. Detailed payload handling and tracing-specific guarded amendments must be explicit at contract review; do not silently turn earlier unapproved policies into requirements.
