# Troubleshooting

Start by identifying whether you launched an editable integrated workflow or a built release. They use different entry points. Personal sandbox programs are outside this guide’s supported application scope.
See [Running workflows](workflows.md) if that distinction is unclear.

## Interpreter, imports and PyCharm

| What you see | What to check or do |
|---|---|
| `agent-playbook: command not found` | From the repository root, use `app/.venv/bin/agent-playbook --help`. This does not require a PATH change. |
| `uv: command not found` | Use the project's bootstrap or version/release tasks. You do not need to configure a global uv command to use those tasks; bootstrap locates/provisions the pinned tool. |
| `No module named crewai` or `agent_playbook` | Check that PyCharm uses this project's `app/.venv/bin/python`. If the environment is missing or stale, rerun setup below. |
| Ruff reports that `src`, `script` or `tests` does not exist | Prefer the shared **Lint** task. For direct Ruff commands use working directory `app`; the folder is `tooling`, not `script` or the old `scripts`. |
| Shared Run tasks are missing | Open the repository root, not just `app`. Inspect the tracked `.run/` files and Run → Edit Configurations. |
| A deleted tracked task does not return after pulling | Pulling does not necessarily undo a local deletion. Inspect `git status --short` and restore the specific task you intended to restore; preserve your custom configurations. |

From the repository root, refresh setup with:

```sh
python3 app/tooling/bootstrap.py
```

Then select the existing `app/.venv/bin/python` interpreter in PyCharm. Bootstrap can require
network access to provision dependencies. It also runs checks; a reported check failure is
not evidence that every setup step failed. Read the first failing section.

## I changed code, but the output is still old

**Dev Run** uses editable source. **Run** launches a completed release, which contains the code
from its recorded commit. Use Dev Run while experimenting, or build another release after
committing the changes you want released.

## Configuration does not seem to change anything

First check which path you are using:

- Integrated workflow: [application configuration](configuration.md), selected by `--config`,
  then `AGENT_PLAYBOOK_CONFIG`, then the source checkout's default YAML.

For the application, a sibling `.local.yaml` or a documented environment override can
replace the value you edited in the shared file. Check the PyCharm task's environment
variables as well as your terminal. An explicitly configured YAML path takes precedence
over the default file.

For an installed release invoked directly, pass `--config` or set
`AGENT_PLAYBOOK_CONFIG`; its wheel has no active YAML file.

| Message or symptom | Meaning |
|---|---|
| Configuration error before any steps, exit 2 | Read the reported location: a required value may be absent, have the wrong type, or be an unknown key. |
| Boolean setting rejected | YAML needs `true` or `false`, not quoted strings/numbers. Documented environment overrides accept true/false text. |
| Referenced environment variable is missing | Set the named variable in the environment of the process you actually launch. |
| CrewAI is already imported with different settings | End the current Python process and start a fresh run. Import-time telemetry/tracing settings cannot be safely switched mid-process. |
| Old release rejects a newer configuration | That release validates its own schema; a shared file is not a promise of compatibility with every version. |

The loader does not load `.env` files. Do not paste tokens or secret values into shared
configuration or diagnostic output. See the [configuration guide](configuration.md)
for the supported precedence and reference syntax.

## A workflow fails or takes an unexpected route

- **Input error / exit 2:** pass one JSON object with the workflow's supported fields.
  A score of `"40"` is a string; `40` is an integer.
- **Workflow failed / exit 1:** read the exception and the last step messages. Input was not
  necessarily the problem; execution may have raised an error, such as division by zero.
- **`needs_work` / exit 0:** this is WF-03's valid below-threshold outcome.
- **Both branches run in example 04:** that is the intentional name-collision experiment.
  Method completion and a router label provide two trigger paths; its README explains them.
- **Output ordering differs in an example:** check its documented dependencies. Do not infer
  a universal scheduling order from one terminal run or from the animated diagram.
- **No trace UI or causal logs:** the current teaching prints/calls lists are not a Langfuse
  integration. Stage 02 is still a design discussion.

An intentional code experiment can make its tests fail. Review the expected assertion and
the change you made; the failure may be the behavior you are exploring. Keep changes you
want to preserve rather than resetting the whole repository.

## Checks and formatting

**Check** stops at its first failing tool. Later tools marked NOT RUN have not passed.
Use **Format** to apply formatting, review the edits, and run Check again. Formatting does
not fix type errors, every lint issue, or failing tests.

The equivalent commands from the repository root are:

```sh
app/.venv/bin/agent-playbook format
app/.venv/bin/agent-playbook check
```

## Building or selecting a release

| Message | Next action |
|---|---|
| Release requires a clean committed checkout | Inspect `git status --short`. Review and commit intended changes, including both version files if changed. Pushing is not required for a local release. |
| Version mismatch between TOML and lockfile | Use the project's version task/script to update them together, then review and commit both. |
| Output already exists | An explicit `--output` must name an unused directory. Omitting it lets the builder choose the normal version/commit directory with a numeric suffix if needed. |
| No completed matching release | Build one first, or select a version that has a completed release. Use Dev Run if you only want to exercise current source. |
| A developer command is rejected by an installed release | Run the command using the source checkout's `app/.venv/bin/agent-playbook`. Tooling is not shipped in the wheel. |

See [CLI and releases](cli.md#patch-commit-release) for the full workflow.
Running Check alone does not commit changes or make the checkout clean.

## When asking for help

Share the task name or command, whether it was source/example/release execution, the first
error, the exit code, and the relevant non-secret input. For a release, include the selected
folder and version. A screenshot of the actual error is more useful than only the final
“process finished” line. Redact credentials and private environment values.

