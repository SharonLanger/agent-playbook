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
