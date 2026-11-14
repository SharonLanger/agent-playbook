# M4.2 — native runner observation design

Status: **DRAFT FOR SHARON'S REVIEW — not approved, locked, implemented or accepted.** Version 1, 2026-11-14, discussion iteration 32.

**Current foundation, iteration 35:** M4.1 is accepted and merged in PR #44 at `942e59344c429454263319e783ea76ad297b7ea6`; PR #43 is merged. This branch incorporates main closeout `6a7b16f6e1947bf911de916b5ec2c1b76be58251`. The earlier pinned-source/handoff descriptions below retain drafting provenance; integration conflicts and duplicate D30 are resolved. M4.2 choices remain unapproved, and the current approved M4.1 contract is unchanged.

[Runner discussion](history/runner-design-discussion.md) · [Proposed test cases](02-runner-test-cases.md) · [Implementation/review plan](02-runner-implementation-plan.md) · [Shared requirements](requirements.md) · [Decisions](decisions.md)

## 1. Purpose, authority and pinned inputs

Add one native, active Langfuse observation around a workflow invocation after its execution context exists. Preserve the current application outcome and make its correlation and duration inspectable in the existing local Langfuse deployment. This small foundation must support the researched automatic CrewAI instrumentation next.

This draft is authorized by the parallel-design instruction recorded in iteration 32. Root completed the [M4.1 final design-session review](history/context-final-review.md): runtime/design PASS, with documentation integration still required. That review is not Sharon's acceptance or merge authorization. This draft's narrow source check supports placement; root owns publication of this package.

| Input | Pinned reference and significance |
|---|---|
| Main source inspected for this draft | `d12b5fc2867d3646b6fab2eb71f1447ff177d8c1`; maintained runner, assembly, results, CLI, configuration and Langfuse adapter fetched read-only |
| M4.1 authorized package | `11bba581291c1b166973848ea8db6a9e2a142413`; [design](01-context-design.md), [cases](01-context-test-cases.md), [plan](01-context-implementation-plan.md). Authorization, review, user acceptance and merge remain separate |
| M4.1 reviewed foundation | PR #44, `feat/m4-1-context`; reviewed candidate `16c1580e96bd36945fa96b6ecfa8f9a563d53913`, published head `9392b39b1e556c1a36c7dfe1fa8574d65f8ce0e2`, release source `2e5d76dde2ec76b5a7ecae8ea0094286838229a9`. Root verified the published delta is report/status-only and independently passed 43 targeted tests; full gate/release evidence was reviewed, not independently repeated |
| M4.1 final-review record | Published on the isolated discussion branch at `68166c94497bf388eb05250c38cccc43f732a0f4`; runtime/design PASS. Duplicate D30 and current target conflicts remain documentation integration work; PR #44 is unmerged, rounds 2/3 unchanged |
| Shared planning record | PR #43, `9aaf31e4b0e6345ed7162da765f37dbe94167f4b`, draft/unmerged at delegation |
| Isolated runner discussion | Branch `docs/m4-2-runner-discussion`, published starting point `9e73a7b2e965f202b742375f0022e5004eb5d878`; read the complete discussion including iterations 31–32 before approval |
| Runtime versions | Python 3.13; CrewAI 1.15.40; Langfuse 5.2.0; existing lock remains the starting point, not a claim these are latest |
| Research | [CrewAI report](research/crewai-langfuse.md) and [preserved probe](research/probe/README.md): eight isolated cases/44 spans; separate iteration-29 SDK metadata check: ten correlated observations plus one clean outside scope |

The local documentation snapshot is not a full application checkout and its Git history is not the remote history. No application code, tests, dependencies, M4.1 file, original research file or guarded document is changed by this draft. Shared records/navigation/Atlas are deliberately left to root so parallel work cannot overwrite M4.1. This isolation is temporary documentation coordination, not permission to omit reconciliation before implementation readiness.

