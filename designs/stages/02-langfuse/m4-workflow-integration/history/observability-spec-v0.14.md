# Historical specification — superseded

This retained v0.14 text is history, including its former statuses and questions. Use [current requirements](../requirements.md) and [decisions](../decisions.md). The broker was removed by D11; this appendix must not be implemented as a current contract.

# Agent Playbook — context, tracing and logging specification

Version: 0.14 · 2026-11-14 · Sharon
Status: **Broker necessity and provider isolation reopened (Q21 / section 26). No removal or new SDK-access policy selected. Tracing capabilities and context isolation retained; local logging deferred.**

## 1. Purpose and authority

**Iteration 16 review takes precedence for architecture:** Sharon asks whether the Langfuse-only phase needs any broker. Section 26 compares direct SDK use, narrow helpers and a provider-neutral facade. Existing broker/provider-isolation decisions are explicitly under review; the recommendation to omit the broker is not approved. Historical sections below must not be used to implement either side before resolving Q21.

**Current scope — iteration 11 takes precedence:** implement no new application logging in the first delivery. Design only a small application-owned broker that calls Langfuse tracing, with the required execution context. Earlier logging requirements/capability assessments remain future reference, not first-delivery gates. Section 21 records this explicit scope change; sections 19–20 are historical/unapproved proposals where they imply abstract broker layers or current dual-destination routing.

Provide correlated Langfuse observations and local application logs through one application-owned access boundary. Workflows, their steps and eventual agents should use the correct execution scope without copying identifiers into every reporting call.

Sharon approved the A–D classification and assessment criteria and requested this specification on 2026-11-14. Existing agreed requirements are preserved below. The decomposition, proposed acceptance details, estimates and new architecture options are review material; they are not silently promoted to approved design.

The living instruction/decision record is [agent-playbook-context-discussion.md](context-discussion.md). Update that record for every discussion iteration. Keep requirements here and the discussion/approval history there, with explicit reconciliation if either changes.

**Iteration 8 decisions:** use ExecutionContext, ObservabilityContext, ObservabilityBroker, LogRecord, workflow_run_id and agent_run_id. Keep one combined logging/tracing ObservabilityContext inside ExecutionContext. Names are accepted; representation, exact fields and APIs are not. Agent lifetime/pooling/invocation-holder decisions belong to later agent-adapter coordination and must not block the next schema discussion. Current examples use the selected names; earlier discussion history remains in the decision record.

**Iteration 9 decisions/direction:** span identity is retained and its mechanics belong to the supported tracing SDK/integration. Public field exposure is still a schema choice. Sharon requests a proposed dependency order and one decision at a time; section 19 begins with responsibilities/representation, then moves to broker contract before the complete schema and implementation.

Implementation starts **after PR #36 merges**, using its actual merged version and validation fixes. The latest metadata check still reports PR #36 draft/open/unmerged at 63f6503f38bc6a3ec45b4b750450a9001c6d013e, based on main 9e4640145e3ab7cf361bc890ffd22180bc365968. Those are dated inspection points, not frozen implementation inputs.

The workflow ABC already owns prepare, execute, validate_output and serialize_output. CrewAI owns steps and routing. A general context is not implemented. Langfuse setup/configuration/mock verification remains with the other session.

## 2. Scope and pass/fail constraints

### Agreed constraints

**Scope qualification:** logging/storage/viewer constraints below remain agreed for a future logging addition. Constraint 16's trace-to-log mirroring is expressly deferred. They must not reintroduce logging or generic routing work into the current Langfuse-only scope.

1. New application logging runs in the Python application, entirely locally. It requires no separate logging collector, database server or other service.
2. Local logging works without an open viewer or a live tracing backend. The existing self-hosted Langfuse stack is an accepted tracing dependency, not a logging prerequisite.
3. New logging/viewer dependencies must offer Apache 2.0 licensing. Langfuse remains the accepted licensing exception.
4. Application code uses an owned broker/facade covering logging and tracing. Logger and tracing implementations remain separately replaceable; provider-specific types stay inside adapters. **Reopened for Langfuse in iteration 16 (D04/R15); no silent change to this rule. Future local logging boundaries remain agreed.**
5. The viewer is separately replaceable. JSONL is welcome; embedded SQLite remains an alternative. Storage and viewer are not selected.
6. One workflow invocation has its own run identity and scope. Workflow, run and trace identifiers have different meanings.
7. Agent fields apply inside that agent and its nested calls, and do not appear in the parent workflow after return or in a sibling agent.
8. Runtime handles remain outside workflow business state. Secrets and raw private configuration are excluded from telemetry.
9. Preserve existing lifecycle guards, result validation, error categories, CrewAI orchestration, configuration order and strict typing.
10. Do not introduce real agent SDK integration, child-workflow orchestration, automatic retry/durable recovery, a network event broker or a custom logging platform as hidden prerequisites. Observability must correctly represent a fallback performed by workflow business logic.
11. Use one general context with a scoped observability access point. Derive an agent's context without changing the workflow's context; do not deep-copy shared backend resources.
12. Support distinguishing separate invocations of the same agent type. Nested methods belonging to one invocation keep that invocation identity; exact field name/generation remains open.
13. Failures can be reported at the current agent/workflow/operation scope. If agent B's failure makes the workflow fail, both operation outcomes must be inspectable with their causal relation; agent A's earlier success remains success.
14. An error-level diagnostic log may remain entirely local. Logging it must not by itself create an error observation, change a span's failure status, or make the agent/workflow fail. Diagnostic logging and operation failure reporting have separate semantics behind the shared broker.
15. A failed observed child and a successfully recovered workflow can have different outcomes. Preserve the child's failure and the workflow's actual final result; a child error must not mechanically determine the parent's outcome.
16. Trace operations also produce corresponding local logs; log-only operations produce no Langfuse observation. One trace reporting operation handles both destinations without callers manually duplicating it. Exact lifecycle/record mapping and automatic-instrumentation coverage remain to be defined.

### First delivery scope — narrowed by Sharon in iteration 11

Use a minimal ObservabilityBroker to call Langfuse tracing. Local logging, LogRecord implementation, storage, viewer, log-only APIs and trace-to-log mirroring are deferred. Keep the accepted execution-context composition, identifiers and scope isolation; exact fields, wiring, API and focused acceptance scenarios still require design agreement. No implementation is authorized by this scope decision.

Real agent runtimes, broad framework/stdout/subprocess capture, distributed propagation and advanced features remain outside this delivery. The context must be usable from the application entry boundary, not depend on CLI-only initialization. Preserve existing application/provider boundaries without introducing a generic backend-replacement framework.

## 3. Agreed classification and assessment

| Class | Definition | Treatment |
| --- | --- | --- |
| A — Essential to operate | Required for a block to produce a usable trace or persist a log record. | Mandatory for that block's first working version. |
| B — Essential for Agent Playbook | Required by our agreed behavior, correctness or robustness, although a bare integration could work without it. | Mandatory for project acceptance. |
| C — Small preparation worth doing now | Limited work avoids credible, materially larger future changes for an identified scenario. | Include only after establishing the benefit and small cost. |
| D — Useful later | Valuable but can wait without an expensive rewrite, or need is uncertain. | Defer explicitly and retain its trigger. |

Constraints in section 2 are pass/fail, not weighted scores.

For each capability record: destination, outcome/omission consequence, class and approval status, implementation/testing/maintenance effort, runtime/operational risk, cost of deferral, and an observable acceptance example.

Estimates below are qualitative judgments about additional work beyond the merged PR #36 foundation, not benchmarks, deadlines or additive totals. S = contained work; M = several lifecycle/adapter interactions; L = broad integration work. Effort and maintenance are shown separately. Classification assignments and acceptance details below are proposed; the underlying user requirements remain agreed.

## 4. Identity and scope examples

The same workflow can run twice inside one trace:

| Activity | workflow_id | workflow_run_id | trace_id |
| --- | --- | --- | --- |
| First invocation of WF-A | WF-A | R1 | T1 |
| Second invocation of WF-A | WF-A | R2 | T1 |

Without workflow_run_id these invocations cannot be distinguished by workflow_id plus trace_id. This is why separate workflow_run_id remains agreed. It does not require implementing child workflows now.

Entering an agent does not create a new workflow run:

| Location in run R1 | Inherited identity | Agent fields |
| --- | --- | --- |
| Workflow | WF-A / R1 / T1 | None active |
| Agent A and its nested methods | WF-A / R1 / T1 | Agent A |
| Workflow after A returns | WF-A / R1 / T1 | None active |
| Agent B and its nested methods | WF-A / R1 / T1 | Agent B |

Observation/span identity may differ within a run. Its precise exposure and lookup timing remain open. Tracing-disabled mode must not pretend that a stored correlation value proves a remotely persisted trace.

Agent-invocation distinction is also required. Three reviewer calls within R1/T1 have the same agent type but distinct invocation identities (illustratively AR1, AR2, AR3). Utility methods within AR1 keep AR1. agent_run_id is the selected name; its generation and relationship to an observation ID are undecided. Design support is required now, while real agent execution stays later.

## 5. Shared capabilities — both tracing and logging

### SH-01 — Consistent identity and queryable metadata · B

- **Outcome / omission:** attach workflow/run correlation and, when a real tracing scope exists, its actual trace/span correlation. Otherwise cross-linking can point to another invocation or the wrong observation. Preserve agent type and distinguish agent invocations where applicable.
- **Basis:** agreed D01, R03 and inspection behavior. Exact field schema, optionality and ID creation rules remain open.
- **Effort / maintenance:** M / S. Identity creation, binding and exporter mapping must agree.
- **Runtime / risk:** small metadata per record; stale span identity and caller overrides are the principal correctness risks.
- **Deferral cost:** high if callers or persisted records already use incompatible identifiers.
- **Acceptance:** two invocations of WF-A in one trace produce distinct run IDs; records correlate to their own observations. Three synthetic reviewer invocations can be distinguished, while each one's nested utility calls retain its identity, including local-only reporting with tracing disabled.

### SH-02 — Scope inheritance and isolation · B

- **Outcome / omission:** nested calls inherit the current workflow/agent information; agent fields do not contaminate parent, sibling or unrelated scopes. Wrong attribution defeats debugging.
- **Basis:** explicitly agreed R04 and accepted AD-01 derived scopes; return-after-exception and concurrent-scope cases are proposed acceptance refinements.
- **Effort / maintenance:** M / M. Ordinary calls are simpler than execution-boundary crossings.
- **Runtime / risk:** small scope metadata/handles; accidental shared mutation or unbalanced active-scope restoration.
- **Deferral cost:** high because scope ownership affects all callers.
- **Acceptance:** workflow → A → nested helper → workflow → B produces the identity table above, including when A raises an error. Two supported independent runs do not share agent fields.

### SH-03 — One owned access boundary, replaceable destinations · B

