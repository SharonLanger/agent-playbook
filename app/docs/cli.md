# CLI and releases

[User documentation](README.md) · [Running workflows](workflows.md) · [Troubleshooting](troubleshooting.md)

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
| `agent-playbook run --version 0.1.0` | Run the latest completed release of that version |
| `agent-playbook version` | Show version/source metadata of the CLI you invoked |
| `agent-playbook check` | Types, lint, formatting verification, then tests |
| `agent-playbook services --help` | Start, inspect or stop the local services together |
| `agent-playbook logs --help` | Start, inspect or stop only local VictoriaLogs |
| `agent-playbook langfuse --help` | Local Langfuse management and project check options |
| `agent-playbook check --types` | Pyright only |
| `agent-playbook check --lint` | Ruff lint only |
| `agent-playbook check --format` | Verify formatting without modifying files |
| `agent-playbook check --types --lint` | Combine selected checks, in normal gate order |
| `agent-playbook test` | Run pytest |
| `agent-playbook format` | Apply Ruff formatting to source, tooling and tests |
| `agent-playbook version patch` | Increase patch version; update TOML and lockfile |
| `agent-playbook version minor` | Increase minor version and reset patch |
| `agent-playbook version major` | Increase major version and reset minor/patch |
| `agent-playbook release` | Build and verify the current committed version |
| `agent-playbook release --output <new-directory>` | Build into an unused directory; relative to your invocation directory |

`check` never fixes files. Selected checks run only those checks, excluding tests;
use `test` for tests or plain `check` for the complete gate. Checks stop at the
first failure and show PASS/FAIL/NOT RUN plus a final summary. A selected check's
PASS means only that selection passed. Release always runs the complete gate.
`format` changes formatting only; it does not automatically fix lint errors.
Review its edits and rerun `check`.

## Local services

In a bootstrapped source checkout, use exactly one action with `services` or `logs`.

| Command | `--start` | `--status` | `--stop` |
|---|---|---|---|
| `agent-playbook services` | Start integrations enabled by effective configuration, VictoriaLogs first | Check both local projects and report their enabled flags and readiness | Stop Langfuse first and VictoriaLogs second, regardless of configuration |
| `agent-playbook logs` | Start local VictoriaLogs even with workflow logging disabled | Show only VictoriaLogs state and health | Stop only VictoriaLogs, retaining its named volume |

`services --start/--status --config PATH` selects application YAML; otherwise
the normal environment or checkout default applies. `services --stop` works
without application YAML. Pass `--env-file PATH` to **every** aggregate action
when Langfuse uses a custom private Compose settings file. Both paths resolve
from your invocation directory. The logging project is always
`agent-playbook-logging-smoke` on `http://127.0.0.1:9428`. Langfuse typically
uses project `observability` and `http://localhost:3000`. The local checks are
independent of workflow destinations. See [application logging](logging.md)
and [local Langfuse](langfuse-local.md).

Aggregate start with both integrations disabled exits 0 without contacting
Docker. Aggregate status exits 0 when enabled services are ready, even if a
disabled service is stopped. Every component is reported. Exit 1 indicates an
operational failure, non-ready enabled service, timeout or interruption. Exit 2
covers invalid invocation, invalid configuration or a local settings/project
conflict. An invalid selection still allows status to report both projects.
A sibling's ordinary failure does not prevent another selected component from
being attempted. Stops retain named volumes.

Start caps are 12 minutes per component and 25 minutes for the aggregate.
Status and stop caps are one minute per component and two minutes ten seconds
for the aggregate. The caps include local process cleanup. After Ctrl-C or a
timeout, inspect `--status` before retrying because Docker may still finish work.
`run` and `dev-run` never start or require these services. All local management
commands require a source checkout and exit 2 in installed releases.

## Optional local Langfuse

From a source checkout after bootstrap, use `app/.venv/bin/agent-playbook langfuse` with **exactly one** action flag:

| Flag | Action |
|---|---|
| `--start` | Initialize private local settings for a fresh project, apply Compose and wait for UI readiness |
| `--stop` | Stop this stack; retain settings and volumes |
| `--status` | Report service state and UI readiness |
| `--logs` | Show recent Docker service logs; add `--follow` to stream until Ctrl-C |
| `--open` | Print and open the UI URL without starting services |
| `--check` | Check selected application/project authentication without sending a trace or requiring local Docker |