Governing boundaries are the root/design instructions, [design contract](../../../governance/design-contract.md), [guard register](../../../governance/guarded-files.md), charter/principles/architecture/project structure, Stage 02 architecture/milestones and the [Workflow contract](../../../refactors/workflow-contract/design.md). The observability exploration was consulted for ownership and privacy; its neutral event/facade proposals are not adopted. D11–D13, D18–D19, D24–D27 and D30/R31 control this proposal. Section 10 lists the narrow guarded reconciliation still needed.

## 2. Fixed scope and decisions Sharon still needs to make

Already agreed: native Langfuse; no broker or provider-neutral tracing facade; the M4.1 data-only context and its route; exact application correlation on every workflow-associated observation; existing local configuration/deployment; M4.2 runner scope followed by M4.3 automatic CrewAI observations. Nothing below reopens those choices.

The following are **recommendations needing Sharon's decision**, not accepted policies inferred from the permission to draft. The rest of this document describes the recommended branch so it is concrete enough to review. Approval must identify the selected choices and the final design revision.

| ID | Smallest recommended choice | Benefit and cost / alternative |
|---|---|---|
| RUN-D01 | One workflow observation begins after M4.1 context creation and covers construction through serialization; delivery happens afterward | Captures rejected input and finalization failures without phase spans. Pre-context failures retain current diagnostics. Verify exact placement against M4.1 code before approval |
| RUN-D02 | Reuse one lazily initialized client for one tracing configuration per process. Flush after each enabled invocation, outside the observation; rely on native SDK exit cleanup for final shutdown | Keeps `run_workflow` usable repeatedly without a new lifetime API or shutting down shared resources. Each Python call pays flush latency. Alternative: an explicit application owner flushes batches; that adds a public lifetime contract and is deferred unless needed |
| RUN-D03 | Telemetry initialization/update/delivery failures preserve the workflow result or original workflow exception; report safe diagnostics. Invalid application configuration still fails normally | Local outages do not turn successful computations into failures. Delivery can be lost; no durable queue or proof of ingestion. Mandatory-delivery/fail-closed mode would be a different policy, not a hidden option |
| RUN-D04 | Metadata and safe outcome only: no raw input, output, config, exception messages or tracebacks in the workflow observation | Small privacy surface and minimal code. Less diagnostic payload detail in the UI. Any later payload allowlist requires a specific use case and tests |
| RUN-D05 | Do not silently truncate identities the SDK cannot propagate. Skip tracing for that invocation, with a fixed diagnostic, while retaining application behavior | Preserves exact R31 equality without narrowing M4.1 dataclass constructors. Very long configured aliases or future supplied IDs may run untraced. Rejecting the application invocation instead would need a separate contract decision |

RUN-D02 also proposes that changing endpoint, project credentials or tracing environment after the first enabled client requires a process restart for tracing. Workflow configuration still reloads on each invocation. A conflicting tracing configuration skips that invocation's tracing with a clear diagnostic; it must never silently send to the previous destination. Disabled invocations skip acquisition entirely. This rule needs explicit approval because the SDK's cached resources do not implement arbitrary per-call configuration replacement.

Not in M4.2: automatic instrumentor installation, per-phase/per-step manual spans, agent execution, logger/storage/viewer/mirroring, scores/datasets/evaluations, session management, sampling controls in YAML, new collectors/services, async runner APIs, detached tasks/process transport, client pools or new retry/recovery machinery. No changes to M4.1 fields, constructors, `for_agent`, Flow storage or context creation timing are proposed.

## 3. Workflow observation contract

The recommended operation name is the stable `workflow.run`, with `as_type="span"`. The selected configured workflow ID, including an alias, is metadata rather than a request-derived span name. One observation is created by the runner for each eligible enabled invocation. No duplicate mock `LangfuseSession.start_trace` root is created.

Here, workflow root means the root of this invocation. With no active SDK parent it starts a new SDK trace; inside a supported active SDK parent it is a child in that same trace. Do not force a new trace, call `create_trace_id`, supply an invented `trace_context`, or equate correlation_id with trace_id. SDK-produced IDs remain available on the native observation and through current-ID accessors while active. This draft leaves public `RunResult`, CLI stdout and exception APIs unchanged; a trace-ID/URL field would require a demonstrated consumer and separate explicit contract.

