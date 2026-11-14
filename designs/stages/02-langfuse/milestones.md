# Four milestones and their checkpoints

Status: **M1–M3 local setup and mock-trace exercise accepted by Sharon on 2026-11-14; PR #36 merged as `44d6919`. Delivery-readback limits are recorded; M4 remains deferred.**
[Review entry point](README.md) · [Required agent verification](verification.md) · [M1 Codex brief](implementation-handoff.md)

Current state: WF-01/02/03 still run without Langfuse. PR #36 implements the
local service, explicit project check and optional mock playground. Sharon
confirmed visible traces and normal stop/start persistence on Mac. See
[acceptance and remaining limits](acceptance-2026-11-14.md); the earlier
[Codex handoff](connection-playground-handoff.md) remains historical.
The workflow refactor is separate. Each checkpoint can include several commits.

Implementation of M2/M3 may proceed before Sharon completes earlier local gates.
Acceptance remains sequential: earlier local prerequisites must work before his
next manual exercise. Keep a tested commit and separate verification file per
milestone; preserve the fixed M1 checkpoint.

## 1. Langfuse runs locally

**Starting point:** no project-managed local Langfuse setup.

**Deliver:** a small pinned Docker Compose setup under maintained tooling, safe
local settings, persistent volumes and clear start/stop instructions. No Python
integration or workflow changes are needed.

**You try:** start it, open the UI, create an account/project and see an empty
trace list. Stop/start it normally; the project still exists.

**We check:** quiet Compose validation and settings/pins/volumes sanity; actual
stack startup, bounded readiness, a UI-page request and normal stop/start when
supported. Record precisely what passed and any blocker. Opening a page is not
proof of authentication, record persistence or ingestion; those need their own checks.

**Gate:** the setup checks pass and Sharon confirms the empty UI/project works.
Record the exact commands, versions and expected results in the implementation
handoff. No volume-deleting reset is part of the normal exercise.

## 2. Our code can connect

**Starting point for local acceptance:** milestone 1 works locally. Development
may use an isolated agent instance while Sharon's acceptance is pending.

**Deliver:** validated external Langfuse settings, a small reusable integration
module and an explicit standalone connection-check entry point. It loads
configuration, checks reachability/authentication, reports safe results and exits.
It does not emit traces, run a workflow or create context objects.

**You try:** supply your local project keys and run the connection check once;
see endpoint and authentication success. The agent checks invalid-key and stopped-
service failures first; you need not repeat them unless local differences warrant it.

**We check:** offline tests for valid/invalid settings, disabled mode with no
keys/network, sanitized errors and connection-result handling; an explicitly
invoked live connection check. Normal application checks require no server.

**Gate:** both the successful check and useful failure reporting work on Sharon's
machine; existing application checks pass.

[Doctor feature request #37](https://github.com/SharonLanger/agent-playbook/issues/37)
will reuse this capability later. Do not expand this milestone into a full doctor
framework or wait for that command to exist.

## 3. I can see and change mock runs

**Starting point for local acceptance:** milestone 2 can connect. Development
follows M2's available agent checks; blocked live checks remain explicit.

**Deliver:** Sharon's explicitly requested `app/examples/langfuse/` playground,
with a simple `run.py` and a short README. Start with editable inputs and a
`fail_step` setting; no generic scenario framework is necessary. Use the
configured integration to send synthetic observations. No workflow ABC/context,
real CrewAI execution or model calls are needed.

**You try:** run the happy path, open a printed trace link and inspect nested
steps, inputs, outputs and durations. Change an input and rerun. Then choose a
different step to fail and see that error in the UI. Repeat freely; previous runs
remain available. Restart Langfuse and inspect an earlier trace.

**We check:** the implementing agent smoke-runs the explicitly requested new
playground with success and failures in add/multiply before delivery. Verify live
observations when a service is available; report a blocked check honestly. This
manual run is separate from maintained integration tests, whose fixtures live in
app/tests and never run/import the playground. Read-back checks do not replace
Sharon seeing and understanding the UI.

**Gate:** Sharon can see successful and failed mock runs and deliberately change
what appears. Application checks remain unaffected by edits to, or removal of,
the playground. No automated job scans examples to establish this.

See [the manual exercise and testing boundary](smoke-plan.md).

## 4. Connect the real workflow — later

**Starting point:** milestones 1–3 accepted and the workflow refactor merged.

**Deliver:** a separately reviewed integration with the actual workflow/context
contract. Use the existing Langfuse setup and connection capability. Determine
context construction, lifecycle observation, error propagation and ownership from
the merged design; do not predefine them in milestones 1–3.

**You try:** run real WF-02 through its normal entry point and open its trace.
Inspect a successful execution and a controlled failing execution.

**We check:** actual lifecycle boundaries, run isolation/correlation, meaningful
error reporting and preserved workflow results. Define telemetry-outage policy
before enabling export for real workflows. Retain independent offline tests.

**Gate:** real runs are observable without weakening the workflow's lifecycle or
failure rules. Real agents are a later step, not part of this milestone.

## Working and merge agreement

Complete the practical agent checks in [verification.md](verification.md) before
handoff. Fix observed failures; distinguish passed checks from blocked/unrun checks.
Leave simple local account/UI acceptance to Sharon instead of building expensive
automation solely for a few clicks.

At each checkpoint, provide: the exact revision to use, setup/run commands,
expected visible output, automated results, and any known limitations. Sharon
runs the manual exercise before acceptance. These commands will be executable
instructions in the implementation PR, not invented working commands in this plan.

Keep milestones as checkpoints even if they share a PR. Continue with the same
branch by default; create a separate PR only after confirming an independent
scope and reviewing actual overlap with concurrent work. Check shared
`pyproject.toml`/`uv.lock`, configuration, navigation and Atlas files in particular.
Regenerate Atlas from reconciled sources; do not hand-merge generated HTML.

No merge is automatic at a checkpoint. Milestones 1–3 do not wait for the workflow
refactor; milestone 4 does. Before milestone 4, update this draft from the merged
contract and explicitly review any guarded logical changes.

## M4 checkpoints — approved context sequence, 2026-11-14

M4.R research established bounded released-version CrewAI/Langfuse feasibility. M4.1 is the separately approved [data-only context design](workflow-integration/01-context-design.md), with an implementation PR under review; it requires identity, runner/factory/Workflow/Flow forwarding, isolation and CTX-01–17 evidence. M4.2 will separately review native runner tracing; M4.3 will separately review CrewAI automatic observations. M1–M3 acceptance and historical checks remain unchanged. Approval of M4.1 does not mark all M4 implemented or Stage 02 complete.