**Iteration 16 qualification:** this previously agreed architecture requirement is reopened for tracing. Its classification/acceptance example must be revised if direct Langfuse access is selected. It is not a technical prerequisite for tracing to work. Future local logger replacement remains required.

- **Outcome / omission:** runner, workflow and agent code use our common reporting access. Replacing the logger or tracing adapter must not require rewriting workflow reporting calls.
- **Basis:** agreed R15, D02–D05. One boundary does not require identical log/trace records or indiscriminate fan-out.
- **Effort / maintenance:** M / M. A small contract is cheaper than a generic event platform.
- **Runtime / risk:** one local dispatch layer; over-broad interfaces and backend-type leakage create maintenance cost.
- **Deferral cost:** high once vendor calls are spread through workflows.
- **Acceptance:** substitute an independent recording adapter in a maintained fixture without changing workflow code or passing backend-specific objects.

### SH-04 — Safe, bounded reporting data · B

- **Outcome / omission:** export selected safe metadata/error details, excluding credentials and private configuration. Arbitrary dumps can leak data or create excessive payloads.
- **Basis:** secret exclusion is agreed R05 and repository policy. Payload limits and the precise permitted-value rules are proposed details.
- **Effort / maintenance:** M / M. Common rules and adapter constraints need alignment.
- **Runtime / risk:** processing cost scales with payload size; exception messages can contain private values too.
- **Deferral cost:** high once unsafe records are stored; schema changes can also affect viewers.
- **Acceptance:** fixtures containing sentinel secrets in configuration and exception messages emit no sentinel. Non-serializable or oversized fields have defined behavior without bypassing the reporting policy.

### SH-05 — Errors visible in both destinations without changing workflow semantics · B

- **Outcome / omission:** an application failure can be represented in local logs and Langfuse using consistent identity. Preserve its cause and current workflow failure classification; avoid accidental duplicate recording at every catch/rethrow boundary.
- **Basis:** agreed R14/R17/R18 and existing workflow contract. Operation failures can be reported at the active operation's own level; no requirement to return to the workflow before reporting. Ordinary error-level log messages can stay local and do not trigger this failure path. Exact call API, sanitization and duplicate policy remain open; see proposed AD-02.
- **Effort / maintenance:** M / M. Failures can occur during preparation, execution, output validation or serialization.
- **Runtime / risk:** error formatting/export overhead; replacing the original exception with a telemetry error or over-reporting one failure.
- **Deferral cost:** M–high because later corrections can touch many exception boundaries.
- **Acceptance:** a controlled failure identifies its phase and relevant failed scope in both destinations when available, while existing CLI exit categories and causal chains remain correct. Legitimate parent failure summaries are distinguished from duplicate exception records.

### SH-06 — Explicit outage, disabled-mode and shutdown behavior · B

- **Outcome / omission:** logging remains available without Langfuse; resources have an owner and bounded cleanup/export behavior. No hidden reliance on an open viewer. Outages must not be mislabeled as successful delivery.
- **Basis:** logging independence is agreed R08; the repository requires an explicit telemetry-outage policy before acceptance. Fail-open versus fail-closed workflow policy is NOT decided.
- **Effort / maintenance:** M / M. Buffering, local write failure and process exit interact.
- **Runtime / risk:** disk writes and buffered export consume resources; shutdown may wait for local I/O or network. Bound waits and memory according to a later agreed policy.
- **Deferral cost:** high if resource ownership is already embedded in per-run objects.
- **Acceptance:** exercise disabled tracing, stopped Langfuse, an unwritable log target and normal exit. Each reports the defined outcome without deadlock, misleading success or losing the original workflow error. Crash-proof durability is not promised.

### SH-07 — Preserve workflow and entry-point contracts · B

- **Outcome / omission:** use the existing ABC lifecycle and application entry boundary. Observability must not become another scheduler or require CLI-only setup.
- **Basis:** agreed R01/R02 and accepted repository constraints.
- **Effort / maintenance:** M / S. Includes integration with current runner/wrappers and regression checks.
- **Runtime / risk:** accidental eager framework initialization, extra business execution or premature completion status.
- **Deferral cost:** high if the first integration bypasses the ABC.
- **Acceptance:** real maintained WF-01/02/03 cases retain results, routing and failure categories; a normal Python application invocation gets the same correlation behavior as CLI execution.

### SH-08 — Defined propagation boundary · B

- **Outcome / omission:** every execution boundary supported in the first release preserves the right scope, including any boundary the current CrewAI path actually uses. Unsupported thread/process transfers must not be implied to work.
- **Basis:** agreed propagation requirement; exact supported concurrency/process scope remains open.
- **Effort / maintenance:** M / M for a bounded first-release scope; broad cross-process support is L and later.
- **Runtime / risk:** copied metadata is cheap; serialization, task inheritance and worker reuse can misattribute observations.
- **Deferral cost:** high for boundaries used immediately; lower for explicitly excluded future boundaries.
- **Acceptance:** inspect and exercise the actual pinned runtime call path, then test the supported boundary. No claim of process propagation based only on an ordinary nested-call test.

## 6. Langfuse capabilities

### LF-01 — Configured local export · A

- **Outcome / omission:** use the existing local endpoint/project configuration and reusable integration to submit observations. A wrong endpoint/key prevents useful traces.
- **Basis:** basic integration necessity; reuse PR #36 rather than redesign deployment/authentication.
- **Effort / maintenance:** S–M / S, depending on merged adapter API.
- **Runtime / risk:** local network/export work; accidental cloud-default fallback or invalid authentication.
- **Deferral cost:** blocking; real traces cannot be accepted without it.
- **Acceptance:** real workflow observations reach the configured local project. Disabled mode requires no keys or export network activity.

### LF-02 — Observations with a bounded lifetime · A

- **Outcome / omission:** create, update as needed and finish observations with meaningful identity/name and timing. Unfinished or disconnected observations give incomplete execution evidence.
- **Basis:** technical necessity; exact provider-neutral operations remain a design decision.
- **Effort / maintenance:** M / S.
- **Runtime / risk:** observation count and export volume; missing end operations on exceptional paths.
- **Deferral cost:** blocking for dependable workflow tracing.
- **Acceptance:** successful and failed real workflow invocations produce finished observations with coherent duration and outcome.

### LF-03 — Workflow/step hierarchy and meaningful completion · B

- **Outcome / omission:** represent the workflow and its executed steps with correct parentage. Do not declare the overall application run complete merely because kickoff returned if validation/serialization later fails.
- **Basis:** accepted workflow lifecycle plus the desired run/step/error inspection. Exact observation granularity is open.
- **Effort / maintenance:** M / M.
- **Runtime / risk:** more observations; duplicate instrumentation, missing parents or false success.
- **Deferral cost:** M–high if callers establish inconsistent parent relationships.
- **Acceptance:** inspect real WF-02 success and a controlled failure; a later validation/serialization failure is reflected in the chosen run-level representation. No observation claims unexecuted downstream business work completed.

### LF-04 — Honest verification of ingestion · B

- **Outcome / omission:** acceptance demonstrates visible persisted observations; an SDK call or constructed trace URL alone is insufficient evidence.
- **Basis:** existing PR #36 verification distinction, reused for real workflows.
- **Effort / maintenance:** S–M / S.
- **Runtime / risk:** bounded read-back/UI checks during verification, not a proposed query after every application log.
- **Deferral cost:** M; missing export could go unnoticed.
- **Acceptance:** an explicit live check or user UI inspection finds the expected roots/children/outcomes. Keep offline application tests independent of the running service.

## 7. Local logger capabilities

### LG-01 — Persist inspectable local records · A

- **Outcome / omission:** record application diagnostics locally and read them after execution and after reopening the viewer. Ephemeral console output alone does not satisfy this task.
- **Basis:** agreed local storage and later inspection; backend/file layout remains open.
- **Effort / maintenance:** S–M / S with existing storage/output tooling.
- **Runtime / risk:** serialization/disk I/O and disk exhaustion. No required collector or database server.
- **Deferral cost:** blocking for useful saved logs; storage format affects later readers.
- **Acceptance:** run the application with the viewer closed and Langfuse stopped, then inspect saved records using the selected supported reading path.

### LG-02 — Structured messages, severity and filtering · B

- **Outcome / omission:** preserve timestamps, severity, useful messages/errors and structured correlation fields. Users can distinguish workflows, invocations and applicable agent types.
- **Basis:** agreed inspection requirements. Exact field names/types and severity/filter defaults remain open.
- **Effort / maintenance:** S–M / S.
- **Runtime / risk:** per-record formatting and volume; dynamic fields can collide with reserved identity.
- **Deferral cost:** high once inconsistent records accumulate.
- **Acceptance:** query/filter records for WF-A across runs, WF-A plus coder, and a selected run/trace. This checks the data contract, not a commitment to implement a new UI or persistent index now.

### LG-03 — Predictable file/storage lifetime · B

- **Outcome / omission:** define the output destination, initialization/close behavior and handling of unwritable/full storage. Decide rotation/retention rather than leave unbounded growth implicit.
- **Basis:** previously recorded open operational requirements. Specific rotation, retention and buffering settings are proposed design work, not chosen here.
- **Effort / maintenance:** S–M / S using existing facilities.
- **Runtime / risk:** disk usage, rotation contention and cleanup blocking.
- **Deferral cost:** M; a contained handler change is possible, but changing layout affects tools/users.
- **Acceptance:** exercise the chosen write-failure behavior and, if rotation is selected, verify record availability across a rollover without requiring another service.

## 8. Small future preparation — C candidates

Each item below is a proposal. Reject it if its implementation cost is no longer small or its future benefit is vague.

| ID / applies to | Candidate and future benefit | Effort / maintenance; runtime risk | Deferral cost and acceptance |
| --- | --- | --- | --- |
| C-01 / logger and future viewer | Identify record-schema compatibility, potentially with one version field, so later readers can recognize changed records. Exact mechanism open. | S / S; negligible field overhead. | Old unversioned records become ambiguous. Demonstrate that a reader can distinguish incompatible layouts. |
| C-02 / both | Keep scope/correlation data distinguishable from live runtime handles so a future process adapter can transfer only needed data. Do not build process transport now. | S if limited to clear ownership / S; no new runtime service. | Mixing clients and transferable data forces later contract surgery. Identify which fields are plain data without claiming all context is serializable. |
| C-03 / both | Keep additional agent/step metadata extensible within defined safe types and reserved-field rules. Do not add every future agent field now. | S–M / S; unchecked extension maps can defeat typing/redaction. | A new field could otherwise require changes in every caller. Demonstrate one harmless additional field without replacing core identity rules. |

Separate workflow_run_id and trace_id and replaceable adapters are already B requirements; do not downgrade them to optional future preparation or count their cost twice.

## 9. Useful later — D candidates and explicit deferrals

