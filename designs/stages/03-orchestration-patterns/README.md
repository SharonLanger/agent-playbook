# Stage 03 — CrewAI concepts and recipes

Status: **Learning direction and organization agreed; exact recipe batch remains proposed. No implementation is authorized by this documentation update.**

[Decision log](decisions.md) records sources, rationale, superseded proposals and open choices. This README is the specification, coverage map and canonical batch index. Stage Design PR: [#52](https://github.com/SharonLanger/agent-playbook/pull/52).

## Agreed purpose

Build a permanent, easily runnable collection of CrewAI examples that Sharon can understand, copy and adapt later. Teach the wiring between nodes and a few useful compositions through simple deterministic Python work. Keep explanations practical and shallow: what to change, which node runs next, and what result to expect.

These are CrewAI learning recipes, not official Agent Playbook workflows. They use the project's installed dependencies but do not require the application runner, registry, shared application.yaml, execution context, Langfuse or logging. Real agents and logging may be added to a copied recipe in later work; that future use is not an integration guarantee or an acceptance requirement here.

Stage 02 is completed. Logging remains a separate workstream. Stage 04 agent execution and Stage 05 provider integration remain separate.

## Requirements and current scope

| ID | Requirement | Authority / status |
|---|---|---|
| S03-R01 | A bounded collection of useful, permanent, copyable recipes; select the exact batch together. | Agreed direction; final list pending |
| S03-R02 | Map existing coverage first. Reuse prior examples, while allowing an existing concept to be composed into a practical recipe. | User clarification; revision-loop recipe explicitly requested |
| S03-R03 | Check the CrewAI behavior being taught using example output and focused temporary verification where useful. No application or trace integration acceptance. | User clarification supersedes the initial application/tracing interpretation |
| S03-R04 | CrewAI remains scheduler and Flow state owner. Label ordinary Python logic honestly; do not invent a new orchestration framework. | Existing architecture; scoped to standalone examples |
| S03-R05 | Logging is separate and not a prerequisite. | Agreed |
| S03-R06 | No real agents, production recovery framework, human approval service or distributed worker platform. Retry/fallback recovery is deferred. | Roadmap boundary and user scope |
| S03-R07 | Agree and implement a complete batch together in one implementation PR, not a separate implementation cycle per recipe. Keep the ongoing Stage Design PR separate and draft/open. | User batch instruction; existing Stage Design lifecycle |
| S03-R08 | Preserve decisions, rationale, sources and pending choices. | Agreed |
| S03-R09 | Organize app/examples/workflows into concepts/ for existing examples and recipes/ for practical compositions. | Explicitly accepted; move not performed yet |
| S03-R10 | Each new recipe contains README.md, flow.py, run.py and input.json. README is the learning guide. | Explicitly accepted |
| S03-R11 | No permanent new test files. Temporary verification may be used and must be removed before implementation merge; retain a brief evidence summary. | Explicit user instruction |
| S03-R12 | Direct PyCharm run.py execution and copying a whole recipe folder are primary uses. No imports from another example or application runtime are needed. | Agreed independence goal |

Existing tests in the older concepts are not authorized for deletion by R11; that instruction concerns new recipes and temporary checks.

## Folder organization and shared recipe shape

| Proposed path | Responsibility |
|---|---|
| app/examples/workflows/README.md | Entry point for concepts and recipes |
| app/examples/workflows/concepts/ | Existing eight examples, retaining identities and history |
| app/examples/workflows/recipes/ | New practical, independently copyable recipes |
| designs/stages/03-orchestration-patterns/ | Scope, decisions and implementation evidence |

The proposed reorganization stays inside the existing examples boundary. Move-related relative links and path references must be updated, with no incidental behavior rewrite. The examples remain checkout-only, excluded from official workflow registration, application gates and release artifacts. They are accessed here under Sharon's specific examples request.

Each recipe's four core files:

- README.md: use case, teaching keywords, a small readable flow drawing, run instructions, expected behavior, walkthrough, editable knobs, copy/adaptation notes, limits and links to relevant official CrewAI documentation.
- flow.py: inspectable CrewAI wiring, state and simple Python work.
- run.py: direct entry point; input resolved relative to the recipe folder so the working directory does not matter.
- input.json: small editable scenario values.

Keep setup minimal. If the pinned framework needs example-local configuration, explain it and avoid pulling in application configuration. Do not create extra scaffolding by default. Follow the repository diagram-authoring guidance when actual drawings are produced; none are introduced in this update.

## Existing coverage map

Code, example documentation and selected tests were inspected at main 4ed7a318e25653d481705d9cb40c35de9ab649c7. They were not rerun in this design session. Current links point to the pre-move locations.

| Existing example | Coverage | Reuse / gap |
|---|---|---|
| [01 — Sequence](../../../app/examples/workflows/ex_01_step_sequence/README.md) | Sequence and returned values | Existing concept reference |
| [02 — Method completion](../../../app/examples/workflows/ex_02_method_completion/README.md) | Method references and method-name listeners | Existing concept reference |
| [03 — Router labels](../../../app/examples/workflows/ex_03_router_labels/README.md) | Exclusive conditional path | Do not reteach as an isolated new recipe |
| [04 — Name collision](../../../app/examples/workflows/ex_04_name_collision/README.md) | Method-name / route-label collision | Existing caution/reference |
| [05 — Revision loop](../../../app/examples/workflows/ex_05_revision_loop/README.md) | Bounded review/revision routing | Adapt the idea into a practical coder/reviewer-shaped recipe, using only counters |
| [06 — Nested conditions](../../../app/examples/workflows/ex_06_nested_conditions/README.md) | Async overlap and A AND (B OR C) join | Existing join wiring; does not show collecting all branch outputs into a useful report |
| [07 — Chained routers](../../../app/examples/workflows/ex_07_chained_routers/README.md) | Two successive routing decisions | Reuse when composing conditional recipes |
| [08 — Persisted routing](../../../app/examples/workflows/ex_08_persisted_routing/README.md) | Routing, convergence and restored saved state | Existing concept; no claim of resuming an interrupted instruction |

The [existing collection guide](../../../app/examples/workflows/README.md) describes independent copy/run behavior. Official WF-03 also covers exclusive routing, but these recipes do not depend on that application workflow.

## Expanded candidate menu — exact batch not selected

Sharon likes the original three areas and requested more variations, plus loops. The following menu translates that direction into discussion candidates; it does not approve eight implementations or fix their numbering.

| Candidate | Practical example | Teaching keywords | Decision still needed |
|---|---|---|---|
| C01 — Combine parallel results | Compute sum and maximum independently, then create one report. | Parallel work, join, state, aggregation | Final data shape and simple completion-order variation |
| C02 — Select one parallel result | Produce several deterministic candidates and choose one result. | Parallel work, selection, convergence | Choose best after all finish, first completed, or first acceptable? These are different contracts; no cancellation promise. |
| C03 — Conditional parallel work | Basic mode performs one calculation; detailed mode performs parallel calculations and combines them. | Router, selected path, join | Exact routes and convergence |
| C04 — Conditional follow-up | Compute a result, then route to either a final answer or additional parallel work. | Composition, routing after work, parallel branch | Whether this adds enough value beyond C03 |
| C05 — Any failure fails the flow | One branch raises while siblings are active; inspect what happens to the overall flow and join. | Exceptions, failure propagation, sibling behavior | Native behavior on the pin; failure does not imply immediate sibling cancellation |
| C06 — Failure threshold | Collect a fixed small group of outcomes; fail overall when failures reach a configured count, e.g. three. | Outcome collection, counters, threshold, final decision | Total branch count and early vs end-of-batch evaluation; distinguish recorded failure outcomes from uncaught exceptions |
| C07 — Fixed repetition | Perform a small update exactly N times, e.g. three, then finish. | Counter, loop, termination | Prefer flow-level repeated routing when teaching transitions; label any ordinary Python loop as Python |
| C08 — Bounded revision cycle | A fake coder updates a counter; a fake reviewer returns revise/accept; route back until accepted or a maximum is reached. | Feedback loop, router, state, bound | Acceptance and exhaustion outcomes; no actual agent calls |

C01 maps to earlier G1; C03/C04 elaborate G2; C05/C06 elaborate G3. C02/C07/C08 broaden the earlier list. These IDs are discussion identifiers, not milestone IDs or final folder numbers.

Counters and thresholds may be plain Python business logic connected by CrewAI. Do not advertise a custom failure-count policy or selection rule as a native framework feature. Inspect official guidance and the pinned runtime only as needed to explain behavior accurately.

Retry/fallback recovery remains deferred. The requested revision loop is a normal workflow feedback path, not automatic exception recovery. Variable-size fan-out remains an unselected idea; no durable recovery or tracing infrastructure is added.

## Teaching and verification

README should show “change this value or this route, and execution follows this path” with a small diagram and concise code explanation. It is a practical reference, not a deep framework course.

Verify the batch's direct-run behavior and meaningful outputs, including the chosen failure/loop cases. Temporary checks are allowed but do not remain as merged test files or join application gates. Keep a short record of commands, observed behavior, limitations and removed temporary checks. No runtime verification has been performed for this draft menu.

## Canonical batch index and next step

| Batch / milestone | Scope / approval | Implementation PR | Evidence / acceptance | Merge state |
|---|---|---|---|---|
| First recipe batch — ID not allocated | Directions agreed; exact selection and concise flow descriptions pending | Not opened | Not run / not accepted | Design PR #52 draft/open |

Discuss the candidate menu next. Then agree the whole batch's short flow descriptions, drawings, keywords and expected observations together. Do not impose a separate design/implementation round per recipe. Detailed rollout and any remaining handoff artifacts should be proportional to this learning scope.

## Governing records and reconciliation

[Roadmap](../../roadmap.md), [charter](../../charter.md), [principles](../../principles.md), [architecture](../../architecture.md), [project structure](../../project-structure.md), [progress](../../progress.md), [design contract](../../governance/design-contract.md), [guards](../../governance/guarded-files.md), [stage process](../../governance/stage-milestone-workflow.md), [handoff rules](../../governance/codex-handover-rules.md).

Sharon's explicit standalone CrewAI/no-permanent-tests/batch instructions govern this stage's working direction. The global roadmap still mentions correlated traces as Stage 03 evidence; this package records the narrower user-approved direction rather than claiming those words have been amended. Reconcile the applicable shared roadmap/progress/Atlas descriptions before final stage approval/closeout. No general governance rewrite, guarded amendment, runtime change or folder move is performed in this two-file update.

Stage Design PR #52 remains open/draft; batch implementation and stage closeout merge authorization are separate. No auto-merge.
