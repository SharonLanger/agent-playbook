# 00.2 — Call main through a command

Goal: run `agent-playbook run` and understand how it reaches the same main from 00.1.
Use the same bootstrap command: `python3 app/tooling/bootstrap.py` from repo root.

| Piece | Role |
|---|---|
| `[project.scripts]` in pyproject.toml | Maps `agent-playbook` to `agent_playbook.cli:main` |
| Bootstrap's `uv sync --locked` | Installs an editable project and creates the environment's command launcher |
| `cli/commands.py` | Parses arguments with Python's built-in argparse; `run` calls the existing main |
| `application/runner.py` | Existing sample behavior, also called by the root module entry point |

1. Run `app/.venv/bin/agent-playbook --help` (Windows: `app/.venv/Scripts/agent-playbook.exe --help`).
2. Run that executable with `run`. Expect the familiar Stage 00.1 message: we added
   a new way to invoke the existing behavior.
3. Try an unknown command; observe the usage error and nonzero exit code.
4. In PyCharm use module `agent_playbook.cli`, parameters `run`, and the existing
   `.venv` interpreter. Debug from CLI main into the imported application main.

For a bare `agent-playbook run`, activate the environment as described in
[app/README.md](../../../../app/README.md). Activation puts its executables on
this terminal's PATH; it does not install a global command.

The uv_build configuration is the minimal installation plumbing needed to expose
the command. Development installation remains editable. Versioned isolated release
builds are still reserved for 00.7. No CLI framework or new runtime dependency.

Current usage: `dev-run` runs editable code; `run` selects a built release. See [CLI documentation](../../../../app/docs/cli.md).
