# Stage 01 — CrewAI Flows: review package

**Design and learning material only. Awaiting Sharon's review before implementation.**
This package describes the completed Stage 01 target, not current application behavior.
All three workflows and all lessons are prepared together; implementation proceeds gradually.
No runtime files, dependencies, versions, tests or IDE configurations are changed by this PR.

## Start here

1. Open [the animated diagram gallery](diagrams/index.html) locally in a browser.
2. Read [the mental model](learning/01-flow-basics.md).
3. Read [the stage architecture](architecture.md) and [file ownership map](file-structure.md).
4. Work through [WF-01](workflows/wf-01-step-sequence.md), [WF-02](workflows/wf-02-shared-state.md), then [WF-03](workflows/wf-03-conditional-route.md).
5. Review [failure behavior](learning/05-failures-and-tests.md), [CLI and releases](learning/06-running-and-releasing.md), and [the test specification](test-plan.md).
6. Review [the implementation sequence](plan.md) and [refactor coordination](coordination.md).

The diagrams are illustrative simulations, not traces of an implemented application.
Moving connectors show direction; the lesson's numbered execution table states actual order.
Static SVGs are embedded in Markdown because GitHub does not run these HTML animations.
Download/check out the branch and open `diagrams/index.html`; no server is needed.

## Three workflows, one new concept each

| ID | Python package | Principal new concept | Default result |
|---|---|---|---|
| WF-01 | `wf_01_step_sequence` | Start and listen; values passed between steps | `[Hello, workflow!]` |
| WF-02 | `wf_02_shared_state` | Typed state and fresh state for every run | `20`, history `[3, 5, 20]` |
| WF-03 | `wf_03_conditional_route` | Choose exactly one branch | score 80 → `pass` |

Each workflow owns its code and tests. The shared application runner selects and invokes one;
it does not contain workflow formulas, threshold rules or workflow-specific state.

## Document roles

| File | Role | Review status |
|---|---|---|
| `architecture.md` | Stage end state and behavioral boundaries | Proposed for approval |
| `file-structure.md` | Exact intended placement and reuse labels | Proposed for approval |
| `plan.md` | Implementation order and gates | Proposed for approval |
| `workflows/*.md` | Workflow contracts, examples and expected behavior | Proposed for approval |
| `learning/*.md` | Full lesson sequence, illustrative code and exercises | Read before implementing |
| `test-plan.md` | Required tests, scenarios and evidence | Specification, not executed tests |
| `coordination.md` | Snapshot of PR #28 and integration checks | Recheck before code work |
| `findings.md` | Verified documentation checks and unresolved implementation probes | Evidence only |
| `sources.md` | Official references and diagram provenance | Reference material |

## Temporary lifecycle

This folder is a review workspace under the same `designs/temporary/` parent as the
other agent's handoff, but owns only its own files. Do not delete or edit that handoff.
After approval, move this complete folder to `designs/stages/01-crewai-flows/`, repair
relative links and add it to the permanent design inventory. Preserve the approved
architecture/plan and lessons; this material is not disposable after implementation.
Do not make application imports or tests depend on the temporary location.
The permanent diagram policy lives separately at [AUTHORING.md](../../diagrams/AUTHORING.md).