| Ordering | Owner and observed behavior |
|---|---|
| Before observation | Existing configuration loading/CrewAI startup, registry/selection and M4.1 context construction, in their existing error boundaries. No synthetic context or pre-context trace |
| Before observation, after context | Validate the three metadata dimensions for SDK propagation; lazily acquire the configured tracing client. Initialization is not workflow business duration |
| Enter native observation | Set the three identity values as root metadata immediately; enter native `propagate_attributes(metadata=identities, as_baggage=False)` before construction or any callback that may emit a child |
| Inside active scopes | Existing wrapper construction; JSON object decoding; `prepare`; `execute`/real Flow kickoff; `validate_output`; `serialize_output`; construct the existing native/display RunResult. Preserve each existing error classification boundary |
| Finish | Record only the invocation's safe outcome; end the native scope and restore its enclosing scope. Hand the original result/exception back to the current runner/CLI contract |
| After observation | Attempt native delivery/flush on normal and ordinary failure exits. It is outside recorded business duration. Do not create an observation for flushing |

The context is still created inside M4.1's CONSTRUCTION error handling immediately before selected wrapper construction. A refactoring that encloses that construction in a native scope must not accidentally classify context creation or telemetry initialization as a new input/execution error, move selection, or catch every phase under one generic application error. Exact helper extraction is reviewed against the actual M4.1 diff at Gate 0.

Read-only inspection of candidate 16c1580's runner, assembly and context models confirms this creation point and the unchanged `assemble_runtime` settings return. Root's final review also found no required M4.1 runtime/contract correction. The proposed scope needs no context redesign. Recheck only subsequent candidate/base changes and resolve the separate documentation integration before the relevant readiness/merge gate.

The root is completed only when output validation and serialization succeed. `needs_work` is a successful WF-03 result. A caught child failure does not force the parent to fail; only this invocation's escaping failure or interruption determines its final projection. The M4.2 production path emits no synthetic agent/tool/generation records for deterministic work.

## 4. Correlation and propagation

Project this one small mapping from the existing context; do not serialize the dataclass or copy arbitrary fields:

| Langfuse metadata key | Sole value source | Contract |
|---|---|---|
| `correlation_id` | `context.correlation_id` | Exact string, unchanged; required on every emitted workflow-associated observation |
| `workflow_id` | `context.observability.workflow_id` | Exact configured ID, including aliases; no replacement with the Python class or CrewAI flow ID |
| `workflow_run_id` | `context.observability.workflow_run_id` | Exact invocation ID; no second generation in tracing code |

Pass ordinary strings to the native SDK. Langfuse 5.2 JSON-encodes propagated metadata internally; tests decode the raw OTel attribute once before checking equality. Do not pass JSON-encoded strings as application values. Use `as_baggage=False`; this disables application metadata propagation through outbound baggage, not every internal SDK context mechanism.

The root receives its explicit mapping at creation and native propagation is entered immediately inside it. This duplication of one mapping is deliberate: the earliest root already has identity, and the propagation context supplies the current root plus future children. Do not enter workflow propagation around an unrelated caller's active parent, which could stamp that parent with this invocation's IDs. Scoped propagation restores the enclosing values on exit.

The exact native API shape is below. This shows scope/projection only; the approved error handling from sections 6–7 must surround the existing lifecycle, so this is not a complete implementation to copy blindly.

```python
from langfuse import propagate_attributes

identities = {
    "correlation_id": context.correlation_id,
    "workflow_id": context.observability.workflow_id,
    "workflow_run_id": context.observability.workflow_run_id,
}
with client.start_as_current_observation(
    as_type="span", name="workflow.run", metadata=identities
) as root:
    with propagate_attributes(metadata=identities, as_baggage=False):
        # Existing construction through serialization, with safe exception
        # projection before leaving this native scope; no per-step spans.
        pass
```

