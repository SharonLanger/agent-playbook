# WF-01 — Step Sequence

**Workflow-specific implementation and learning guide.**

New capability: Start/listen dependencies and return-value passing.

![WF-01 — Step Sequence](../diagrams/01-sequence-animated.svg)
[Optional pause controls](../diagrams/01-sequence.html) · [Lesson](../learning/02-sequence-and-values.md)

## Ownership

Implementation: `app/src/agent_playbook/workflows/wf_01_step_sequence/`.
Tests: `app/tests/workflows/wf_01_step_sequence/`.
This flow, its steps and any state models belong only to this workflow. Reuse the application
runner and CLI entry points; do not put this workflow's domain rules in either shared owner.
See [the file map](../file-structure.md) for file ownership.

## Input

No fields; absent input or {}. Unknown fields and non-object JSON are rejected before execution.
Create a fresh Flow instance for each invocation. No randomness, sleeps, filesystem writes,
network operations or model invocations are part of the business steps.

## Execution

1. produce: make_message() returns Hello, workflow!.
2. decorate: wrap the previous string in brackets.
3. finish: return the decorated string.

Expected default outcome: **[Hello, workflow!]**.
Start/finish messages identify WF-01 and the step name; they explain execution rather
than replacing state/result assertions. A failing step reports failure and prevents downstream
success. Test failures through dependency replacement scoped to the test, not public flags.

## Tests and review

Required test IDs: S01, F01, F02. Definitions are in [test-plan.md](../test-plan.md).
Check computation, real framework execution and failure behavior separately. Confirm the
expected result manually, then deliberately break one relevant rule, observe the failing
test, and restore it. The full quality gate remains required before release.

## Read the implemented code

| File | Read | Ownership |
|---|---|---|
| [steps.py](../../../../app/src/agent_playbook/workflows/wf_01_step_sequence/steps.py) | `make_message`, `decorate_message` | WF-01 string rules only |
| [flow.py](../../../../app/src/agent_playbook/workflows/wf_01_step_sequence/flow.py) | `StepSequenceFlow.produce`, `decorate`, `finish` | WF-01 scheduling and messages |
| [runner.py](../../../../app/src/agent_playbook/application/runner.py) | wf-01 selection and empty-input rule | Shared selection boundary |
| [test_steps.py](../../../../app/tests/workflows/wf_01_step_sequence/test_steps.py) | Default and empty-string behavior | WF-01 unit tests |
| [test_flow.py](../../../../app/tests/workflows/wf_01_step_sequence/test_flow.py) | Real kickoff, exact order, failure skip | WF-01 framework tests |

There is no WF-01 state.py. The generic Flow still maintains its own internal state/ID, but
this exercise passes the message as a return value. The type parameter `FlowState` uses CrewAI's built-in ID-only state, keeping the generic
explicit for Pyright without inventing an application state model.

## Run and follow the value

Use **WF-01 Sequence** in PyCharm. From the repository root:

```sh
app/.venv/bin/agent-playbook dev-run --workflow wf-01
```

The runner rejects any input fields, creates a fresh StepSequenceFlow, then calls kickoff.
`produce` calls make_message and returns a string. `@listen(produce)` supplies that string
as decorate's `message` parameter. Decorate calls decorate_message and returns the bracketed
string. Finish receives it and returns it unchanged. The runner wraps the successful value
in RunResult; the CLI prints the result. No workflow calls the CLI to print its final status.

```text
[WF-01] produce started
[WF-01] produce finished
[WF-01] decorate started
[WF-01] decorate finished
[WF-01] finish started
[WF-01] finish finished
[WF-01] result: [Hello, workflow!]
```

Set breakpoints on the first executable line of each method in flow.py and use Debug.
Inspect `message` entering decorate and finish. Returning from a method releases its listener;
source-code ordering alone is not a workflow definition. Only decorated dependencies drive it.

## Verify and experiment

Use **Test WF-01**. `test_real_kickoff_and_order` verifies both the final return and all six
application messages. `test_failure_skips_finish` patches the domain decoration function to
raise, executes real kickoff and verifies that finish never starts. It does not simulate
CrewAI by manually calling the three methods.

Exercise: temporarily make decorate_message return braces instead of brackets. Predict the
failed unit and flow assertions, run the test button, then restore the brackets. Pyright
will still accept both strings: types and behavioral contracts prove different things.
Then read the failure test rather than adding a permanent `--fail` production option.

The only reusable pieces here are the runner, CLI/result contract and framework. The message,
bracket rule and step names remain WF-01-specific. Continue with WF-02 after you can explain
how the return value reaches the next listener without an ordinary explicit function call.
