# Agent Playbook — automatic CrewAI Flow tracing research

Date: 2026-11-14. Status: **research and isolated runtime evidence; integration recommendation, not an approved implementation design.** Repository baseline: `SharonLanger/agent-playbook` at `44d69194f6add6f646795b14f7c3f43c656baeda` (merged PR #36).

Planning update, iteration 21: the permanent shared-records draft PR is authorized now. Basic context structure is accepted; the detailed context document remains unwritten pending alignment. See [requirements](../requirements.md) and [decisions](../decisions.md). The research below is unchanged evidence from its original baseline; no new probe, dependency adoption or application/UI acceptance is claimed by this migration.

## Research brief and acceptance checklist

Evaluate the smallest supported integration that automatically observes **all maintained deterministic WF-01, WF-02 and WF-03 executions**, including `@start`, `@listen`, `@router`, conditions and the branches actually executed. Each invocation must retain one runner trace, with real Flow/step observations beneath it, actual SDK trace/span IDs and inherited `workflow_id`/`workflow_run_id`.

| Research acceptance item | Finding |
| --- | --- |
| Released package, Python 3.13 and current dependency compatibility | Proven with released wheel installation, dependency check and runtime probe. |
| One runner → Flow → executed steps, without manual decorators on every step | Proven for all three maintained Flow definitions copied unchanged from the baseline. |
| Routing, failure, repeat and async behavior | Proven for both WF-03 branches, WF-02 failure/repeat, direct async kickoff, and an independent AND/OR fixture. |
| Shared workflow/run metadata and actual IDs | Proven on every exported observation in eight cases. |
| Minimal code, no broker/facade or additional service | Supported by native Langfuse active scopes and one in-process OpenInference instrumentor. |
| Local destination and privacy | Direct local Langfuse export is supported; live ingestion is not tested here. Blocked CrewAI PyPI version checks and payload-redaction limitations remain explicit. |
| Evidence beyond current upstream main | Released 1.1.25 wheel inspected and executed; hashes and reproducible probe supplied. |

Constraints: keep one `ExecutionContext` with one `ObservabilityContext`; do not implement `ObservabilityBroker` or a provider-neutral tracing facade. Reuse local Langfuse and existing configuration. Scores and application logging remain later work. Do not prescribe agent lifecycle, pooling, event contracts or harness behavior. Research may recommend justified version changes, but makes no repository/code/pin changes and does not inspect `app/examples/`.

## Recommendation

**Proceed with `openinference-instrumentation-crewai==1.1.25` in its default wrapper mode, using the existing `crewai==1.15.40` and `langfuse==5.2.0`.** No framework or Langfuse upgrade is required by this evidence. Add the instrumentor once during configured runtime initialization; create one native active Langfuse runner scope per invocation and call the existing workflow normally inside it. The released integration creates the actual Flow and executed method observations automatically. The official Langfuse integration uses the same package, although its example disables dependency checks; this research did not. [S1–S3]

This is a practical recommendation, conditional on the remaining application/local-ingestion checks below. It does not promise every arbitrary CrewAI feature is instrumented. Prefer narrow native SDK additions only where a demonstrated gap matters; do not construct a custom tracing platform to force full coverage.

**Important boundary:** the probe passed eight tracing scenarios and exported 44 spans through the real Langfuse SDK's default processor/filter to an in-memory exporter. It did not run a Langfuse server, exercise the actual application runner/ABC wrapper, or prove UI ingestion. The Python network audit blocked eight DNS attempts to `pypi.org`; no outbound connection succeeded. Released CrewAI includes a PyPI version checker, distinct from its telemetry exporter. Thus these attempts are not evidence of telemetry sent to a cloud tracing service, but telemetry-off alone is not proof of zero network behavior. Do not describe this probe as fully offline without that qualification.

## Exact package evidence

| Component | Baseline / tested recommendation | Evidence and license |
| --- | --- | --- |
| Python | 3.13.5; project `>=3.13,<3.14` | Runtime probe used `/usr/bin/python3.13`. |
| CrewAI | Keep `1.15.40`; core and CLI also `1.15.40` | Current app lock and installed wheel; declared Python `>=3.10,<3.14`. Existing component; no license change proposed. |
| Langfuse Python | Keep `5.2.0` | Released Nov 5; MIT; Python `>=3.11,<4.0`. [S4] |
| CrewAI instrumentor | Add `1.1.25` | Released Nov 11; Apache-2.0; Python `>=3.10,<3.14`; instrumented dependency declares `crewai>=1.10.1`. [S2] |
| OpenInference base | Lock `0.1.77` in tested closure | Apache-2.0. Instrumentor requires `>=0.1.76`. |
| OpenInference conventions | Lock `0.1.44` in tested closure | Apache-2.0. Instrumentor requires `>=0.1.42`. |
| OTel instrumentation | Add/lock `0.66b2` | Apache-2.0. |
| OTel API / SDK / OTLP HTTP | Keep existing `1.45.2` | Apache-2.0; already in the application lock. CrewAI needs `>=1.45.1,<2`, Langfuse `>=1.45.0,<2`. |
| OTel semantic conventions | Keep existing `0.66b2` | Already in application lock. |
| wrapt / typing-extensions | Keep existing `2.5.2` / `4.16.0` | Existing transitive dependencies: BSD-2-Clause / PSF-2.0; not newly selected replacements. |

The four newly added packages in the tested closure are Apache-2.0: the CrewAI instrumentor, OpenInference base, OpenInference conventions and OTel instrumentation. Installed metadata was inspected. The instrumentor also declares unbounded dependencies on OTel API/instrumentation/conventions, typing-extensions and wrapt; the lockfile, not those broad declarations, must make delivery reproducible.

`uv pip check` passed for 144 installed packages. After resolving an isolated environment, three incidental resolver changes were restored to the application lock (`uv==0.13.6`, `onnxruntime==1.31.1`, `pydantic-settings==2.16.2`) and the probe passed again. Every installed package already present in the app lock then matched its baseline version. This is stronger than a permissive package metadata check, but is not a clean application release/gate run.

PyPI now lists 1.1.27 (Nov 12); it was not runtime-tested here. Recommendation 1.1.25 is the tested candidate, **not a claim that it is latest**. There is no demonstrated requirement to choose a newer release for these Flow cases. Reassess a newer release if its changelog fixes a relevant defect; do not infer wheel behavior from current `main` alone. [S2, S5]

Wheel SHA-256 evidence:

```text
crewai-1.15.40-py3-none-any.whl
5dc1d2cc26c7b0344ffa7e9a318e928b90b6f05da0fe322c1f7c6f94af225836
langfuse-5.2.0-py3-none-any.whl
4763cbad358960f1036078a4c6e9f86f04690ea566541709c2c40aa1998e2b0f
openinference_instrumentation_crewai-1.1.25-py3-none-any.whl
855245466c6faebec5d997b199bf658ba950ce0870dd9ae1fb359ea780cdd836
```

PyPI's instrumentor wheel provenance identifies publishing commit `cac2a7d7c73c8e2243954e0ad44675ec1a6b1167`; its published wheel hash matches the downloaded artifact. [S2]

## What was actually observed

The fixture copied only maintained `flow.py`, `state.py` where present, and `steps.py` from:

- `app/src/agent_playbook/workflows/wf_01_step_sequence/`
- `app/src/agent_playbook/workflows/wf_02_shared_state/`
- `app/src/agent_playbook/workflows/wf_03_conditional_route/`

No private examples or live models were used. The actual native Langfuse `start_as_current_observation` and `propagate_attributes` APIs ran with a shared OTel provider and Langfuse's public `span_exporter=InMemorySpanExporter()` hook. The default Langfuse span filter was retained. Instrumentation used dependency checking normally, with no `skip_dep_check=True`.

| Scenario | Observed nodes | Exported spans including runner + Flow |
| --- | --- | ---: |
| WF-01 | produce → decorate → finish | 5 |
| WF-02 | initialize → add → multiply → finish; output 20 | 6 |
| WF-03 score 80 | begin → choose → accept; output pass | 5 |
| WF-03 score 20 | begin → choose → revise; output needs_work | 5 |
| WF-02 fresh repeat | Same four nodes, separate trace/run IDs | 6 |
| WF-02 controlled multiply exception | initialize → add → multiply; finish absent | 5 |
| Independent condition fixture | begin, asynchronous left/right, AND join, OR listener finish | 7 |
| Direct `await kickoff_async()` | WF-03 begin → choose → accept | 5 |

Assertions passed: exactly one kickoff span per run; kickoff parent is the runner; every executed node's parent is the kickoff; all observations share the runner's actual trace ID and carry both workflow metadata keys; spans have distinct operation identities; run trace IDs differ; active context is restored after normal/failing execution; expected workflow outputs remain correct. Failure marked the failing method, Flow and escaping runner scope ERROR; successful earlier steps remained OK. Native runner success status remained UNSET, which is not an error.

This is **runner → Flow → sibling step observations**, not a new independent trace per step and not a fabricated parent-child chain mirroring graph arrows. AND/OR scheduling decisions do not become standalone observations. Routing is visible through the router method and only the listener actually executed. Method attributes include `flow.node.name` and `flow.node.type` (`start`, `listen`, `router`). Default names were `Flow_<framework-id>.<method>`; do not confuse framework `flow_id` with application `workflow_id` or `workflow_run_id`.

Langfuse 5.2 encodes propagated metadata values as JSON strings in OTel attributes; the probe correctly decoded those before equality assertions. For example, a string appears as `"research-wf02"` in the raw `langfuse.trace.metadata.workflow_id` attribute. This is SDK behavior, not a reason to double-encode inputs.

## Coverage and limits

Evidence levels: **Runtime** means the released versions above were executed; **Released source** means the downloaded wheel was inspected; **Unverified** means no claim of observed behavior.

| Capability | Evidence | Practical limit |
| --- | --- | --- |
| Runner active root, inherited trace identity | Runtime | Application lifecycle scope and returned result contract still need design. |
| Flow synchronous kickoff | Runtime | Sync wrapper creates the Flow span before its async bridge; duplicate kickoff is suppressed. |
| start/listen/router | Runtime, all maintained definitions | `_execute_method` is a private CrewAI hook, so framework upgrades need regression checks. |
| Executed branch selection | Runtime, both WF-03 branches | No spans for unexecuted branches; no graph-wide static trace promised. |
| AND/OR conditions, async step methods | Runtime, independent fixture | Conditions themselves are orchestration, not separate spans. |
| Async kickoff | Runtime | Arbitrary thread/process handoffs and concurrently interleaved workflow runs remain unverified. |
| Repeated fresh invocations | Runtime | Same Flow object re-entry, loops, persistence/resume, cancellation and retries remain unverified. |
| Escaping failure | Runtime | Recovered child failure/successful parent remains a focused follow-up; no automatic business-outcome inference. |
| Inputs/outputs | Released source + observed output | Flow records kickoff input/output; method wrapper records returned output, not every state mutation or method argument. WF-02 methods returning None do not expose state history automatically. |
| Crews/tasks/standalone agents/tools | Released source | Wrappers exist for Crew.kickoff, Task._execute_core, Agent.kickoff, BaseTool.run and overridden Tool.run; no real agent/tool scenario executed. Agent internals may suppress their internal Flow spans. |
| Model generations/token usage | Unverified for this mode | Do not promise complete generation/usage capture from wrapper mode alone. Event-listener mode can create LLM-event spans; model-provider instrumentation is another later option. Choose one owner to avoid duplicates. |
| Langfuse UI types/mapping/ingestion | Documented, not runtime server-tested | OpenInference CHAIN/type/input/output attributes must be confirmed against the deployed local server; arbitrary fields may remain metadata. |

Default wrapper mode is the release's recommended mode for ordinary Python CrewAI use. Event-listener mode is intended for execution surfaced through the event bus, such as AMP/low-code use. It is not required for the tested deterministic Flows and introduces extra event-context/lifecycle considerations. Do not combine both approaches merely to get more spans. [S2, S3]

## Minimal initialization and execution recipe

The following is **an illustrative application integration recipe using APIs verified in the probe/released SDK**, not an application patch. Initialization belongs at assembly after settings have been applied and before workflow imports/execution. The runner owns the per-invocation active scope; CrewAI owns orchestration.

```python
# Once per process, only when configured Langfuse tracing is enabled.
# Existing configure_crewai(settings) runs first, before framework imports.
from langfuse import propagate_attributes
from openinference.instrumentation.crewai import CrewAIInstrumentor
from agent_playbook.observability.adapters.langfuse.connection import create_client

client = create_client(langfuse_settings, tracing_enabled=True)
CrewAIInstrumentor().instrument()  # use Langfuse-initialized global provider

# Per invocation, around the reviewed runner lifecycle boundary:
with client.start_as_current_observation(
    as_type="span", name=workflow_id
) as root:
    with propagate_attributes(metadata={
        "workflow_id": workflow_id,
        "workflow_run_id": workflow_run_id,
    }):
        trace_id = root.trace_id
        runner_observation_id = root.id
        result = execute_selected_workflow()  # existing ABC lifecycle boundary

# After scopes end: entry-point/application owner flushes before short CLI exit.
client.flush()
# That same owner shuts down at final application exit, including error paths.
# Do not shut down a shared client after each invocation of a long-lived caller.
```

`create_client` currently defaults to `tracing_enabled=False`; passing True explicitly is essential. Keep the separate authentication checker, which deliberately avoids poisoning the SDK's resource cache with a disabled preflight client. Do not extend the explicit mock `LangfuseSession/Observation` wrapper into an auto-tracing broker. [S8]

The probe instead passed one explicit `TracerProvider(sampler=ALWAYS_ON)` to **both** `Langfuse(..., tracer_provider=provider, span_exporter=exporter)` and `CrewAIInstrumentor().instrument(tracer_provider=provider)`. This isolates test resources. Production may similarly inject a single provider if needed, but must not accidentally initialize two disconnected providers. No separate exporter, OTel collector, Phoenix server, Arize service or cloud account is necessary. Langfuse 5.2 sends OTLP HTTP directly to the configured base URL's `/api/public/otel/v1/traces`, including the v4 ingestion header. [S6]

The probe environment inherited `OTEL_TRACES_SAMPLER=parentbased_traceidratio` and argument `0.01`, initially producing no sampled spans. Explicit ALWAYS_ON resolved this. Initialization must review sampler configuration and existing global provider ownership; setting a Langfuse sample rate does not necessarily override an already configured provider. This is an environment issue, not a Flow-coverage failure.

## Effect on the context contract

**Current recommendation, iteration 24:** use the ordinary active-scope recipe above without create_trace_id or explicit trace_context. The official basic CrewAI example and this report's original eight-case probe already use that route. SDK-generated/inherited trace IDs and active parentage do not require a stored trace field or passing a span handle through application methods. P04 in decisions.md recommends retaining application workflow/run/agent fields only, with actual SDK IDs read at reporting boundaries. The preallocation option below is supported but unnecessary for the present scope.

Keep `ExecutionContext.observability` as the single explicit application context. Its workflow/run identities and safe inherited metadata can exist before tracing begins. **Iteration 23 clarification:** a trace ID may also be allocated locally in advance using the supported static `Langfuse.create_trace_id()` helper and supplied through `trace_context` when starting the SDK scope. The earlier assertion that the trace ID must remain optional/unbound until span creation was too restrictive. A reserved ID is not an active observation or proof of backend ingestion; operation/span references still come from actual SDK scopes. Context schema remains a design decision.

An immutable context copy is **not** an active span. OpenTelemetry's current context, managed by Langfuse/OpenInference scopes, owns activation and restoration. Do not maintain a competing mutable “current span” field or span stack inside `ObservabilityContext`. A retained root observation ID is a root reference; it must not be presented as the active child ID while CrewAI is executing a step. When immediate current-operation correlation is needed, obtain the SDK/OTel current span's actual context at that point. The probe establishes shared trace identity, not a finalized application accessor/schema.

Use native `propagate_attributes` for safe metadata scoping. Child metadata additions should live in a nested scope and end on return; no copying clients or overwriting parent/sibling metadata. Only project selected fields into telemetry; do not serialize the full ExecutionContext. Keep runtime handles outside recoverable workflow business state. Future agent invocation identity can use the same nested metadata mechanism without choosing an agent lifecycle today.

The public `get_current_trace_id()` and `get_current_observation_id()` accessors support correlation in logs; the pinned 5.2.0 implementations return None when disabled or when there is no active span. Capture IDs when a record is created, before asynchronous delivery. Scope exit restores the enclosing operation, so later consumers need a retained SDK-produced reference when they genuinely outlive that scope. Ordinary same-context nesting is automatic; unrelated threads/processes and external CLIs remain separate propagation work. This source check reuses the existing runtime evidence and does not claim a new probe run.

## Locality, privacy and operational risks

Focused trace-ID check, 2026-11-14 / iteration 23: Langfuse 5.2.0 generated a nonzero 32-character hexadecimal ID before client construction. A client with explicit ALWAYS_ON provider and InMemorySpanExporter then started a root with `trace_context={"trace_id": trace_id}` and a normal nested child. Both exported spans retained the supplied ID; the child's parent was the root; zero Python socket/DNS attempts were observed. No Langfuse server/UI or CrewAI scenario was involved. The original eight-case/44-span research results above are unchanged. The static helper and trace_context path were also inspected in the released 5.2.0 client source. See [official trace-ID documentation](https://langfuse.com/docs/observability/features/trace-ids-and-distributed-tracing).

- Preserve existing `CREWAI_DISABLE_TELEMETRY=true` and `CREWAI_TRACING_ENABLED=false` before framework imports. Built-in CrewAI/AMP tracing is a different destination. **Do not use `OTEL_SDK_DISABLED=true` to disable only CrewAI telemetry**: it also disables the Langfuse OTel pipeline.
- The probe blocked eight `pypi.org` DNS lookups. Captured call stacks show CrewAI's event-bus `on_flow_started` handler → console formatter → version update check → `crewai_core/version.py` requesting `https://pypi.org/pypi/crewai/json`. This was direct framework startup with the same two environment flags set by current `config/crewai.py`, not the actual configured application runner path. Other application display/startup behavior was not reproduced, so this is **not evidence of an application regression**. Confirm the normal runner's existing display/startup suppression path before claiming zero external attempts. Do not silently replace framework behavior in this research. These are update/version lookups, not observed trace exports.
- Auto-instrumentation can record inputs, outputs and exception messages/stack traces. OpenInference `TraceConfig(hide_inputs=True, hide_outputs=True)` controls standardized fields, but the released Flow wrapper also sets raw `flow_inputs`; do not assume those two flags redact every attribute. Langfuse's native `mask_otel_spans` hook is available for comprehensive export masking. Validate with synthetic sentinel secrets; avoid a home-grown provider-neutral redaction platform.
- Use the explicit existing local base URL and external local project keys. Keep `as_baggage=False` unless cross-service propagation is deliberately needed: propagating metadata in outbound baggage can expose it to third-party requests. [S7]
- Langfuse 5.2's default export filter recognizes the `openinference` scope prefix; the probe proved these non-LLM Flow spans survive it. Do not install a filter that allows only generations and silently discards runner/Flow/steps.
- Instrument once; avoid stacking manual step decorators over automatic wrappers or adding a second OTLP exporter for the same backend. Keep wrapper/event-listener/model-instrumentor ownership explicit.
- Flush is a delivery attempt, not proof of durable ingestion. Preserve the existing readback limitation. Define telemetry outage behavior separately from workflow business success; do not label telemetry failure as a failed computation automatically.

## Remaining focused validation before integration acceptance

1. Wire the reviewed M4.1 context and M4.2 runner scope through the actual maintained CLI/Python runner, factory and ABC lifecycle. Test all three workflows and both WF-03 branches against the same released pins.
2. Repeat the in-memory assertions in maintained tests: exact expected method set, one kickoff, root/Flow/node parent IDs, common actual trace ID, propagated keys, failure propagation, recovered child with successful parent, run/sibling isolation, scope restoration and disabled mode. Add concurrency only where the supported application entry point permits it.
3. Test startup twice in one process and relevant import ordering. Disabled Langfuse must not create an exporting client or install an exporting pipeline. Check effective sampler and forbid accidental CrewAI cloud telemetry. Audit Python socket/DNS attempts and identify/suppress irrelevant update checks through the supported application path.
4. Exercise safe payload projection/masking with sentinel credentials and inspect exported attributes, events and errors, including `flow_inputs`. Ensure successful None-returning methods are visible even though state history is not automatically captured.
5. With the existing local stack, run WF-01, WF-02 success/failure and both WF-03 branches. Confirm actual IDs, hierarchy, metadata, observation types and error levels through the local UI or suitable bounded readback. Confirm only the configured local destination receives telemetry. Do not infer this from flush or a printed URL.
6. Run relevant application gates and the locked release process after implementation; retain exact dependency hashes. Update official documentation for supported configuration/behavior, and reconcile governed design/Atlas records before calling the integration accepted.

## Governance and placement

Root instructions, mandatory design entry, charter, architecture, principles, project structure, roadmap/progress, Stage 02 architecture/milestones and the observability exploration were read at the baseline. At research time this was a session artifact and no repository text/code/pins changed. Iteration 21 now preserves it under the permanent Stage 02 draft workspace and adds discovery/Atlas links. That documentation migration does not make the recommendation an approved implementation design.

The native-SDK/no-broker session direction conflicts with guarded wording requiring provider-neutral observations and exporter-only backend dependencies. Reconcile that wording explicitly before implementation: `designs/principles.md` principle 5, `designs/architecture.md` observability/replaceability sections, and `designs/project-structure.md` observability ownership/dependency rules are material surfaces. Preserve the separate agent-execution adapter boundary. Existing stage guards remain protected; research is not approval to rewrite them.

Proposed responsibility placement stays small: assembly owns configuration and once-only instrumentation; the runner owns invocation scope/outcome; the existing Langfuse integration owns client/export settings and cleanup support. Workflows retain their present routing/state code. Exact context module placement and runner lifecycle extent remain design decisions.

## Reproduction and evidence package

The [unpacked reproducibility package](probe/README.md) accompanies this report. It contains the probe, exact resolved requirements, raw exported-span results with actual IDs, the eight maintained source files copied at the stated SHA, and a README. It contains no credentials, model calls, repository edits or private examples. The wheel hashes above identify the main tested artifacts. Dependency installation needs package-index access; the probe itself installs a Python audit hook that blocks socket connection/DNS attempts. Run the commands below from a disposable copy of the research/probe directory; the preserved probe files are not application test inputs.

```bash
python3.13 -m venv .probe-venv
uv pip install --python .probe-venv/bin/python -r requirements.txt
uv pip check --python .probe-venv/bin/python
.probe-venv/bin/python probe.py
```

Expected final line for this environment: `PASS: 8 trace cases; 44 exported spans; 8 blocked socket/DNS attempts`. Update-check cache/environment differences can change the blocked-attempt count; the script records it rather than treating blocked calls as successful traffic. This is a Python-level audit, not an OS-wide network sandbox. Raw evidence is in `results.json`; no Langfuse UI/server result is claimed.

## Primary sources

- **S1.** [Langfuse CrewAI integration](https://langfuse.com/integrations/frameworks/crewai) — recommended integration package, native runner scope and propagation pattern. Its bypassed dependency check is not adopted here.
- **S2.** [OpenInference CrewAI 1.1.25 release, wheel, license and provenance](https://pypi.org/project/openinference-instrumentation-crewai/1.1.25/) — wheel metadata and README; downloaded wheel executed in this report.
- **S3.** [Released publishing commit: instrumentor](https://github.com/Arize-ai/openinference/blob/cac2a7d7c73c8e2243954e0ad44675ec1a6b1167/python/instrumentation/openinference-instrumentation-crewai/src/openinference/instrumentation/crewai/__init__.py) and [wrappers](https://github.com/Arize-ai/openinference/blob/cac2a7d7c73c8e2243954e0ad44675ec1a6b1167/python/instrumentation/openinference-instrumentation-crewai/src/openinference/instrumentation/crewai/_wrappers.py). Findings verified against the wheel's corresponding files rather than inferred from main.
- **S4.** [Langfuse 5.2.0 release](https://pypi.org/project/langfuse/5.2.0/) — wheel metadata and SDK; local wheel files `_client/client.py`, `resource_manager.py`, `span_processor.py`, `span_filter.py`, `span.py` inspected.
- **S5.** [OpenInference CrewAI 1.1.27 release](https://pypi.org/project/openinference-instrumentation-crewai/1.1.27/) — newer release observed, not runtime-tested.
- **S6.** [Langfuse native OpenTelemetry ingestion and mapping](https://langfuse.com/integrations/native/opentelemetry) — direct local endpoint, ingestion header, attribute mappings and interoperability.
- **S7.** [Langfuse metadata propagation](https://langfuse.com/docs/observability/features/metadata) and [Python API reference](https://python.reference.langfuse.com/langfuse) — version-specific metadata and propagation semantics; tested against 5.2.0.
- **S8.** [Baseline connection helper](https://github.com/SharonLanger/agent-playbook/blob/44d69194f6add6f646795b14f7c3f43c656baeda/app/src/agent_playbook/observability/adapters/langfuse/connection.py), [CrewAI startup configuration](https://github.com/SharonLanger/agent-playbook/blob/44d69194f6add6f646795b14f7c3f43c656baeda/app/src/agent_playbook/config/crewai.py), and [application lock](https://github.com/SharonLanger/agent-playbook/blob/44d69194f6add6f646795b14f7c3f43c656baeda/app/uv.lock).
- **S9.** [CrewAI 1.15.40 release](https://pypi.org/project/crewai/1.15.40/) and installed `crewai-core==1.15.40` `version.py` — runtime framework and PyPI version-lookup evidence.

## Supplemental metadata check — iteration 29, 2026-11-14

This is separate from the preserved eight-case/44-span CrewAI probe above. Official metadata/API references (S7) and installed Langfuse 5.2.0 propagation.py, span_processor.py and create_event source confirm that propagate_attributes sets the current observation and future observations in scope. It does not retroactively update previously completed observations. The pinned SDK accepts correlation_id and JSON-encodes propagated values; pass the ordinary UUID string, not a pre-encoded string. Keep as_baggage=False.

Focused disposable check: explicit ALWAYS_ON TracerProvider, InMemorySpanExporter, dummy keys/local URL and Python socket/DNS audit guard. Two independent roots each entered propagate_attributes with a fresh correlation_id plus workflow_id/workflow_run_id; inside, native SDK agent/tool/generation observations and create_event were emitted. All ten exported observations had exactly their group's correlation value. A further root outside both scopes lacked the metadata, proving cleanup for this synchronous case. Result: PASS, SDK 5.2.0, 10 correlated observations, two groups, one clean outside-scope observation, zero socket/DNS attempts.

The initial check could not construct the SDK client because the tool environment had a SOCKS proxy but no socksio package. Clearing proxy variables solely within the disposable probe process resolved it; no dependency or application setting was changed. These are synthetic SDK observations, not actual agent/LLM work. No CrewAI rerun, application test, local server ingestion/filter check, score metadata inheritance or thread/process propagation is claimed. R31 still requires those relevant acceptance checks in the milestone that implements each capability.
