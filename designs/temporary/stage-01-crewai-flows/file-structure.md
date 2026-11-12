# File ownership — reusable versus workflow-specific

**Proposed end-of-stage layout. These runtime files are not created in this PR.**
Paths are relative to `app/`; `WF-01` is a display/CLI identifier, while Python package names
use underscores. Each named workflow has its own test directory.

## Shared application files

| Path | Purpose | Reuse / change expectation |
|---|---|---|
| `src/agent_playbook/cli/commands.py` | Public options, selection forwarding and presentation | Reused; integrate with PR #28's final parser shape |
| `src/agent_playbook/application/runner.py` | Validate request, select/invoke fresh flow, normalize result | Reused; one explicit selection entry per new workflow |
| `src/agent_playbook/application/results.py` | Small immutable successful RunResult | Reused; no workflow state here |
| `src/agent_playbook/releases/selection.py` | Forward workflow/input argv to selected installation | Reused; preserve version selection and isolation |
| `src/agent_playbook/__main__.py` | Preserve direct-module default run | Reused entry point; defaults to WF-01 in Stage 01 |
| `tooling/` | Existing setup/check/version/release machinery | Reused; runtime dependency installation added deliberately |
| `tests/application/test_runner.py` | Selection, input rejection, fresh invocation, normalized outcomes | Shared application tests |
| `tests/cli/test_workflow_commands.py` | Parsing, argv forwarding, exit codes, help | Shared CLI tests |
| `tests/releases/test_workflow_launch.py` | Selected release receives the exact requested workflow/input | Shared release tests |

Do not freeze internal helper filenames from another agent's in-progress refactor. Read PR #28's
actual merged tree before extending these owners. No workflow imports `tooling` or CLI modules.

## Workflow files (W = workflow-specific)

| Path under `src/agent_playbook/workflows/` | Scope | Purpose |
|---|---|---|
| `wf_01_step_sequence/__init__.py` | W: WF-01 | Package marker |
| `wf_01_step_sequence/flow.py` | W: WF-01 | `StepSequenceFlow`: start/listen chain |
| `wf_01_step_sequence/steps.py` | W: WF-01 | Produce and decorate strings |
| `wf_02_shared_state/__init__.py` | W: WF-02 | Package marker |
| `wf_02_shared_state/flow.py` | W: WF-02 | `SharedStateFlow`: initialize/add/multiply/finish |
| `wf_02_shared_state/state.py` | W: WF-02 | `NumberInput` and `NumberState`; distinct external/internal schemas |
| `wf_02_shared_state/steps.py` | W: WF-02 | Pure addition and multiplication |
| `wf_03_conditional_route/__init__.py` | W: WF-03 | Package marker |
| `wf_03_conditional_route/flow.py` | W: WF-03 | `ConditionalRouteFlow`: start/router/two terminal listeners |
| `wf_03_conditional_route/state.py` | W: WF-03 | `ScoreInput`, `ScoreState`, decision Literal |
| `wf_03_conditional_route/steps.py` | W: WF-03 | Score threshold decision |

WF-01 intentionally has no empty state.py. Workflow functions may be called directly in unit
tests, but end-to-end flow tests use kickoff. Similar tiny formulas are not grounds for a shared
utils module. Future execution/observability/config folders stay reserved until needed.

## Tests: the folder identifies the subject

| Test folder | Files | What it proves |
|---|---|---|
| `tests/workflows/wf_01_step_sequence/` | `test_steps.py`, `test_flow.py` | Message transformations, order, downstream skip on failure |
| `tests/workflows/wf_02_shared_state/` | `test_steps.py`, `test_state.py`, `test_flow.py` | Math, input schema, history and no state leakage |
| `tests/workflows/wf_03_conditional_route/` | `test_steps.py`, `test_state.py`, `test_flow.py` | Boundary scores, input validation, exactly one route |

Because repeated test filenames will exist, add `__init__.py` consistently in `tests/`,
`tests/workflows/` and each named workflow test package (or explicitly adopt pytest importlib
mode after a compatibility check). Proposed default: package markers, preserving current
pytest mode. Verify collection alongside existing `tests/tooling` and `tests/cli`; no sys.path
patches inside individual tests. These package markers are structural files, not shared logic.

## Documentation and task placement

After approval this review folder becomes `designs/stages/01-crewai-flows/` with the same
README/architecture/plan/learning/workflows/diagrams structure. Add three shared Python tasks,
named **WF-01 Sequence**, **WF-02 State**, **WF-03 Route**, invoking `agent_playbook.cli`
with `dev-run --workflow wf-01`, etc. Existing Run/Dev Run default to WF-01. Workflow-specific
instructions belong in each lesson; the durable CLI guide lists public options centrally.