R31 covers native span/agent/tool/generation/event observations and future automatic CrewAI observations associated with this invocation. A later meaningful nested agent scope may add its own fields using native scope support while preserving these three identities. M4.2 does not implement that agent lifecycle. There is no per-step metadata boilerplate, custom span stack, mutable global current context, post-export backfill or SDK object in ExecutionContext.

The pinned propagation implementation drops values whose compact JSON encoding exceeds 200 characters. Default UUIDs fit, but M4.1 permits explicit strings and selected workflow aliases are not bounded that way. Under RUN-D05, a small preflight checks the actual three string encodings before emitting a root; values are never truncated, hashed, regenerated or silently omitted. Tests cover escaping/Unicode near the boundary, not only a 198-character ASCII guess. This is a telemetry eligibility check, not a new context validator. No uncorrelated partial root is acceptable as the ordinary fallback.

This metadata association does not join independent traces. Future context-associated local logs must carry correlation_id independently of optional SDK IDs. Scores, datasets and other non-observation APIs, arbitrary threads/processes and detached background work have no automatic propagation promise here.

## 5. Native client lifetime, configuration and delivery

Retain existing `LangfuseSettings`, external credentials, endpoint selection and `connection.create_client`. The exporting path must explicitly request `tracing_enabled=True`; its existing default is False. Keep `check_connection` separate and do not add an authentication preflight to every workflow. The existing checker intentionally uses the API client rather than creating a disabled cached tracing client.

Recommended ownership is the existing application assembly boundary calling small Langfuse-specific lifecycle functions. One lazy process slot contains only the configured native client and the effective immutable tracing settings needed to compare subsequent calls. It holds no invocation context, current span or workflow result. No pool, generic service, dependency injection framework or public reporting interface is needed. A failed acquisition is not cached as a permanently disabled client; a later independent invocation may try acquisition again, with no application retry loop within the failed invocation.

Langfuse 5.2 caches its resource manager by public key. Reconstructing a Python wrapper does not establish fresh resource ownership, apply every new endpoint setting or undo shutdown. Do not use SDK private cache-reset APIs, repeatedly register exporters, or close a shared client after each run. Same-config repeated calls must reuse the selected native client. Changed tracing settings follow RUN-D02's explicit restart/skip policy; comparisons and diagnostics must not reveal credentials.

The recommendation keeps `assemble_runtime` strictly settings-only, with its configuration-before-framework behavior and current return contract. It must not initialize tracing during early assembly. If a small client-acquisition helper lives in assembly.py, the runner calls that separate helper only after context creation and metadata eligibility preflight, using the already loaded settings; no second YAML load. Provider imports are lazy/TYPE_CHECKING where appropriate. The existing factory, Workflow ABC and concrete flows do not receive the client.

After each enabled invocation ends, attempt `client.flush()` once. This gives short CLI calls a deliberate delivery point and also covers repeated Python callers without changing their public signature. Native SDK final exit cleanup owns shutdown; ordinary `run_workflow` must not shut down the process resource. A host that deliberately terminates its tracing resources cannot resume them through this API without a new process. Abrupt process termination is outside delivery guarantees.

This is a blocking native flush policy, not a hard deadline promise. The current helper's `timeout=5` is a transport setting; `flush()` has no public timeout argument and does not return an ingestion receipt. SDK queues/retries and shutdown behavior must be measured in the supported observation-only path. Do not invent `flush(timeout=...)`, build a timeout thread that cannot cancel export, or claim a five-second end-to-end bound. A strict wall-clock shutdown deadline would need another explicit choice; the proposed tests use an external test deadline to expose hangs, not to implement production cancellation.

Use the SDK's native provider/export processor/default filter. Production needs no separate OTel provider, exporter or collector. Its default filter admits native Langfuse and the researched OpenInference scopes; do not replace it with a generations-only filter. Keep CrewAI's existing startup flags and display behavior; never set `OTEL_SDK_DISABLED=true` merely to disable CrewAI cloud telemetry, because it disables the Langfuse pipeline too. Acceptance fixtures use an explicit ALWAYS_ON provider and in-memory exporter; they must not replace the production provider unnoticed. Record effective sampling/environment for live checks. Custom host providers, multiple projects and sampling overrides are outside the first supported standalone profile, not reasons to install a second global provider.

