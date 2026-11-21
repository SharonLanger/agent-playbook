# Stage 03 — CrewAI concepts and recipes

Status: **Complete — accepted by Sharon on 2026-11-16; PR #53 merged; design closeout and cleanup delivered through PR #52 with his explicit merge authorization.**

[Acceptance and cleanup record](m1-recipe-batch/closeout.md).

[Final review and remaining work](m1-recipe-batch/reviews/final-review.md) records independent checks and distinguishes them from the implementation reviewers' runtime evidence.

[Decision log](decisions.md) records sources, rationale, superseded proposals and open choices. This README is the stage index and coverage map. The shared requirements are in [requirements.md](requirements.md). Stage Design PR: [#52](https://github.com/SharonLanger/agent-playbook/pull/52).

## Agreed purpose

Build a permanent, easily runnable collection of CrewAI examples that Sharon can understand, copy and adapt later. Teach the wiring between nodes and a few useful compositions through simple deterministic Python work. Keep explanations practical and shallow: what to change, which node runs next, and what result to expect.

These are CrewAI learning recipes, not official Agent Playbook workflows. They use the project's installed dependencies but do not require the application runner, registry, shared application.yaml, execution context, Langfuse or logging. Real agents and logging may be added to a copied recipe in later work; that future use is not an integration guarantee or an acceptance requirement here.

Stage 02 is completed. Logging remains a separate workstream. Stage 04 agent execution and Stage 05 provider integration remain separate.

## Requirements and current scope

Read the [shared Stage 03 requirements](requirements.md) for S03-R01–R12 and the scope of the temporary-test cleanup.

## Folder organization and shared recipe shape

| Proposed path | Responsibility |
|---|---|
| app/examples/workflows/README.md | Entry point for concepts and recipes |
| app/examples/workflows/concepts/ | Existing eight examples, retaining identities and history |
| app/examples/workflows/recipes/ | New practical, independently copyable recipes |
| designs/stages/03-orchestration-patterns/ | Scope, decisions and implementation evidence |

The proposed reorganization stays inside the existing examples boundary. Move-related relative links and path references must be updated, with no incidental behavior rewrite. The examples remain checkout-only, excluded from official workflow registration, application gates and release artifacts. They are accessed here under Sharon's specific examples request.

Each recipe's four core files:

- README.md: title followed immediately by its approved diagram, then use case, teaching keywords, run instructions, expected behavior, short wiring walkthrough, editable knobs, copy notes and limits. Relevant official documentation links form the footer.
- flow.py: inspectable CrewAI wiring, state and simple Python work.
- run.py: direct entry point; input resolved relative to the recipe folder so the working directory does not matter.
- input.json: small editable scenario values.

Keep setup minimal. If the pinned framework needs example-local configuration, explain it and avoid pulling in application configuration. Do not create extra scaffolding by default. The approved [diagram reference](diagrams/approved-preview.html) now travels with this design. Follow the repository diagram-authoring guidance when producing final portable assets inside recipe folders.

## Existing coverage map

Code, example documentation and selected tests were inspected at main 4ed7a318e25653d481705d9cb40c35de9ab649c7. They were not rerun in this design session. Links now use the merged concepts/ locations.

| Existing example | Coverage | Reuse / gap |
|---|---|---|
| [01 — Sequence](../../../app/examples/workflows/concepts/ex_01_step_sequence/README.md) | Sequence and returned values | Existing concept reference |
| [02 — Method completion](../../../app/examples/workflows/concepts/ex_02_method_completion/README.md) | Method references and method-name listeners | Existing concept reference |
| [03 — Router labels](../../../app/examples/workflows/concepts/ex_03_router_labels/README.md) | Exclusive conditional path | Do not reteach as an isolated new recipe |
| [04 — Name collision](../../../app/examples/workflows/concepts/ex_04_name_collision/README.md) | Method-name / route-label collision | Existing caution/reference |
| [05 — Revision loop](../../../app/examples/workflows/concepts/ex_05_revision_loop/README.md) | Bounded review/revision routing | Adapt the idea into a practical coder/reviewer-shaped recipe, using only counters |
| [06 — Nested conditions](../../../app/examples/workflows/concepts/ex_06_nested_conditions/README.md) | Async overlap and A AND (B OR C) join | Existing join wiring; does not show collecting all branch outputs into a useful report |
| [07 — Chained routers](../../../app/examples/workflows/concepts/ex_07_chained_routers/README.md) | Two successive routing decisions | Reuse when composing conditional recipes |
| [08 — Persisted routing](../../../app/examples/workflows/concepts/ex_08_persisted_routing/README.md) | Routing, convergence and restored saved state | Existing concept; no claim of resuming an interrupted instruction |

The [existing collection guide](../../../app/examples/workflows/README.md) describes independent copy/run behavior. Official WF-03 also covers exclusive routing, but these recipes do not depend on that application workflow.

## Approved batch — S03.M1

Sharon approved every diagram and explanation in the eight-recipe walkthrough. [Detailed design](m1-recipe-batch/design.md), [verification cases](m1-recipe-batch/test-cases.md) and [implementation plan](m1-recipe-batch/implementation-plan.md) specify one batch; no per-recipe handoff cycles.

| Recipe | Approved behavior | Folder under app/examples/workflows/recipes/ |
|---|---|---|
| C01 | Combine sum and maximum after both parallel branches finish | recipe_01_parallel_results |
| C02 | Wait for all candidates, then choose highest score; deterministic tie rule | recipe_02_select_result |
| C03 | Basic/detailed input selects single work or parallel work, then common report | recipe_03_conditional_parallel |
| C04 | Initial sum determines whether additional parallel analysis runs | recipe_04_conditional_followup |
| C05 | One branch's exception makes the overall run fail; observe sibling behavior honestly | recipe_05_parallel_failure |
| C06 | Wait for all five outcomes, then fail at configured count, default three | recipe_06_failure_threshold |
| C07 | Repeat through Flow routing exactly N times, default three | recipe_07_fixed_loop |
| C08 | Fake coder/reviewer feedback until accepted or maximum attempts | recipe_08_revision_loop |

C01 maps to G1; C03/C04 elaborate G2; C05/C06 elaborate G3. C02/C07/C08 expand the earlier scope. No first-winner race, retries/fallback, real agents or durable recovery. Threshold/selection decisions are Python policy wired through CrewAI, not asserted native framework features.

## Teaching, temporary tests and acceptance

The README starts with the approved diagram and explains “change this value/route and execution follows this path.” Keep it practical; official sources appear at the bottom.

New code stays inside the individual recipe folders. Temporary verify.py scripts also live there, are pushed with implementation and independently runnable by Sharon, and are inspected by the reviewers. Do not remove them at the first handoff. Under U10 / S03-D26, the temporary files remain after implementation merge. Delete them during Stage 03 closeout, before marking the stage complete and merging design PR #52; retain immutable pre-cleanup evidence. Existing concept tests remain preserved.

Only CrewAI recipe behavior and directly affected files are checked; no integration testing of unrelated application behavior. This design session inspected code/tests and independently rendered all eight static diagrams for final review. It did not rerun CrewAI; the exact-candidate runtime evidence and environment limits are linked in the final review.

## Canonical milestone index

| Milestone / outcome | Design and approved revision | Implementation PR | Review evidence | Acceptance | Merge |
|---|---|---|---|---|---|
| S03.M1 — eight runnable copyable recipes and concepts/recipes organization | [Approved contract `6067fb65`](https://github.com/SharonLanger/agent-playbook/blob/6067fb652f0bffe2fa1f8a0e53f045a421a16f11/designs/stages/03-orchestration-patterns/m1-recipe-batch/design.md) | [#53](https://github.com/SharonLanger/agent-playbook/pull/53) | [Implementation reviews](m1-recipe-batch/reviews/status.md) PASS, 1/3 rounds; [final review](m1-recipe-batch/reviews/final-review.md) PASS; test-bearing head `906e0e5921fae726f37c5bdbb61551578373c908` | Accepted by Sharon 2026-11-16; temporary checks removed at closeout | [#53](https://github.com/SharonLanger/agent-playbook/pull/53) merged at `529fe15895afc8211d833fc2544e98f0d18fb451`; [#52](https://github.com/SharonLanger/agent-playbook/pull/52) merged at `50e8dcc9c84d120fb06df8ecda29f016431a356c` |

Start with [M1 README](m1-recipe-batch/README.md). The outgoing handoff gives immutable links and the full contract SHA. Sending that prompt authorizes its concrete revision. Codex implements the whole batch using one coder plus independent design-drift and test-gap/behavior reviewers; maximum three rounds on frozen candidates. This design session reviews the returned evidence before any merge.

## Next action

Stage 03 is closed. The [milestone README](m1-recipe-batch/README.md) and [closeout record](m1-recipe-batch/closeout.md) are the entry points for revisiting the recipe batch. Further work proceeds under its own stage approvals.

## Governing records and reconciliation

[Roadmap](../../roadmap.md), [charter](../../charter.md), [principles](../../principles.md), [architecture](../../architecture.md), [project structure](../../project-structure.md), [progress](../../progress.md), [design contract](../../governance/design-contract.md), [guards](../../governance/guarded-files.md), [stage process](../../governance/stage-milestone-workflow.md), [handoff rules](../../governance/codex-handover-rules.md).

Sharon's explicit standalone CrewAI/no-permanent-tests/batch instructions govern this stage's working direction. The global roadmap still mentions correlated traces as Stage 03 evidence; this package records the narrower user-approved direction rather than claiming those words have been amended. The design session owns shared roadmap/progress/Atlas semantic reconciliation before stage closeout; this does not add integration work to the explicit recipe-only contract. No general governance rewrite, runtime change or folder move is performed by this handoff-authoring turn. The package and diagram reference are permanent stage material.

At the recorded implementation handoff, Stage Design PR #52 was draft and open under a separate merge gate. The closeout below records Sharon’s subsequent authorization.


## Closeout supersession — 2026-11-16

Stage 03 is complete and accepted by Sharon on 2026-11-16. He confirmed that he checked everything and that it was good, authorized removal of the temporary verification scripts, and explicitly authorized merging design PR #52. Implementation PR #53 merged at 529fe15895afc8211d833fc2544e98f0d18fb451. Temporary-check lifecycle instructions above are retained as the agreed process; cleanup is now complete. Earlier pending reconciliation and keep-open wording is superseded by this recorded closeout authorization. No further Stage 03 milestone is planned.
