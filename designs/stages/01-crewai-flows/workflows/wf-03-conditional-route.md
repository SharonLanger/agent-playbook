# WF-03 — Conditional Route

**Workflow-specific implementation and learning guide.**

New capability: Exclusive routing from validated state.

![WF-03 — Conditional Route](../diagrams/03-route-pass-animated.svg)
[Optional pause controls](../diagrams/03-route-pass.html) · [Lesson](../learning/04-routing.md)

### Alternative valid outcome: score 40

![WF-03 — Needs work route](../diagrams/04-route-needs-work-animated.svg)

## Ownership

Implementation: `app/src/agent_playbook/workflows/wf_03_conditional_route/`.
Tests: `app/tests/workflows/wf_03_conditional_route/`.
This flow, its steps and any state models belong only to this workflow. Reuse the application
runner and CLI entry points; do not put this workflow's domain rules in either shared owner.
See [the file map](../file-structure.md) for file ownership.

## Input

score=80; strict integer 0..100. Unknown fields and non-object JSON are rejected before execution.
Create a fresh Flow instance for each invocation. No randomness, sleeps, filesystem writes,
network operations or model invocations are part of the business steps.

## Execution

1. begin: return the validated score.
2. choose: route pass for score >= 60, otherwise needs_work.
3. accept OR revise: set decision and return it; only one runs.

Expected default outcome: **pass for 80; needs_work for 40; both exit 0**.
Start/finish messages identify WF-03 and the step name; they explain execution rather
than replacing state/result assertions. A failing step reports failure and prevents downstream
success. Test failures through dependency replacement scoped to the test, not public flags.

## Tests and review

Required test IDs: S03, V03, F06, F07, F08. Definitions are in [test-plan.md](../test-plan.md).
Check computation, real framework execution and failure behavior separately. Confirm the
expected result manually, then deliberately break one relevant rule, observe the failing
test, and restore it. The full quality gate remains required before release.

## Read the implemented code

| File | Read | Ownership |
|---|---|---|
| [state.py](../../../../app/src/agent_playbook/workflows/wf_03_conditional_route/state.py) | ScoreInput, ScoreState and Decision | WF-03 schemas and route vocabulary |
| [steps.py](../../../../app/src/agent_playbook/workflows/wf_03_conditional_route/steps.py) | decide(score) | WF-03 threshold rule |
| [flow.py](../../../../app/src/agent_playbook/workflows/wf_03_conditional_route/flow.py) | begin, choose, accept, revise | WF-03 exclusive routing |
| [test_steps.py](../../../../app/tests/workflows/wf_03_conditional_route/test_steps.py) | 0, 59, 60, 100 | WF-03 boundary tests |
| [test_state.py](../../../../app/tests/workflows/wf_03_conditional_route/test_state.py) | Invalid and injected fields | WF-03 validation tests |
| [test_flow.py](../../../../app/tests/workflows/wf_03_conditional_route/test_flow.py) | One branch only, terminal failure | WF-03 real-flow tests |

Decision is a Literal type with two allowed strings: pass and needs_work. ScoreInput accepts
only strict integer score 0..100. ScoreState starts with decision=None because no branch has
completed yet. The shared runner validates input and constructs the flow; it knows none of
the threshold rules.

## Follow the router

Use **WF-03 Route** for default score 80. Begin returns the validated score. The `@router(begin)`
method calls the pure decide function. Its returned label selects exactly one listener:
`@listen("pass")` calls accept; `@listen("needs_work")` calls revise. That method writes the
state decision and returns it. There is no join that waits for the branch that was skipped.

```sh
app/.venv/bin/agent-playbook dev-run --workflow wf-03 --input '{"score":80}'
app/.venv/bin/agent-playbook dev-run --workflow wf-03 --input '{"score":40}'
```

For 80, application messages show begin → choose → accept, then `result: pass`.
For 40, they show begin → choose → revise, then `result: needs_work`. Both exit 0.
Set breakpoints in accept and revise, run each input and verify only one is reached. The two
animations above show separate example executions, not branches running simultaneously.

## Verify the boundary and failure semantics

Use **Test WF-03**. Pure tests check the exact >=60 rule, including 59 and 60. Flow tests call
real kickoff, assert state and result, count the chosen step once and assert the unchosen
step never starts. A final-value assertion alone could miss accidental execution of both.

The terminal-failure test injects a state model that rejects assigning needs_work. It runs the
actual ConditionalRouteFlow, reaches revise, raises during state assignment and verifies that
no valid decision or accept execution is reported. The failure is injected only in the test;
there is no production failure flag or copied framework scheduler.

Exercise: temporarily change >=60 to >60 in decide. Predict that score 60 changes to needs_work
while 59 and 80 retain their outcomes. The boundary test fails; restore the original rule.
Try score 101 or `"80"`: validation rejects them before begin, with exit 2. A terminal Python
exception is an execution failure (exit 1), while a low but valid score is a normal result.

The route names and threshold belong only to WF-03. Future workflows get their own package,
state and test folder. They can reuse selection, input-error presentation and release plumbing
without changing this graph or colliding with these route labels in a separate flow instance.
