# Shared learning and root sandbox migration

[PR #59](https://github.com/SharonLanger/agent-playbook/pull/59) applies this documentation migration on the draft branch `docs/project-refactor`. The exact source is [`ef7b22492d6091c8c4b47c4226a24550a9b23ccb`](https://github.com/SharonLanger/agent-playbook/commit/ef7b22492d6091c8c4b47c4226a24550a9b23ccb). Main was [`cdbc06c2e9a9b87910b5145ac116aeb8a81e06e4`](https://github.com/SharonLanger/agent-playbook/commit/cdbc06c2e9a9b87910b5145ac116aeb8a81e06e4) at preflight. The PR remains draft and unmerged for Sharon's final disposition.

## Authorization and placement

On 2026-11-19 Sharon requested both cleanup tasks using the filenames and archive proposed in the [project refactor](README.md). The approved logical changes keep the system-wide walkthrough next to the target architecture, put historical System One Harness decisions under the owning refactor, and keep a curated root sandbox for historical references and draft ideas. Stage-specific learning stays with its stage.

| Guarded file | Authorized change |
| --- | --- |
| [Architecture](../../architecture.md) | Point the existing live walkthrough link at its new location. System behavior and approved boundaries are unchanged. |
| [Project structure](../../project-structure.md) | Describe the curated root sandbox and record ownership of the system-wide walkthrough, stage-local learning and refactor archives. The runtime, dependency rules and approved application responsibilities are unchanged. |

The [charter](../../charter.md), [principles](../../principles.md), [design contract](../../governance/design-contract.md) and [guarded-file register](../../governance/guarded-files.md) govern this migration. The charter already keeps historical experiments separate. Principle 11 is met by explicit scope, preserved originals in Git, byte-identical archival and reviewable changes. The [role and execution exploration](../../explorations/agent-execution/README.md) and [harness exploration](../../explorations/harness.md) explain why these materials remain historical or draft.

## Applied dispositions

These are all two shared-learning files and all 17 root-sandbox files at the exact migration base. The linked originals preserve the source paths and versions.

| Original file at migration base | Applied disposition |
| --- | --- |
| [`designs/learning/architecture-walkthrough.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/designs/learning/architecture-walkthrough.md) | [Moved system-wide walkthrough](../../architecture-walkthrough.md) |
| [`designs/learning/README.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/designs/learning/README.md) | [Folded into the design index and retired at its old location](../../README.md#learning) |
| [`sandbox/agents/reviewer.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/agents/reviewer.md) | [Reviewer, evidence and earlier handoff protocol](../../../sandbox/references/reviewer.md) |
| [`sandbox/agents/designer.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/agents/designer.md) | [Former design and approval process](../../../sandbox/references/designer.md) |
| [`sandbox/verification/reviewer-handoff.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/verification/reviewer-handoff.md) | [Historical delivery and readback checklist](../../../sandbox/references/reviewer-handoff.md) |
| [`sandbox/projects/agent-playbook/features/f-01-reviewer-trial/design.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/projects/agent-playbook/features/f-01-reviewer-trial/design.md) | [Draft `f-01-reviewer-trial`](../../../sandbox/ideas/reviewer-trial.md) |
| [`sandbox/projects/agent-playbook/features/f-02-implementer-handoff/design.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/projects/agent-playbook/features/f-02-implementer-handoff/design.md) | [Draft `f-02-implementer-handoff`](../../../sandbox/ideas/implementer-handoff.md) |
| [`sandbox/projects/agent-playbook/features/f-03-design-deviations/design.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/projects/agent-playbook/features/f-03-design-deviations/design.md) | [Draft `f-03-design-deviations`](../../../sandbox/ideas/design-deviations.md) |
| [`sandbox/projects/system-one-harness/features/f-01-offline-test-suite/design.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/projects/system-one-harness/features/f-01-offline-test-suite/design.md) | [Archived offline test suite design](archive/system-one-harness/features/f-01-offline-test-suite/design.md) |
| [`sandbox/projects/system-one-harness/reviews/pr-46.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/projects/system-one-harness/reviews/pr-46.md) | [Archived PR 46 requirements](archive/system-one-harness/reviews/pr-46.md) |
| [`sandbox/agents/code-writer.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/agents/code-writer.md) | Retired unimplemented writer placeholder |
| [`sandbox/agents/orchestrator.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/agents/orchestrator.md) | Retired unimplemented routing placeholder |
| [`sandbox/agents/replanner.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/agents/replanner.md) | Retired deferred-role placeholder |
| [`sandbox/agents/tester.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/agents/tester.md) | Retired deferred-role placeholder |
| [`sandbox/workflows/implement-change.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/workflows/implement-change.md) | Retired unimplemented workflow placeholder |
| [`sandbox/projects/project-a/review-rules.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/projects/project-a/review-rules.md) | Retired example rules template |
| [`sandbox/projects/project-a/reviews/pr-14.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/projects/project-a/reviews/pr-14.md) | Retired example PR naming placeholder |
| [`sandbox/README.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/README.md) | [Rewritten root sandbox index](../../../sandbox/README.md) |
| [`sandbox/AGENTS.md`](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/AGENTS.md) | [Rewritten root sandbox maintenance instructions](../../../sandbox/AGENTS.md) |

The archived PR 46 requirements retain their internal link to the archived draft design, external PR references and later file-persistence clarification. The retained ideas keep their original IDs and draft approval caveats. The six moved sandbox records identify former instructions and paths as historical. The reviewer reference retains the earlier cleanup's explicit-supplied-destination rule.

## Verification and review

| ID | Acceptance criterion |
| --- | --- |
| LSM01 | Exactly 19 source files have recorded dispositions. There are no files under the old shared-learning directory. Root sandbox has exactly its two maintenance files and the six retained Markdown files. |
| LSM02 | The walkthrough preserves its target explanation and resolves both diagram links. The design index surfaces it directly, distinguishes the architecture's authority and links to stage learning. |
| LSM03 | The six retained documents preserve substantive source content, IDs, revision and approval context. Current framing keeps their old role paths and permissions historical. The old source links and new sandbox navigation resolve. |
| LSM04 | Both archived files match the source blobs byte-for-byte. The archived PR rules link to the archived draft design. The seven placeholders are absent from the working tree and accessible in Git history. |
| LSM05 | Atlas rebuild and freshness checks pass. Current shows the moved walkthrough as draft PR documentation and excludes sandbox internals. Explorations labels all 19 old paths as historical and pins the main snapshot. Live links and anchors resolve. |
| LSM06 | The two guarded diffs match approval. Charter, principles, guard register, existing stage records, completed review evidence and all application paths retain their source tree entries. The changed documentation introduces no private destination link or ID. PR #59 remains draft and unmerged. |

Principles 1, 3, 4, 8, 9, 11, 12, 13, 14 and 15 apply through the documented approval, preserved runtime and learning boundaries, checked evidence, bounded scope, explicit migration, source provenance, personal-sandbox isolation, guide assessment and draft status. Principle 2 applies to preserving the prior privacy cleanup. Principles 5, 6, 7 and 10 govern integrations, runtime configuration, application quality gates and deployment. This move changes none of those surfaces.

The application, its supported commands and its official guides are unaffected. This document-only migration calls for navigation, preservation and scope checks. The application gate is outside this change. Project progress, stage contracts and previous reviews retain their own evidence. PRs #45 and #51 overlap on shared design navigation or Atlas paths and may need reconciliation by their owners when integrating main. PR #57 has no path overlap with the migration.

Independent review uses the existing bounded review method, with this migration's reports under `reviews/learning-sandbox/`.
