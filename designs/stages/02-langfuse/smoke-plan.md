# Personal Langfuse playground and manual exercise

Status: **DRAFT for milestone 3; no example has been implemented.**
[Milestones and gates](milestones.md) · [Configuration](architecture.md)

This file replaces the earlier test-first seed-script proposal. The main goal is
for Sharon to see traces, edit the example and learn how changes appear in the UI.
Automated integration verification remains separate. The implementing agent must
first smoke-run the requested new example on its success and selected failure
paths, following [the verification requirements](verification.md). This targeted
manual run does not put examples in the automated application gate.

## Requested example

Create `app/examples/langfuse/` when implementing M3, with a simple `run.py` and
README. A candidate invocation is:

```text
# Proposed entry point; does not exist yet.
python app/examples/langfuse/run.py
```

Provide clear external configuration/key instructions and a small editable set of
inputs in the example. It may use the maintained Langfuse integration without
importing application runner/workflow/context code. Do not create a dummy context.

Start with arithmetic input `initial=3, increment=2, multiplier=4` and four nested
steps: initialize, add, multiply, finish. The successful result is 20. This is a
simulation, not an actual CrewAI run. Label runs `source=mock` and
`workflow_id=mock-wf-02`; each invocation gets fresh run and trace IDs. Record the
actual trace identifier rather than assume an arbitrary run ID is an OTel ID.

Make the following easy to change without a framework:

- Inputs: change the initial value, increment or multiplier.
- Which step fails: `fail_step=None`, then `"add"`, then `"multiply"`.
- Step names or small output payloads for UI experimentation.

Those are proposed example settings, not a public production configuration API.
A single scenario per invocation is sufficient; additional mock runs are optional.

## What Sharon sees and does

1. Run the default example and open the printed trace link.
2. Expand the root and its steps. Inspect input, output and elapsed time.
3. Change an input and rerun; a new trace shows the new values.
4. Select failure in add. Inspect the error message and failed step/root; later
   steps must not appear as completed.
5. Move failure to multiply and compare the two runs.
6. Stop/start Langfuse without removing volumes and reopen a previous trace.

The script computes actual fixture values and records real execution timing.
Any optional teaching delay is explicit, zero by default. Do not invent tokens,
costs, provider activity or model calls. Input/output is small and synthetic.

Print run ID, trace ID, outcome and URL without secrets. Distinguish an intentional
simulated error from transport failure and from telemetry not yet visible.
Success for this milestone includes Sharon actually seeing the expected data,
not merely the script exiting or creating a URL.

## Independent verification boundary

| Surface | Purpose and acceptance |
|---|---|
| Personal example | Manual exploration; Sharon may edit success/failure scenarios freely |
| Maintained connection check | M2 diagnostic function/entry point outside examples, later reusable by doctor |
| Offline application tests | Validate settings/export behavior using their own fixtures under `app/tests/` |
| Explicit live integration test | If included, emits its own fixed fixture and reads back trace/steps with a bounded timeout |
| Ordinary application checks | Need no server, never discover/import/run examples, unaffected by playground edits/removal |

A live verification fixture may check nesting, identity and values after a flush
and bounded polling period (initial proposal: up to 30 seconds). Flush is not
proof of completed server ingestion. Missing observations or wrong values fail
that explicit test. Do not move the personal example into tooling merely to make
it testable, or make maintained tests depend on its editable data.

Future access to the personal playground remains subject to Sharon's specific
requests. This PR updates its design only and does not inspect existing examples.
The historical filename `smoke-plan.md` is retained to preserve PR links; its
current purpose is this manual playground plan and the separate test boundary.
