# TEMPORARY HANDOFF — CLI, development tooling, and release refactoring

> **Disposable working document. Not an approved architecture baseline.**
> This file exists to transfer a completed review to the implementation agent.
> It may be deleted after the useful work and its verification have been recorded in implementation PRs.
> Do not make runtime code, tests, or permanent documentation depend on this file.

| Field | Value |
|---|---|
| Repository | SharonLanger/agent-playbook |
| Reviewed branch | main |
| Reviewed commit | 4c9e74dcaf6897f6337f367dbbf17177bbada6c1 |
| Review and handoff date | 2026-11-12 |
| Suggested location | designs/temporary/cli-tooling-release-refactor-handoff.md |
| Current delivery | Documentation-only handoff in a separate draft PR |
| Code implementation in this delivery | None |
| User objective | Make CLI/tooling easier to extend, remove, change, and test, without abstractions that do not pay for themselves |
| Highest-value starting work | Consistent tooling imports, shared pinned-uv resolution, focused release functions |

## 1. Read this first: state, next action, and authority

Sharon requested an honest review of the main branch, especially CLI commands, development tooling, release scripts, and opportunities to extract useful functions or reusable components. The review concluded that the existing component boundaries are sensible. It did not recommend a broad redesign, a generic utilities layer, or a class hierarchy.

Sharon then requested a very detailed Markdown handoff for another agent and suggested a separate PR with an obviously temporary document under designs. This document fulfills that request. The handoff PR itself is documentation only; it does not establish that any proposed code refactor has already been approved or implemented.

### Immediate next actions for the receiving agent

1. Read this section and the priority table in section 4.
2. Read the current root AGENTS.md and the required design documents listed there.
3. Read designs/project-structure.md before deciding where helpers belong.
4. Compare the current main branch with the reviewed commit. Re-check any finding whose source changed.
5. Read the current source and tests named in sections 3 and 5–9.
6. Follow the implementation authorization in your receiving conversation. Do not infer blanket permission to alter guarded architecture from this handoff.
7. Start with the concrete import and uv-resolution problems, then extract release steps.
8. Preserve the command compatibility and release invariants in sections 10–11.
9. Run meaningful regression tests and the full local gate for actual code changes.
10. Record the resulting commits, verification, remaining limitations, and rejected suggestions in the implementation PR.

### Which documents govern what

Read these documents in the repository, rather than relying solely on this handoff:

- AGENTS.md
- designs/README.md
- designs/charter.md
- designs/architecture.md
- designs/principles.md
- designs/roadmap.md
- designs/progress.md
- designs/project-structure.md
- designs/stages/00-environment/architecture.md
- designs/stages/00-environment/plan.md
- app/docs/cli.md
- app/README.md

The current project-structure document is the approved layout authority. The historical Stage 00 architecture still contains old approval wording and an old layout; progress.md explicitly records those discrepancies. Do not restore the obsolete layout or silently edit the protected historical documents while doing this refactor.

Ordinary helper files inside an existing ownership boundary are different from changing component responsibilities. Keep tooling helpers in app/tooling, CLI parsing and checkout invocation in cli, and runtime release selection in releases. Changes to guarded boundaries or protected design text need the applicable exact-diff review.

The temporary document does not override those rules. It also does not create Stage 01 behavior, authorize CrewAI/Langfuse integration, or redefine a workflow design.

## 2. How to use and remove this handoff

### Recommended PR usage

Keep this handoff in its own draft PR. The receiving agent can read its branch or fetch this single file without merging it into main.

A useful implementation workflow is:

1. Read the handoff from its PR.
2. Start the implementation branch from the current main.
3. Carry across only the relevant code changes and durable operational documentation.
4. Reference this handoff PR from the implementation PR for review context.
5. Close the handoff PR when its purpose is complete.

If the handoff is merged for convenience, deleting this one file later is expected. Remove the temporary directory if it becomes empty. Do not delete unrelated temporary documents or another agent's work.

### What must survive deletion

The implementation PR or durable documentation should preserve:

- The concrete problem fixed.
- The final behavior and any intentional behavior changes.
- Commands and interfaces that remain supported.
- Actual verification results and limitations.
- Any unresolved decision that still affects the project.

Do not add a permanent documentation link to this temporary file. This keeps deletion uncomplicated and avoids broken navigation. A new README or a link from designs/README.md is unnecessary for this one-file handoff.

## 3. Reviewed inventory and current ownership

The review inspected the active Python code, existing tests, all twelve shared PyCharm configurations, CLI documentation, and both diagram-generation scripts. Historical sandbox experiments were outside the active refactoring scope.

