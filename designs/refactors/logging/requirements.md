# Logging requirements / initial specification

**DRAFT.** Derived from Sharon's supplied handover. This is not a locked runtime contract.

Goal: debug Agent Playbook through structured local records, workflow/agent correlation and practical filtering. Preserve native Langfuse and workflow semantics; reuse the existing data-only context.

| ID | Requirement / acceptance intent | State |
|---|---|---|
| LOG-01 | Filter by workflow_id, workflow_run_id, agent_type, agent_run_id, correlation_id; distinguish repeated invocations even within one trace. | Handover requirement |
| LOG-02 | Workflow identity is inherited; derived agent context reaches helpers without leaking agent fields into parents, siblings or other runs. | Requirement; context foundation delivered |
| LOG-03 | Stable application correlation exists independently of tracing and is retained in descendants. No required trace ID. | Requirement |
| LOG-04 | Timestamp, severity, message and useful error details. | Requirement; exact schema open |
| LOG-05 | Viewer availability must not gate recording. Storage-service dependence and outage behavior must be decided explicitly. | Viewer independence retained; service policy reopened |
| LOG-06 | Query selected filters before loading matching results; sort/filter loaded results without another query. | Requirement; result bounds/pagination to design |
| LOG-07 | Error severity does not set workflow outcome; recovery may leave a successful parent with error records. | Requirement |
| LOG-08 | Local storage/processing; Apache 2.0 for newly selected logging/viewer components, Langfuse separately accepted. | Constraint; exact licenses to verify |
| LOG-09 | Existing maintained open source, minimal custom code and independently replaceable formatting/storage/viewer responsibilities. | Constraint |
| LOG-10 | Never log secrets/configuration wholesale. Specify field selection, redaction limits, safe exceptions and payload bounds. | Guarded security constraint; mechanism open |
| LOG-11 | Define retention, rotation, disk bounds, concurrent writers, shutdown/flush and delivery failures before claiming reliable recording. | Open design requirement |
| LOG-12 | Retain eventual execution-event logging; coordinate exact coverage with Stage 04, without defining its contracts here. | Deferred integration |
| LOG-13 | Reconsider whether automatic Langfuse/CrewAI observations also become local records; avoid duplication if selected. | Deferred; not automatic MVP scope |
| LOG-14 | Reuse existing external configuration ownership; no new loader or per-step client setup. | Principle; settings open |

## Field inventory — not a final wire schema

| Field | Meaning | Decision still needed |
|---|---|---|
| timestamp | Occurrence time | UTC format/precision |
| severity / message | Diagnostic importance and description | Level mapping; optional event name |
| correlation_id | Stable application correlation | Startup records before context exists |
| workflow_id / workflow_run_id | Workflow and invocation | Absence outside workflow execution |
| agent_type / agent_run_id | Agent and invocation | Absent versus null outside agent scope |
| exception | Failure details | Type, message, cause chain, stack, sanitization and bounds |
| trace_id / span_id | Optional native observation link | Active-scope lookup; disabled/sampled behavior |
| additional fields | Useful event-specific data | Types, reserved-key protection and serialization |

## Acceptance intent for later milestone tests

- Separate and combined queries for two invocations of the same workflow.
- A and B inherit workflow/correlation; repeated A calls have distinct agent_run_id; subsequent workflow records have no agent fields.
- Concurrent runs/branches and nested helpers retain correct identities.
- A recovered failure produces an error record without forcing parent failure.
- Tracing disabled still permits logging under the selected recording policy.
- Viewer stopped does not prevent recording; stopped storage follows the explicit outage contract.
- Bounded query results can be sorted/filtered locally without requery.
- Synthetic secret/configuration fixtures are excluded under a documented payload policy.
- Restart, disk pressure, rotation, shutdown and simultaneous writers expose measured delivery/loss limits.

No exactly-once, durable replay, complete framework capture or universal secret recognition is promised. No custom logging engine, viewer, second context system, scheduler, generic event bus or tracing facade.

## Follow-up requirements — 2026-11-15

These are explicit user requirements; the detailed implementation is not yet approved.

| ID | Requirement | Acceptance intent |
|---|---|---|
| LOG-15 | Golden rule: logging backend is easily detachable/replacable; native Langfuse remains the exception | Change backend/collector configuration without changing workflow/agent log calls or context; demonstrate alternate output; disclose query/UI/data migration differences |
| LOG-16 | Component Compose files plus one umbrella entry point | Langfuse/logging separately owned; combined startup; component isolation and existing data/secret identity preserved |
| LOG-17 | Clear prerequisites and repeatable component/all-services setup | Docker installed and engine running; explicit Compose minimum and tested versions; bounded readiness, idempotence and actionable errors |
| LOG-18 | Logging management CLI mirrors langfuse action flags | Start/stop/status/open/check and diagnostics; exact install/aggregate spelling pending; no custom framework |
| LOG-19 | Verify the actual logging path | Distinguish service availability from explicit synthetic emit/export/ingest/query round trip; bounded timeouts and honest failure |
| LOG-20 | Configuration-first, low/no custom infrastructure | Existing logger/collector/store/UI; explain necessary setup/context/CLI glue; no broker solely for abstraction |

