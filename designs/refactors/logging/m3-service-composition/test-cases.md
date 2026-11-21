# Acceptance cases for the revised service CLI

These cases cover the November 21 design. Earlier MC identifiers refer to the earlier contract in Git history.

| Case | Expected observation |
|---|---|
| Shared start | Exercise all four enabled combinations through the CLI. Verify effective overrides, exact targeted components and a successful empty selection. |
| Explicit component | For each group, only its target receives the action. Lock the agreed disabled-start behavior before implementation. Logs-only operations work without Langfuse credentials. |
| Status and stop | Show both states separately or just the selected state. After disabling a running integration it remains visible and stoppable. Repeat stop is safe. |
| Partial failure | A failing component leaves its sibling running. Attempt the other selected component, identify each outcome and return failure. Simulate stalled Docker and HTTP probes to verify the readiness deadline. |
| Compatibility | Exercise existing Langfuse actions, current project identities, local addresses and port selection. Check workflow execution does not invoke service management. |
| Live Mac | Start each service separately and together. Run a workflow, identify its trace and log by matching correlation ID. Stop one while the other remains usable. Restart and find the prior data. Repeat startup without duplicate containers. |

Use simulated component operations for the default Docker-free checks. Make Compose and live checks opt-in. Record actual results separately from proposed checks and keep the remaining M2 LG-10 evidence distinct.
