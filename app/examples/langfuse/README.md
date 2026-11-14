# Personal mock Langfuse playground

This is an explicit learning script, not an application test or a real CrewAI
workflow. Start the [local Langfuse service](../../docs/langfuse-local.md) when
using a local endpoint, then create a Langfuse project. Follow the
[connection guide](../../docs/langfuse-connection.md) to store project keys in
`~/.config/agent-playbook/secrets.env` outside the repository, select it with
`AGENT_PLAYBOOK_SECRETS_FILE`, and keep Langfuse explicitly enabled. The
application secrets file is distinct from Docker's `app/tooling/observability/.env`.
An export in a terminal applies to that shell and child processes; set the same
selector in PyCharm when running the script there. Use the official
[Langfuse hands-on guide](../../docs/langfuse-hands-on.md) for the complete
authentication, trace inspection, changed-input, failure and persistence exercise.

- Prepare the application environment from the repository root.

```sh
python3 app/tooling/bootstrap.py
```

- Verify project authentication before sending the synthetic traces.

```sh
app/.venv/bin/agent-playbook langfuse --check
```

- Run the successful arithmetic scenario from the repository root.

```sh
app/.venv/bin/python app/examples/langfuse/run.py
```

- Run the deliberate add failure from the repository root.

```sh
app/.venv/bin/python app/examples/langfuse/run.py --fail-step add
```

- Run the deliberate multiply failure from the repository root.

```sh
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