| Applies to | Capability | Why it can wait / revisit trigger |
| --- | --- | --- |
| Logger | Viewer selection/integration, indexes, query-before-load, rich clickable correlation | Logs and a stable readable schema can exist first. Revisit after core logging is accepted; viewer remains a product requirement, not canceled. |
| Logger | Comprehensive CrewAI/library capture plus stdout/subprocess capture | Ordinary application reporting works first. Assess framework logging separately; investigate earlier if missing logs block the first debugging scenarios. |
| Langfuse | Trace URL conveniences, rich input/output capture, token/cost metrics, evaluation features | Add when the workflow/model use case requires them; safe core metadata is sufficient initially. |
| Both | Actual child-workflow orchestration, distributed processes and real agent adapters | Identity compatibility is retained; execution features belong to their later scopes. |
| Both | Durable telemetry queues, replay, crash recovery, exactly-once guarantees | Significant persistence/reliability work, not implicit in local logging or SDK flushing. |
| Both | OpenLLMetry or other automatic instrumentation | Evaluate once manual correlation works and duplicate-observation/coverage tradeoffs can be measured. |

These deferrals are proposed delivery sequencing, not a blanket approval to omit existing requirements. A currently used runtime boundary that needs propagation belongs to SH-08, not this table.

## 10. Accepted context architecture decision

**AD-01 — How should context expose logging and tracing?**
Status: **Accepted by Sharon on 2026-11-14, iteration 4: option 2 plus derived scopes without parent mutation.**

We already require one owned access boundary. This choice concerns how callers reach it and how scope is represented.

| Option | Shape | Benefits | Costs |
| --- | --- | --- | --- |
| 1. Flat context | Context directly exposes correlation fields and reporting operations. | Few objects and short access paths. | General configuration/agent concerns can make the root object grow; identity and reporting need strong consistency rules. |
| 2. General context with one observability section | Context exposes one scoped observability access point containing reporting operations and the relevant correlation view. | Cohesive reporting/correlation; keeps a future general context organized; preserves one application boundary. | One extra object/access level. Unnecessary splitting would add complexity if allowed to expand unchecked. |
| 3. Separately passed contexts | Callers receive separate logging/tracing scope objects plus other runtime context. | Individual dependencies can be narrow. | More arguments and more coordination to keep IDs/scopes consistent; weaker fit for Sharon's requested consolidated access. |

**Selected: option 2**, with ExecutionContext containing one ObservabilityContext for logging and tracing. Do not split it into separate logging/tracing/identity contexts or create empty future agent/configuration sections now. Keep each shared field represented once. The illustrative access path is context.observability; exact property/API spelling remains open. The other architectural options above remain historical rationale. Future splitting is allowed when justified by a concrete use case.

**Also selected:** derive a new scoped context/view for an agent rather than alter the workflow's context and later remove fields. Agent A and B retain inherited workflow/run/trace identity, but each has its own agent metadata and observation scope. Backend resources may be shared through the broker; a derived view is not a new SDK client or file handle. A context with the same public type and a different object identity is a suitable illustration; exact concrete classes and construction APIs are still undecided.

This addresses SH-01, SH-02, SH-03 and future preparation C-02. Its main counterargument is simplicity: a flat context is sufficient if the general context stays small. Composition is worthwhile here because Sharon explicitly anticipates additional context responsibilities and wants reporting kept together. Avoid building a hierarchy of context classes without concrete responsibilities.

### Agreed behavior

1. The workflow keeps its original context throughout the run.
2. Agent A receives a derived context. Methods called as part of A use that scope, usually the same context reference unless a narrower operation needs its own metadata/observation.
3. Returning to workflow code uses the original context, which never acquired A's fields.
4. Agent B receives another derived context.
5. Active tracing observations still need correct enter/exit/finish behavior, including exceptions. Deriving an object alone does not solve SDK active-context restoration.
6. Explicit passing is shown for clarity in examples; the final propagation contract and any internal active-context mechanism remain separate decisions. No automatic propagation across threads/processes is claimed.

### Decisions deliberately still open

- ABC, Protocol or concrete class for the context and broker contracts.
- Exact fields, field ownership, mutability and override validation.
- Broker operations and which operations produce logs, observations or both.
- Runner/factory/ABC injection timing and pre-construction failures.
- Trace ID generation/reuse, active span lookup and disabled mode.
- Shared resource ownership, client reuse and shutdown.
- Outage/write-failure policy and duplicate error reporting.
- Logger/storage/viewer selection and retention.
- Supported async/thread/process propagation.

## 11. Review and acceptance path

AD-01 and the names in section 17 are accepted. Iteration 9 proposes first settling responsibilities/representation direction, then the broker contract and exact schema together, before placement/propagation and operational policies. Section 19 is the active proposal; section 18 retains the unresolved inventory. Agent lifetime stays outside this session's scope; the observability API must accommodate per-invocation context without prescribing execution architecture. AD-02's detailed mechanics remain open until needed before implementation.

Before implementation:
- Confirm the first-delivery boundary and proposed capability details.
- Refresh the actual merged PR #36 and affected governing documents.
- Resolve the relevant open policies; record explicit later-scope deferrals.
- Present logical guarded-file changes, if any, before editing them.
- Reuse maintained offline fixtures and explicit live verification. Do not inspect or depend on the personal examples sandbox.
- Preserve the deferred stale PR #40 design-header marker until its correction is authorized.

There is no claim of completed implementation, benchmark or passing new tests in this specification.

## 12. References and evidence limits

