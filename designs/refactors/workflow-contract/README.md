# Workflow contract refactor

**Status: Completed and accepted as part of Stage 01.** Design PR #38 and implementation PR #40 are merged. Sharon confirmed Stage 01 completion after these merges.

Merged implementation: `a98e1041c0edb51a447472b6ebd78ab2a650150b`. Verification evidence remains attached to the revisions on which the checks ran.

## Goal

Adding a workflow should require its own implementation, a stable registry entry, YAML configuration and tests. The shared runner must not acquire another workflow-ID branch, CrewAI flow union or workflow-specific output check.

CrewAI retains orchestration, decorated steps, routing and business state. Our workflow ABC owns application-facing preparation, execution, output validation, serialization and their call-order guards.

The dated [review-follow-up.md](review-follow-up.md) preserves the A1–F6 test matrix; [review-test-quality.md](review-test-quality.md) preserves the Q1–Q4 corrections and sensitivity evidence. The original review assessed PR #40 at b3d279b; the second review assessed it at f61683c. The merged implementation incorporates both rounds of corrections.

## Read in order

| Document | Purpose |
|---|---|
| [Design](design.md) | Contracts, lifecycle transitions, configuration, typed results and errors |
| [File structure](file-structure.md) | Proposed folders, files, ownership and dependencies |
| [Test plan](test-plan.md) | Lifecycle, isolated runner, configuration, real flows, CLI and release scenarios |
| [Implementation plan](implementation-plan.md) | Milestones, risks, guarded changes and Langfuse handoff |
| [Review follow-up](review-follow-up.md) | Historical corrections, test-gap matrix, release checks and implementation-agent instructions |
| [Second review and Q1–Q4 evidence](review-test-quality.md) | Historical corrected assertions, negative controls and verification evidence |

The [living discussion record](https://chatgpt.com/space/page_c032a077e22c8191b5c91d3b96a38d23) retains the decision history. This repository package records the implemented contract. The review follow-up records the decision to add lazy dependency imports before context integration.

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

## Completion and evidence

Sharon approved the workflow ABC design and the enumerated guarded changes for implementation in PR #40. Earlier reviews and their findings remain historical evidence. The I-1–I-4 implementation corrections and Q1–Q4 test corrections were completed before PR #40 merged. Their recorded verification is linked above. This package records the completed workflow-contract refactor.

This package is permanent refactor material under designs/refactors. Children, recovery, optional-package installation profiles and context/Langfuse remain separate scopes.
