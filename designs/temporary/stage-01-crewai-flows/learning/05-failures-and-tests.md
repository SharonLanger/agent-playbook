# Lesson 5 — Failure is not another successful string

A useful workflow exercise includes both valid outcomes and broken execution. These are
separate cases with different exit statuses and different tests.

## Four layers of tests

| Layer | Example | Why it exists |
|---|---|---|
| Pure step | decorate a string, add numbers, compare threshold | Verify computation without framework setup |
| Input/state | reject `true` as integer; independent history | Verify boundaries and data ownership |
| Real flow | call kickoff; inspect actual route/order/state | Verify CrewAI wiring instead of a hand-written imitation |
| Application/CLI/release | invoke selected flow, capture process exit, run installed wheel | Verify integration and packaging |

## Deliberate failure exercise

In a WF-01 integration test, replace the workflow's decoration operation with a callable
that raises `RuntimeError("exercise failure")`. Capture events or spy on finish. Expected:
produce completes; decorate starts then fails; finish is never called; failure propagates.
A separate CLI test verifies exit 1 and an error containing the workflow identifier. Neither
test should accept a final success message. Restore the operation through test cleanup.

Do not add a production failure flag just to demonstrate an exception. Do not monkeypatch
CrewAI's entire scheduler: the purpose is to test real framework failure behavior.
Do not sleep or call a model to manufacture a failure.

## Input failures

Malformed JSON, arrays, unknown fields, numeric strings and out-of-range numbers fail before
any workflow step starts. CLI usage errors and application input errors both map to exit 2.
Use a side-effect spy to prove no steps started; an error message alone is insufficient.

## Repeatability

Default inputs always produce the same business result and step ordering. Framework UUIDs
or diagnostic timestamps may differ; do not assert their exact text. Repeat WF-02 with two
different inputs to catch accidental reuse of a flow instance. Captured step messages are
teaching output, not a durable event store or Stage 02 telemetry implementation.

## Regression discipline

Keep workflow test folders separate. Shared CLI tests assert reusable behavior, while domain
assertions live under their workflow. Use temporary files and restore deliberate edits.
The full `agent-playbook check` must still pass. Do not invoke the full check recursively
from a pytest test. The end-to-end release exercise runs separately from the unit suite.
See [the complete test matrix](../test-plan.md).
