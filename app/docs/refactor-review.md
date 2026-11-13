# Review the runtime structure refactor

[Documentation index](README.md) · [Proposal and review map](../../designs/refactors/2026-11-12-runtime-structure/README.md)

## One command

After checking out this branch and running the usual Setup, run from the repository root:

```sh
app/.venv/bin/python app/tooling/verify_refactor.py
```

Or run the shared **Verify Refactor** task in PyCharm with `app/.venv/bin/python`
as the project interpreter. It runs the application type/lint/format/test gate, help/version,
console and module entry points, all integrated workflow paths, invalid input and
offline checks. CLI smoke checks run from an unrelated temporary working directory.

Any failed check produces a nonzero exit. Default mode explicitly reports that
installed-release checks were **NOT RUN**. The helper is checkout-only and can be
removed after review; it is not shipped in the wheel.

## Verify a normal versioned release

After building a release with `agent-playbook release`, verify its directory:

```sh
app/.venv/bin/python app/tooling/verify_refactor.py --release /absolute/path/to/app/dist/0.1.1-<commit>
```

Use the actual directory reported by the release command. This checks the
existing installation, hashes, workflows, import isolation, wheel contents
and developer-command rejection. The helper does not build another release
or change which release `run` selects.

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
3. Build a normal versioned **Release**, verify its directory with `--release PATH`, then run **Run**; confirm the chosen release path.
4. Try your local override and any explicit configuration paths.
5. Inspect the proposed folder ownership and future role/harness/tool placement.

macOS/PyCharm execution is local acceptance work; automated Linux checks do not
claim to verify the IDE or your machine-specific configuration.