- [PR #36](https://github.com/SharonLanger/agent-playbook/pull/36) and its stage documents at the inspected head; the implementation base will be its eventual merge.
- [Workflow contract package at inspected main](https://github.com/SharonLanger/agent-playbook/tree/9e4640145e3ab7cf361bc890ffd22180bc365968/designs/refactors/workflow-contract).
- [Approved architecture at inspected main](https://github.com/SharonLanger/agent-playbook/blob/9e4640145e3ab7cf361bc890ffd22180bc365968/designs/architecture.md).
- [structlog bound loggers](https://www.structlog.org/en/stable/bound-loggers.html): derived bindings leave the original binding unchanged. This establishes a feasible implementation building block, not a dependency decision.
- [Langfuse instrumentation](https://langfuse.com/docs/observability/sdk/instrumentation): nested active observations support hierarchy; exact usage must match the merged project's pinned SDK.
- [Langfuse advanced features](https://langfuse.com/docs/observability/sdk/advanced-features): export filtering and thread/process propagation need attention; broader automatic instrumentation is not free compatibility.
- [Python contextvars](https://docs.python.org/3/library/contextvars.html): context-local values and restoration are another possible mechanism. It is not selected here. Current documentation can describe newer Python versions; use APIs supported by the project's pinned runtime.

The specification's proposed capabilities and effort judgments are engineering analysis. Source documentation does not approve our architecture or prove end-to-end compatibility.

## 13. Code illustration: child objects and nested methods

This is a proposed application API to explain accepted scope behavior. ExecutionContext is an accepted name; agent_scope and observability.info are illustrative methods, not implemented project or Langfuse APIs. This example chooses neither ABC versus Protocol nor an agent runtime lifetime and does not replace the existing runner/CrewAI scheduler.

A normal workflow step would invoke the agent using its existing workflow context:

```python
# Fragment inside a CrewAI workflow step, after context injection:
run_reviewer(self.context)
self.context.observability.info("Reviewer finished")
```

The agent invocation receives a child context and passes it to ordinary utility methods:

```python
def run_reviewer(workflow_ctx: ExecutionContext) -> None:
    with workflow_ctx.agent_scope("reviewer") as agent_ctx:
        assert agent_ctx is not workflow_ctx
        assert agent_ctx.observability is not workflow_ctx.observability
        agent_ctx.observability.info("Review started")
        inspect_files(agent_ctx)


def inspect_files(ctx: ExecutionContext) -> None:
    # Same scoped reference as run_reviewer received.
    # It still carries this reviewer's invocation identity.
    ctx.observability.info("Inspecting files")
    validate_patch(ctx)


def validate_patch(ctx: ExecutionContext) -> None:
    ctx.observability.info("Validating patch")
    # Work or an exception can happen here.
```

Proposed meaning of agent_scope: allocate a new context and scoped observability view, inherit workflow/run/trace correlation, assign one agent-invocation identity, and enter/finish its observation. Under AD-02 below, it would record an escaping failure and re-raise. Its exact API, observation lifecycle and error behavior are not yet approved.

- The outer context and scoped view are new objects. Read-only configuration and backend resources can remain shared references under their owner.
- This is not deepcopy of SDK clients, locks, buffers, file handlers or connection pools.
- inspect_files and validate_patch do not allocate another agent context or another agent-run ID merely because a method was called.
- If a helper deserves its own observed operation, it may derive a narrower operation scope retaining the same agent-invocation identity and using a child observation. Instrumentation granularity is a later decision.
- A call to another agent is a different invocation: it gets its own identity; parent observation relationships retain ancestry. Whether an additional explicit parent-agent ID is useful remains open.
- The workflow's original context retains no active-agent fields. A workflow failure summary can refer to agent B as a cause without changing the workflow's own scope into agent B's scope.
- If dataclasses are chosen, replace can create new outer/nested data objects while retaining unchanged referenced resources. A shallow copy of only the outer object would still share its nested mutable metadata and would not satisfy isolation. Frozen dataclasses do not recursively freeze mutable members.
- Copying data alone does not activate, finish or restore a tracing span or rebind a pre-existing bound logger. The eventual scope constructor must keep reporting identity and active observation consistent.

## 14. Error policy — AD-02 outcomes accepted, mechanics proposed

Status: **Required failure visibility, diagnostic-log separation and independent child/workflow outcomes are confirmed (R17–R19). Shared wrapper placement, detailed exception ownership and duplicate handling remain proposals. Iteration 6 deliberately parks further mechanics discussion while context fields are designed.**

### Terminology and observable behavior

A trace groups the overall operation. Workflow/agent/step work appears as related observations/spans inside it. Reporting an agent failure normally updates the agent's observation within that trace; it does not require a new independent trace.

Langfuse supports observation severity and a status message. Start/end time and duration belong to the observation's lifetime; optional progress records are separate. A successful observation is described as successful outcome here, not as a literal SUCCESS Langfuse level.

For the user example:

| Operation | Outcome | What the user should inspect |
| --- | --- | --- |
| Agent A | Completed successfully | Its inputs/metadata as permitted, timing and outcome. |
| Agent B | Failed | Safe error details at its failing scope, linked to its agent invocation. |
| Workflow 1 | Failed because B failed | A run-level failure summary and a cause reference to B's failed observation/invocation. |

This requires both an operation hierarchy and diagnostic exception information. A trace hierarchy is not a Python traceback. An exception traceback supplies available Python call frames; the cause chain preserves wrapped causes. Separate processes/remote runtimes require explicit causal correlation and any traceback supplied by that runtime, not an invented continuous Python stack.

### Recommended policy

1. Record a detailed, sanitized exception at the nearest relevant instrumented boundary whose operation failed. If an uninstrumented helper fails inside B, B owns that detail; if an independently instrumented tool is the originating failing operation, it can own it.
2. Use the current context at that scope. There is no requirement to ask the workflow to report the agent's error.
3. Permit one explicit operation-failure report to project that single origin report into local logging and a Langfuse representation. Ordinary diagnostic log operations do not automatically use this path. Intentional projection into two destinations is not an instruction to emit the full exception again at each caller.
4. Preserve and propagate application failures outside intentional business recovery. Merely logging an unhandled failure must not turn it into success. If adding domain-specific context to an exception, preserve its original cause.
5. Each enclosing operation that also fails gets a failure outcome and concise causal summary. Its own workflow/agent scope remains correct; a cause reference is additional metadata.
6. A successful earlier sibling remains successful. If the workflow handles the failure and succeeds through a valid fallback, its final outcome remains successful, while a distinct failed child attempt remains inspectable.
7. A handled internal exception that does not make the observed operation fail should not automatically mark that whole operation as failed. Diagnostic reporting and the operation's terminal result are related but distinct.
8. A logged error message alone does not establish that a workflow failed or that a Langfuse observation changed status. Define the broker's diagnostic-versus-failure operations explicitly.
9. Close observations and restore any active scope on success and exception paths. Application errors and reporting/export errors must remain distinguishable; the broader outage policy stays open.

The recommended implementation direction is centralized scope/lifecycle handling around meaningful boundaries, so workflow/agent authors do not repeat catch/log/re-raise in every helper. Explicit reporting remains useful for non-exception domain failures and controlled recovery. Exact methods/decorators/context managers are not selected.

### Clarification requested in iteration 5: logs, exceptions and operation failure

Central handling means one reusable in-process implementation around selected complete operations (for example, an agent invocation or the workflow lifecycle). It does not monitor log text/severity or wrap every utility method. No new service is introduced.

For a recoverable problem, business code retains its own recovery logic. Illustrative API names only:

```python
try:
    rules = load_optional_rules()
except FileNotFoundError:
    ctx.observability.log_error("Optional rules unavailable; using defaults")
    rules = DEFAULT_RULES

continue_review(rules)
```

If review completes successfully, the agent's observation remains successful. The log is local; no error observation is created by this logging call. This example deliberately uses error severity to make the independence clear; choosing severity remains a diagnostic policy.

A proposed shared execution wrapper would instead perform conceptual logic like this around the whole agent invocation:

```python
try:
    result = agent.execute(agent_ctx)
except Exception as error:
    report_agent_failure(agent_ctx, error)
    raise
else:
    report_agent_success(agent_ctx)
    return result
```

These names are explanatory pseudocode, not existing APIs. The example omits cleanup and reporting-error handling; it is not production code. A caught internal exception never reaches this wrapper if the agent recovered. A typed non-exception failure needs an explicit result contract; it is not inferred from normal return values or log messages.

The bare raise propagates the original application exception to the caller. It does not mean forwarding a log message. If the calling workflow also fails, its own boundary can record a failed workflow outcome and a concise cause reference. If it catches the agent failure and validly recovers, its outcome can remain successful. Parent summary means this enclosing operation's outcome, not a folder or an automatic duplicate of every log.

Reason for recommending a shared wrapper: reuse lifecycle reporting and cleanup, avoid missed failed spans, and avoid repeated full exception dumps. Tradeoff: automatic handling can be too broad unless operation boundaries and domain failure/result rules are explicit. The mechanism is still a proposal; R18's diagnostic separation is confirmed.

### Duplication, privacy and compatibility

OpenTelemetry's general recording-errors guidance discourages repeatedly recording the same propagated exception. It separately recommends error status for operations that fail. This supports detailed origin reporting plus parent outcome summaries; it does not forbid multiple parent operations from having failure status.

The application therefore needs an ownership/deduplication contract, not an assumption that wrapping every level in SDK defaults will produce the desired result. Automatic instrumentation may also record exceptions. Verify the pinned SDK behavior before combining it with our broker. There is no promise of exactly-once delivery.

The representation and UI visibility of traceback/cause details in the merged project's pinned Langfuse version still need a targeted check. Do not assume an OpenTelemetry exception event or local log is automatically displayed as a stack trace by Langfuse. The required information must be deliberately exported in a supported form with sanitization and size limits.

### Proposed acceptance examples

- A completes; B's nested utility raises; B is failed and workflow is failed with a cause reference. A stays successful.
- The origin diagnostic is not redundantly emitted at every stack frame; parent summaries are clearly different records.
- After an agent returns or raises, any later permitted workflow reporting uses workflow scope, not stale agent fields.
- Three invocations of reviewer have distinct identities, including two within the same workflow run.
- A workflow that successfully handles an agent failure is not falsely reported as a failed workflow.
- A recoverable internal problem emits a local error-level diagnostic, review succeeds, and no failure observation/status is produced from the log call alone.
- A business failure returned as a typed result is representable without manufacturing a Python exception.
- Safe traceback/cause details are inspectable where the selected Langfuse representation supports them and in local records; no cross-process traceback is fabricated.

### Sources checked 2026-11-14

- [Langfuse observation levels and status messages](https://langfuse.com/docs/observability/features/log-levels).
- [Langfuse nested observations](https://langfuse.com/docs/observability/sdk/instrumentation).
- [OpenTelemetry recording errors](https://opentelemetry.io/docs/specs/semconv/general/recording-errors/) — marked Development; used as engineering guidance.
- [Python 3.13 dataclass replacement](https://docs.python.org/3.13/library/dataclasses.html#dataclasses.replace).

These references support the conceptual distinctions. AD-02's exact handling mechanisms and APIs remain proposals; the outcome behavior identified at the beginning of this section is accepted.

## 15. Brief future-capability scan — iteration 6

Purpose: check for architectural blockers, not expand the first delivery. The feature descriptions below come from current official documentation checked on 2026-11-14. The proposed preparation is our engineering assessment, not a verified integration. Current documentation may describe a newer server/SDK than PR #36; exact feature availability and adapter calls must be checked against the eventual merged pins. This scan selects no cloud service, paid edition or external evaluator model. A later evaluator must respect the chosen local-only deployment/data requirements.

| Future capability | Langfuse capability | Proposed preparation now | Deferred work |
| --- | --- | --- | --- |
| Scores and feedback | Scores can describe a trace or an individual observation, including after execution. | Retain a stable provider-neutral reference to the actual trace/observation. A completed reference must remain usable as data without keeping its live context open. | Score schema, APIs, manual/automated scoring and delivery. |
| Evaluations and experiments | Evaluators assess selected outputs; dataset experiments compare executions. | Preserve operation identity/type and an optional path for safe inputs/outputs. Allow an existing parent tracing scope so an experiment runner need not become a disconnected trace. | Dataset integration, evaluation configuration, expected outputs and local evaluator choice. |
| Sessions | Sessions group multiple related traces. | Keep workflow_id, workflow_run_id and trace_id distinct; permit an optional session attribute later. Do not reuse workflow_id as a session ID. | When a session starts/ends and whether the product needs sessions at all. |
| Model usage and cost | Generation observations can carry model/usage details and reported or inferred costs. | Permit typed model-call observations under an agent, not just one generic agent-wide record. | Runtime adapters extracting usage and pricing policy; context does not manufacture missing metrics. |
| Prompt-version comparison | Prompt references can link generations to managed prompt versions. | Keep per-call reporting extensible through our boundary and permit a neutral prompt reference later. | Prompt-management adoption, resolution and adapter mapping; no Langfuse PromptClient in application context. |
| Filtering and dashboards | Stable names, tags and metadata help aggregate/filter activity. | Use stable operation names; keep run IDs and other changing values in structured fields. Treat scope attributes separately from per-record payloads. | Additional dimensions such as session/user/version, saved views and dashboards. |
| Nested/distributed work and optional instrumentation | Langfuse can join an existing trace using parent context; export filtering affects visible nesting. | Separate transferable identity from live resources; preserve parent relationships and coordinate automatic instrumentation with the broker. | Process transport, additional instrumentors and duplicate-ownership checks. |

Proposed small preparation (C), in addition to existing required identity/isolation: expose an immutable observation reference when available; keep names stable; permit bounded safe metadata with reserved identity fields. These have concrete uses above and should not become a speculative plugin framework. Adding each future capability remains D until selected. Correct local logging, scope identity and safe reporting remain B, not optional preparation.

Current official best-practice guidance emphasizes meaningful hierarchy, observation types, stable names, and useful input/output. Our inference: the chosen composed/derived context model has no identified structural blocker for the listed features if those properties survive the adapter boundary. Context copying alone neither implements those features nor proves their integration.

Masking must cover both destinations: Langfuse-side masking does not sanitize local files. Existing secret-exclusion requirements still apply before storage/export. Avoid automatic argument/context dumps.

References:
- https://langfuse.com/docs/observability/best-practices
- https://langfuse.com/docs/evaluation/scores/overview
- https://langfuse.com/docs/evaluation/experiments/data-model
- https://langfuse.com/docs/observability/features/sessions
- https://langfuse.com/docs/observability/features/token-and-cost-tracking
- https://langfuse.com/docs/prompt-management/features/link-to-traces
- https://langfuse.com/docs/observability/sdk/instrumentation
- https://langfuse.com/docs/observability/sdk/advanced-features
- https://langfuse.com/docs/observability/features/masking

## 16. Proposed context field and ownership inventory

Status: **Class/concept names accepted; field inventory, types, signatures and representation still proposed.** Start with one ObservabilityContext inside ExecutionContext. Keep shared correlation data there once; no extra identity-context class or separate logging/tracing contexts are required. The table is a field discussion, not a class/file-per-row design.

### Core data and access

| Field/concept | Proposed availability and owner | Derivation rule |
| --- | --- | --- |
| workflow_id | Required on a workflow-run context; configured workflow identity. | Retain for steps/agents. A separately invoked child workflow uses its own workflow identity. |
| workflow_run_id | Selected name for workflow invocation identity; created at the invocation boundary. Exact type/generation still open. | Retain within that invocation. A child workflow receives a new workflow invocation ID even if it shares the trace. |
| trace_id; internal observation identity includes span_id | Correlate to the actual trace/observation when it exists. Public span_id exposure, reference type and inclusion in local records are undecided. The adapter can manage span details internally. | Retain trace identity within the same trace and obtain each child observation's real span identity. Workflow/agent run IDs alone do not distinguish operations within the same agent invocation. Incoming-parent/disabled policies remain open. |
| operation name and kind | Defined when creating an observed scope; stable name and category such as workflow, step, agent, tool or model call. | Derive for a new observed operation. Do not derive merely because a Python helper is called. Exact supported categories and mappings remain open. |
| step_id / step name | Optional, only when a defined workflow step supplies that identity. | Inherit while executing inside that step. Naming/generation still open; do not confuse definition identity with one step attempt. |
| agent_type + agent_run_id | Agent invocation scope; agent_run_id name selected. Exact type/optionality rules remain open. | Retain for that agent's ordinary nested methods; replace for a new agent invocation. ID generation and relation to spans remain open. |
| safe scope attributes | Proposed bounded read-only values, separate from reserved identity and one-off log fields. | Derive additions/overrides without changing parent/sibling values. Reject reserved-ID overrides; exact safe value types and override rules remain open. |
| observability | Project-owned scoped access object for correlated logs and observations. Backend clients/handlers stay behind it. | New scoped view for a new scope; underlying resources may be reused under their chosen owner. It must bind the same identity shown by context data. |
| relevant configuration access | Existing requirement, but contents and access path remain unresolved. | Share a safe read-only view where appropriate. Do not expose credentials or treat the entire configuration as telemetry. Avoid an empty placeholder config hierarchy. |

Optional future dimensions include session_id, a safe user identifier, workflow/application version, tags and experiment correlation. They do not all become required constructor arguments now. Environment should reuse existing application configuration rather than introduce a second conflicting setting. Session identity groups related traces and is independent of a workflow definition.

### What is not inherited context state

Scores, output payloads, token usage, monetary cost, error details and terminal outcomes are reports about an operation. They should be passed to the broker when needed, associated with the proper reference, and not accumulated in a shared mutable bag copied into every child. Neither full inputs/outputs nor the exception traceback belongs in automatically propagated context metadata. Actual API names remain open.

A later scoring operation should be able to use a retained observation reference after a scope closes; it must not need to mutate or resurrect that scope. Parent failure reporting may refer to a child's identity as a cause without replacing the parent's own identity.

### Isolation and return behavior

1. The workflow retains its original context.
2. An agent receives a distinct derived context and scoped reporting view, with inherited run correlation and its own agent/observation information.
3. Its ordinary helpers can receive that same child reference. A truly narrower observed operation may derive another scope.
4. On return, workflow code resumes using its original context. There is no copy-back, subtraction of agent fields or new parent copy.
5. Outcomes/results pass back through normal return/exception/result contracts. They do not depend on mutating ancestor contexts.
6. Parent/sibling isolation must cover nested attribute values, not only the outer object. A shallow copy with a shared mutable dictionary is insufficient. Shared clients/sinks can still perform normal reporting side effects; scope-data isolation does not imply side-effect-free resources.
7. The tracing adapter must enter/exit/restore the matching active SDK scope. A new Python object alone does not establish correct SDK parentage.

### Processes

A workflow invocation is an application operation, not a process-launch instruction. A fresh CLI invocation normally runs in a fresh Python process; another workflow called by a Python method may execute in the same process. Therefore isolation is a context contract even without multiprocessing.

If a future launcher uses another process, transfer only plain correlation/allowed metadata and create local reporting handles there. Correlation does not happen merely because both processes are on the same computer. Live SDK clients and file handlers are not a transferable/deep-copy context. Shared-file writing strategy and explicit worker propagation remain deferred, unless the actual merged runtime already uses such a boundary, in which case SH-08 requires addressing it in the first implementation.

### Next design decision

Review AD-04's responsibility/representation proposal in section 19 first, then broker operations and this exact field inventory together. Derivation, injection and resource ownership follow. No runtime code or dependencies are changed by this inventory.

## 17. Accepted names; schema open; agent lifetime deferred — AD-03

Status: **Names accepted in iteration 8. Schema/representation/source placement open. Agent lifetime options explicitly deferred, not selected.** Sharon prefers convenient properties, but another session is designing agent adapters. This observability effort must not prescribe their constructor, reusable object, invocation-holder or pool structure.

### Names accepted in iteration 8

| Responsibility | Selected name | Historical alternatives / remaining boundary |
| --- | --- | --- |
| General passed context | ExecutionContext | RuntimeContext is plausible but can sound process-wide; WorkflowContext is too narrow for agent/tool scope. |
| Shared logging/tracing section | ObservabilityContext | TelemetryContext is reasonable. TraceContext would understate local logging and can be confused with an OTel propagation carrier. |
| Owned reporting wrapper/interface | ObservabilityBroker | TelemetryReporter is a descriptive alternative. Do not imply an execution event bus by naming it EventBroker. |
| One persisted local diagnostic | LogRecord | LogEvent is possible, but could be confused with future agent-runtime/execution events. This is data, not the broker. |
| Workflow invocation identity | workflow_run_id | workflow_execution_id is clear but longer; workflow_invocation_id is precise but less familiar. The former unqualified name run_id is rejected. |
| Agent invocation identity | agent_run_id | Paired with workflow_run_id. The exact generation/reuse contract remains open. |

Keep one shared ObservabilityContext initially; do not create a separate identity record/context as a prerequisite. It holds the shared correlation fields once. Future non-telemetry context sections can be introduced for real use cases and can read those values without maintaining duplicate mutable IDs. The broker needs the observability information; receiving that narrow view versus a bound handle/full ExecutionContext remains an API choice. Only allowlisted safe information is projected into records.

### Schema and source ownership

Unselected options: concrete typed data objects can define fields and invariants; an abstract behavior contract can define replaceable reporting operations. Frozen dataclasses, ABCs and Protocols remain candidates. Sharon explicitly left these undecided in iteration 8. A choice of ABC does not eliminate the need for a concrete instance. Type hints/frozen dataclasses do not provide external-data validation or recursively freeze dictionaries. Keep the implementation small and select mechanisms only after the minimal schema is understood.

Reviewed current main on 2026-11-14: project-structure.md owns folder boundaries; workflows/contracts.py owns the existing guarded lifecycle. Proposed source locations below are relative to app/src/agent_playbook and are not existing-file claims:

| Proposed location | Ownership | Approval status |
| --- | --- | --- |
| context/models.py | General ExecutionContext composition, with no provider dependencies. | Candidate only; a new component would change approved folder responsibilities and needs design review before implementation. No extra identity component is selected. |
| observability/context.py | Scoped ObservabilityContext/view; common identity must not be independently duplicated. | Within the existing neutral observability boundary; detailed class dependencies still open. |
| observability/contracts.py and records.py | Broker behavior contract and typed LogRecord/observation-reference data. | Proposed files within an existing boundary. Do not add empty abstractions. |
| observability/adapters/ | Langfuse and selected logging backend implementations. | Existing ownership boundary; exact files depend on merged PR #36. |

Avoid placing the general context in the CLI or a Langfuse adapter. Putting it in application/ would make lower-level agents/workflows depend on the orchestration layer; a workflow-owned general context could also force agent execution contracts to import their callers. A neutral home is the current recommendation, with its structural cost explicit. No guarded repository files are edited by this proposal.

### Passing and retaining context: deferred alternatives

The table below preserves iteration 7 alternatives for the agent-adapter design. It is not a request to choose or implement agent lifetime machinery in the current observability iteration. Only per-invocation correlation/isolation and no forced SDK-client recreation constrain observability compatibility.

| Option | Advantages | Costs / conditions |
| --- | --- | --- |
| Fresh agent object per invocation, constructor receives context | Simple self.context; naturally matches invocation lifetime and isolation. | Repeated setup if expensive dependencies are built in that constructor. Sharing clients avoids much of that cost. Provider conversation state/reset is a separate decision. |
| Reuse agent; run(input, context) receives each invocation context | Few extra objects; context is explicit and naturally separate for concurrent calls. | More parameter passing to helpers. Other mutable agent/provider state must still support the intended reuse/concurrency. |
| Reuse agent runtime; fresh lightweight AgentExecution(context, runtime) per invocation | Keeps self.context convenience in execution code while allowing expensive runtime/client reuse. Each invocation owns its fields. | One additional lifetime/type to understand. Introduce only if it earns its place; do not build an agent framework for this context PR. |
| Reuse agent and replace agent.context before each call | Superficially small API and convenient properties. | Stale callbacks, nested/reentrant calls and overlaps can see another invocation's context. Strict sequential ownership/reset could constrain it, but this is not the recommended default. |

Historical recommendation, deferred in iteration 8: a fresh execution holder could preserve self.context convenience over a reusable runtime; passing context to run is another viable option. Neither is selected. The separate adapter design may choose either or another equivalent mechanism without changing the required correlation/isolation behavior. No agent lifecycle decision is needed before discussing the observability schema.

The inspected workflow factory constructs a fresh wrapper and the ABC enforces one lifecycle. The workflow holds its context; exact factory/ABC/flow signatures and timing remain open. Read-only public access is proposed, not selected, while keeping runtime handles outside serializable workflow state remains required. A wrapped CrewAI Flow does not automatically receive a wrapper property; propagation must be explicit in the final design.

For A → B → A, one reusable A runtime can serve two separate execution holders/contexts:

| Invocation | Runtime object | Agent invocation ID | Context |
| --- | --- | --- | --- |
| First A | A runtime | AR1 | A1 context |
| B | B runtime | BR1 | B1 context |
| Second A | Same A runtime, if supported | AR2 | A2 context |

None of these options requires creating a fresh SDK client or OS process for every invocation. Conversely, a fresh Python object does not guarantee a new external CLI session or cleared conversation memory. Runtime reusability, conversational continuity and concurrency safety require their own later adapter contract.

### Span and agent identity explanation

A trace identifies the overall operation. A span identifies one observed block within it; parent span references express nesting. One agent invocation may include its own span plus several tool/model spans, all retaining that agent invocation's identity. Logging a message does not require creating a new span. Thus span identity and agent invocation identity have different roles even if an implementation eventually reuses the agent-root span ID as the invocation's value. That choice stays open, especially with tracing disabled.

Independent shell launches of the normal CLI are fresh Python executions. The earlier same-process caveat concerned method calls from an already running process. Later, a common session ID could group separate traces from a CLI and subagents if their adapters explicitly report it; it does not automatically instrument subprocesses or join them into a single trace.

### Iteration 7 action list — superseded by section 18

1. Names were selected in iteration 8. Agent lifetime selection is now explicitly deferred to adapter coordination.
2. Define the typed context schema: required/optional fields, one identity owner, safe metadata types, derivation rules and read-only access; retain workflow and agent invocation distinction.
3. Define the broker's minimal behavior and record schema, separating local diagnostics, scoped observations and explicit operation failure reports without designing an event bus.
4. Review source placement and dependency direction, then the factory/runner/Workflow ABC/CrewAI injection path. Keep context and live resources out of recoverable business state.
5. Specify supported lifetime/propagation acceptance cases: A → B → A has distinct invocation identities; nested helpers inherit; parent remains unchanged; local-only logging still works; permitted overlaps do not mix contexts. Runtime provider concurrency is not established by these context tests.

## 18. Iteration 8 resolution and open actions

**Iteration 11 update:** logging-specific actions in this historical inventory are deferred. The current work is the small Langfuse broker and the context needed to use it; see section 21. Agent lifecycle remains deferred separately.

Resolved: ExecutionContext, ObservabilityContext, ObservabilityBroker, LogRecord, workflow_run_id and agent_run_id; one combined logging/tracing context initially; no EventBroker naming or mandatory future subdivision. Existing parent/child isolation, local logging independence, replaceable providers and recovery-outcome semantics remain unchanged.

| Action | Status / timing |
| --- | --- |
| Define the smallest ObservabilityContext schema: required/optional fields, safe types, step/agent fields and public span visibility. | Open; section 19 proposes responsibility/representation direction and broker call shape first, then finalizing fields and signatures together. |
| Choose concrete context/broker representation: ABC, Protocol, dataclass or a small combination. | First active proposal in section 19; no representation approved. |
| Choose source placement and create/inject/derive path through runner, factory, Workflow ABC and flow. | Open; workflow holds context, exact signature/lifetime boundaries remain to be defined. No new folder/file split selected. |
| Define ObservabilityBroker's minimal calls, context binding and LogRecord schema. | Open; decide whether it receives ObservabilityContext or a bound view. Avoid imposing the whole execution context on code needing only reporting data. |
| Define reporting resource ownership, disabled/outage behavior, shutdown/flush and local logging backend/storage. | Required before implementation acceptance; retain existing Q09/Q11/Q13. No service requirement may be introduced for local logs. |
| Coordinate agent runtime/instance/invocation lifetime, reuse/pooling and prompt/tool variation. | IMPORTANT DEFERRED item for agent-adapter design, before that API is finalized. Must not force new SDK clients or a particular AgentExecution class. Not a blocker for the next observability-schema iteration. |
| Detailed exception mechanics, broader instrumentation, viewer/dashboard/sessions and advanced evaluation delivery. | Deferred; retain prior requirements and triggers, including desired token usage. |

Span decision, accepted iteration 9: retain distinct span identity and use the supported tracing SDK/integration for identifiers, creation and parent/scope mechanics. Multiple model/tool calls inside one agent invocation share workflow_id, workflow_run_id, agent_run_id and trace_id, so that tuple does not distinguish their observations. Application integration still specifies which operations are observed; automatic coverage of every function/tool is not promised. Public span_id/reference exposure and local-record inclusion remain schema choices. Workflow authors must not have to hand-build spans or IDs.

Contradiction check: accepted names replace earlier candidates, not identity semantics. One combined context is consistent with AD-01 and supersedes only optional splitting proposals. Deferring agent lifetime removes premature implementation constraints while retaining per-invocation isolation. No agent lifecycle, schema, frozen/read-only implementation or ABC choice was inferred from tentative remarks. No repository code or guarded document was edited by this update.

Token usage is explicitly wanted; scores/evaluation are supported future directions. Sessions and dashboard work remain deferred. Core structured fields for log filtering remain required. This comparison does not authorize agent implementation, choose a logging dependency or resume detailed exception mechanics.

References checked in iteration 7:
- https://github.com/SharonLanger/agent-playbook/blob/main/designs/project-structure.md — inspected content blob 8f7f8422e9a5352d201d4c4cb00c56bb5f598e26.
- https://github.com/SharonLanger/agent-playbook/blob/main/app/src/agent_playbook/workflows/contracts.py — inspected content blob f032f6b588bea64346034feda55d3a50d2154ead.
- https://opentelemetry.io/docs/concepts/signals/traces/
- https://langfuse.com/docs/observability/features/sessions
- https://docs.python.org/3.13/library/dataclasses.html

## 19. Proposed decision order and first representation decision — AD-04

Status: **Historical proposal; not approved, parked in iteration 11.** The abstract broker and dual-output implementation are not the current recommendation. Prefer the small tracing-only direction in section 21; do not infer approval of concrete dataclasses, ABCs or forwarding methods. Accepted names/composition remain intact.

| Order | Decision | Why here |
| --- | --- | --- |
| 1 — current | Context versus broker responsibilities and representation direction. | Establish which objects hold scoped information and which contract must be replaceable. Do not define every field yet. |
| 2 | Minimal ObservabilityBroker operations, context binding and caller ergonomics. | Define what application code can report and which operations stay local or represent observed work. Avoid designing unused schema fields. |
| 3 | Exact ObservabilityContext and LogRecord fields/types/invariants; refine broker signatures with them. | Resolve optionality, safe values, IDs, span visibility and record serialization once the reporting use cases are explicit. |
| 4 | Source ownership and runner/factory/Workflow/flow creation, injection and child derivation. | Place the agreed types and wire their lifecycle while preserving current orchestration. |
| 5 | Select logging output/backend and settle reporting-resource ownership, failure/disabled/flush policies and acceptance cases. | Finish the operational contract before implementation and verification. Backend constraints discovered earlier may refine draft contracts. |

Agent runtime lifecycle, pooling, conversation reuse and constructor shape remain external coordination items. Their design cannot be a prerequisite to choosing the observability representation. No real agent implementation is added here.

### First proposal: concrete contexts, abstract broker contract

| Object | Proposed representation | Responsibility |
| --- | --- | --- |
| ExecutionContext | Concrete typed dataclass | Holds the selected ObservabilityContext and later only genuinely needed general-execution sections. |
| ObservabilityContext | Concrete typed dataclass/scoped object, with small forwarding methods | Holds current correlation fields once and a reference to our broker. Supplies convenient reporting access without importing a provider. |
| ObservabilityBroker | ABC with a concrete implementation behind it | Defines supported reporting operations; implementation delegates to replaceable tracing/logging adapters. |
| LogRecord | Concrete typed data record, dataclass candidate | Describes one emitted local log record; full schema belongs to step 3. |

Dataclasses generate field-oriented boilerplate and remain regular classes that can have methods. ABC abstract methods/properties define requirements for implementations. These mechanisms can coexist; choosing an ABC for behavior does not require making every data holder abstract. ABC plus concrete context implementations remains possible, but adds indirection without a current second context implementation to justify it. A broker Protocol is a viable alternative if structural typing becomes useful; ABC is the current recommendation for explicit inheritance and a required method contract.

This proposal preserves the accepted combined context. It does not introduce separate logging, tracing or identity contexts, another agent execution layer or a service.

Illustrative caller ergonomics only; method spelling is not approved:

```python
self.context.observability.info("Workflow started")
```

The ObservabilityContext supplies the current correlation and forwards reporting through the broker. The concrete broker/adapters handle formatting, persistence and SDK operations. There is no separate broker argument to every workflow helper, and no Langfuse/structlog client in workflow code. These forwarding methods must not reimplement serialization, export or exception policy in the context class.

On derivation, create a new scoped context with inherited/added fields while retaining the same broker reference where its owner allows. Do not deep-copy a client. Shared broker state must not be overwritten with a global "current run"; each reporting call/binding must carry its own correct scope. Exact binding APIs remain step 2.

Unresolved by AD-04: exact field schema, frozen/read-only settings, nested mutable-value rules, runtime validation, signatures, source files and startup/shutdown ownership. Parent isolation remains mandatory regardless of the selected representation; dataclass annotations alone do not guarantee it. Runtime handles must not be automatically serialized as context data.

The representation proposal remains: **concrete typed context objects and an ABC for ObservabilityBroker, with optional scoped forwarding access.** Iteration 10 pauses choosing it while the public behavior is explained. Forwarding methods are a convenience option; exact broker access/ownership remains unselected. Do not silently mark this proposal accepted.

Sources supporting Python mechanism descriptions, not the project recommendation:
- https://docs.python.org/3.13/library/dataclasses.html
- https://docs.python.org/3.13/library/abc.html

## 20. Trace-plus-log versus log-only — iteration 10 clarification

Status: **Deferred by D09 in iteration 11.** Preserve this desired routing for a later logging addition. None of the dual-output API, mirroring or instrumentation-projection work below belongs in the present Langfuse-only scope. Example APIs and context forwarding remain unselected.

| Intent | Local logging | Langfuse/tracing |
| --- | --- | --- |
| Log-only diagnostic | Write the diagnostic with current correlation. | No observation created/updated by this call. |
| Traced operation/report | Automatically produce corresponding correlated local records. | Record the observed operation through the tracing integration. |

The earlier self.context.observability.info(...) illustration assumed ObservabilityContext had a small method forwarding to our broker, using that object's correlation information. It was not the backend logger and did not imply trace creation. The object would hold a broker reference; its methods would be ordinary methods defined on the class, not copied broker implementations. A separate trace operation would have distinct routing semantics. This convenience is optional and has not been selected.

For explanation, show the broker explicitly. The following is proposed application pseudocode, not existing methods, Langfuse APIs or an injection decision:

```python
obs = context.observability

# Local diagnostic only.
broker.log(obs, "Cache miss", level="INFO")

# Observed operation plus corresponding local records.
with broker.trace_operation(obs, name="review"):
    review()
```

trace_operation here means an observed span inside the current trace; the entry boundary may establish a root trace. It does not mean every local message creates another independent trace. Context propagation into the body and exact yielded scope/handle are intentionally omitted until that API is designed. A lifecycle representation could produce start/completion/failure log records, but exact record count, update handling and safe payload fields remain open.

If forwarding syntax is later selected, an info method would delegate to the log-only broker operation and a distinctly named tracing method would delegate to the trace-plus-log operation. The method's intent determines routing, not whether it was reached through a context or broker property. Full ExecutionContext versus narrow ObservabilityContext arguments and the location of the broker reference are still decisions to make; the explicit example does not change accepted composition.

### Keep the implementation proportional

The broker has an immediate purpose: consistent scope and two different destination rules. Its justification does not depend only on a future Langfuse replacement. Use a small project-owned layer delegating to the existing tracing SDK and chosen local logging library. Preserve the agreed replacement boundary without building a generic event platform or abstract interface for every context.

Routing semantics belong to our integration contract; do not assume a Langfuse SDK call itself writes an application JSONL record. Local logging must remain independent of a live tracing backend. A local record can describe the observed operation/export attempt without asserting successful Langfuse ingestion. Detailed failure/delivery policy remains open, as previously required.

Automatic SDK/framework spans need an explicit projection path if enabled. Calls bypassing the broker are not magically intercepted; Q19 records the need to cover them or resolve the coverage boundary explicitly. This is not permission to silently exempt them from Sharon's desired trace-to-log correspondence. Avoid duplicate local records if both explicit and automatic instrumentation see the same operation. Do not mirror network retries as new business operations or copy sensitive payloads indiscriminately.

Proposed acceptance examples: a log-only INFO/ERROR call creates no observation; a traced operation produces a trace representation and correlated local record(s) without a second application log call; local diagnostics remain available with Langfuse stopped; tracing instrumentation coverage is documented and verified before claiming all traces are mirrored.

No class representation, forwarding API, automatic instrumentation package or backend is selected by this clarification. Agent runtime lifecycle and the existing deferred topics remain outside this iteration.

## 21. Langfuse-only broker — iteration 11

**Iteration 16:** Langfuse-only scope is retained; the broker itself and provider boundary are reopened in section 26. The accepted construction history below is not a new decision to retain the object after that review.

**Accepted scope (D09):** keep the broker extremely simple and have it call Langfuse tracing only for now. Defer local logging, log-only methods, trace-to-log mirroring, storage/viewer selection and LogRecord implementation. Earlier logging requirements remain future requirements; they are not current acceptance gates. This explicitly supersedes the previous combined first-delivery proposal and active R25 routing scope.

**Representation accepted in iteration 12 (D10):** one ordinary concrete ObservabilityBroker that delegates tracing to the existing Langfuse integration. Do not introduce an abstract broker plus implementation, context forwarding methods, generic plugin routing or speculative feature APIs now. Existing provider-specific code remains at its existing adapter boundary; the thin broker does not require moving SDK code into workflow classes or duplicating that adapter. Exact methods and module placement remain open.

### When the broker object is created

| Location of construction | When it runs | Consequence |
| --- | --- | --- |
| Module or class body | When the module executes or class is defined, ordinarily during import. | An instance created there can be shared; startup/configuration happens less explicitly. A class-body attribute is shared through that class. |
| Owning object's __init__ | Every time that owning object is constructed. | A broker created there has that owner's lifetime. Passing an existing broker into __init__ merely stores its reference, without constructing another broker. |
| Inside a method | Each time execution reaches the construction statement. | Repeated construction if the method is repeatedly called; unnecessary for each trace operation. |
| Application startup/assembly | Explicitly at the beginning of the CLI/script's application execution. | Create once and pass to the workflow constructor; selected by D10 in iteration 12. Exact cleanup policy remains open. |

Python supports class attributes and static methods. A static method is a calling convention; it does not eliminate initialization of configured reporting resources. There is no Python requirement to recreate the broker for each method or trace.

Minimal lifetime direction accepted in iteration 12: create one broker at command/script initialization, pass it to the workflow constructor and reuse that reference during execution. Individual operations have their own tracing scopes. Separate ordinary CLI launches create separate application objects. Whether reporting takes ObservabilityContext explicitly, exact constructor/method signatures and resource cleanup remain undecided. A reused broker must not hold an overwriteable global current workflow/agent context.

Retained: ExecutionContext containing one ObservabilityContext; derived scopes do not mutate parents or siblings; workflow_run_id/trace_id/span semantics; SDK-managed span mechanics; meaningful failure outcomes. No context schema/type, ABC, singleton/global-access policy, source file layout or agent runtime lifetime is selected by this iteration. The minimal tracing startup, failure and shutdown behavior still needs to be defined without resuming the deferred logging design.

## 22. CLI/script initialization and agent references — iteration 12

Startup is ordinary code at the beginning of an execution, not a persistent service, Spring-like container or Python-specific startup subsystem. A CLI command or script runs its entry function, initializes resources, executes the workflow, completes cleanup and exits. Compilation versus interpretation does not determine this lifetime. The existing self-hosted Langfuse backend is separate from the short-lived application broker.

The workflow stores a reference to the broker supplied by its constructor. Passing that reference onwards does not copy or recreate the broker. An in-process agent can use that same broker while receiving a distinct agent-invocation context derived from the workflow context. Sharing reporting machinery must not share mutable current-run/agent fields.

Illustrative argument passing only, not existing repository code or an approved agent API:

```python
# In the CLI/script's initialization code:
broker = ObservabilityBroker(...)
workflow = MyWorkflow(broker=broker, context=workflow_context)

# Later, inside the workflow:
agent = MyAgent(broker=self.broker)
agent.run(context=agent_context)
```

Here workflow_context and agent_context stand for the already-discussed scoped contexts; this snippet does not define their creation or bypass the workflow's existing prepare/execute lifecycle. The agent constructor/run signatures are an example of how reference passing works, not a constraint on agent reuse or the other session's adapter design. A reusable agent can retain a broker reference while each invocation receives its own correlation scope through the eventual agreed API.

The same-reference statement is limited to one Python process. An external agent CLI process cannot receive a live Python broker reference this way; its Python adapter may hold the broker and translate/report its events. Cross-process propagation stays deferred. No additional service, process-global singleton or per-agent SDK client initialization is implied.

Iteration 13 confirmation: Sharon explicitly agrees with this lifetime/reference-sharing explanation and requests the next design step. Exact agent constructor/run signatures remain examples owned by the separate agent design effort.

## 23. First tracing method — AD-05 proposal, iteration 13

**Status: initial proposal, refined in iteration 15 by section 25.** Its scoped lifecycle remains useful, but a generic span-only method is not the complete reporting contract. Typed agent/tool/model observations, point events and usage/output updates must be considered before finalizing the API. No new abstract interface or local logging method is required.

Proposed spelling: span(name, context=observability_context). It takes the ObservabilityContext already held inside ExecutionContext. The name is a stable operation label, such as prepare_document, rather than a dynamically generated invocation ID. The integration uses the correlation data; application callers do not reconstruct the IDs or import Langfuse.

Illustrative use inside workflow code, not a replacement for the existing workflow lifecycle:

```python
with self.broker.span(
    name="prepare_document",
    context=self.context.observability,
):
    prepared = prepare_document(document)
```

The Python with statement marks the beginning and end of the observed block. This is a tracing scope managed in the current process, not another broker instance, background service or new agent runtime.

### Proposed behavior

1. On entry, start the observed operation and establish its active SDK scope, using the relevant parent correlation and SDK-generated identity. The initial workflow observation can start a new trace; operations inside it are spans in that trace, not separate traces per call.
2. On normal exit, end the observation and report normal completion. An escaping application exception records this operation's failure and continues propagating to its caller. Do not swallow it, retry, or convert it to success. A caller that catches it outside this block and recovers can still succeed, preserving R19.
3. On exit, restore the enclosing SDK scope. Leave the supplied context object and its metadata unchanged. Shared broker resources must not hold an overwriteable global current workflow/agent field set.
4. For a caller that uses as, propose yielding a derived ObservabilityContext with the actual trace/span identity for this operation. The minimal example omits it because no descendant call needs correlation. Nested explicitly reported work must receive the correct child scope; a stale parent ID must not silently flatten the hierarchy. Exact returned fields, root initialization, parent precedence and recomposition into ExecutionContext remain part of the schema refinement.

Delegate span creation, active context and closure to the existing Langfuse integration. The broker supplies our context mapping and agreed behavior; it does not reimplement a tracing engine. Current documentation supports context-manager lifecycle and nesting, but the final implementation must use and verify the project's pinned SDK API. The proposed failure policy is a project contract, not a claim that every SDK default, cancellation or export failure already has the required behavior.

### Alternatives and recommendation

| Shape | Benefit | Tradeoff / recommendation |
| --- | --- | --- |
| with broker.span(...) | The observed block and automatic closure are visible together; works with explicit broker/context references. | Recommended first method. Exact parent/scope mapping still needs definition. |
| Separate start and end calls | Supports non-contiguous native events and lifetimes spanning multiple callbacks. | More caller bookkeeping/cleanup; retain for a concrete future adapter requirement rather than making every workflow manage it now. |
| Decorator on a method | Concise when the entire method is the observed operation. | Needs binding to the injected broker/context and a deliberate argument/output capture policy. Not selected or prohibited; optional future convenience. |

This proposal only defines the first lifecycle operation. Safe input/output updates, model usage, explicit failure results, shutdown/flush, telemetry outages and exact exception-detail ownership remain separate questions. No broad data capture, raw context serialization, new logging output or extra abstraction is included. Real agent loops and native event lifetimes remain with their adapter design; this block API does not constrain that later work.

Next refinement after this call shape: the smallest concrete context schema and its representation, including unstarted/root versus active trace/span correlation and deriving/restoring the right child context. Then confirm exact placement in the existing runner/factory/Workflow/flow paths and essential cleanup behavior. No file split or implementation is selected by the example.

Primary feasibility reference checked 2026-11-14: https://langfuse.com/docs/observability/sdk/instrumentation — context managers, decorators, manual observation lifecycle and nested scopes.

## 24. Expected failed-document trace — explanation, iteration 14

Status: teaching example of AD-05's proposed behavior, not an executed trace, final API or implementation approval. Assume the existing startup path supplies broker and initial_context. The outer block explicitly observes the workflow; the inner block observes document preparation. as workflow_obs uses the proposed derived ObservabilityContext return from section 23, whose concrete schema is still open.

```python
def prepare_document(document: str) -> str:
    text = document.strip()
    if not text:
        raise ValueError("Document is empty")
    return text


with broker.span(
    name="document_workflow",
    context=initial_context.observability,
) as workflow_obs:
    with broker.span(name="prepare_document", context=workflow_obs):
        prepared = prepare_document("   ")
```

prepare_document contains no tracing code and receives no span object. It raises an ordinary Python exception. Unwinding leaves the inner block first, then the outer block; the proposed broker reports each failed operation and preserves the application exception. No prepared result is returned. The original input context remains unchanged.

Expected observation content after successful export to Langfuse; layout and message formatting are illustrative:

| Observation | Parent | Ended? | Level | Illustrative status message |
| --- | --- | --- | --- | --- |
| document_workflow | None in this example | Yes | ERROR | ValueError: Document is empty |
| prepare_document | document_workflow | Yes | ERROR | ValueError: Document is empty |

Both observations belong to one trace, with different span identities. Their timings reflect their own boundaries. The repeated short error summary describes the same exception affecting two operation outcomes; this is not a choice to duplicate complete exception payloads. Exact traceback capture/rendering and error-detail ownership remain open. Without the explicit outer observation, the example would only create the observed preparation operation, not magically add a workflow span.

A span ends on both ordinary completion and ordinary exception unwinding. Failure is additional outcome/error information, not failure to close the span. Langfuse supports ERROR level and a status message. SDK export can be buffered/batched, so starting/ending an observation is not a promise of an immediate network message or live UI update; existing shutdown/export requirements still apply.

Recovery variant, preserving R19: if the workflow catches ValueError outside the inner with block but inside the outer one and completes a valid fallback, the preparation span remains ERROR while the workflow observation can end normally at DEFAULT level. DEFAULT expresses observation severity, not a universal success enum. The trace still contains an error; do not promise that all UI summaries turn green. If code catches the exception inside the preparation block, the exception no longer escapes that boundary and automatic scope-exit error handling cannot infer failure from it alone.

The actual broker/adapter must map the agreed error behavior using the pinned SDK. This example does not certify default SDK exception handling or authorize full workflow-context serialization. The current request asks for the general trace representation, not a live Langfuse run.

Official references checked 2026-11-14:
- https://langfuse.com/docs/observability/features/log-levels — levels and status messages.
- https://langfuse.com/docs/observability/sdk/instrumentation — scoped observations and nesting.
- https://langfuse.com/docs/observability/sdk/advanced-features — SDK export/flush and related lifecycle controls.

## 25. Typed observations, point events and model usage — iteration 15

**Status:** R26/R27 express Sharon's required reporting direction; the specific broker APIs, native integrations and delivery boundary remain proposed. He asks for established Langfuse practices and alternatives before choosing the context schema. The scoped-operation explanation is welcomed, not an instruction to force every report into a generic span or trace every helper. Local application logging remains deferred.

### Use the existing observation model

| Project activity | Langfuse representation | Why |
| --- | --- | --- |
| Workflow execution / meaningful non-model step | span (or chain where semantically useful) | Timed operation with a parent and an outcome. |
| One reviewer/coder invocation | agent | Contains that invocation's model calls and tool work. |
| One actual model request | generation | Model, request/result, timing, usage and cost for that request. |
| One executed tool call | tool | Tool name, arguments/result, timing and failure information. |
| A decision, tool-request notification or other discrete fact | event | A point in the trace, without pretending a notification is the full execution. |

Langfuse calls these observations. A trace contains the related observations; it is not recreated for each notification. Typed timed observations have their own observation/span IDs, while operations within one invocation retain workflow_run_id/agent_run_id correlation. Updates to a recorded operation keep that operation's identity. The SDK owns the underlying IDs and representation; no custom ID machinery is implied.

Pushback on the initial example: a tool execution generally is timed work and should use the tool observation type. A message stating that a tool was requested is a distinct point event; it cannot establish success or fabricated duration. If a supported integration already creates the tool observation, do not also create an equivalent tool span just to mirror it. Extra start/completion events are optional and should add information rather than duplicate an existing observation.

Recommended hierarchy for a controlled workflow: a workflow observation contains a reviewer agent observation; model invocation 1, executed tool call and model invocation 2 are children of the reviewer (or a meaningful step beneath it). The requesting generation and the resulting tool call are normally siblings under the orchestrating operation. Distinct generation/tool observations allow per-request inspection. A useful turn/iteration marker can be metadata; do not mandate an extra span for every streaming chunk or ordinary code block.

### Cost and turn detail

Retain one generation per actual model invocation, rather than one generation around the complete loop. A user-visible turn may contain multiple model calls. Capture source-provided model identity and usage at the call level, including cache categories where available; direct reported costs may also be supplied. Langfuse can infer model cost from usage and matching model prices. Validate the mapping against the pinned SDK/backend and provider counts rather than implementing our own pricing engine.

Keep usage updates, outputs and costs on their operation, not in inherited execution-context fields. Agent/turn totals should aggregate each billable call once. Do not additionally post the same aggregate as another charge or count cumulative provider totals as independent deltas. If only final per-agent totals are available, mark the coverage limitation: exact individual-call cost cannot be reconstructed from that total alone.

Ordinary tool observations are not automatically priced model requests. The model request that selected read_file incurs its own generation cost; a local file read has no inherent token price. A tool that calls a model can contain a nested generation. Paid external API/tool fees require a deliberate cost representation supplied by the source; current Langfuse model-cost tracking is on generation/embedding observations. Designing paid-tool billing is not added to the initial delivery by this clarification.

### Existing ways to record the observations

| Mechanism | Good fit | Practical limit |
| --- | --- | --- |
| SDK context manager / with block | Contiguous workflow, agent-wrapper or helper code whose beginning/end we control. | Cannot by itself observe work hidden inside an external runtime. |
| SDK decorator | A whole function with a clear operation boundary. | Must integrate with our injected broker/context and intentional input/output capture. |
| SDK manually managed observations plus events | Agent streams/callbacks where start, result, usage and completion arrive separately. | Correlate start/end by native call identity; close/update the same observation without duplicating existing instrumentation. |

An existing supported integration may supply much of the third-party instrumentation automatically. Prefer reuse after checking runtime, self-hosted backend/SDK versions, local destination, required granularity and trace-parent compatibility. Official Claude Agent SDK and Codex examples are evidence that these use cases are established, not selection of those exact packages/hooks. A developer-tool plugin that emits an independent trace per turn does not automatically satisfy a workflow-owned trace hierarchy. The current documentation's latest majors are not a project upgrade instruction.

If native runtime events need mapping, the adapter translates their facts to existing Langfuse observations through our owned boundary. It does not take over tool execution, permissions or the agent loop. The separate agent-design effort still owns that runtime/event contract. OpenLLMetry or another auto-instrumentor is an option only when it actually covers the chosen runtime; no new dependency selected here.

### Revised broker recommendation — still to decide

**Iteration 16 update:** this recommendation is paused. Section 26 first asks whether a broker is justified at all; do not extend its API merely because more native capabilities are useful.

Cover three behaviors with the existing ordinary broker: (1) typed timed observations, (2) point-in-time trace events, and (3) updates such as safe output, model usage and cost on an existing observation. Use Langfuse's existing observation/SDK mechanisms. This is a capability list, not a demand for three methods, five wrapper classes, a replacement tracing engine or local log output.

Possible public shapes to compare next are a single typed observe/operation method plus event reporting, versus small named helpers for agent/tool/generation plus event reporting. Dedicated helpers are more explicit but increase wrapper surface; the typed method keeps the surface smaller but needs type-appropriate fields. A raw SDK in every workflow is technically possible but conflicts with D04's existing provider boundary and is not the recommendation.

The earlier proposal yielding only ObservabilityContext is not final: updates may need an owned observation handle or broker methods receiving a reference. Choose that minimal contract together with context representation; do not insert a new handle/class silently. Partial SDK/integration adoption must not duplicate billable generations. Exact method names, parameter types, fields and tests remain unselected.

### Open action Q20

Determine which supported integration or native adapter supplies accurate model request boundaries, tool-request/execution distinctions, native call IDs, usage/cost granularity and updates. Confirm parentage and duplicate prevention. Keep timing/usage/outputs on observations and execution correlation in context. Separate capability support from first-release delivery: real agent runtime integration and advanced cost reporting are not automatically authorized by this design discussion.

Primary sources checked 2026-11-14:
- https://langfuse.com/docs/observability/features/observation-types
- https://langfuse.com/docs/observability/best-practices
- https://langfuse.com/docs/observability/features/token-and-cost-tracking
- https://langfuse.com/docs/observability/sdk/instrumentation
- https://langfuse.com/integrations/frameworks/claude-agent-sdk
- https://langfuse.com/integrations/developer-tools/codex



## 26. Broker necessity — reopened, iteration 16

**Status:** Q21 is open. Sharon requests a critical comparison, not automatic removal. The current recommendation is direct Langfuse instrumentation plus only demonstrated application helpers. This would change D04, broker-specific D09/D10 and R15/SH-03; it needs an explicit design choice before implementation. Logging scope, context composition/isolation and reporting capabilities remain intact.

### Options and practical costs

| Option | Benefit | Cost and limit | Assessment for current scope |
| --- | --- | --- | --- |
| Direct Langfuse SDK and compatible native integrations | Immediate access to supported capabilities and official examples; minimal project-owned reporting code. | Langfuse imports/types appear at instrumentation points; replacement requires editing those points and checking semantics/integrations. | Recommended baseline. Configure the client centrally and define cleanup/outage behavior. |
| Small Langfuse-aware application helpers | Reuse actual project policy, such as mapping safe correlation fields or recording a repeated workflow lifecycle. Native SDK operations/handles remain usable. | Helpers are intentionally coupled to Langfuse. Excessive forwarding would recreate the same broker cost under a different name. | Add only where concrete repetition or required policy warrants it; no new mandatory helper layer. |
| Owned provider-neutral broker | A stable application vocabulary; consistent policy for calls it controls; a substitute recorder can simplify some tests; can route to multiple destinations. | Must define and maintain types, handles, lifecycle/error rules and feature mapping; provider-specific extensions weaken neutrality; auto-instrumentation can bypass it. | Not justified solely by hypothetical replacement now. Reconsider if an actual second implementation or shared routing need materializes. |

An ordinary Langfuse-only delegating class sits between the latter two options. Its lack of ABCs reduces code, but a class forwarding span/event/update method-for-method still duplicates an API. Give it a concrete application responsibility before keeping it. Runtime call overhead is likely secondary to API maintenance, correctness and testing work; no performance measurement was made.

### Pushback in both directions

- A wrapper does not inherently prevent full Langfuse use. It can grow methods or expose native handles, at the price of maintaining that surface and accepting provider coupling. The relevant risk is an artificially restricted contract or a second SDK, not a universal prohibition on wrappers.
- A provider-neutral interface cannot promise effortless migration. Observation semantics, feature differences, third-party instrumentation, cost/evaluation behavior and historical data still need validation. A future provider can require both adapter and application changes.
- Centralized initialization, client reuse, context propagation, testing and safe telemetry do not each require a broker. They need explicit ownership/policies; use SDK facilities and limited application code where sufficient.
- A broker can enforce application policy only for reporting that crosses it. Native SDK/framework instrumentation may report independently. Context coverage, sanitization and future local mirroring need explicit integration even if a broker exists.
- Direct calls have a real migration cost and can lead to inconsistent metadata if authors improvise. Keep configuration/cleanup centralized, define the context-to-telemetry mapping and instrument meaningful boundaries; do not equate removing the facade with removing integration discipline.

### Proposed direction and preserved requirements

For the present Langfuse-only phase, omit ObservabilityBroker and use the supported SDK/native integration at reporting boundaries. Keep existing application assembly for configuration/client initialization and cleanup ownership. Add narrow Langfuse-aware helpers only for policy that is actually repeated; do not wrap every SDK method or introduce a replacement OTel abstraction. This is a proposal, not authorization to move provider code or change repository architecture documents.

ExecutionContext and its single ObservabilityContext still carry application correlation/scoped data. The SDK owns active trace/span mechanics. The exact bridging fields and propagation/injection contract remain to be designed; no live-client copying or mutable shared current-agent field is introduced. Removing a broker does not settle agent runtime object lifetimes.

D02/D03 local logger/viewer replacement, Apache 2.0 requirements and local-only/no-required-service constraints remain deferred requirements. R25 trace-to-local-log correspondence is not cancelled. When logging resumes, decide how to cover manual and native instrumentation without duplicate records. Its future need alone does not mandate a full facade today, but it remains a real design consideration.

Native SDK support and OpenTelemetry interoperability are reuse benefits, not proof that prompt management, scores or model-cost semantics migrate unchanged. Before implementation, verify the selected path against the project's actual pinned SDK and self-hosted baseline. No library upgrades or new services are selected.

Next design choice: select the provider dependency boundary. Only then finalize reporting call shapes and the minimal context schema. Keep public names already selected as history; ObservabilityBroker is only needed as an implementation name if that object survives the review.

Primary evidence checked 2026-11-14:
- https://langfuse.com/docs/observability/sdk/instrumentation — SDK context managers, decorators, manual observations and native integrations interoperate.
- https://langfuse.com/docs/observability/sdk/overview — SDK uses OpenTelemetry and supports Langfuse-specific observation capabilities.
- https://langfuse.com/integrations/native/opentelemetry — recommends the Langfuse SDK for Python/TypeScript instead of recreating Langfuse mapping directly on raw OTel.

The recommendation to omit our broker is an engineering assessment for this project's current scope, not a quoted Langfuse architectural requirement.
