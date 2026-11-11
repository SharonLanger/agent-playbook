# Stage 00.6 — Unified checks

Adds one fail-fast check command: Pyright, Ruff lint, Ruff format verification, then pytest.

## Read the check results

Run `agent-playbook check`, or use your PyCharm Python configuration with module
`agent_playbook.cli`, parameters `check`, interpreter `app/.venv` and working
directory `<repo>/app`.

The order is always **1. types → 2. lint → 3. formatting → 4. tests**.
Each numbered section shows the command, its original diagnostics and PASS/FAIL.
The summary at the bottom distinguishes a failed check from one that never ran.
For example, if formatting fails:

```text
Check summary
  PASS     Pyright (types)
  PASS     Ruff (lint)
  FAIL     Ruff (formatting) (exit 1)
  NOT RUN  pytest (tests)

Result: FAIL (2 passed, 1 failed, 1 not run)
```

`All checks passed!` inside Ruff's section refers only to lint. Only the final
`Result: PASS (4 passed, 0 failed, 0 not run)` means the whole gate passed.
The gate stops at the first failure and preserves its exit code. Fix that failure
and rerun; the next check may then reveal a separate problem. Nothing is auto-fixed.
If a tool is missing, no checks start; the summary identifies the missing tool and
the message directs you to rerun bootstrap.

## One setup command

Prerequisite: Python **3.10+ with `venv` and `ensurepip`** (the standard Python
installer includes them; some Linux distributions package them separately).
Initial setup needs network access to PyPI/files.pythonhosted.org if uv is
missing, and GitHub release downloads if Python 3.13.5 is missing.

From the repository root, on macOS/Linux:

```sh
python3 app/scripts/bootstrap.py
```

On Windows, use `py -3 app/scripts/bootstrap.py`.
The script also works from another directory if given its absolute path.
It reuses uv **0.13.6** from PATH or installs that version in
`app/.bootstrap-tools/`, then uses uv to prepare Python **3.13.5**, sync the
committed lockfile into `app/.venv/`, install the project in editable development mode, and run `agent-playbook run`. It does not modify
global Python packages. The prerequisite Python launches setup; `.venv` runs
the application. uv can download the application interpreter if needed.

Run the same command again to verify repeatable setup. A missing or stale lockfile
causes failure rather than a silent lockfile rewrite (`uv sync --locked`).
Expected application output:

```text
Agent Playbook — Stage 00.1: Python environment ready.
```

The final setup line prints the interpreter path. Any failed setup step exits
nonzero; fix the reported prerequisite/network problem and rerun the same command.
Concurrent bootstrap runs in one checkout are not supported.

## Run the CLI

From the repository root, macOS/Linux:

```sh
app/.venv/bin/agent-playbook run
app/.venv/bin/agent-playbook --help
```

Windows PowerShell: `& app/.venv/Scripts/agent-playbook.exe run`.
To use the short command, activate the environment in your terminal:

```sh
source app/.venv/bin/activate
agent-playbook run
```

On Windows PowerShell activation is `app/.venv/Scripts/Activate.ps1`; using
the explicit executable path avoids any activation-policy requirements.
Missing/unknown commands and unexpected arguments exit with code 2. The output
still says Stage 00.1 because `run` invokes that unchanged sample main.

## Run main independently

From the repository root, macOS/Linux:

```sh
app/.venv/bin/python app/src/agent_playbook/__main__.py
```

Windows PowerShell:

```powershell
& app/.venv/Scripts/python.exe app/src/agent_playbook/__main__.py
```

No environment activation is necessary for the explicit paths above.
The project is now installed in editable development mode, so source edits are
visible immediately. This is not the isolated release introduced at 00.7.

## PyCharm

1. Open the repository's **app** folder as your project and run the bootstrap in
   its terminal (`python3 scripts/bootstrap.py`, or `py -3 scripts/bootstrap.py`).
2. In the project's Python Interpreter settings, add/select an **existing local
   interpreter**: `<repo>/app/.venv/bin/python` on macOS/Linux, or
   `<repo>\app\.venv\Scripts\python.exe` on Windows. Labels vary by PyCharm version.
3. Open `src/agent_playbook/__main__.py`; run the file with that interpreter.
   If creating a Python run configuration manually, use this file as Script path
   and `<repo>/app` as Working directory.
4. For the CLI, create another Python configuration: **Module name** =
   `agent_playbook.cli`, **Parameters** = `run`, working directory = `<repo>/app`,
   interpreter = the same `.venv` Python. This executes the same CLI function
   registered by the console command.
5. Put a breakpoint on `print(...)` inside `main()` and choose Debug. Confirm the
   breakpoint is reached, then resume and compare the expected output above.

Actual PyCharm UI/debugging and macOS/Windows setup require user validation;
Linux command-line verification is recorded in the stage findings.

## Commands accumulated on this branch

From repo root, after bootstrap and `source app/.venv/bin/activate`:

```sh
agent-playbook run
agent-playbook test
agent-playbook check
```

For Windows, bootstrap uses `py -3 app/scripts/bootstrap.py`; executable paths
are `app/.venv/Scripts/python.exe` and `app/.venv/Scripts/agent-playbook.exe`.
No activation is necessary when using their explicit paths.

PyCharm commands: module `agent_playbook.cli`, parameters `run` or another command
listed above; interpreter `app/.venv`, working directory `app`. Pyright alone:
module `pyright`, no parameters, working directory `app`. These configurations
use the installed tools; native editor inspections are separate from Pyright.

See [00.6 exercise](../designs/stages/00-environment/learning/00-6-unified-checks.md)
and [verification evidence](../designs/stages/00-environment/findings.md).

Bootstrap installs everything introduced so far and checks it. Pyright uses Node;
its wrapper provisions Node when absent (network access needed). That fallback
and non-Linux platforms are unverified here. Python runtime dependencies remain
empty; the tools are development dependencies. No CrewAI, Langfuse or CI.
