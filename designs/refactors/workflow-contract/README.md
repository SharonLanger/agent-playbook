# Workflow contract refactor

Status: **Design approved by Sharon for implementation on 2026-11-13. Implementation is in review on `feat/workflow-contract`.**
Updated: 2026-11-13. Source baseline: main at `a4264ac985005b6e9c104bf8a8c4c1f1492abfb1` (PR #35 merged; PR #34 runtime split preserved).

## Goal

Adding a workflow should require its own implementation, a stable registry entry, YAML configuration and tests. The shared runner must not acquire another workflow-ID branch, CrewAI flow union or workflow-specific output check.

CrewAI retains orchestration, decorated steps, routing and business state. Our workflow ABC owns application-facing preparation, execution, output validation, serialization and their call-order guards.

## Read in order

| Document | Purpose |
|---|---|
| [Design](design.md) | Contracts, lifecycle transitions, configuration, typed results and errors |
| [File structure](file-structure.md) | Proposed folders, files, ownership and dependencies |
| [Test plan](test-plan.md) | Lifecycle, isolated runner, configuration, real flows, CLI and release scenarios |
| [Implementation plan](implementation-plan.md) | Review gate, milestones, estimates, risks, guarded changes and Langfuse handoff |

The [living discussion record](https://chatgpt.com/space/page_c032a077e22c8191b5c91d3b96a38d23) retains the decision history. This repository package contains the concrete proposal for implementation review.

## Decisions carried forward

- Python ABC with public lifecycle methods marked `@final`; subclasses implement `_prepare`, `_execute`, `_validate_output` and `_serialize_output`.
- One shared enum and transition implementation; separate read-only status on every instance.
- Failures are explicit, retain their phase and cause, and stop that attempt. No automatic retries.
- YAML uses stable implementation keys mapped to actual Python classes. No import strings, configurable module root or dynamic plugin discovery.
- Workflow definitions remain in `app/application.yaml`. Several IDs can select the same implementation with different configuration.
- Validate only the selected workflow entry and its implementation-specific settings. Invalid shared YAML still fails.
- Preserve rich validated results internally. CLI presentation remains a separate string produced by the workflow.
- Preserve WF-01/02/03 computations, routing, inputs, CLI text and exit codes.
- No compatibility work for old installed releases consuming new configuration.
- Context and Langfuse are the next separate integration step.
- Child/composite workflows and recovery are future features.

## Authority and readiness

Sharon approved the direction and lifecycle/error behavior in the 13 November discussion and requested documentation only. He explicitly authorized revising Stage 01's base-class restriction. The narrow Stage 01 clarification is included; Sharon approved the remaining per-file guarded changes listed in the implementation plan for this implementation PR.

There are no unresolved product decisions preventing review of this package. Precise typing, import-order and framework failure behavior have explicit implementation gates; passing them is not claimed here. Sharon gave the implementation go-ahead on 2026-11-13.

This package is permanent refactor material under `designs/refactors/`. It is not a product guide, a new framework, or authorization to implement future observability or recovery designs.
