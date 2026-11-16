# M4.2 + M4.3 — native runner and automatic CrewAI tracing

Version 2, 2026-11-15. **REVIEW DRAFT.** Sharon approved consolidation and preparation of this simplified design, not this unseen detailed implementation contract. M4.1 is accepted and merged through PR #44. PR #47 remains draft and MERGE LAST.

[Requirements](../requirements.md) · [Decisions](../decisions.md) · [Tests](test-cases.md) · [Implementation plan](implementation-plan.md) · [Handover rules](../../../../governance/codex-handover-rules.md)

## 1. Goal and revision boundary

Run the existing workflows through the CLI/Python runner and see one native runner observation containing automatic CrewAI Flow and executed-method observations in local Langfuse. Every observation carries the existing correlation_id, workflow_id and workflow_run_id. Preserve outputs, validation, exception classification and scheduling.

This version supersedes the unapproved version-1 runner-only proposal. It removes custom client-cache/configuration-change policy, per-value tracing eligibility rules, root outcome projection and catch/store/rethrow exception machinery. Those were proposals, not accepted requirements. Earlier text remains in Git history at 7ffa9228a1e131f9f252d7d5def3abdde144f793. Historical RUN-D01–05 are retired; this version's explicit remaining choices govern.

Use native SDK lifecycle, attribute propagation and batching. Add no broker, parallel span stack, generic telemetry registry, custom event listener, manual per-step decorator or duplicate exporter. No agent runtime, local logger, scoring pipeline, model-specific cost integration or cross-process propagation.

## 2. Existing foundation and actual path

M4.1 already creates immutable ExecutionContext/ObservabilityContext and UUID4 correlation identity in application/workflow_runner.py after configuration and workflow selection. The factory forwards the same reference into Workflow; each maintained wrapper forwards it into its private Flow context during prepare. for_agent creates separate contexts without altering the parent.

Retain this location and schema. Do not allocate SDK trace IDs or store clients/span handles in context. The runner lifecycle is construction → input decoding → prepare → execute/kickoff → output validation → serialization → RunResult. Configuration/selection failures before context creation retain existing diagnostics and are outside the invocation observation.

## 3. Small application wiring

1. Apply existing external configuration, including local Langfuse destination and CrewAI telemetry/display settings.
2. When tracing is enabled, initialize the native Langfuse client and the released CrewAI instrumentor before workflow execution. Use one shared tracing provider. Initialization must be safe when the Python runner is invoked repeatedly; rely on native client/instrumentor facilities rather than building a cache or pool.
3. Create the existing per-invocation execution context at its current boundary.
4. Start one native current observation named for the selected workflow around construction through successful RunResult creation.
5. Immediately inside it, enter native propagate_attributes with only correlation_id, workflow_id and workflow_run_id from the context.
6. Execute the existing lifecycle unchanged. OpenInference creates Flow/step observations. Let native scopes close and record escaping exceptions; keep existing error wrapping/cause chains.
7. At the short-lived CLI exit boundary, attempt native flush in finally, after observation scopes close, including failure paths. Cleanup must not replace an existing workflow exception.

No per-observation callback or metadata loop is needed. Do not shut down a shared client after each library call. Flush is a delivery attempt, not proof of ingestion. Hard termination cannot execute finally. Disabled mode must execute normally without an exporting pipeline or installing this integration for that invocation. The supported enablement configuration is process-scoped; dynamic reconfiguration is not a new feature.

## 4. Responsibility and placement

Paths are relative to app/src/agent_playbook unless stated otherwise.

| File/component | Responsibility |
|---|---|
| application/assembly.py and existing initialization path | Configure integrations; arrange once-only instrumentation before Flow execution. Preserve existing settings contract; do not eagerly create per-run context |
| observability/adapters/langfuse/connection.py | Reuse typed configuration/native client creation; preserve independent authentication checker and explicit tracing_enabled=True for exporting clients |
| observability/adapters/langfuse/runtime.py, only if a separate setup file is warranted | Small concrete initialization/flush functions using public SDK calls. No span/event facade, custom caching or client registry |
| application/workflow_runner.py | Native enclosing scope and three-field metadata mapping around existing lifecycle |
| Existing CLI entry point | finally-based delivery at process exit; preserve errors/exit codes and ordinary output |
| workflow_factory.py, Workflow ABC, maintained Flow/step files, context/models.py | No new instrumentation is needed; existing context forwarding remains |
| app/pyproject.toml and app/uv.lock | Add released CrewAI instrumentor and lock tested dependencies |
| app/tests/application and app/tests/observability | Real runner/export integration assertions and initialization/cleanup tests |
| app/docs | Update supported setup/configuration/workflow/troubleshooting guidance after implementation; no internal review material |