## 6. Error and interruption ownership

The design distinguishes invalid application settings from an unavailable telemetry service. Proposed RUN-D03 behavior:

| Condition | Application outcome | Telemetry behavior |
|---|---|---|
| Langfuse disabled | Existing result/exception | No client acquisition, exporter construction, auth check or observation for this call; fresh-process disabled execution has zero tracing network attempts |
| Invalid YAML/required keys/selection | Existing configuration or selection exception and CLI category | No root; do not silently reclassify invalid application configuration as a recoverable outage |
| Client acquisition fails after valid config | Run workflow once normally | Fixed sanitized diagnostic; invocation untraced; no fallback cloud endpoint |
| Required metadata cannot be propagated | Run workflow once normally | Fixed diagnostic and no root under RUN-D05; no silently missing correlation |
| Workflow fails inside the observed lifecycle | Exact classified exception type, cause chain and CLI category retained | Root ERROR with safe outcome/phase; no successful result, no business retry |
| SDK start/update/exit/flush fails | Preserve completed result or original workflow failure; if business work has not begun, execute it once through the ordinary path | Catch only telemetry boundary errors; issue fixed safe diagnostic. Never rerun work after a partial/complete business invocation |
| Exporter rejects, times out or drops a batch asynchronously | Existing result/exception | SDK diagnostics remain visible and sanitized; no claimed delivery success. No polling/retry queue in the normal runner |
| KeyboardInterrupt/SystemExit or other BaseException interruption | Propagate the original interruption; no conversion to WorkflowExecutionError or success | Best-effort safe `interrupted` projection and normal scope cleanup; do not guarantee completion after termination |

An outer `except Exception: run_again_without_tracing()` is forbidden: it would retry actual workflow failures and duplicate side effects. The implementation must distinguish scope-entry failure before callback execution, a captured business result/failure, and scope-exit/delivery failure afterward. The existing lifecycle can be factored into one private callable, invoked at most once; no new public result envelope or tracing facade is required. Telemetry error handling may not replace a stored business exception during cleanup.

The smallest diagnostic path is fixed messages through Python's existing diagnostic facilities, with no new logger package, handlers, log storage or structured local LogRecord contract. Never interpolate raw SDK exceptions, keys, response bodies, payloads or full settings. Native exporter diagnostics need a sentinel test too: absence of `str(error)` in our code is not proof that third-party logs are safe. If a narrow logger filter is required, scope it to the actual integration loggers and fixed failure messages; do not add a general logging platform. Exact diagnostic text is implementation detail; visibility, sanitization and preserved exits are acceptance requirements. A failed telemetry diagnostic must not mask a workflow exception.

Native `flush()` can complete without providing a per-trace delivery verdict. Do not turn successful return, a trace ID or a URL into “ingested” output. Only live UI inspection or bounded readback of the expected observation establishes ingestion. An asynchronous loss that the SDK does not surface remains a known limit; this milestone does not promise complete failure detection.

## 7. Safe outcome projection and pinned masking limit

Under RUN-D04 the root gets the three identity fields, the configured environment, native timing/IDs, and a tiny explicit outcome projection. Recommended outcome values are `completed`, `failed`, and `interrupted`; only failed/interrupted observations add a safe phase token (`CONSTRUCTION`, `INPUT`, `PREPARE`, `EXECUTE`, `VALIDATE_OUTPUT`, or `SERIALIZE_OUTPUT`) when known. Keep these outcome fields on the root, not propagated as child business outcomes. `level="ERROR"` and a fixed message such as `Workflow EXECUTE failed` are sufficient for an ordinary escaping failure. Successful completion uses the native default level; do not equate OTel UNSET with failure.

No raw input JSON, validated business output, serialized presentation, `asdict(context)`, exception object/message/cause traceback, configuration, credentials, environment dump, path or native state is exported. This is a project allowlist, not a claim every current context field is sensitive. Python callers retain the actual exception/cause for their existing local debugging behavior.

