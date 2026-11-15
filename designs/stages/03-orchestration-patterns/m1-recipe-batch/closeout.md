# Stage 03 closeout — temporary verification cleanup

**Pending. Complete this checklist before marking Stage 03 done and merging design PR #52.**

Sharon's 2026-11-15 instruction U10 / S03-D26 explicitly revised the original lifecycle: implementation PR #53 may merge with the temporary scripts retained; their removal belongs to design closeout. #53 merged at `529fe15895afc8211d833fc2544e98f0d18fb451`. This is the current cleanup instruction and supersedes pre-implementation-merge wording in the pinned design/test/plan and historical reports. No recipe behavior changed.

## Required cleanup

- [ ] Remove these eight files from the final repository tree:
- [ ] `app/examples/workflows/recipes/recipe_01_parallel_results/verify.py`
- [ ] `app/examples/workflows/recipes/recipe_02_select_result/verify.py`
- [ ] `app/examples/workflows/recipes/recipe_03_conditional_parallel/verify.py`
- [ ] `app/examples/workflows/recipes/recipe_04_conditional_followup/verify.py`
- [ ] `app/examples/workflows/recipes/recipe_05_parallel_failure/verify.py`
- [ ] `app/examples/workflows/recipes/recipe_06_failure_threshold/verify.py`
- [ ] `app/examples/workflows/recipes/recipe_07_fixed_loop/verify.py`
- [ ] `app/examples/workflows/recipes/recipe_08_revision_loop/verify.py`
- [ ] Update recipe/collection READMEs to remove commands and present-tense claims that these temporary scripts remain available. Preserve historical review evidence and immutable links.
- [ ] Preserve all existing concept tests and permanent flow.py, run.py, input.json and diagram assets.
- [ ] Retain test-bearing head `906e0e5921fae726f37c5bdbb61551578373c908`, code/test candidate `fdb60f3a3964f9620758e7e3f8be03bbe1084711`, implementation reviewer reports and design-session final review.
- [ ] Prove the recipe Python diff contains only the eight verify.py deletions; list README cleanup separately. Any behavior change requires review, not silent cleanup. Round count remains 1/3.
- [ ] Rerun direct recipe smoke checks after deletion: default 01–04 and 06–08 succeed; 05 fails deliberately with its recognizable error; check the documented 05 success and 06 aggregate-failure variants using disposable copied inputs. Record actual results/environment and any unrun checks.
- [ ] Reconcile Stage 03 coverage links, roadmap, progress and Atlas; preserve other stages and separate logging ownership. Run applicable documentation/Atlas checks and resolve/report the existing freshness issue.
- [ ] Record Sharon's stage acceptance and separate explicit authorization for design PR #52. Do not label local Mac/PyCharm execution verified without his confirmation.

The design PR remains the documentation workspace. Perform executable-file deletion through an appropriate scoped cleanup change before closing it; this note does not turn temporary checks into permanent tests. No scheduled automation or unattended merge is requested.