Before coding, identify the actual CLI entry filename from the current checkout and record it in the coder report. Do not add a new CLI framework. Direct native SDK imports at reviewed integration/runner boundaries require the narrow guarded reconciliation below; context and business steps stay provider-free.

## 5. CrewAI integration and dependencies

Adopt the researched normal wrapper mode of openinference-instrumentation-crewai==1.1.25 with existing crewai==1.15.40 and langfuse==5.2.0, subject to a clean lock/install check against the actual implementation base. The research supplies compatible dependency closure and Apache-2.0 license evidence for new packages. This is the tested candidate, not a claim of latest versions. Use normal dependency checking; do not copy skip_dep_check=True merely because an upstream example uses it.

Initialize CrewAIInstrumentor once against the same provider used by Langfuse. Keep the SDK's OpenInference-aware default export behavior. Do not add a collector, cloud account or second exporter. Keep existing CrewAI/AMP telemetry disabled; do not globally disable OTel, which would also disable Langfuse.

Expected hierarchy: runner → Flow kickoff → executed steps as siblings. Router choice is visible through the router operation and the branch that ran; skipped branches are absent. No span for every graph edge, state mutation or arbitrary utility call. Existing three workflows suffice; no new production agent is needed.

## 6. Identity, nesting and future agents

Native propagation supplies all three application IDs to the root and automatic descendants. Passing an immutable application context alone does not activate a trace. Langfuse/OTel supplies actual trace/span IDs and parentage.

Future agent-specific fields must be propagated INSIDE the corresponding active agent observation. Propagating them while the workflow is current would also stamp the workflow. Native exit restores the enclosing propagation context. Reuse the automatic agent observation where the actual future integration supplies it; do not add a duplicate manual agent span preemptively.

The isolated 5.2.0 check proved A/tool → workflow → B/tool isolation and flush after normal/error exits. Future real-agent wiring and arbitrary thread/process handoffs are not claimed implemented.

## 7. Errors, delivery and payload choice

Preserve existing application error types, cause chains and exit behavior. Native instrumentation records escaping operation failures; a recovered child can remain failed while its parent succeeds. No custom retry/recovery engine or manual synthesized error records.

Proposal for delivery faults: use the SDK's normal behavior; prevent an unexpected cleanup exception from hiding the existing workflow outcome, with a small fixed diagnostic if needed. Do not create persistent queues or custom retries.

**PAYLOAD-01 — accepted by Sharon, 2026-11-15:** retain native capture of workflow inputs, outputs and exception details for the current workflows. Configuration and credentials must never become trace payloads, including through automatic capture; verify the real exported attributes/events/status with synthetic configuration-secret sentinels. Do not serialize complete settings or context. Authentication headers used to authenticate to the configured local server are distinct from recorded trace payloads.

Capture can be adjusted later through supported SDK/instrumentor controls and, if useful, application configuration; no context redesign is required. Langfuse decorator input/output switches do not automatically govern CrewAI instrumentation. OpenInference hide_inputs/hide_outputs does not necessarily hide raw flow_inputs; pinned Langfuse attribute masking does not rewrite exception events/status. Do not promise automatic recognition/redaction of arbitrary secrets embedded in business input or exceptions. If the real integration exposes configuration/credentials, report and resolve that concrete defect before acceptance using supported controls where possible; do not silently relax the requirement or invent a generic redaction framework.

Use the existing local destination only. Verify framework update-check behavior through the normal application path: prior isolated research blocked PyPI version lookups, distinct from trace export. Do not add ad hoc monkeypatches to make a locality test green.

## 8. Acceptance and evidence

The [RUN test cases](test-cases.md) are the combined milestone acceptance list. Use the actual runner/factory/ABC and maintained flows with a real SDK in-memory exporter; inspect generated observations instead of merely mocking SDK call counts. Cover all workflows, both conditional branches, disabled/repeat/failure paths, exact correlation, non-duplication, recovered failure and CLI flush.

Then verify actual ingestion/hierarchy/metadata in the existing local Langfuse deployment. Offline export tests do not replace UI/server acceptance. Run the repository's applicable quality/release and documentation checks; keep sandbox exclusions.