**Verified source limit:** Langfuse 5.2 `start_as_current_observation` delegates to OTel's context manager, which can record an escaping exception automatically. Its `mask_otel_spans` API patches attributes only; it cannot rewrite exception events, status descriptions, names, resources or links. Therefore an attribute mask alone is not a safe implementation of the no-raw-exception policy.

For this single manual root, the recommended small solution is to catch the business exception/interruption *inside* the native scope, retain that same Python object and traceback locally, update only the safe root outcome, exit the native scope without exposing the raw exception to automatic capture, then re-raise the original outside. Preserve its existing cause chain. The retained exception is a local variable for this call, never context/state/metadata. Telemetry exceptions from update/cleanup use the precedence in section 6. Tests inspect actual exported events/status as well as attributes and verify identity/cause, so a green fake-span test cannot hide leakage.

Do not add a masking hook just to return unchanged attributes when M4.2 sends no payloads. Preserve the supported `mask_otel_spans` extension point in client construction for M4.3 if needed. Before automatic CrewAI enablement, M4.3 must address its raw `flow_inputs`, standardized input/output fields and exception data separately. Released OpenInference wrappers explicitly record exception events/status, so neither `hide_inputs/hide_outputs` nor an attribute-only mask proves complete redaction. This is a source-backed next-milestone decision; do not silently weaken privacy, drop required failed observations, patch third-party code or build a custom span engine here. The native provider/root/propagation choices remain compatible with the researched integration.

## 8. Source placement and dependencies

All runtime paths below are relative to `app/src/agent_playbook/` and remain proposed until the guarded reconciliation is approved.

| Repository → component → file | Responsibility, inputs/outputs and failure owner |
|---|---|
| `application/assembly.py` | `assemble_runtime` stays settings-only. A separate optional acquisition helper is called by the runner after context creation/metadata preflight, using validated settings; never initialize the client in early assembly. Acquisition failures follow telemetry policy |
| `observability/adapters/langfuse/connection.py` | Existing typed settings → native client creation and independent auth checker. Preserve checker behavior/default; exporting caller requests True. Add only concrete constructor options actually needed by approved policy/tests |
| `observability/adapters/langfuse/runtime.py` (small new file if warranted) | One configured native-client slot, settings consistency, native flush support and fixed telemetry diagnostics. Langfuse-specific functions, no reporting methods or provider-neutral interface. A few cohesive functions may remain in connection.py if clearer |
| `application/workflow_runner.py` | Native workflow scope, three-field projection, safe outcome and exception precedence around existing lifecycle. Direct reviewed native SDK use is intentional, subject to section 10 |
| Existing factory / workflows / context / results / CLI | No new client/handle field, step instrumentation, lifecycle signature, output text or trace URL API. Ordinary implementation adjustments require a documented reason and must not reopen M4.1 |
| `app/tests/application/test_runner_observability.py` | Runner export/lifecycle/correlation/failure cases through real integration; existing fixtures retained |
| `app/tests/observability/` | Existing SDK/connection regressions plus minimal native-client lifetime/loopback checks; follow actual repository naming |
| `app/docs/workflows.md`, `langfuse-connection.md`, relevant configuration/troubleshooting guide | After implementation, explain enabling runner tracing, safe payload scope, repeated Python use, flush/restart policy and delivery limits. Internal reviews remain in this design package |

Dependency rule: context remains standard-library-only; factory/ABC/business steps need no Langfuse import. Native Langfuse imports are reviewed in the runner, assembly type/lazy setup and existing adapter package. No OTel private imports or SDK cache manipulation in production. Test fixtures may use the public OTel provider/exporter types already present in the lock to exercise the real SDK. M4.3's instrumentor is not installed in this milestone; no new package or lock change is currently justified.

Minimality check: every helper must implement actual application policy (safe metadata, lifecycle consistency or diagnostic boundary). Do not add wrappers named trace/span/event/agent/generation that mirror SDK APIs, a neutral Observation model, generic registry, no-op provider hierarchy, metadata bus or exporter framework. Native SDK scopes continue to own IDs, parenting and activation.

