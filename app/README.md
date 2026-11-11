# Stage 00.1 — Python environment

This substage introduces a virtual environment and a runnable `main()` only.
No application CLI, CrewAI, Langfuse or quality-check tools yet.

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
committed lockfile into `app/.venv/`, and run the entry point. It does not modify
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

## Run independently

From the repository root, macOS/Linux:

```sh
app/.venv/bin/python app/src/agent_playbook/__main__.py
```

Windows PowerShell:

```powershell
& app/.venv/Scripts/python.exe app/src/agent_playbook/__main__.py
```

No environment activation is necessary. This is source execution, not an installed
package or release. `agent-playbook run` is introduced in Stage 00.2.

## PyCharm

1. Open the repository's **app** folder as your project and run the bootstrap in
   its terminal (`python3 scripts/bootstrap.py`, or `py -3 scripts/bootstrap.py`).
2. In the project's Python Interpreter settings, add/select an **existing local
   interpreter**: `<repo>/app/.venv/bin/python` on macOS/Linux, or
   `<repo>\app\.venv\Scripts\python.exe` on Windows. Labels vary by PyCharm version.
3. Open `src/agent_playbook/__main__.py`; run the file with that interpreter.
   If creating a Python run configuration manually, use this file as Script path
   and `<repo>/app` as Working directory.
4. Put a breakpoint on `print(...)` inside `main()` and choose Debug. Confirm the
   breakpoint is reached, then resume and compare the expected output above.

PyCharm execution/debugging and macOS/Windows setup still require user validation;
Linux command-line verification is recorded in the stage findings.

## What to inspect

See [the short exercise](../designs/stages/00-environment/learning/00-1-python-environment.md).
Commit `pyproject.toml`, `.python-version`, `uv.lock`, source and docs. Keep
`.venv`, `.bootstrap-tools`, `.idea`, caches, build outputs and secrets out of Git.
The app has no third-party dependencies; its lockfile is intentionally small.

The first verified release is deferred to 00.7; `0.0.0` is development metadata.
