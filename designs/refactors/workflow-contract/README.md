# Workflow contract refactor

Status: **Approved workflow-contract design. Implementation PR #40 is in review; I-1–I-4 and Q1–Q4 are implemented on its branch, with final verification recorded in the follow-up evidence; pending review.**
Updated: 2026-11-13. Source baseline: main at `a4264ac985005b6e9c104bf8a8c4c1f1492abfb1` (PR #35 merged; PR #34 runtime split preserved).

## Goal

Adding a workflow should require its own implementation, a stable registry entry, YAML configuration and tests. The shared runner must not acquire another workflow-ID branch, CrewAI flow union or workflow-specific output check.

CrewAI retains orchestration, decorated steps, routing and business state. Our workflow ABC owns application-facing preparation, execution, output validation, serialization and their call-order guards.

Start with [review-follow-up.md](review-follow-up.md) for the A1–F6 test matrix, then [review-test-quality.md](review-test-quality.md) for the second review's Q1–Q4 corrections and sensitivity evidence. The original review assessed PR #40 at b3d279b; the second review assessed it at f61683c. The implementation branch preserves both rounds of corrections.

## Read in order

| Document | Purpose |
|---|---|
| [Design](design.md) | Contracts, lifecycle transitions, configuration, typed results and errors |
| [File structure](file-structure.md) | Proposed folders, files, ownership and dependencies |
| [Test plan](test-plan.md) | Lifecycle, isolated runner, configuration, real flows, CLI and release scenarios |
| [Implementation plan](implementation-plan.md) | Milestones, risks, guarded changes and Langfuse handoff |
| [Review follow-up](review-follow-up.md) | Current corrections, test-gap matrix, release checks and implementation-agent instructions |
| [Second review and Q1–Q4 evidence](review-test-quality.md) | Corrected test assertions, negative controls and final review evidence |

The [living discussion record](https://chatgpt.com/space/page_c032a077e22c8191b5c91d3b96a38d23) retains the decision history. This repository package is the implementation contract. The review follow-up records the latest decision to add lazy dependency imports before context integration.

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
- Load concrete flow dependencies only for the selected workflow; release verification still exercises every built-in implementation.
- Context and Langfuse are the next separate integration step.
- Child/composite workflows and recovery are future features.

## Authority and readiness

Sharon approved the workflow ABC design and the enumerated guarded changes for implementation in PR #40. After the review he requested lazy dependency loading now, constructor and diagnostic fixes, and completion of the planned tests. The precise follow-up and evidence requirements are in [review-follow-up.md](review-follow-up.md).

The reviewer independently verified the original PR #40 head with 166 passing tests and passing type/lint/format checks, but identified coverage gaps and three reproduced issues. That evidence does not establish follow-up completion. The follow-up implementation is being verified on PR #40; neither PR is authorized to merge by this document.

This package is permanent refactor material under designs/refactors. Children, recovery, optional-package installation profiles and context/Langfuse remain separate scopes.
