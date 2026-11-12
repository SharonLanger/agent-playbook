# CLI and releases

From the repository root, run `python3 app/tooling/bootstrap.py` once.
Activate `source app/.venv/bin/activate` to use `agent-playbook`, or replace it
with `app/.venv/bin/agent-playbook` in the commands below. The equivalent Python
module entry point is `python -m agent_playbook.cli`.

## Commands

| Command | Action |
|---|---|
| `agent-playbook --help` | List commands; each command also accepts `--help` |
| `agent-playbook dev-run` | Run current editable source; edits take effect immediately |
| `agent-playbook run` | Run the latest completed local release |
| `agent-playbook run --version 0.0.8` | Run the latest completed release of that version |
| `agent-playbook version` | Show version/source metadata of the CLI you invoked |
| `agent-playbook check` | Types, lint, formatting verification, then tests |
| `agent-playbook check --types` | Pyright only |
| `agent-playbook check --lint` | Ruff lint only |
| `agent-playbook check --format` | Verify formatting without modifying files |
| `agent-playbook check --types --lint` | Combine selected checks, in normal gate order |
| `agent-playbook test` | Run pytest |
| `agent-playbook format` | Apply Ruff formatting to source, tooling, examples and tests |
| `agent-playbook version patch` | Increase patch version; update TOML and lockfile |
| `agent-playbook release` | Build and verify the current committed version |
| `agent-playbook release --output <new-directory>` | Build into an unused directory; relative to your invocation directory |

`check` never fixes files. Selected checks run only those checks, excluding tests;
use `test` for tests or plain `check` for the complete gate. Checks stop at the
first failure and show PASS/FAIL/NOT RUN plus a final summary. A selected check's
PASS means only that selection passed. Release always runs the complete gate.
`format` changes formatting only; it does not automatically fix lint errors.
Review its edits and rerun `check`.

## Editable source versus releases

`dev-run` executes the source you are editing. `run` uses a previously built
release, so source changes require another build before they appear there.

The editable CLI selects from `app/dist/*/release.json`, requiring an installed
interpreter/CLI and a completed verification marker (legacy manifests are supported).
Newest means the most recently written manifest, with folder name breaking ties.
Incomplete releases are skipped; missing versions fail with an actionable error.
The selected folder is printed and the launched program's exit code is returned.

`version` reports the invoked CLI: development reports `development` as its source;
a built release reports its source commit. An installed release's own `run` runs
that exact release rather than searching for another. For an exact build:

```sh
app/dist/<actual-release-folder>/venv/bin/agent-playbook version
app/dist/<actual-release-folder>/venv/bin/agent-playbook run
```

Developer commands (`check`, `test`, `format`, `version patch`, `release`) require
the source checkout and its environment. Installed wheels reject them clearly;
checkout tooling is not bundled into the wheel.

## Patch, commit, release

1. Run `agent-playbook version patch`, for example changing `0.0.8` to `0.0.9`.
2. Review `app/pyproject.toml` and `app/uv.lock`, then commit the intended changes.
3. Run `agent-playbook release` to build and verify that committed version.
4. Run `agent-playbook run` to execute the new release.

The version command finds bootstrap's pinned uv, updates project metadata and
lockfile, and syncs the editable environment. It does not commit, push or build.
The bump reads the current TOML version, so repeated calls increment again.
There is no automatic major/minor bump command. Set an exact version with:

```sh
python3 app/tooling/version.py 0.1.0
```

Review and commit both metadata files afterward. Do not edit TOML alone and leave
the lockfile stale; release rejects mismatched versions. Pushing is optional for
a local release. A clean committed checkout is mandatory: if release fails,
inspect the listed paths or run `git status --short`. Commit intended changes;
do not discard unrelated edits just to make the build pass.

## Release behavior

Release runs the full gate, archives the exact Git commit, builds a Wheel,
records and verifies SHA-256, installs in an isolated environment, then checks
execution and version/source metadata. It also verifies rejection of developer
commands. A release is marked complete only after verification succeeds.

Default output is `app/dist/<version>-<commit-prefix>/`, containing the wheel,
`release.json`, `SHA256SUMS` and `venv/`. Repeated builds choose `-2`, `-3`, etc.
An explicit output directory must not exist. Builds preserve the committed version;
no automatic bump, commit, push or upload occurs. The script remains available:

```sh
app/.venv/bin/python app/tooling/release.py
app/.venv/bin/python app/tooling/verify_wheel.py <wheel-path> <recorded-sha256>
```

## Shared PyCharm tasks

Open the repository root, run bootstrap, and select `<repo>/app/.venv/bin/python`
as the project interpreter. Shared `.run/` files use `$PROJECT_DIR$/app` as their
working directory and the selected interpreter, with no machine-specific paths.

| Button | Module parameters |
|---|---|
| Dev Run | `dev-run` |
| Run | `run` |
| Types | `check --types` |
| Lint | `check --lint` |
| Format Check | `check --format` |
| Format | `format` (changes files) |
| Tests | `test` |
| Check | `check` |
| Version | `version` |
| Bump Patch | `version patch` (changes version metadata) |
| Release | `release` |

These are Python configurations using module `agent_playbook.cli`.
**Setup**, the twelfth task, runs script `app/tooling/bootstrap.py`.
For an exact major/minor version, manually run `app/tooling/version.py` with the
version as its parameter. If tasks are missing, confirm the repository root is
open and inspect Run → Edit Configurations. Existing manually saved tasks may
need their module/parameters updated; avoid duplicate names.

## Folder migration

Scripts moved from `app/scripts/` to `app/tooling/`; typing exercises now live in
`app/examples/`. Bootstrap, CLI dispatch, shared tasks and the gate use those paths.
The gate covers `src`, `tooling`, `examples`, and `tests`. For direct Ruff usage,
run `python -m ruff format src tooling examples tests` from `app`.
See the [guarded project structure](../../designs/project-structure.md).
