# Running workflows and learning examples

Use this guide to choose what to run, change its input, and understand the output.
For the complete command reference, see [CLI and releases](cli.md).

## Choose a starting point

| What you want to do | Run this | Where the code lives |
|---|---|---|
| Try the integrated application with editable code | PyCharm **WF-01 Sequence**, **WF-02 State**, **WF-03 Route**, or **Dev Run** | `app/src/agent_playbook/workflows/` |
| Run a previously built application | PyCharm **Run**, or the CLI `run` command | The selected installation under `app/dist/` |
| Experiment with one CrewAI behavior directly | Open an example's **run.py** and click Run | `app/examples/workflows/ex_*/` |

The integrated application validates input/configuration and selects a workflow through
its application runner. A standalone example creates and starts its own flow directly.
You do not register an example with the runner or pass its folder name to `--workflow`.

Before either route, follow [setup](../README.md) and select `app/.venv/bin/python`
as the project interpreter. The examples reuse that environment and its installed dependencies.

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

## Independent examples

Start with the [examples index](../examples/workflows/README.md). It lists every folder,
its README and its runnable entry point.

1. Open `app/examples/workflows/ex_01_step_sequence/run.py` and click Run.
2. Read that folder's README and `flow.py` together.
3. Where the example has inputs, edit its `input.json`, then rerun `run.py`.
4. Move through examples 02–04 to compare method references, string names, router labels
   and the intentional name collision.
5. Continue to examples 05–08 for loops, nested conditions, chained routers and persistence.

You can also run an example from the repository root:

```sh
app/.venv/bin/python app/examples/workflows/ex_01_step_sequence/run.py
```

Each example resolves files relative to its script, so its working directory need not be
the repository. Its integration settings live in its own `settings.toml`; workflow input
lives in its `input.json`. Application YAML does not configure these examples. See
[configuration scope](configuration.md#which-configuration-does-this-guide-cover).

The example scripts print **Result** and **State**. Read the per-example README before
interpreting them: where multiple methods can finish independently, the last result is not
necessarily a named final node. A `calls` list is teaching instrumentation, not a framework
trace or proof of simultaneous CPU execution.

Example 08 writes SQLite data to its own ignored `.runtime/` folder. Each run.py invocation
starts a new first flow and a second flow restored from the first flow's saved state.
It does not automatically select an earlier run from a previous click.

## Errors and checks

For the integrated CLI, exit 0 means success, exit 2 means invalid input/configuration/usage
or unavailable release, and exit 1 means workflow execution failed. Standalone examples
let Python exceptions propagate; they do not use the CLI's error translation.

Use the existing **Tests** or **Check** tasks to include the application and example tests.
Each example's `test_ex_XX.py` can also run individually as a pytest file in PyCharm.
Tests for examples copy their folders and run independently, so they do not reuse your
persistent example database.

See [troubleshooting](troubleshooting.md) for unexpected output or startup errors.
For an explanation of the code itself, continue with the
[Stage 01 learning material](../../designs/stages/01-crewai-flows/learning/00-reading-the-code.md).
