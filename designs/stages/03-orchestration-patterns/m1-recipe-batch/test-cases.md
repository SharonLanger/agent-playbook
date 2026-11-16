# S03.M1 — Verification cases

These are permanent design expectations, not permanent executable tests. Implement temporary verify.py inside EACH recipe folder. They remain published and runnable for Sharon until his hands-on review; remove them before merge, preserving reports and the pre-cleanup SHA.

## Running

From repo root, using the existing project environment:

```bash
app/.venv/bin/python app/examples/workflows/recipes/recipe_01_parallel_results/run.py
app/.venv/bin/python app/examples/workflows/recipes/recipe_01_parallel_results/verify.py
for recipe_dir in app/examples/workflows/recipes/recipe_*/; do
  app/.venv/bin/python "${recipe_dir}verify.py" || exit 1
done
```

Each verify.py must also run directly in PyCharm with app/.venv/bin/python and from a different working directory. Verification catches expected recipe failures and reports them as passing checks; default run.py for recipe05 deliberately exits nonzero. Verification does not alter checked-in input.json or leave temporary input changes behind. Use temporary copied folders or direct inputs. No root-level test runner, application test change or new dependency.

## Common cases — apply to all eight

| ID | Observable assertion | Level |
|---|---|---|
| V01 | Default run produces the design's result/state and exit behavior. Compare meaningful fields, not banners or generated IDs. | Direct entry subprocess |
| V02 | Copy the whole recipe folder outside the repository and run it with the project interpreter from another working directory, with PYTHONPATH cleared. Same outcome; no app/sibling imports. | Copy/run subprocess |
| V03 | Two fresh Flow instances with different inputs retain independent state; counters/results from one do not leak. | Direct Flow |
| V04 | Entry has no model/service prerequisites; CrewAI telemetry/tracing disabled before imports. Report configuration evidence without claiming an OS network sandbox. | Inspection + run |
| V05 | README begins title then matching diagram, explains actual nodes/knobs/outcomes and ends with working official sources. Diagram assets/links remain valid in copied folder. | Documentation/visual |
| V06 | verify.py reports failed assertions with nonzero exit, does not rewrite input.json and is runnable by Sharon. Include one temporary negative control to show an assertion detects a wrong expected value, then restore it. | Verification quality |

Map these as V01.C01 ... V06.C08 so every recipe has explicit evidence. Native context/tracing, performance benchmarking and real providers are not tests for this batch.

## Recipe cases

| ID | Scenario and required evidence |
|---|---|
| C01-T1 | [2,4,6] -> sum12/max6, both branches once, join/report once and after both outputs. |
| C01-T2 | Reverse which branch finishes first; same result. Show overlapping execution with start/finish markers or controlled synchronization, not a timing-speed threshold alone. |
| C02-T1 | A70/B90 -> B90; both branches complete before selection. |
| C02-T2 | A95/B90 -> A95; tied scores -> A. Reverse completion order without changing winner. |
| C03-T1 | basic -> sum12/max null; detailed-only nodes absent; terminal report once. |
| C03-T2 | detailed -> sum12/max6; both branches complete before join; terminal once; reversed completion order remains correct. |
| C04-T1 | [2,4,6], threshold10 -> sum12/min2/max6 after both extra branches. |
| C04-T2 | Sum below and exactly at threshold -> min/max null and no extra branch execution; terminal once. |
| C05-T1 | fail_a=true -> recognizable propagated error/nonzero direct-run exit; no success report or successful all-required join. Capture sibling's observed state. |
| C05-T2 | Exercise failure before sibling completion and after sibling completion; record actual native behavior/version. No assumed cancellation assertion or vacuous pass that accepts a swallowed failure. |
| C05-T3 | fail_a=false -> both results combined and successful exit. |
| C06-T1 | Fixed five checks, failures A/B, threshold3 -> all five outcomes retained; two failures reported; overall returned result with truthful status. |
| C06-T2 | Failures A/B/C, threshold3 -> all five complete before decision, summary retained, overall failure/nonzero run exit. |
| C06-T3 | Zero failures and all five failures exercise both bounds; verify correct count and all identities without missing/duplicated outcomes. |
| C06-T4 | Change threshold to2 with failures A/B -> fail exactly at threshold; no early exit. |
| C07-T1 | iterations3 -> counter3, exactly three routed work executions and one terminal result. |
| C07-T2 | iterations1 and iterations10 terminate exactly at the configured bound. |
| C08-T1 | accept_on_attempt3/max_attempts4 -> three coder/reviewer pairs then accepted. |
| C08-T2 | accept_on_attempt5/max_attempts2 -> two pairs and explicit limit_reached; no third attempt or accepted result. |
| C08-T3 | accept_on_attempt2/max_attempts2 -> accepted on final allowed attempt. |

For C01/C02/C03/C04/C06, assert identities and aggregation prerequisites, not an arbitrary total branch order. Framework-native scheduling is part of what is taught; replacing it with a hand-rolled scheduler is a design failure even if outputs match.

## Collection and review cases

| ID | Assertion / evidence |
|---|---|
| X01 | Existing eight concept folders move without behavioral/code changes; retained files match prior blobs except necessary documented path fixes. Existing tests/notices preserved. |
| X02 | workflows/concepts/recipes index and affected relative links resolve; no new dangling old-location links outside immutable historical references. |
| X03 | New Python files exist only inside recipe folders. Application source/config/dependency/gate files unchanged; no official registry entries. |
| X04 | Local lint/format checks target new recipe code explicitly. Application gates remain sandbox-independent. Sharon explicitly limited this work to CrewAI examples; do not run unrelated application regression tests for unchanged runtime. Record this scoped exception and the unchanged application boundary. |
| X05 | All eight diagrams rendered and visually inspected; SVG/link/authoring checks appropriate to delivered assets pass. Preserve approved topology and meaning, including recipe05's honest sibling note. |
| X06 | Both reviewers assess the same candidate; every Vxx.Cxx/Cxx-Tx/Xxx has a mapping to assertions or review evidence with actual commands and results. |
| X07 | At initial handoff, temporary verify.py scripts are PRESENT for Sharon. Mark cleanup pending, not failed. Before merge, prove their removal, preserve last test-bearing SHA/evidence, and rerun direct-run smoke checks without them. |

Checks stay proportionate: no new CI, coverage target, exhaustive input-validation suite or dependency upgrade. Input validation should make invalid small-domain scenarios understandable, but this batch tests CrewAI patterns rather than application validation machinery.

## Cleanup after Sharon's review

Do not delete verify.py in the initial implementation handoff. After Sharon has run them, remove the eight temporary scripts and references implying they remain available in the merged checkout. Remove any temporary test-only assets; do not remove learning inputs, outputs, notices or existing concept tests.

Keep run.py/flow.py behavior unchanged during cleanup. Compare against the reviewed candidate; report the exact deletion-only diff and execute direct runs including expected failures. Cleanup is not a fourth implementation round or a reset of the round count. Any additional behavioral fix after three rounds needs a new explicit user decision. Historical reports and immutable links retain the verification evidence.
