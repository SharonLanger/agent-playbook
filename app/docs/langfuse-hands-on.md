# Langfuse hands-on: send and inspect a mock trace

This exercise sends synthetic arithmetic observations from the explicitly run
personal playground. They are not application workflow logs. It makes no model
calls and uses no LLM tokens or spend. Ordinary workflows remain uninstrumented.

## Authenticate first

- Create the required credentials file using the [connection guide](langfuse-connection.md#create-the-private-credentials-file), then prepare the application environment if needed.

```sh
python3 app/tooling/bootstrap.py
```

- Configure the project keys and YAML settings by following the [connection guide](langfuse-connection.md).

That guide covers the `Project Settings → API Keys` page, the external
`~/.config/agent-playbook/secrets.env` path, user-only file permissions and
the top-level YAML `secrets.file` setting. No terminal export is required. The application key file is separate from
Docker's service `.env`.

- Start the local Langfuse service if you are using `http://localhost:3000`.

```sh
app/.venv/bin/agent-playbook langfuse --start
```

Hosted Langfuse endpoints do not require local Docker.

- Check project authentication before sending observations.

```sh
app/.venv/bin/agent-playbook langfuse --check
```

Continue after the check reports project authentication succeeded. A disabled
integration is skipped; an invalid file or missing key fails before connecting.

## Run a successful example

- Send a synthetic arithmetic run from the repository root.

```sh
app/.venv/bin/python app/examples/langfuse/run.py
```

The default calculation is `(3 + 2) * 4 = 20`. The script prints a fresh run
ID, trace ID, outcome and trace URL. `delivery: verified` confirms API readback;
a printed URL or SDK flush alone does not confirm ingestion.

## Inspect the trace

- Open the Langfuse UI.

For a local instance, open `http://localhost:3000`.

- Open **Traces** from the navigation.

- Select the trace using its printed ID or open the printed URL.

- Expand the root trace and its four child steps.

Review `initialize`, `add`, `multiply` and `finish`, including synthetic inputs,
outputs, elapsed times and status. The trace is labelled `source=mock` and
`workflow_id=mock-wf-02`; it does not represent a real CrewAI workflow.

## Change the input and rerun

- Change the initial value and rerun the example.

```sh
app/.venv/bin/python app/examples/langfuse/run.py --initial 5 --increment 2 --multiplier 4
```

The result is `28`. This invocation has a new trace ID; previous traces remain
in the project.

## Inspect simulated failures

- Simulate a failure in the add step.

```sh
app/.venv/bin/python app/examples/langfuse/run.py --fail-step add
```

The mock outcome is a failure. In the trace, `initialize` completes, `add` and
the root show errors, and `multiply` and `finish` do not run.

- Simulate a failure in the multiply step.

```sh
app/.venv/bin/python app/examples/langfuse/run.py --fail-step multiply
```

The mock outcome is a failure. In the trace, `initialize` and `add` complete,
`multiply` and the root show errors, and `finish` does not run. A failed mock
step is deliberate example behavior; an export/readback failure is reported
separately and exits with status 1.

## Confirm persistence

- Stop the local Langfuse stack normally after creating a trace.

```sh
app/.venv/bin/agent-playbook langfuse --stop
```

- Start the local Langfuse stack again.

```sh
app/.venv/bin/agent-playbook langfuse --start
```

- Open **Traces** again after the service restarts.

- Select the earlier trace and confirm it is still present.

Normal stop/start keeps the named volumes and does not reset the local project.
Do not remove volumes for this exercise. Hosted projects are managed by their
service and do not use these local Docker volumes.

- Stop the local stack after finishing if you do not need the UI anymore.

```sh
app/.venv/bin/agent-playbook langfuse --stop
```

The trace screen shows only the mock observations sent by this example. It does
not show routine Agent Playbook application logs or trace ordinary workflows.
See [local Langfuse setup](langfuse-local.md) for daily service commands and
[configuration](configuration.md) for loader precedence and file syntax.
