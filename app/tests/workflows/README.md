# Workflows tests

Tests for `workflows/` cover the shared lifecycle contract, typing contract,
execution context and application-facing workflow wrappers.

The `wf_01_step_sequence/`, `wf_02_shared_state/` and `wf_03_conditional_route/`
folders cover each workflow's flow and steps, with state tests where applicable.
Shared application-runner tests live in [application tests](../application/README.md).
