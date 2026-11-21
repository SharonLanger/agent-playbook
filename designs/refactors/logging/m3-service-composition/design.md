# Logging M3 service control

Working design, revised 2026-11-21 after Sharon's Mac verification. PR #57 owns the design of one explicit command to start enabled local services. Runtime implementation follows agreement on the interface and review of the revised design, tests and plan.

## Agreed behavior

- Reuse the existing VictoriaLogs and Langfuse Compose projects. Each can start and stop independently. An explicit shared start reads the existing application configuration and starts each service whose integration is enabled. Running a workflow never starts Docker.
- Keep the Docker project identities `agent-playbook-logging-smoke` and `observability`. [Issue #56](https://github.com/SharonLanger/agent-playbook/issues/56) owns the future names `act-logs` and `act-langfuse`. M3 requires neither data migration nor a clean install. Ordinary stop/start preserves the project's volumes.
- Reuse the existing settings loader, local overrides and component startup paths. Application credentials belong in the existing external file selected by `secrets.file`, normally `~/.config/agent-playbook/secrets.env`. Langfuse setup generates its own ignored deployment settings. VictoriaLogs currently requires no credential.

## Interface for discussion

Proposed checkout command: `agent-playbook services --start`. With logging alone enabled, it starts VictoriaLogs. With both enabled, it attempts both independently. With neither enabled, it reports that there is nothing to start. Repeating start should also work when a component is already running.

Propose matching `--status` and `--stop` actions. Status reports each component separately. Stop acts on the managed projects even if their configuration has since been disabled. For individual control, retain the existing Langfuse command and logging Compose commands. A full logging CLI, guided first-time setup and combined doctor are later work.

Reuse each service's readiness check with a bounded wait and the configured local URL. If one component fails, report which service failed, continue with the other enabled service and return an unsuccessful command result. A readiness check reports whether the service responds. Actual stored logs and traces verify delivery.

## Implementation sequence once approved

1. Agree on the shared command spelling, actions and first-release scope.
2. Bring the test cases and implementation plan into line with this design. Cover the four enabled combinations, repeat start, independent failure, stop after disabling, volume persistence and bounded readiness. Default tests run without Docker. Live Compose checks are opt-in.
3. Review the revised contract, then implement the small coordinator using the existing component operations. Publish copyable Mac verification steps with the implementation.

## Mac evidence and review history

Sharon ran a real workflow on the existing services. He observed the trace in Langfuse, DEBUG records in VictoriaLogs and the same correlation ID in both. This verifies the current integration. Verification of the proposed shared command and the remaining M2 failure/shutdown cases is pending.

The [previous design](https://github.com/SharonLanger/agent-playbook/blob/3c641fe4760adfcd487e6eacdc468bcf44148236/designs/refactors/logging/m3-service-composition/design.md), its reviews and the earlier follow-up record preserve the prior scope. The earlier tests and implementation plan require revision before handoff. The previous review exhausted its three rounds. The revised contract awaits a new review plan and approval.
