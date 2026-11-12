# Review the runtime structure refactor

[Documentation index](README.md) · [Proposal and review map](../../designs/refactors/2026-11-12-runtime-structure/README.md)

## One command

After checking out this branch and running the usual Setup, run from the repository root:

```sh
app/.venv/bin/python app/tooling/verify_refactor.py
```

Or run the shared **Verify Refactor** task in PyCharm with `app/.venv/bin/python`
as the project interpreter. It runs the full type/lint/format/test gate, help/version,
console and module entry points, all integrated workflow paths, invalid input and
offline checks. CLI smoke checks run from an unrelated temporary working directory.

Any failed check produces a nonzero exit. Default mode explicitly reports that
installed-release checks were **NOT RUN**. The helper is checkout-only and can be
removed after review; it is not shipped in the wheel.

## Include an isolated release

With a clean, committed checkout:

```sh
app/.venv/bin/python app/tooling/verify_refactor.py --build-release
```

This runs the gate through the normal release builder, builds and installs a new
release under a unique `app/dist/refactor-review-*` directory, and verifies hashes,
installed workflows, import isolation, wheel contents, developer-command rejection
and selection through the source CLI. Installing locked dependencies may download
packages. Existing releases are retained. Because `run` selects the newest completed
release, the newly built review release becomes the default selection in this checkout.

To check an existing release made from this refactor instead:

```sh
app/.venv/bin/python app/tooling/verify_refactor.py --release /absolute/path/to/release
```

This verifies that exact installation; it does not assert that it is the newest
release selected by the source CLI. A pre-refactor wheel deliberately fails the
new module-layout check.

All automated smoke checks select `tests/fixtures/offline.yaml` and remove application
environment overrides. They do not edit your settings or validate your chosen live
telemetry configuration. The Python audit probe records socket/DNS attempts for
these execution paths; it is not a general OS network sandbox.

## Configuration move

Shared settings now live in `app/application.yaml`, with optional ignored overrides
in `app/application.local.yaml`. If you already have `app/configs/application.local.yaml`,
move it to the new location. If both exist, merge them deliberately before removing
the old file. Default application startup detects the old file and exits with an
actionable message; it never overwrites either file. An explicit `--config` or
`AGENT_PLAYBOOK_CONFIG` selection still wins. Update any external scripts or PyCharm
parameters that explicitly reference the old shared path.

## Short manual review

1. Run **Setup**, **Check** and **Verify Refactor** using the project interpreter.
2. Run **WF-01 Sequence**, **WF-02 State** and **WF-03 Route**; compare their existing outputs.
3. Run the build-release command above, then **Run**; confirm the chosen release path.
4. Try your local override and any explicit configuration paths.
5. Inspect the proposed folder ownership and future role/harness/tool placement.

macOS/PyCharm execution is local acceptance work; automated Linux checks do not
claim to verify the IDE or your machine-specific configuration.
