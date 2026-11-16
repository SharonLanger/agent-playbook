# S03.M1 round 01 — test-gap and behavior review

Author role/model: independent test-gap/behavior reviewer, `gpt-6.1-sol`.
Candidate: `fdb60f3a3964f9620758e7e3f8be03bbe1084711`.
Verdict: **PASS**. Required findings: none.

Read the pinned contract `6067fb652f0bffe2fa1f8a0e53f045a421a16f11`, inspected the actual candidate, and independently executed all eight `verify.py` scripts with `app/.venv/bin/python` and `XDG_DATA_HOME=/tmp/recipe-review-data`. All exited 0. Each verifier checks direct and copied-folder entries from temporary working directories with `PYTHONPATH` cleared. The reviewer did not edit the candidate.

The initial rerun could not import `crewai` because this reviewer's sandbox lacked read access to the installed venv. Retrying with explicit venv read and network/socket permission succeeded. This is an environment qualification, not an OS offline guarantee. Native LanceDB initialization required the latter permission. Linux execution does not establish Mac/PyCharm acceptance.

For each of the eight recipes, a disposable copied `verify.py` had its common expected result changed to `{"negative_control_wrong_expected": true}`. All eight exited 1 at the intended assertion. Original scripts and inputs remained unchanged. Scoped Ruff lint/format passed 24 Python files. `git diff --check`, all 16 SVG XML parses, all workflow README local links and 96 moved-concept byte comparisons passed. No changes outside workflow examples were found. The design reviewer separately supplied rendering/visual evidence for X05.

## Common IDs — all eight recipes

Each row expands to the eight stable IDs `Vxx.C01` through `Vxx.C08`; every listed instance passed in the independent run.

| IDs | Meaningful assertion/evidence | Result |
|---|---|---|
| V01.C01–C08 | Each `verify.py` runs `run.py` as a subprocess, checks exit and parsed default result/state; C05 requires recognizable error and absence of success JSON. | PASS ×8 |
| V02.C01–C08 | Copies whole folder outside repo, runs from another cwd with `PYTHONPATH` removed; compares result/exit and copied SVG XML. | PASS ×8 |
| V03.C01–C08 | `verify()` creates two fresh Flow instances with different inputs and checks earlier state and distinct mutable containers. | PASS ×8 |
| V04.C01–C08 | Each entry and verifier sets CrewAI telemetry/tracing switches before CrewAI imports; source inspection finds deterministic Python work and no model/service/application imports. | PASS ×8 |
| V05.C01–C08 | Common checks require title followed by matching diagram and official-source footer; local link/XML checks passed. Design reviewer confirmed topology, rendering and guide fidelity. | PASS ×8 |
| V06.C01–C08 | Common checks preserve `input.json`; wrong-expected disposable controls all exited 1 at intended assertion. | PASS ×8 |

## Recipe IDs

| ID | Assertion in the numbered recipe's `verify.py` and observed outcome | Result |
|---|---|---|
| C01-T1 | Sum12/max6, each branch once, both complete before join, one terminal report. | PASS |
| C01-T2 | Reversed delays preserve result and reverse finish order; both starts precede first finish. | PASS |
| C02-T1 | Both candidates complete before B90 is selected. | PASS |
| C02-T2 | A95 wins, tie selects A, reversed finish order leaves B90 winner. | PASS |
| C03-T1 | Basic sum12/max null, exact basic-only events, one report. | PASS |
| C03-T2 | Detailed sum12/max6; both before join, one report and reverse completion variant. | PASS |
| C04-T1 | Default sum12/min2/max6 after both extra branches. | PASS |
| C04-T2 | Thresholds 12 and 13 take simple path, null extras and no extra-node events. | PASS |
| C05-T1 | Propagated `ValueError`, direct exit 1, no join/report/success JSON. | PASS |
| C05-T2 | Early A error lacks B completion; reversed delays complete B before A error. Observed native sibling state recorded without assumed universal cancellation semantics. | PASS |
| C05-T3 | `fail_a=false` joins A/B, reports combined success and direct exit 0. | PASS |
| C06-T1 | Five unique outcomes, A/B failures, count 2, truthful tolerated result, all complete before threshold. | PASS |
| C06-T2 | A/B/C failures, five outcomes and retained summary, threshold after join, subprocess exit 1. | PASS |
| C06-T3 | Zero/all-five failures verify all identities and exact counts without duplicates. | PASS |
| C06-T4 | A/B with threshold 2 fails exactly at threshold after all five complete. | PASS |
| C07-T1 | Three exact work executions, ordered values, counter 3 and one terminal report. | PASS |
| C07-T2 | Bounds 1 and 10 terminate at exact configured iteration. | PASS |
| C08-T1 | 3/4 creates exactly three coder/reviewer pairs then accepted. | PASS |
| C08-T2 | 5/2 creates exactly two pairs and `limit_reached`, no third attempt. | PASS |
| C08-T3 | 2/2 accepts on final allowed attempt. | PASS |

The reviewer inspected native decorators/joins and found no `asyncio.gather` or custom scheduler replacing Flow. Parallel assertions check identities and prerequisites without imposing arbitrary total branch order. Expected failure checks reject swallowed exceptions.

## Collection IDs

| ID | Evidence | Result |
|---|---|---|
| X01 | All 96 relocated concept files byte-identical, including tests, notices and inputs. | PASS |
| X02 | Workflow Markdown links resolve; no obsolete live old-location references outside examples/historical material found. | PASS |
| X03 | Diff confined to workflow examples; new Python only in recipe folders. Application/config/dependency/gates/registry unchanged. | PASS |
| X04 | Explicit Ruff lint and format checks passed for 24 recipe Python files. Unrelated application regressions intentionally unrun per approved scope. | PASS |
| X05 | Own XML/link checks pass; design reviewer independently reported Dashmotion zero violations and Inkscape visual review. This reviewer did not render images. | PASS |
| X06 | This report covers 48 common, 20 recipe and seven collection IDs. Both reviewers assessed the same frozen candidate SHA. | PASS |
| X07 | Eight runnable temporary verification scripts remain present. Hands-on review, deletion and post-cleanup smoke checks are pending by design. | PASS for initial handoff |

No permanent application test, integration trace, performance or provider check was part of this batch. User acceptance and merge authorization are pending.