`--env-file PATH` selects private Compose settings for local actions; `--config PATH` selects application YAML for `--check`. Relative paths resolve from the invocation directory. The files have separate owners. `--help`, invalid combinations and missing action perform no external action. Exit 0 means the selected action completed or status is ready; 1 means operational failure/non-ready; 2 means invalid invocation/configuration; 3 means the project check was disabled and skipped. Root `agent-playbook check` remains the application quality gate, separate from Langfuse `--check`. These are development-checkout commands; installed releases reject them with exit 2 and contain no deployment assets. The [setup guide](langfuse-local.md) includes the Python 3.10+ direct-script fallback for UI-only use before bootstrap.

## Select a workflow

Both `dev-run` and `run` accept `--workflow`, `--input` and `--config PATH`. The default is wf-01. Any ID configured under `workflows` may be selected; see [configuration](configuration.md#configured-workflows).
`--input` must be one JSON-object argument. These options are available from version 0.1.0.

| Workflow | Input fields/defaults | Result |
|---|---|---|
| wf-01 | No fields; omit input or `{}` | `[Hello, workflow!]` |
| wf-02 | Strict integers initial=3, increment=2, multiplier=4; each -1000..1000 | `(initial + increment) * multiplier` |
| wf-03 | Strict integer score=80, range 0..100 | `pass` for >=60; otherwise `needs_work` |

```sh
agent-playbook dev-run --workflow wf-02 --input '{"initial":10,"increment":-2,"multiplier":3}'
agent-playbook dev-run --workflow wf-03 --input '{"score":40}'
agent-playbook run --version 0.1.0 --workflow wf-03 --input '{"score":80}'
```

Unknown fields, numeric strings, booleans as integers and malformed/non-object JSON are
rejected before steps start. Exit codes: 0 for success (including needs_work), 2 for invalid
input/configuration/usage or missing release, 1 for a workflow execution failure. Every run gets a new flow.
`python -m agent_playbook` executes default WF-01 directly.

The editable release launcher forwards explicit workflow/input arguments unchanged as argv
entries; the selected release validates its own schema. A bare run can still launch an older
Stage 00 release. Sending new options to an older release surfaces its usage error rather than
silently ignoring them or running editable code.

Read [CrewAI basics](../../designs/stages/01-crewai-flows/learning/01-flow-basics.md) first, then the [overall code guide](../../designs/stages/01-crewai-flows/learning/00-reading-the-code.md)
and its per-workflow guides for code, debugging exercises and expected test outputs.

## Runtime configuration

See [configuration rules and examples](configuration.md). Runtime settings live
in `app/application.yaml`, separate from package/version metadata. Source
runs use that file by default; the source release launcher passes its path to the
selected installation. `--config PATH` overrides `AGENT_PLAYBOOK_CONFIG`; both
allow another external file. Installed releases invoked directly need one of those
selectors. An optional sibling `.local.yaml` overrides shared fields. The merged
YAML must define `secrets.file`, pointing to a readable external credentials file;
an empty file is allowed. Named credential references resolve from that file,
with process environment values taking precedence. Enable switches, URLs and
environment labels stay in YAML; documented environment overrides remain available.

Edit the file and rerun the same release: no rebuild or version bump is needed.
Configuration is read per invocation, not hot-reloaded mid-run. Missing/invalid settings
fail with exit 2 before workflow steps. Settings are validated by the selected release,
so an old release may reject a newer schema. Help/version need no configuration.

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
app/dist/<actual-release-folder>/venv/bin/agent-playbook run --config "$PWD/app/application.yaml"
```

Developer commands (`check`, `test`, `format`, `version patch/minor/major`, `release`, `langfuse`) require
the source checkout and its environment. Installed wheels reject them clearly;
checkout tooling is not bundled into the wheel.

## Patch, commit, release

1. Run `agent-playbook version patch`, for example changing `0.1.0` to `0.1.1`.
2. Review `app/pyproject.toml` and `app/uv.lock`, then commit the intended changes.
3. Run `agent-playbook release` to build and verify that committed version.
4. Run `agent-playbook run` to execute the new release.

The version command finds bootstrap's pinned uv, updates project metadata and
lockfile together, restoring both files if the update fails. It does not commit, push or build.
The bump reads the current TOML version, so repeated calls increment again.
From `0.2.7`, patch gives `0.2.8`, minor gives `0.3.0`, and major gives `1.0.0`.
In 0.x, a minor may introduce documented breaking changes; choosing 1.0 declares
stability. Set an exact version with:

```sh
python3 app/tooling/version.py 0.1.0
```

Review and commit both metadata files afterward. Do not edit TOML alone and leave
the lockfile stale; release rejects mismatched versions. Pushing is optional for
a local release. A clean committed checkout is mandatory: if release fails,
inspect the listed paths or run `git status --short`. Commit intended changes;
do not discard unrelated edits just to make the build pass.

At a maintainer bump, reconcile [CHANGELOG.md](../../CHANGELOG.md) against all merged
PRs in `previous-included-main..new-included-main`: the previous version entry’s
included-main cutoff is exclusive and this entry’s cutoff is inclusive. Do not use
the version-bump commit as the lower endpoint; its merge may follow its cutoff.
Record both commit endpoints and list each PR number/title once, including docs
and maintenance PRs already listed under Unreleased. Move those entries into a
dated version heading, keeping Unreleased for later work. Include a one-line
upgrade note for a breaking change. The version-preparation PR belongs to the next
interval if it merges after the recorded cutoff. Use Git history and GitHub merged
PRs where necessary; the local bump itself stays offline. An empty interval or an
offline clone must not invent history. The initial lower bound is the first 0.2.0
commit recorded in the changelog (#54); earlier history is not reconstructed.

For example, two successive hypothetical entries use these continuous intervals:

| Version entry | Merged-PR interval |
|---|---|
| 0.2.1 (example) | `8895c2dbf6674716656d5b780f8c181a743e44f2..cutoff-A` |
| 0.2.2 (example) | `cutoff-A..cutoff-B` |

Record actual full cutoff SHAs and dates when preparing each entry. A PR merged
after cutoff-A, including the 0.2.1 preparation PR, belongs to the second interval.
These examples do not claim releases or invent merged PRs.

## Release behavior

Release runs the full gate, archives the exact Git commit, builds a Wheel,
exports production dependencies with hashes from that same archived lockfile, installs them
in an isolated environment, then installs the hash-verified application wheel with no new
dependency resolution. It checks dependency consistency, every workflow/both routes, invalid
input, a network-denied fresh-process probe using a dedicated offline fixture, import isolation and version/source metadata. It also verifies rejection of developer
commands. It also verifies the wheel console entry point and runtime inputs,
rejects checkout-only wheel paths, and invokes the installed console outside the
checkout with a copied offline fixture. A release is marked complete only after verification succeeds.

Default output is `app/dist/<version>-<commit-prefix>/`, containing the wheel,
`release.json`, `SHA256SUMS`, `requirements.txt`, the archived `uv.lock`, and `venv/`.
The manifest records wheel, requirements and lock hashes. The wheel contains the application
package, not the repository or the entire dependency tree. The venv contains the installed
runtime dependencies; CrewAI makes it much larger than the application wheel. Dev-only pytest,
Pyright and Ruff are excluded. Dependency downloads may need network; workflow runs with telemetry/tracing disabled do not. Repeated builds choose `-2`, `-3`, etc.
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
**Setup**, the twelfth original task, runs script `app/tooling/bootstrap.py`.
Stage 01 adds **WF-01 Sequence**, **WF-02 State**, **WF-03 Route** with `dev-run --workflow wf-0N`.
It also adds **Test WF-01**, **Test WF-02**, **Test WF-03**, using module `pytest` with
`-q tests/workflows/<named-workflow-folder>`. All 18 tasks use the project interpreter.
For an exact version, manually run `app/tooling/version.py` with the
version as its parameter. If tasks are missing, confirm the repository root is
open and inspect Run → Edit Configurations. Existing manually saved tasks may
need their module/parameters updated; avoid duplicate names.

## Folder migration

Scripts moved from `app/scripts/` to `app/tooling/`; typing exercises now live in
`app/examples/`. Bootstrap, CLI dispatch, shared tasks and the gate use those paths.
The gate covers `src`, `tooling`, and `tests`. The personal `examples/` directory
is excluded from the application gate and release. From `app/`, you can inspect
or format it explicitly whenever you choose:

```sh
python -m ruff check examples
python -m ruff format --check examples
python -m ruff format examples
```

These commands are manual; the last one changes example files.
See the [guarded project structure](../../designs/project-structure.md).


Configured aliases use the same `--workflow` option. The CLI displays serialized output; Python `run_workflow()` returns a typed native `output` and `serialized_output`. Configuration/selection/input errors exit 2; prepare defects, CrewAI execution, output validation and serialization errors exit 1.

The application loads only the selected workflow’s concrete CrewAI flow. A setup or constructor defect exits 1; the failure message names the configured ID and phase. Validation messages report field/type without input values. A release build verifies every built-in workflow despite this per-run loading.

For a CrewAI step failure, the CLI suppresses CrewAI's raw error log and prints its classified workflow/phase message. Python callers can inspect the preserved exception cause locally.
