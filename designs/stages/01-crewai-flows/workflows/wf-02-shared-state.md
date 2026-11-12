# WF-02 — Shared State

**Workflow-specific design. Proposed, not implemented.**

New capability: Typed mutable state scoped to one execution.

![WF-02 — Shared State](../diagrams/02-state-animated.svg)
[Optional pause controls](../diagrams/02-state.html) · [Lesson](../learning/03-typed-state.md)

## Ownership

Implementation: `app/src/agent_playbook/workflows/wf_02_shared_state/`.
Tests: `app/tests/workflows/wf_02_shared_state/`.
This flow, its steps and any state models belong only to this workflow. Reuse the application
runner and CLI entry points; do not put this workflow's domain rules in either shared owner.
See [the file map](../file-structure.md) for every proposed file.

## Input

initial=3, increment=2, multiplier=4; strict integers -1000..1000. Unknown fields and non-object JSON are rejected before execution.
Create a fresh Flow instance for each invocation. No randomness, sleeps, filesystem writes,
network operations or model invocations are part of the business steps.

## Execution

1. initialize: value = initial; history = [initial].
2. add: value += increment; append value.
3. multiply: value *= multiplier; append value.
4. finish: return final value, leaving history available to tests.

Expected default outcome: **20; history [3, 5, 20]**.
Start/finish messages identify WF-02 and the step name; they explain execution rather
than replacing state/result assertions. A failing step reports failure and prevents downstream
success. Test failures through dependency replacement scoped to the test, not public flags.

## Tests and review

Required test IDs: S02, V02, F03, F04, F05. Definitions are in [test-plan.md](../test-plan.md).
Check computation, real framework execution and failure behavior separately. Confirm the
expected result manually, then deliberately break one relevant rule, observe the failing
test, and restore it. The full quality gate remains required before release.
