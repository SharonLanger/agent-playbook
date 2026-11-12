# WF-01 — Step Sequence

**Workflow-specific design. Proposed, not implemented.**

New capability: Start/listen dependencies and return-value passing.

![WF-01 — Step Sequence](../diagrams/01-sequence-animated.svg)
[Optional pause controls](../diagrams/01-sequence.html) · [Lesson](../learning/02-sequence-and-values.md)

## Ownership

Implementation: `app/src/agent_playbook/workflows/wf_01_step_sequence/`.
Tests: `app/tests/workflows/wf_01_step_sequence/`.
This flow, its steps and any state models belong only to this workflow. Reuse the application
runner and CLI entry points; do not put this workflow's domain rules in either shared owner.
See [the file map](../file-structure.md) for every proposed file.

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
