# Stage 01 — Test and acceptance specification

**These are required tests and expected outcomes, not results already obtained.**
Every workflow has its own package under `tests/workflows/`. Shared infrastructure tests
have separate owners. Use actual kickoff for framework integration cases.

| ID | Test location | Case | Expected assertion |
|---|---|---|---|
| S01 | wf_01_step_sequence/test_steps.py | Default and empty decoration | Exact strings including brackets |
| F01 | wf_01_step_sequence/test_flow.py | Fresh kickoff | Correct final string and produce→decorate→finish order |
| F02 | wf_01_step_sequence/test_flow.py | Decorate raises | Failure propagates; finish not called |
| S02 | wf_02_shared_state/test_steps.py | Negative, zero, default operands | Correct integer math |
| V02 | wf_02_shared_state/test_state.py | Strings, bools, unknown fields, bounds | Strict input rejected; no coercion |
| F03 | wf_02_shared_state/test_flow.py | Default input | value 20, history [3,5,20] |
| F04 | wf_02_shared_state/test_flow.py | Input 10,-2,3 | value 24, history [10,8,24] |
| F05 | wf_02_shared_state/test_flow.py | Two consecutive independent runs | No history or state leakage |
| S03 | wf_03_conditional_route/test_steps.py | Scores 0,59,60,100 | Correct inclusive boundary |
| V03 | wf_03_conditional_route/test_state.py | -1,101,true,"80", unknown fields | Input rejected |
| F06 | wf_03_conditional_route/test_flow.py | Score 80 | accept exactly once; revise never |
| F07 | wf_03_conditional_route/test_flow.py | Score 40 | revise exactly once; accept never; successful result |
| F08 | wf_03_conditional_route/test_flow.py | Chosen step raises | Execution error, not business outcome |
| A01 | application/test_workflow_runner.py | Unknown ID or malformed/non-object JSON | Input error; no step executes |
| A02 | application/test_workflow_runner.py | Three workflow IDs | Fresh selected flow only; common result wrapper |
| C01 | cli/test_workflow_commands.py | Defaults and each explicit input | Correct dispatch/help and exit 0 |
| C02 | cli/test_workflow_commands.py | Invalid input / injected execution failure | Exit 2 / exit 1, no success message |
| R01 | releases/test_workflow_launch.py | JSON with spaces and quotes | One preserved argv entry, no shell interpolation |
| R02 | releases/test_workflow_launch.py | Default old release versus explicit new options | Bare run preserved; unsupported options fail visibly |

## Separate release acceptance exercise

Build from a clean committed snapshot using the final PR #28 tooling. Require the full gate.
Verify locked dependency export matches the same committed lock, install without dev tools,
validate hashes/import locations, and execute WF-01, WF-02, WF-03 pass and needs_work through
the installed CLI. Check invalid input and developer-command rejection. Incomplete installation
or verification must never set verified=true. Compare output/state contracts to source runs.

Repeat the build to ensure old output is preserved; select an older release explicitly.
Temporarily edit a source step and show dev-run changes while the installed release does not.
Restore the edit. Record Python, CrewAI, Pydantic, uv versions, commit, wheel/export hashes,
platform, wheel size and total environment size. Do not commit generated distributions.

## Evidence and exclusions

Tests must not contact models or Langfuse. Verify telemetry/tracing settings and perform a
no-credentials/offline runtime probe after dependency installation. A code inspection of env
settings alone is not evidence of zero outbound traffic. Distinguish network setup requirements
from runtime behavior. Actual Mac PyCharm verification belongs to Sharon; Linux checks do not
certify the Mac UI. Parallel, persistence and retry semantics have no acceptance tests here
because they are explicitly deferred, not implicitly supported.


## External configuration follow-up

- Validate selected shared YAML plus partial local and documented environment overrides.
- Reject unknown/missing keys, invalid types and unreadable files before workflow execution.
- Do not echo private values in configuration errors; reject unsafe YAML object tags.
- Verify explicit path precedence, cwd-independent source defaults and installed path requirements.
- Apply startup settings before CrewAI import; reject changed startup settings in a reused process.
- Run the same code with an edited external file and observe changed event display.
- Forward the shared configuration to installed releases without exposing editable Python imports.
- Verify releases with a dedicated offline fixture; inspect the wheel for excluded active/local settings.

## Approved successor

The [workflow-contract test plan](../../refactors/workflow-contract/test-plan.md) adds ABC, registry, selected YAML and typed-result coverage. The original CrewAI flow regression scenarios above remain required.
