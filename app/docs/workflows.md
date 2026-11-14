# Running workflows

Use this guide to choose what to run, change its input, and understand the output.
For the complete command reference, see [CLI and releases](cli.md).

## Choose a starting point

| What you want to do | Run this | Where the code lives |
|---|---|---|
| Try the integrated application with editable code | PyCharm **WF-01 Sequence**, **WF-02 State**, **WF-03 Route**, or **Dev Run** | `app/src/agent_playbook/workflows/` |
| Run a previously built application | PyCharm **Run**, or the CLI `run` command | The selected installation under `app/dist/` |

The integrated application validates shared configuration and selects a workflow ID through
its registry and factory. Each wrapper validates input and output while CrewAI runs its steps. Personal sandbox contents are outside the supported application workflow catalog.

Follow [setup](../README.md) and select `app/.venv/bin/python` as the project interpreter.

## Integrated workflows

| Workflow | Purpose | Default input | Default result |
|---|---|---|---|
| `wf-01` | Pass a string between three methods | No fields | `[Hello, workflow!]` |
| `wf-02` | Change typed state through arithmetic steps | initial 3, increment 2, multiplier 4 | `20` |
| `wf-03` | Choose one score-based branch | score 80 | `pass` |

WF-02 calculates `(initial + increment) * multiplier`. Its history is maintained explicitly
by the workflow; it is not automatic framework history. WF-03 returns `needs_work` below 60.
That is a successful routing outcome, not an execution failure.

The input fields and ranges are listed in the [CLI workflow reference](cli.md#select-a-workflow).
Input is a JSON object, not a filename. Unknown keys and invalid types are rejected; for
example, use `40`, not `"40"`, for a score.

### Run in PyCharm

1. Choose the existing **WF-02 State** task and run it to see the default result.
2. In that task's parameters, use:
   `dev-run --workflow wf-02 --input '{"initial":10,"increment":-2,"multiplier":3}'`.
3. Run again. The result should be `24`.
4. For **WF-03 Route**, use `dev-run --workflow wf-03 --input '{"score":40}'`.
   The result should be `needs_work`, with exit code 0.

These shared tasks use module `agent_playbook.cli`, the project interpreter and
`$PROJECT_DIR$/app` as the working directory. They run editable source.

### Equivalent terminal commands

Run these from the repository root after bootstrap; no shell activation is required:

```sh
app/.venv/bin/agent-playbook dev-run --workflow wf-01
app/.venv/bin/agent-playbook dev-run --workflow wf-02 --input '{"initial":10,"increment":-2,"multiplier":3}'
app/.venv/bin/agent-playbook dev-run --workflow wf-03 --input '{"score":40}'
```

To use an existing release instead, change `dev-run` to `run`. The editable launcher
prints the selected release directory. Editing source does not modify that installation:
build a new release when you want those edits available through `run`.
See [release selection](cli.md#editable-source-versus-releases).

A YAML entry may give the same implementation a new ID and different defaults; see [configured workflows](configuration.md#configured-workflows). The native result is retained for Python callers, while the CLI prints the workflow’s serialized text.

## Errors and checks

For the integrated CLI, exit 0 means success, exit 2 means invalid input/configuration/usage
or unavailable release, and exit 1 means workflow execution failed.

See the [CLI reference](cli.md) for check commands and their supported scope.

See [troubleshooting](troubleshooting.md) for unexpected output or startup errors.
For an explanation of the code itself, continue with the
[Stage 01 learning material](../../designs/stages/01-crewai-flows/learning/00-reading-the-code.md).


Only the selected workflow loads its CrewAI flow module during preparation. Each run uses a fresh wrapper; a configured alias changes defaults and identity without changing step routing.

## Execution context for Python workflow integrations

Each `dev-run` or installed workflow invocation creates a fresh, typed application
`ExecutionContext` after YAML selection. Its `correlation_id` is a UUID4 grouping
identifier; `observability.workflow_id` is the selected ID (including an alias),
and `observability.workflow_run_id` identifies this invocation. The runner passes
the same context object through the factory, Workflow wrapper and CrewAI Flow.
Python integration code can read `workflow.context` or `flow.context`.

`context.for_agent(agent_type=..., agent_run_id=...)` creates an independent child
value that retains the workflow and correlation identities. The caller supplies
an identity for each agent invocation; this method does not execute an agent.
The context is separate from CrewAI state and ordinary Flow serialization.
CLI flags and displayed workflow results are unchanged. Tracing and Langfuse
export are planned as later milestones; a correlation ID is not a trace ID.
