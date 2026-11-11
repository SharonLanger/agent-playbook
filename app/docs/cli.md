# CLI and releases

Run these commands from the repository root after `python3 app/scripts/bootstrap.py`.
You can either activate `source app/.venv/bin/activate` and use `agent-playbook`,
or replace it with `app/.venv/bin/agent-playbook` in each example.

| Command | Result |
|---|---|
| `agent-playbook version` | Show the version of the CLI you launched and its source metadata |
| `agent-playbook run` | Run the newest completed local release, across all versions |
| `agent-playbook run --version 0.0.1` | Run the newest completed local 0.0.1 release |
| `agent-playbook dev-run` | Run the editable source in this checkout |
| `agent-playbook check` | Run Pyright, Ruff lint, Ruff format verification, and pytest in order |
| `agent-playbook test` | Run the development tests |

`run` and `run --version` select from `app/dist/*/release.json` with an installed
release interpreter and CLI. New builds are marked verified only after their
installation checks pass; older releases are recognized by their installed CLI. Newest means the most recently written manifest, with the
folder name breaking timestamp ties. An incomplete folder is ignored. When no
matching release exists, the command fails clearly; build one first. A release
launch reports the exact folder it selected and returns that program's exit code.
`version` by itself reports the CLI you invoked, so the editable CLI reports
`development` and a release CLI reports its source commit. A release's own `run`
executes that exact release; it does not select another folder.

Editing source affects `dev-run` immediately. `run` continues to use the last
completed release until you build again. `--version` selects a version number;
it does not select a commit or a numbered attempt. For an exact build, use the
folder printed by Release:

```sh
app/dist/0.0.1-<commit-prefix>/venv/bin/agent-playbook version
app/dist/0.0.1-<commit-prefix>/venv/bin/agent-playbook run
```

The output folder can end in `-2`, `-3`, and so on. Replace the example with
the actual printed folder name.

## Change the version

From the repository root, run:

```sh
python3 app/scripts/version.py 0.0.7
```

The script locates the pinned uv installed by bootstrap (including its private
`app/.bootstrap-tools/bin/uv`), changes `app/pyproject.toml`, refreshes `app/uv.lock`,
and syncs the development environment. Review and commit **both files** in PyCharm
before Build Release. Pushing is optional for a local build; a clean committed
checkout is required. Editing only the TOML file leaves the lockfile at the old
version, and Release now reports that mismatch explicitly.

If Release reports a dirty checkout, run `git status --short` from the repository
root to see what Git still considers modified or untracked. Commit the intended
changes. The release error lists those same paths. Do not discard an unrelated
file just to make the release pass.

## Build a release

Use a clean, committed Git checkout and the bootstrapped interpreter:

```sh
app/.venv/bin/python app/scripts/release.py
```

Release first runs the full local gate, archives the exact Git commit, builds a
Wheel, records and checks its SHA-256, installs it into a separate virtual
environment, and runs it. The output in `app/dist/` contains the Wheel,
`release.json`, `SHA256SUMS`, and `venv/`. Repeating Build Release chooses the
next unused numbered directory without changing earlier builds. An explicit
`--output <new-directory>` can select a location; an existing directory is
rejected. The version remains `0.0.1` until project version metadata changes;
different builds can have the same version and distinct commit hashes. Nothing
is uploaded or published by this command.

To verify the recorded Wheel digest manually, use the values printed by Release:

```sh
app/.venv/bin/python app/scripts/verify_wheel.py <release-dir>/<wheel> <sha256>
```

## Checks and formatting

`agent-playbook check` shows numbered sections for types, lint, formatting and
tests. It stops on the first failure and finishes with PASS/FAIL/NOT RUN for each
section. A tool saying "All checks passed" inside one section only means that
part passed. `Result: PASS (4 passed, 0 failed, 0 not run)` means the whole gate
passed. Fix a failure and rerun; nothing is automatically formatted.

To format all application Python files from the `app` working directory:

```sh
.venv/bin/python -m ruff format src scripts tests
```

From the repository root, use `app/src app/scripts app/tests` as the three paths.
Ruff lint is a separate check; `ruff check --fix` applies eligible lint fixes.

## PyCharm configurations

Use interpreter `<repo>/app/.venv/bin/python` and working directory `<repo>/app`.
For Run, Dev Run, Check, Test, and Version, choose a **Python** configuration with
module `agent_playbook.cli` and parameters `run`, `dev-run`, `check`, `test`, or
`version`. To run a particular version, set parameters to `run --version 0.0.1`.
For Set Version, choose script `<repo>/app/scripts/version.py` and set parameters
to the desired version, such as `0.0.7`. For Build Release, choose script
`<repo>/app/scripts/release.py` and leave
parameters empty. For Ruff Format, choose module `ruff` and parameters
`format src scripts tests`. To run Pyright alone, choose module `pyright` with no
parameters. The release path printed by Build Release lets you invoke an exact
installed build in a terminal.

## Shared PyCharm buttons

Open the repository root (`agent-playbook`) in PyCharm. Run bootstrap once, then
register `<repo>/app/.venv/bin/python` as the **project interpreter**. The six
project files in [`.run/`](../../.run/) should appear in the Run dropdown after
pulling this branch. They use `$PROJECT_DIR$/app` as working directory and the
project interpreter, with no machine-specific interpreter path in Git.

| Button | Action |
|---|---|
| Setup | Rerun `app/scripts/bootstrap.py` using the selected project interpreter |
| Run | `agent-playbook run` — newest verified local release |
| Types | Pyright strict |
| Tests | `agent-playbook test` |
| Check | Full local quality gate |
| Release | `app/scripts/release.py` — build and verify an isolated release |

If PyCharm does not show them, confirm the repository **root** is the open project,
not the `app` subfolder, and check Run → Edit Configurations. Choose the project
interpreter locally; do not store your home directory or `.idea` settings in Git.
The first bootstrap still uses the terminal because `.venv` does not exist yet.