| Area | Files | Current responsibility | Assessment |
|---|---|---|---|
| CLI | app/src/agent_playbook/cli/commands.py | Parse arguments, route commands, show metadata | Small cleanup useful; no command framework needed |
| Development bridge | app/src/agent_playbook/cli/development.py | Invoke checkout-only scripts as subprocesses | Keep this boundary; remove positional option assumptions |
| Application | app/src/agent_playbook/application/runner.py | Existing Stage 00 example | Leave simple |
| Release selection | app/src/agent_playbook/releases/selection.py | Find and launch completed local releases | Optional explicit directory input |
| Bootstrap | app/tooling/bootstrap.py | Provision pinned tools/environment and run checks | Share discovery; retain installation responsibility |
| Quality checks | app/tooling/checks.py | Select checks, run them in order, report results | Already reasonably factored |
| Version update | app/tooling/version.py | Patch/exact version changes through pinned uv | Share resolution; preserve mutation/error semantics |
| Release build | app/tooling/release.py | Validate, archive, build, install, verify, mark complete | Highest-value functional decomposition |
| Hash verification | app/tooling/verify_wheel.py | Validate an expected SHA-256 digest | Already small and reusable |
| Packaging | app/pyproject.toml, app/uv.lock, app/.python-version | Dependency/toolchain pins and package configuration | Preserve pins and package boundaries |
| IDE tasks | .run/*.run.xml | Portable PyCharm command entry points | Keep hand-maintained unless real repetition costs emerge |
| Diagram generation | designs/diagrams/render.py, build_viewer.py | Generate SVGs and local HTML gallery | Defer refactoring until further work requires it |

At the reviewed revision:

- The project version is 0.0.10.
- Application Python is constrained to >=3.13,<3.14.
- Bootstrap advertises Python 3.10+ as its starting interpreter.
- uv is pinned to 0.13.6.
- uv_build is pinned to 0.13.6.
- Development tools are pyright 1.1.407, pytest 8.4.2, and ruff 0.14.4.
- Runtime dependencies are currently empty.
- The installed package is under app/src/agent_playbook.
- Checkout-only tooling and learning examples must remain outside the Wheel.
- No GitHub Actions CI is required by this work.

Re-read configuration before implementation; these are snapshot facts, not a request to freeze future upgrades indefinitely.

## 4. Recommendations, ordered by value

| ID | Priority | Recommendation | Why it earns its complexity |
|---|---|---|---|
| R1 | High | Share pinned-uv discovery and validation | Existing implementations disagree under a realistic installation layout |
| R2 | High | Extract focused operations from build_release | One function currently owns almost the entire release lifecycle |
| R3 | Medium; implement early | Make tooling imports consistent | Normal module import fails and tests compensate with sys.path changes |
| R4 | Medium | Separate parser construction and normalize named options before forwarding | Easier tests and fewer option-order assumptions |
| R5 | Low; optional | Pass a release search directory into discovery | Removes tests' dependency on patching __file__ |

Suggested execution order is R3 → R1 → R2 → R4, with R5 only if its small benefit is useful in the implementation scope. Priority and dependency order are not the same thing: import cleanup supports subsequent helper extraction.

These are focused refactors with two observed problems. Avoid turning the list into a mandate to create every possible module, data class, or test seam.

## 5. R1 — Share pinned-uv discovery and validation

### Source evidence

- app/tooling/bootstrap.py, especially UV_VERSION and main's discovery/provisioning logic.
- app/tooling/version.py, especially the candidate loop around lines 38–57.
- app/tooling/release.py, especially uv selection around lines 73–84.
- app/pyproject.toml, particularly tool.uv.required-version and the build backend pin.

The three scripts perform similar work but implement different policies.

| Script | Relevant behavior at reviewed revision |
|---|---|
| bootstrap.py | Checks PATH uv; if its version differs, provisions the private copy |
| version.py | Tries PATH uv, then an existing private copy when PATH reports a different version |
| release.py | Picks PATH uv whenever present, then rejects it if its version differs; does not try the private copy in that case |

### Confirmed problem

Given:

- PATH resolves to an uv reporting a version other than 0.13.6.
- The checkout has a usable private uv reporting 0.13.6.

The version command can select the private tool, while release rejects the setup with:

~~~text
Release requires uv 0.13.6; use the bootstrap-provisioned uv on PATH.
~~~

This disagreement was reproduced with controlled subprocess responses. It was not reproduced through a real uv installation or full release build. The distinction matters when reporting evidence.

There is additional static evidence of drift: version.py constructs a private bin/uv path, while bootstrap.py and release.py contain Windows path handling. This is not a claim that the entire project currently supports Windows; release selection and documented commands are still POSIX-oriented.

### Proposed implementation

Introduce a focused Python-standard-library helper under app/tooling, such as toolchain.py.

Reasonable responsibilities:

- Return the private executable location for the current platform.
- Probe an executable's reported version.
- Choose a usable pinned uv from the permitted candidates.
- Report an actionable failure when none is suitable.

Illustrative interfaces, not mandatory signatures:

~~~python
def private_uv_path(app: Path) -> Path: ...
def probe_uv_version(executable: Path) -> str | None: ...
def find_pinned_uv(app: Path) -> Path | None: ...
def require_pinned_uv(app: Path) -> Path: ...
~~~

Use fewer functions if that is clearer. Avoid exposing internal details solely to create tiny functions.

Bootstrap should install/provision when discovery returns no suitable executable. Versioning and release should fail with a setup instruction; they should not silently install developer tools.

### Pin ownership and Python compatibility

Consolidate the Python-side expected uv version instead of keeping one literal in each script.

Do not blindly import tomllib from a helper loaded by bootstrap: tomllib is unavailable in Python 3.10, and bootstrap must still start before the project's Python 3.13 environment exists.

A practical approach is:

- One Python-3.10-compatible toolchain constant used by the scripts.
- Keep declarative pins in pyproject.toml.
- Check consistency of those values in an appropriate regression check.

Alternatively use an equally simple solution that preserves bootstrap's starting requirements. Do not introduce a TOML dependency just to eliminate one configuration assertion. Do not assume the uv CLI and uv_build backend must always share a version merely because they currently do.

### Error handling details

Distinguish discovery failures from operation failures.

- A candidate that cannot be started or reports malformed output should not produce an IndexError.
- It can be reasonable to continue to another candidate during discovery.
- Once a valid executable has started a version-changing operation, a failed mutation must be reported. Do not automatically rerun the mutation against another candidate.
- Preserve useful underlying error context.
- Do not mutate PATH globally or require the user to reorder PATH when the private pinned copy is already usable.

### Regression scenarios

Test the behavior, not shutil.which itself:

1. Correct PATH uv is accepted.
2. Incorrect PATH uv plus correct private uv selects the private copy.
3. No PATH uv plus correct private uv succeeds.
4. No acceptable candidate produces a clear setup instruction.
5. Malformed version output is handled without an uncaught indexing error.
6. Candidate probe failure has the intended fallback behavior.
7. Bootstrap remains the only consumer that provisions missing uv.
8. Version mutation failure does not cause a second mutation attempt.

Cover platform path construction only to the extent it is part of existing toolchain behavior; do not expand this task into a Windows-support project.

## 6. R2 — Split release orchestration into focused operations

### Source evidence

app/tooling/release.py defines build_release at line 48. It spans approximately 135 lines and currently performs all of the following:

1. Locate the Git repository.
2. Reject dirty tracked or untracked work.
3. Capture the source commit.
4. Read the project version and compare it with uv.lock.
5. Choose an unused release destination.
6. Resolve and validate uv.
7. Run the full quality gate.
8. Verify the checkout and HEAD did not change during checks.
9. Archive the exact committed app tree.
10. Inject build metadata into the temporary archive.
11. Build a Wheel.
12. Require exactly one Wheel output.
13. Compute and record its digest.
14. Write incomplete release evidence.
15. Verify the Wheel digest.
16. Create an isolated environment and install the Wheel.
17. Execute the installed application.
18. Check installed version/source metadata.
19. Check the imported module's location.
20. Check rejection of developer commands.
21. Mark the release verified.
22. Present the final evidence.

Each individual step is understandable. The maintenance problem is that unrelated lifecycle operations and their side effects are all concentrated in one function.

### Proposed decomposition

Keep build_release as the readable coordinator. Start with focused functions in the same module; additional files are not required merely because functions were extracted.

| Possible function | Responsibility | Useful result |
|---|---|---|
| validate_release_source | Clean checkout, commit, metadata/lock agreement | Validated source information |
| assert_source_unchanged | Verify clean state and same HEAD after the gate | Success or clear failure |
| build_wheel | Archive the exact source, inject metadata, build, identify Wheel | Wheel path |
| write_release_manifest | Serialize release evidence consistently | No hidden build/install activity |
| install_release | Create environment and install the artifact | Installed interpreter/environment path |
| verify_installed_release | Run application, verify metadata/location and rejection behavior | Verified evidence or failure |

Names and exact grouping are suggestions. A helper should correspond to a meaningful responsibility, not just move five lines elsewhere.

Keep the temporary archive's cleanup lifetime explicit. If an operation returns a path to a temporary directory, ensure that directory still exists for its consumer. Do not accidentally return a path after its TemporaryDirectory context has ended.

### Functions versus classes

Plain functions are sufficient for this pipeline.

A small immutable data class may be useful if the same related source values repeatedly travel between functions, for example repository path, application path, version, and commit. Introduce it only if it reduces confusing parameter lists.

Do not introduce:

- A stateful ReleaseManager coordinating mutable hidden state.
- An abstract build pipeline.
- A generic task graph.
- A plugin registry for build steps.
- A dependency-injection container.
- A persistence/retry framework.

The current linear flow is a strength. Preserve it.

### Required behavioral invariants

- Validate before starting expensive or mutating release steps.
- The full gate remains mandatory for release.
- The checkout must remain clean and on the same commit after the gate.
- Archive the captured commit, rather than the live working tree.
- Inject build information only into the temporary archived source.
- Preserve the committed project version; release must not bump or commit.
- Existing output must not be overwritten.
- Default repeated builds must select a new suffixed directory.
- Explicit output paths must be resolved from the caller's working directory.
- Require exactly one Wheel.
- Verify the recorded digest before installation.
- Keep incomplete releases visibly incomplete.
- Do not mark a release verified if execution, metadata, location, or developer-command verification fails.
- Preserve isolation flags and environment handling.
- Propagate failures clearly; do not report a completed release after partial success.
- Do not introduce auto-push, publication, or release uploads.

An atomic manifest-write strategy may be worth considering if concurrent discovery becomes a real requirement, but it is not a prerequisite for the functional extraction. Do not silently bundle a larger publication protocol into this task.

### Regression tests that justify the extraction

Existing tests cover dirty-checkout reporting, version mismatch, output collision behavior, and hash rejection. Preserve them, but adapt their setup to normal imports.

The valuable additions concern failure boundaries:

- Gate failure prevents build/install.
- A changed HEAD or dirty checkout after checks aborts.
- A build producing zero or multiple Wheels fails.
- Hash failure prevents installation.
- Installation/verification failure leaves no verified=true completion marker.
- Incorrect installed metadata fails verification.
- An imported source location outside the isolated environment fails verification.
- A release accepting a developer command fails verification.
- Success marks completion only after all required verification passes.

Use temporary directories and targeted subprocess seams. Avoid tests that only assert the extracted functions are called in a particular order while ignoring the behavioral outcome.

Do not recursively launch the full check command from a unit test that itself runs inside pytest. Keep the quality-gate boundary mocked for unit tests and exercise the complete release separately.

### Scope caution for future dependencies

The release currently installs the Wheel with --no-deps, and runtime dependencies are currently empty. That is compatible with the reviewed Stage 00 application.

When runtime dependencies are added, installation and reproducibility policy will need an explicit decision. Do not remove --no-deps or add dependency installation as an incidental part of this behavior-preserving refactor. Record it as a future integration concern, not a present failure of the dependency-free release.

## 7. R3 — Make tooling consistently importable

### Confirmed problem

release.py contains:

~~~python
from verify_wheel import verify_wheel
~~~

That import works when release.py is executed as a script because Python puts the script directory on its import path. It fails under a normal package-style import from app:

~~~python
from tooling import release
~~~

The observed error was:

~~~text
ModuleNotFoundError: No module named 'verify_wheel'
~~~

Both test_release_destination.py and test_release_preflight.py temporarily prepend app/tooling to sys.path before importing the module. There are four such test-local insertion blocks across those two files.

### Goal

Reusable tooling implementation should import normally. Tests should not repair its import environment individually.

### Implementation guidance

Choose one consistent import strategy for app/tooling and verify both package-style imports and supported direct script entry points.

A workable design is:

- Importable implementation uses explicit tooling package imports.
- CLI-facing script entry points remain thin.
- Internal subprocess invocations can use module execution from app where appropriate.
- Preserve documented direct-script entry points through compatible launchers if the internal invocation style changes.

Adding an __init__.py alone does not fix sibling absolute imports, and replacing them with relative imports alone can break direct script execution. Evaluate both modes.

If a compatibility launcher must explicitly add the app root to the import path, keep that adjustment small and confined to the launcher. The goal is not to hide the same sys.path mutation in every module or every test.

Do not force the installed runtime package to import tooling. The current subprocess bridge exists precisely to keep developer code out of installed runtime dependencies.

### Required checks

1. Import tooling.release normally from the app project context.
2. Import the new shared toolchain helper normally.
3. Run supported scripts with --help or another safe path.
4. Verify script execution from a different working directory.
5. Remove the test-local sys.path insertion/pop blocks.
6. Run the existing release tests after adapting imports.
7. Inspect the built Wheel to ensure tooling did not enter the installed runtime package.

This change should support R1 and R2, not become a separate packaging framework.

## 8. R4 — Simplify CLI parsing and remove positional forwarding assumptions

### Current parser shape

commands.py currently constructs the entire argparse parser and dispatches its result in main. The file is small enough that a command-class architecture would be excessive.

A minimal improvement is:

~~~python
def build_parser() -> argparse.ArgumentParser: ...
def main(argv: list[str] | None = None) -> int: ...
~~~

main(None) should continue parsing the process arguments, preserving the console entry point. Tests can pass explicit argument lists instead of patching global sys.argv.

Keep uncomplicated dispatch branches readable. Extract only branches with enough behavior to deserve a separate function. Do not create a file or class for each tiny command.

### Concrete forwarding weakness

development.py currently does this:

~~~python
if command == "release" and arguments:
    arguments[1] = str(Path(arguments[1]).resolve())
~~~

It assumes that the second item is the output path. That is true for the current caller, which constructs ["--output", value].

It becomes wrong if the forwarding convention later puts another option before --output. A synthetic probe with a preceding option demonstrated that the unrelated option value was resolved as a path instead.

This is an extensibility weakness, not a claim that the existing public CLI accepts that synthetic option or that current --output use is broken.

### Proposed change

Resolve the parsed, named output value at the CLI boundary, before converting it into subprocess arguments. The development bridge should receive arguments already prepared for forwarding.

Preserve:

- Output paths relative to the user's invocation directory.
- Tooling execution with the application directory as cwd.
- Existing stderr messages and meaningful exit codes.
- Rejection of developer commands in installed releases.
- Existing behavior for no output option.

Do not parse command arguments twice or replace one positional assumption with a general-purpose option parser inside the bridge.

### Regression cases

- No-argument invocation still reports the required command.
- Unknown command still produces argparse exit status 2.
- All current dispatch mappings remain valid.
- check selectors retain normal gate order.
- release --output relative-path reaches tooling as the correct absolute path.
- Absolute output paths remain correct.
- A path containing spaces remains one subprocess argument.
- The installed-release guard prevents developer subprocess launch.
- main([...]) and the console/module entry points have equivalent behavior.

## 9. R5 — Optional explicit release discovery directory

### Current behavior

find_release currently derives app from __file__. Its tests patch that module attribute to point discovery at a temporary tree.

The production lookup is short and understandable. This is a small testability improvement, not urgent architectural debt.

### Suggested change

Let discovery accept an explicit directory. Keep the normal CLI behavior pointed at app/dist.

For example, the caller can choose the directory and invoke:

~~~python
def find_release(
    requested_version: str | None,
    releases_dir: Path,
) -> tuple[Path, str] | None: ...
~~~

An optional parameter preserving an internal call signature is also acceptable. Choose the simplest API with a clear caller.

### Preserve selection semantics

- Scan local release manifests under the selected root.
- Keep version filtering.
- Skip incomplete/unverified releases.
- Preserve documented legacy-manifest support.
- Require the installed executable and CLI files as today.
- Preserve newest-manifest ordering and folder-name tie-breaking.
- Return the launched program's exit code.

Do not silently change the current missing-verified-marker compatibility policy. The implementation currently uses data.get("verified", True); removing legacy acceptance is a separate behavior decision.

Do not add a new public --release-root option, an index database, a release repository class, or a manifest schema framework just to improve test setup.

External directories created through release --output are not automatically added to app/dist discovery today. This refactor should not silently change that behavior.

## 10. Compatibility checklist: public commands and entry points

### Application commands

| Invocation | Behavior to preserve |
|---|---|
| agent-playbook --help | Show available commands |
| agent-playbook dev-run | Execute editable application source |
| agent-playbook run | In development, choose the latest completed local release |
| agent-playbook run --version VERSION | Choose the newest completed local release of that version |
| Installed release: agent-playbook run | Execute that installed release |
| Installed release: run --version OTHER | Reject selecting another version |
| agent-playbook version | Report invoked package version and source metadata |
| agent-playbook version patch | Update checkout version metadata through pinned uv |
| agent-playbook test | Run pytest |
| agent-playbook check | Run types, lint, format verification, then tests |
| agent-playbook check --types / --lint / --format | Run selected checks in normal gate order; exclude tests |
| agent-playbook format | Apply formatting; do not automatically fix lint |
| agent-playbook release | Build and verify committed version |
| agent-playbook release --output PATH | Use an unused output directory relative to the invocation location |

### Python and script entry points

Preserve these documented modes:

~~~sh
python -m agent_playbook.cli --help
python -m agent_playbook.cli dev-run
python -m agent_playbook
python3 app/tooling/bootstrap.py
app/.venv/bin/python app/tooling/release.py --help
python3 app/tooling/version.py 0.1.0
app/.venv/bin/python app/tooling/verify_wheel.py WHEEL SHA256
~~~

The exact-version command above mutates metadata; it is a compatibility example, not a command to run indiscriminately during review.

The direct package entry point, python -m agent_playbook, currently invokes the application runner. It is not identical to the full CLI parser. Preserve this distinction unless a separate change is requested.

### Installed-release restrictions

Existing release verification checks rejection of test, check, format, release, and version patch. dev-run is separately rejected by commands.py in installed-release mode. Preserve all these restrictions.

Do not accidentally make developer functionality available because a new helper is importable. Importable within the checkout does not mean shipped in the Wheel.

### PyCharm tasks

Preserve the twelve named configurations:

- Setup
- Dev Run
- Run
- Types
- Lint
- Format Check
- Format
- Tests
- Check
- Version
- Bump Patch
- Release

They use the selected project interpreter and portable project-relative paths. Update them only when an actual entry-point change requires it. Do not generate machine-specific interpreter paths or commit .idea state.

## 11. Quality-check behavior that should stay intact

checks.py already separates command selection, execution, labeling, and summary output. The review found no compelling reason to redesign it.

Preserve these details:

- The full gate order is types → lint → formatting verification → tests.
- Selected checks follow the normal order, not the argument order.
- Selected checks exclude pytest.
- test runs tests independently.
- format mutates formatting; check --format does not.
- Missing required tooling is detected before starting the selected checks.
- A failure stops subsequent checks.
- Reports distinguish PASS, FAIL, and NOT RUN.
- Overall PASS must never imply checks that were not requested or executed.
- The failing subprocess exit code is propagated.
- Launch errors have an actionable message and a failing result.

A generic command registry, reusable task runner, or new check-result class is not justified merely to remove a few simple lists.

The existing source/tooling/examples/tests path list and pyproject configuration should stay aligned. Do not enlarge the application gate to include design-generation scripts without an explicit reason; that would add unrelated scope.

## 12. Verification plan for the implementation agent

### Before making changes

1. Record current main SHA and the implementation branch base.
2. Read git status and preserve unrelated user work.
3. Confirm the intended application interpreter and toolchain.
4. Run the existing local gate when the environment is ready.
5. Record baseline failures separately from regressions introduced by this work.
6. Reproduce the import problem and the uv-selection disagreement at the current source revision.

### During implementation

Use deterministic tests for the changed behaviors described above. Prefer temporary directories and explicit inputs over global __file__ or sys.path patching.

Some subprocess mocking is appropriate because tests must not install tools or build releases on every unit-test run. It should simulate meaningful boundaries and assert consequences, not mirror the implementation statement by statement.

### After implementation

From the repository root, using the project's configured environment:

~~~sh
app/.venv/bin/agent-playbook check
app/.venv/bin/agent-playbook --help
app/.venv/bin/agent-playbook dev-run
app/.venv/bin/agent-playbook version
~~~

Verify direct tooling entry points as appropriate. Run formatting first only if needed, then run the complete gate after the final edits.

For packaging and release validation:

1. Commit the intended implementation so release's clean-checkout requirement is meaningful.
2. Build from a clean checkout; do not bypass the clean-source check to make a smoke test pass.
3. Run the full release command.
4. Inspect Wheel contents for the expected runtime package and absence of checkout tooling/tests/examples.
5. Run the installed release's version and run commands.
6. Check developer-command rejection.
7. Verify the recorded digest.
8. Repeat a release and confirm the earlier output is preserved.
9. Exercise an explicit output path from a different working directory.
10. Check that the normal runtime selects only completed releases.

Use a disposable clean checkout when source-edit isolation testing would otherwise disturb active work. Do not discard unrelated edits to satisfy release preflight.

For bootstrap/helper changes, verify the bootstrap starting-interpreter compatibility separately. A Python 3.13 check does not establish Python 3.10 bootstrap support.

PyCharm on Sharon's macOS machine cannot be certified by a Linux terminal check. If task paths or invocation modes change, distinguish static XML inspection from actual IDE execution and record any remaining local confirmation.

### Verification reporting

Report actual commands, outcomes, and limitations. Avoid claiming a release passed because unit tests mocked the build/install subprocesses.

Do not add CI infrastructure as part of this handoff's work. The repository currently asks for local checks.

## 13. Evidence already collected versus work still required

### Completed review evidence

The review inspected the source at the pinned commit and ran focused probes using the retrieved source snapshot.

| Evidence | Method | Observed outcome |
|---|---|---|
| Normal tooling.release import | Import from application project context without adding tooling directly to sys.path | ModuleNotFoundError for verify_wheel |
| Wrong PATH uv plus private pinned copy | Temporary app files and controlled version-probe responses | release rejected PATH uv instead of trying private uv |
| Same candidate arrangement for version command | Controlled subprocess responses | version selected the private pinned uv |
| Positional release forwarding | Synthetic argument list with another option before --output | Bridge resolved the wrong positional value |
| Eight CLI dispatch cases | Python 3.13, mocked development subprocess boundary | Expected task/argument forwarding and exit status |
| Full and selected check ordering | Direct select_commands calls | Expected order and selection |
| Five installed-release development guards | Patched release metadata and subprocess spy | Developer subprocesses were not invoked |

The eight dispatch cases were check; check with lint/types; check with format; format; test; version patch; release; and release with output. These probes validate the inspected paths, not the complete application.

The uv/import/forwarding probes used the available default Python 3.12 runtime. The later dispatch/order/guard probes used Python 3.13. The proposed implementation still needs verification under the project's actual pinned environment.

### Not completed during review

- The full pytest suite.
- Pyright and Ruff.
- A real uv provisioning/fallback scenario.
- Clean bootstrap.
- A complete release build/install.
- Wheel contents inspection.
- A macOS PyCharm run.
- Windows verification.
- Diagram regeneration or visual verification.

pytest was not installed in the checked Python environments. No claim of a full passing gate was made.

No application code was changed during the review. The handoff PR adds only this document.

## 14. Suggested implementation PR organization

This is a proposal for reviewable work, not a requirement to create all PRs immediately.

| PR | Scope | Intended outcome |
|---|---|---|
| Handoff PR | This temporary Markdown file only | Another agent can start with complete context |
| Implementation PR A | R3 tooling imports and R1 shared uv resolution | Normal imports and consistent tool selection |
| Implementation PR B | R2 release decomposition and relevant failure-boundary tests | Readable coordinator with preserved release guarantees |
| Optional implementation PR C | R4 CLI cleanup, optionally R5 directory injection | Easier argument handling and test setup |

If PR A is too large to review comfortably, separate import cleanup from toolchain resolution. If a later change is tiny and directly supports the current change, combining it can be reasonable. Prefer coherent outcomes over an arbitrary number of PRs.

Avoid a giant patch that simultaneously renames every script, reorganizes the whole package, changes release semantics, and introduces future workflow behavior.

Each implementation PR should explain:

- The concrete prior problem.
- Resulting behavior.
- Why the extraction is useful.
- Which interfaces and guarantees remain stable.
- Verification performed.
- Remaining limitations.

Do not include this entire temporary handoff in each implementation PR body.

## 15. Deliberately rejected or deferred suggestions

| Suggestion | Decision | Reason |
|---|---|---|
| Global utils.py | Reject | Hides ownership and attracts unrelated helpers |
| Class for every CLI command | Reject | Current commands are small; additional indirection provides little benefit |
| ReleaseManager class hierarchy | Reject | The release is a straightforward linear process |
| Generic pipeline/task framework | Reject | No demonstrated need for dynamic task composition |
| Dependency-injection container | Reject | Explicit function arguments are sufficient |
| Plugin-based command registry | Defer | Current command count and extension needs do not justify it |
| Rewriting checks.py | Reject for now | It already separates the relevant responsibilities |
| Generic subprocess abstraction everywhere | Defer | Commands have different output, capture, cwd, and failure needs |
| New shared runtime/tooling package | Reject for this scope | Risks weakening the installed-runtime boundary |
| PyCharm XML generator | Defer | Twelve small configurations do not yet justify another tool |
| Diagram framework/refactor | Defer | These are low-frequency generation scripts outside the core task |
| Broad Windows compatibility work | Defer | Existing cross-platform fragments do not establish end-to-end support |
| Runtime dependency installation changes | Defer | Requires the future dependency/reproducibility decision |
| New CI, deployment, publishing | Out of scope | Not requested and not part of the repository's current local workflow |
| Stage 01 workflow or integration implementation | Out of scope | Separate learning/design work |

Small helpers are not automatically bad; they should have a concrete reason. Conversely, not every repeated line deserves extraction. Avoid sharing code across ownership boundaries merely to eliminate a short expression.

## 16. Questions the implementation agent should resolve from code

These are investigation prompts, not reasons to stop before doing useful work:

1. Has main already changed the uv discovery or imports?
2. Which import strategy preserves all supported script invocations with the least complexity?
3. Can the shared toolchain module remain Python-3.10-compatible without new dependencies?
4. Which release values genuinely travel together often enough to warrant a data class?
5. Which verification failures need new behavior tests rather than more mocks of helper calls?
6. Does CLI output normalization fit cleanly in the parsed release branch?
7. Is R5 worthwhile after the higher-value changes, or should it be left alone?

Ask Sharon only for actual scope or protected-design decisions that cannot be resolved from the current authorization and repository rules. Routine naming and helper extraction within existing boundaries should not become an unnecessary approval sequence.

## 17. Completion checklist

### Handoff delivery

- [x] Review commit recorded.
- [x] Current source ownership described.
- [x] Findings separated from proposals and future risks.
- [x] Concrete implementation sequence provided.
- [x] Public behavior and release invariants listed.
- [x] Tests and unverified areas stated honestly.
- [x] Temporary lifecycle and deletion instructions included.
- [x] No runtime or tooling implementation bundled into this document.

### Future implementation

- [ ] Revalidate findings against current main.
- [ ] Fix ordinary tooling imports without breaking script entry points.
- [ ] Share uv discovery/validation and preserve bootstrap compatibility.
- [ ] Preserve useful discovery fallback without retrying failed mutations.
- [ ] Extract focused release operations without introducing a framework.
- [ ] Keep completion marking after all verification.
- [ ] Simplify CLI argument handling if included.
- [ ] Perform optional directory injection only if useful.
- [ ] Preserve command contracts, installed-release guards, and Wheel boundaries.
- [ ] Run meaningful regression tests and the full local gate.
- [ ] Verify clean bootstrap/release paths affected by the changes.
- [ ] Record any outstanding macOS/PyCharm confirmation.
- [ ] Summarize durable outcomes in implementation PRs/documentation.
- [ ] Close the handoff PR, or delete this file after it is no longer needed.

## 18. Pinned source references

These links refer to the reviewed commit. Use them to understand the finding, then inspect current main before implementing.

- [Reviewed commit](https://github.com/SharonLanger/agent-playbook/commit/4c9e74dcaf6897f6337f367dbbf17177bbada6c1)
- [Guarded project structure](https://github.com/SharonLanger/agent-playbook/blob/4c9e74dcaf6897f6337f367dbbf17177bbada6c1/designs/project-structure.md)
- [CLI and release contract](https://github.com/SharonLanger/agent-playbook/blob/4c9e74dcaf6897f6337f367dbbf17177bbada6c1/app/docs/cli.md)
- [Bootstrap](https://github.com/SharonLanger/agent-playbook/blob/4c9e74dcaf6897f6337f367dbbf17177bbada6c1/app/tooling/bootstrap.py)
- [Version updates](https://github.com/SharonLanger/agent-playbook/blob/4c9e74dcaf6897f6337f367dbbf17177bbada6c1/app/tooling/version.py)
- [Release builder](https://github.com/SharonLanger/agent-playbook/blob/4c9e74dcaf6897f6337f367dbbf17177bbada6c1/app/tooling/release.py)
- [Wheel verification](https://github.com/SharonLanger/agent-playbook/blob/4c9e74dcaf6897f6337f367dbbf17177bbada6c1/app/tooling/verify_wheel.py)
- [Quality checks](https://github.com/SharonLanger/agent-playbook/blob/4c9e74dcaf6897f6337f367dbbf17177bbada6c1/app/tooling/checks.py)
- [CLI parser and dispatch](https://github.com/SharonLanger/agent-playbook/blob/4c9e74dcaf6897f6337f367dbbf17177bbada6c1/app/src/agent_playbook/cli/commands.py)
- [Development bridge](https://github.com/SharonLanger/agent-playbook/blob/4c9e74dcaf6897f6337f367dbbf17177bbada6c1/app/src/agent_playbook/cli/development.py)
- [Release selection](https://github.com/SharonLanger/agent-playbook/blob/4c9e74dcaf6897f6337f367dbbf17177bbada6c1/app/src/agent_playbook/releases/selection.py)
- [Tooling tests](https://github.com/SharonLanger/agent-playbook/tree/4c9e74dcaf6897f6337f367dbbf17177bbada6c1/app/tests/tooling)
- [Release selection tests](https://github.com/SharonLanger/agent-playbook/blob/4c9e74dcaf6897f6337f367dbbf17177bbada6c1/app/tests/releases/test_release_selection.py)