Docker services are accepted. LOG-05's outage policy is configurable under LOG-26; initialization is required by default, while runtime failures warn only. LOG-08 requires an Apache-2.0 option for new selected projects; MIT-only does not qualify. Exact bundled/transitive artifact licensing is a review gate, not yet certified. See [research](research/2026-11-15-victorialogs.md) and [action items](action-items.md).

## Current scope clarification — 2026-11-15

| ID | Requirement | State |
|---|---|---|
| LOG-21 | Initialize logging once per CLI run invocation at the runner/composition boundary; use a context manager to attempt bounded flush/shutdown on normal exit or exception unwinding; preserve the original exception; no per-step setup | Agreed direction |
| LOG-22 | Application logging helpers require ExecutionContext and message; extract its correlation/workflow/agent identity and support optional event-specific attributes without allowing context identity overwrite | ExecutionContext agreed; detailed schema pending |
| LOG-23 | Direct OTLP/HTTP to self-hosted VictoriaLogs with local storage/UI; no required intermediary collector or JSONL file | Selected direction; pinned setup to validate |
| LOG-24 | Local-only logging configuration: local endpoint, local Docker daemon/storage, loopback UI exposure, no remote forwarding/fallback | Required; source-backed setup, no absolute host-wide guarantee |
| LOG-25 | First milestone is a small opt-in configuration/logging sanity check using synthetic data | Draft M1; no broad reliability/security audit |

LOG-19 is satisfied initially by a bounded smoke demonstration, not a new general test framework. LOG-11 reliability scenarios remain later work, not an M1 completion condition. LOG-17/18 setup and management CLI requirements are retained but deferred. ExecutionContext is selected (LD22). Optional-field rules and implementation of LOG-26 are specified for review in M2; standard exception capture is agreed under LOG-31. No whole-context serialization.

Cleanup scope: ordinary scope exit and Python exception unwinding are covered. Forced termination, interpreter crashes and power loss are outside that guarantee; flush is an attempt, not a guarantee of delivery to an unavailable service. No remote fallback.

## Configurable failure policy — 2026-11-15

| ID | Requirement | State |
|---|---|---|
| LOG-26 | Each integration has required_start (default true), alongside enabled. Enabled integration initialization failure blocks startup when required, otherwise warns. Runtime/export/cleanup failures warn only and preserve workflow outcomes/exceptions. Disabled integrations do not block startup. | User clarification LD21; supersedes strict_logging |

M2 must isolate logging/tracing infrastructure failures from workflow errors and surface safe terminal diagnostics. required_start concerns initialization only, not a mandatory backend connectivity probe. No assertion of backend availability, durable delivery or automatic replay. Diagnostic error-level records alone still do not fail a workflow (LOG-07).

## Application diagnostic coverage — 2026-11-15

| ID | Requirement | State |
|---|---|---|
| LOG-27 | Shared runner code emits workflow started/completed/failed records; useful surrounding application infrastructure also emits diagnostics for setup, configuration, selection/construction and execution. Include detailed DEBUG messages for troubleshooting. | User agreed coverage and delegated placement (LD23) |
| LOG-28 | Record operational exceptions at their handling/reporting boundary, including recovered failures; avoid duplicate reports of one propagated exception and preserve workflow semantics. | Coverage intent; exact ownership and sanitized error schema in M2 |

Automatic context extraction does not mean automatic interception of every operation. No whole-context/configuration serialization or blanket Langfuse/CrewAI trace duplication. Pre-context/pre-logger failures remain safely visible in terminal diagnostics; do not fabricate run identity. Standard SDK stack-trace formatting is selected under LOG-31; automatic agent events remain deferred.

## Severity filtering — 2026-11-15

| ID | Requirement | State |
|---|---|---|
| LOG-29 | integrations.logging.level selects the minimum recorded application severity using standard levels; default DEBUG for current development. Configuration validation rejects unsupported levels. Existing safe-payload constraints apply at every level. | User agreed (LD24) |

## Retention — 2026-11-15

| ID | Requirement | State |
|---|---|---|
| LOG-30 | Default VictoriaLogs retention is seven days, adjustable through the logging component's Compose configuration; rely on VictoriaLogs to expire older records. | User agreed (LD25) |

## Standard exceptions and minimum custom code — 2026-11-15

| ID | Requirement | State |
|---|---|---|
| LOG-31 | Include standard exception type/message/stack trace and native chained causes for recorded operational failures using Python logging exc_info and the OTel handler; retain existing safe-data constraints | User agreed; LD26 |
| LOG-32 | Reuse SDKs for formatting, exception conversion, batching, export, retries and shutdown; our code is limited to context mapping, configuration/lifecycle wiring and necessary failure containment | Explicit user constraint; LD26 |

The SDK's exception field representation is authoritative; do not reconstruct an alternate exception tree or pretend exception.message always equals Python str(exception). Native traceback includes chain details without capturing local variable values. Existing secret/configuration exclusions still apply; no universal automatic secret-recognition promise.
