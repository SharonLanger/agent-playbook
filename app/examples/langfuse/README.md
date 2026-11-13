# Personal mock Langfuse playground

This is an explicit learning script, not an application test or a real CrewAI
workflow. Start the [local Langfuse service](../../docs/langfuse-local.md), create
a project and configure its keys using the [connection guide](../../docs/langfuse-connection.md).
From the repository root, run `python3 app/tooling/bootstrap.py`, then
`app/.venv/bin/agent-playbook langfuse --check`. Keep the same shell's key variables.

From the repository root:

```sh
app/.venv/bin/python app/examples/langfuse/run.py
app/.venv/bin/python app/examples/langfuse/run.py --fail-step add
app/.venv/bin/python app/examples/langfuse/run.py --fail-step multiply
```

The default computes `(3 + 2) * 4 = 20` through initialize, add, multiply and
finish. Each invocation prints a new run ID, actual Langfuse trace ID, outcome
and SDK-provided trace URL. Open the URL and expand the four steps. The run is
labelled `source=mock`, `workflow_id=mock-wf-02`; it sends no model calls, tokens
or costs. Inputs, outputs and elapsed times are synthetic arithmetic evidence.

Change the `INITIAL`, `INCREMENT`, `MULTIPLIER` and `FAIL_STEP` constants in
`run.py`, or pass `--initial`, `--increment`, `--multiplier` and `--fail-step`.
For a visible delay use `--delay-seconds 0.2`; default delay is zero. A simulated
add failure ends the root and add as errors without multiply or finish. A
multiply failure leaves initialize/add completed and ends multiply/root as
errors. Each run uses a fresh ID and does not overwrite earlier traces.

The script checks project access, sends observations, flushes and waits briefly
for project API readback. `delivery: verified` means the trace was visible through
that API; inspect the UI for its hierarchy and values. `delivery: unconfirmed` or
`rejected` exits 1 even if the mock arithmetic succeeded. A printed URL or flush
alone is not proof of server ingestion.
A technical connection/export failure is reported separately from an intentional
mock failure. Nothing emits traces merely by importing the package, starting
Docker or running the ordinary application.

To stop the local service safely, from the repository root run
`app/.venv/bin/agent-playbook langfuse --stop`. Named volumes and earlier traces remain. This personal
script is excluded from normal tests, coverage, formatting and releases.