Original evidence: [CrewAI research](../research/crewai-langfuse.md), eight scenarios/44 spans on preserved fixtures, not actual runner acceptance. Iteration 38 tested synthetic native scope isolation, not real agents or local UI. No application implementation or new acceptance run is claimed by this design.

Principle assessment: external config and local deployment retained; shared context remains data-only; SDK reuse replaces custom tracing code; deterministic evidence and independent reviews required; history/guards/sandbox boundaries preserved; product guides follow delivered behavior. Native tracing is a narrow exception to provider-neutral wording, not a relaxation of agent execution adapter isolation.

## 10. Proposed guarded amendments — do not apply during drafting

D11 already selects the no-broker direction. The following changes reconcile that choice and the newly selected runner policies with protected text. They are **proposed, needing file-specific approval**, not permission to broadly relax integration rules. Recheck each file after M4.1's approved G01–G08 changes; retain its dated amendments and approval evidence.

| ID | Guarded file | Logical change and consequence |
|---|---|---|
| RUN-G01 | `designs/principles.md`, principle 5 | Permit direct native Langfuse instrumentation at reviewed application boundaries while centralizing configuration/resource policy; no required provider-neutral tracing facade. Agent execution adapters and all other integration boundaries remain |
| RUN-G02 | `designs/architecture.md` | Replace mandatory neutral observation/exporter path for this tracing phase with native SDK scope/propagation and Langfuse setup. Add selected lifetime/error/payload policy; preserve CrewAI scheduling, safe data, workflow outcomes and deferred logging |
| RUN-G03 | `designs/project-structure.md` | Reconcile observability ownership and exporter-only dependency rule; list approved runner/assembly/native adapter imports and small lifecycle functions. Do not move context, add brokers or permit backend imports throughout workflow business code |
| RUN-G04 | Root `AGENTS.md`, engineering integration rule | Add the same narrow reviewed native-tracing exception so agent instructions do not contradict the target. All guarded-change, secrets, quality and sandbox rules remain |
| RUN-G05 | `designs/stages/02-langfuse/architecture.md` | Add combined native client/root/propagation and automatic CrewAI instrumentation ownership, replacing any remaining handle-in-context placeholder; preserve M1–M3 setup/checker/mock contracts and evidence |
| RUN-G06 | `designs/stages/02-langfuse/milestones.md` | Record the accepted combined runner + automatic CrewAI milestone separately from completed context; distinguish design, implementation, live verification and user acceptance; no stage renumbering |
| RUN-G07 | `designs/refactors/workflow-contract/implementation-plan.md`, dated Langfuse handoff amendment | Supersede obsolete requirements for context-held clients, required per-phase observation events and an outer trace covering pre-context configuration/selection. Explain the selected one-scope/post-context boundary and preserved errors; retain the original historical handoff |
| RUN-G08 | `designs/governance/guarded-files.md` | Only after approval, register these three M4.2 documents with exact approval reference/revision. Preserve every existing guard |

No change to charter, roadmap stage order or design-contract procedure is proposed. M4.1 design/test/plan and CTX acceptance remain its own baseline. A genuine context defect is reported to root for a separate authorized follow-up; it is not repaired in this draft or hidden in a runner PR. No genuine M4.1 contract blocker has been established from the inspected inputs.



## 11. Review and handoff

Before implementation, confirm the minimal failure/initialization placement above against current main, approve the exact design/test/plan revision and the applicable RUN-G amendments. Approval of consolidation is not approval of those unseen file changes.

Use [Codex handover rules](../../../../governance/codex-handover-rules.md). One combined implementation PR; two independently testable acceptance sections (runner and CrewAI). Keep documentation PR #47 open until all covered implementation is merged and Sharon separately authorizes it.

Sources: [official CrewAI integration](https://langfuse.com/integrations/frameworks/crewai), [native instrumentation](https://langfuse.com/docs/observability/sdk/instrumentation), [metadata](https://langfuse.com/docs/observability/features/metadata), [Python API](https://python.reference.langfuse.com/langfuse), and the pinned research above.

## LOG-G03 — Stage 02 tracing follow-on for logging M2, 2026-11-16

This dated amendment does not rewrite the approved Stage 02 tracing implementation. During logging M2, operational Langfuse initialization, observation scope entry/update/exit and flush faults must be narrowly contained: issue a safe terminal warning and preserve the business workflow result or original exception. Disabled tracing skips initialization. Invalid configuration and missing required credential references retain existing validation errors. Preserve native SDK scopes, CrewAI instrumentation and capture; do not wrap them in a generic observability broker. Refer to logging M2 LG-05/06/08 for acceptance.