## 9. Requirements, principles and evidence

| Capability / rubric | Outcome, risk and deferral cost | Acceptance |
|---|---|---|
| Native active workflow scope — A/B, tracing | Timing/outcome parent for M4.3; omitted scope leaves children detached from the application boundary. Small SDK call surface; main risk is changing exception order | RUN-01–05, RUN-08–09 |
| Exact identity projection — B, tracing and future logs | R30/R31 grouping on all emitted observations; omission or truncation loses joins. Small mapping/native propagation; SDK value limit needs an eligibility check | RUN-02–04, RUN-13 |
| Client lifetime and disabled/failure policy — A/B, tracing | Repeated calls and short CLI delivery; omission risks resource reuse bugs or masked business failures. Small native client ownership; export latency/loss remain explicit | RUN-06–12 |
| Payload minimization — B, tracing | Avoid implicit private data export. Catch/project at one boundary; raw framework exception handling remains M4.3 work | RUN-14–15 |
| Stable native extension boundary — C, tracing | M4.3 can share the active provider and correlation without rewriting workflow steps. Native default filter retained; no speculative framework cost | RUN-03–04, RUN-18 |
| Automatic CrewAI, logging, scores and distributed transport — D here | Separate milestones own coverage and policies; deferral does not remove R28/R31 | Explicit exclusions; no M4.2 completion claim for them |

R01–R04/R23/R29/R30 are preserved from M4.1; M4.2 directly supplies R31 and the workflow portion of R14/R17/R19/R26. Synthetic native child/event tests demonstrate propagation mechanics, not actual agents/LLMs. R28 receives the active parent foundation; full automatic Flow coverage belongs to M4.3. R05's privacy/configuration limit is retained. Logging-only R06–R13/R18/R25, agent lifetime R16/R21/R24 and advanced R20/R22/R27 receive no new implementation.

| Principles | Assessment |
|---|---|
| 1, 3, 12, 15 | Explicit draft/pending choices, exact pinned inputs and proposed amendments; no approval or implementation inferred. M4.1 final review is recorded separately; subsequent base drift is checked before coding |
| 2, 6 | External settings retained; explicit identity/outcome allowlist; safe diagnostics and actual exported-data checks |
| 4, 9 | One observable runner milestone; automatic CrewAI immediately next; no logger/agent detour |
| 5 | Narrow direct-native tracing exception proposed, centralized setup retained; separate agent-provider isolation unchanged |
| 7, 8 | Existing strict gate, real SDK export and meaningful regression assertions; same-candidate independent reviews. No tests are claimed run by this document |
| 10 | Existing local deployment only; disabled tests need no backend; no cloud fallback |
| 11, 13 | No history rewrite, sandbox access or dependency; original research evidence remains unchanged |
| 14 | Product guides change with supported runtime behavior; this draft has no product behavior. Root reconciles shared navigation at the agreed publication point |

Research supports API feasibility, not the real runner or live acceptance. The eight-case/44-span evidence has no actual application assembly/UI result; its blocked PyPI version lookups are distinct from telemetry. Iteration 29's zero-attempt check was SDK-only, with disposable proxy cleanup after an initial environment failure. Neither counts as RUN test acceptance.

## 10. Proposed guarded amendments — do not apply during drafting

D11 already selects the no-broker direction. The following changes reconcile that choice and the newly selected runner policies with protected text. They are **proposed, needing file-specific approval**, not permission to broadly relax integration rules. Recheck each file after M4.1's approved G01–G08 changes; retain its dated amendments and approval evidence.

