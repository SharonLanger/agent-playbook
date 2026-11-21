# S03.M1 round 01 — implementation

Author role/model: coder, `gpt-6.1-sol`.
Candidate: `fdb60f3a3964f9620758e7e3f8be03bbe1084711`.
Base: `4ed7a318e25653d481705d9cb40c35de9ab649c7`.
Contract: `6067fb652f0bffe2fa1f8a0e53f045a421a16f11`.

Implemented all eight standalone recipe folders with local `flow.py`, `run.py`, `input.json`, temporary `verify.py`, learning README, animated/static SVG, local viewer and diagram license notice. The eight existing concepts moved with 96 identical blobs. Collection navigation changed only inside `app/examples/workflows/`. No application runtime, registry, dependency, configuration, gate or guarded contract changed.

Executed on Linux, Python 3.13.5, CrewAI 1.15.40:

```bash
cd /tmp
for recipe_dir in /workspace/agent-playbook/app/examples/workflows/recipes/recipe_*/; do
  /workspace/agent-playbook/app/.venv/bin/python "${recipe_dir}verify.py" || exit 1
done
```

All eight exited 0, including direct and copied-folder subprocess runs, default/variant outcomes, state isolation and expected failures. Eight separate disposable copies with deliberately wrong expected result each exited 1 at the intended assertion; checked-in inputs and scripts were unchanged. Default entries 01–04 and 06–08 exited 0; recipe 05 exited 1 with the original `ValueError` and no success report. For recipe 05, early A failure observed `input, A:start, B:start, A:error, B:cancelled`; reversed delays observed `input, A:start, B:start, B:done, A:error` on this version. No general cancellation policy is asserted.

```bash
app/.venv/bin/ruff check app/examples/workflows/recipes/recipe_*/{flow,run,verify}.py
app/.venv/bin/ruff format --check app/examples/workflows/recipes/recipe_*/{flow,run,verify}.py
python3 /tmp/recipe-dashmotion/skills/dashmotion/scripts/check_diagram.py \
  app/examples/workflows/recipes/recipe_*/diagram.html \
  app/examples/workflows/recipes/recipe_*/diagram.svg \
  app/examples/workflows/recipes/recipe_*/diagram-static.svg
git diff HEAD~1 --check
```

Ruff passed 24 files, Dashmotion checker passed all 24 assets with zero violations, and diff check passed. All 16 SVGs parsed, local links resolved, and official footer URLs returned HTTP 200. Inkscape rendered all eight static SVGs; contact sheet and the final loop arrows were visually inspected. All 96 moved concept files matched their base blobs.

Environment qualification: the managed sandbox initially blocked CrewAI's user storage and LanceDB initialization; checks succeeded with writable user-data storage and additional network/socket allowance. The recipes do not promise an OS offline sandbox. Chromium screenshots were blocked by managed-home constraints; Inkscape provided the visual render. `designs/atlas/build.py --check` reported pre-existing generated drift for five unrelated diagrams; no unrelated generated change was retained. Application regression tests and existing concept suites were not run under the approved examples-only scope. Mac/PyCharm hands-on acceptance remains pending.