| ID | Guarded file | Logical change and consequence |
|---|---|---|
| RUN-G01 | `designs/principles.md`, principle 5 | Permit direct native Langfuse instrumentation at reviewed application boundaries while centralizing configuration/resource policy; no required provider-neutral tracing facade. Agent execution adapters and all other integration boundaries remain |
| RUN-G02 | `designs/architecture.md` | Replace mandatory neutral observation/exporter path for this tracing phase with native SDK scope/propagation and Langfuse setup. Add selected lifetime/error/payload policy; preserve CrewAI scheduling, safe data, workflow outcomes and deferred logging |
| RUN-G03 | `designs/project-structure.md` | Reconcile observability ownership and exporter-only dependency rule; list approved runner/assembly/native adapter imports and small lifecycle functions. Do not move context, add brokers or permit backend imports throughout workflow business code |
| RUN-G04 | Root `AGENTS.md`, engineering integration rule | Add the same narrow reviewed native-tracing exception so agent instructions do not contradict the target. All guarded-change, secrets, quality and sandbox rules remain |
| RUN-G05 | `designs/stages/02-langfuse/architecture.md` | Add M4.2 native client/root/propagation/error/data ownership, replacing any remaining handle-in-context placeholder; preserve M1–M3 setup/checker/mock contracts and evidence |
| RUN-G06 | `designs/stages/02-langfuse/milestones.md` | Record runner acceptance separately from context and automatic CrewAI; distinguish design, implementation, live verification and user acceptance; no stage renumbering |
| RUN-G07 | `designs/refactors/workflow-contract/implementation-plan.md`, dated Langfuse handoff amendment | Supersede obsolete requirements for context-held clients, required per-phase observation events and an outer trace covering pre-context configuration/selection. Explain the selected one-scope/post-context boundary and preserved errors; retain the original historical handoff |
| RUN-G08 | `designs/governance/guarded-files.md` | Only after approval, register these three M4.2 documents with exact approval reference/revision. Preserve every existing guard |

No change to charter, roadmap stage order or design-contract procedure is proposed. M4.1 design/test/plan and CTX acceptance remain its own baseline. A genuine context defect is reported to root for a separate authorized follow-up; it is not repaired in this draft or hidden in a runner PR. No genuine M4.1 contract blocker has been established from the inspected inputs.

## 11. Sources and completion gate

Primary sources checked read-only on 2026-11-14: [native instrumentation](https://langfuse.com/docs/observability/sdk/instrumentation), [metadata propagation](https://langfuse.com/docs/observability/features/metadata), [advanced SDK features](https://langfuse.com/docs/observability/sdk/advanced-features), [masking](https://langfuse.com/docs/observability/features/masking), and [Python API](https://python.reference.langfuse.com/langfuse). Version-specific behavior was checked against installed Langfuse 5.2.0 `client.py`, `resource_manager.py`, `propagation.py`, `types.py`, and the OpenInference 1.1.25 wrappers in the isolated research environment; no installed file was edited or probe rerun. The typed masking definitions explicitly limit patches to attributes. Public documentation alone is not substituted for the pinned source.

Application sources were read at the pinned main SHA through the GitHub connector, including [runner](https://github.com/SharonLanger/agent-playbook/blob/d12b5fc2867d3646b6fab2eb71f1447ff177d8c1/app/src/agent_playbook/application/workflow_runner.py), [connection helper](https://github.com/SharonLanger/agent-playbook/blob/d12b5fc2867d3646b6fab2eb71f1447ff177d8c1/app/src/agent_playbook/observability/adapters/langfuse/connection.py) and the existing mock observations module. Later, [M4.1 candidate runner](https://github.com/SharonLanger/agent-playbook/blob/16c1580e96bd36945fa96b6ecfa8f9a563d53913/app/src/agent_playbook/application/workflow_runner.py), its assembly and context models were checked for the placement noted above. No personal examples or historical sandbox were inspected.

Before implementation: use the reviewed M4.1 candidate and its final-review record, check subsequent drift/document integration, settle RUN-D01–05, approve the exact design/tests/plan and RUN-G01–08, and resolve any source-backed feasibility gap in the selected policies. Before completion: satisfy the RUN cases, both independent reviews on one candidate SHA, permanent reports and the relevant application/doc/release gates. Actual local ingestion and Sharon's UI acceptance remain explicit separate evidence. No automatic merge or M4.3 implementation follows approval of this draft.
