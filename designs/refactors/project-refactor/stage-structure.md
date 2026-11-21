# Stage and milestone structure

Sharon approved this documentation structure and authorized applying it in draft [PR #59](https://github.com/SharonLanger/agent-playbook/pull/59) during the 2026-11-18 conversation. That approval covers the organization and the two guarded amendments below. It approves no individual stage, milestone contract, implementation or merge.

The implementation target is `docs/project-refactor`. The [starting PR head](https://github.com/SharonLanger/agent-playbook/commit/514f5360c7d986937178fb26a8b464a4462635d8) already includes the proposal and Drive-link cleanup. Its base is [`main` at `cdbc06c2`](https://github.com/SharonLanger/agent-playbook/commit/cdbc06c2e9a9b87910b5145ac116aeb8a81e06e4). This record documents the conversational approval. The reviewed candidate SHA is recorded in the implementation evidence.

## Approved structure

| Location | Contents |
|---|---|
| `designs/stages/<two-digit-number>-<slug>/` | `README.md`, `requirements.md` and `decisions.md`. Add `learning/` and `research/` when they have material. |
| `m<number>-<outcome-slug>/` under the stage | `README.md`, `design.md`, `test-cases.md` and `implementation-plan.md` |
| `reviews/` under the milestone | `status.md` and the folders for review rounds actually run |

The stage README contains one canonical milestone/status table and the next action. Each row identifies the outcome, design approval and exact approved revision, implementation and PR, verification and review evidence, acceptance and merge state. The milestone README provides detail and links. Use [repository-wide progress](../../progress.md) for the project roll-up. Avoid separate stage `milestones.md` or `progress.md` copies.

Agree on the stage boundary and all milestone outcomes upfront. Approve and pin each milestone's design, test cases and implementation plan together before implementing it. Keep one draft Stage Design PR for the stage and one implementation PR per milestone. The Stage Design PR stays open through closeout and merges only with Sharon's explicit authorization for that PR.

## Implementation scope

- Update the guarded [stage and milestone working method](../../governance/stage-milestone-workflow.md) to define the directory contents, README status ownership, incremental approval and PR lifecycle.
- Update the guarded [project structure](../../project-structure.md) to record placement and link to the working method for procedure. Keep the [design index](../../README.md) and [Atlas](../../atlas/README.md) navigation aligned with the canonical method.
- Keep this decision and its review record with the [project refactor](README.md). Preserve the prior proposal and link cleanup. The shared-learning and root-sandbox migration, archive path and six retained filenames remain proposed.

Existing and historical stages, named working packages, combined milestone folders, stable IDs and frozen contracts remain in their established locations. The compatibility examples are Stage 02's [workflow-integration package](../../stages/02-langfuse/m4-workflow-integration/README.md) and Stage 04's separate [draft design PR](https://github.com/SharonLanger/agent-playbook/pull/45). Leave separately owned PRs alone. This change creates no stage or milestone packages, empty learning or research folders, or placeholder review reports.

The [2026-11-21 Stage 02 alignment note](stage-alignment.md#stage-02-documentation-relocation--2026-11-21) records Sharon’s later location approval for that completed stage.

The [charter](../../charter.md), [principles](../../principles.md), [design contract](../../governance/design-contract.md) and [guarded-file register](../../governance/guarded-files.md) govern the amendment. The [exploration index](../../explorations/README.md) gives context for research ownership. Its candidate runtime paths are outside this change. Stage acceptance and project progress do not change. Official guides need no update because commands, configuration and supported behavior are unchanged. Application files, tests and personal examples are outside the scope.

## Acceptance checks

| ID | Check |
|---|---|
| SS01 | The working method and project structure agree on stage and milestone locations. The required documents and optional learning and research have clear owners. Existing layouts and stable IDs are preserved. |
| SS02 | The stage README owns the canonical milestone/status table and next action. Design approval, implementation, verification, acceptance and merge states are distinct. The repository progress authority remains linked. |
| SS03 | The documentation distinguishes upfront outcomes from incrementally approved exact design, test and plan revisions. It specifies one draft Stage Design PR and one implementation PR per milestone, with the separate stage closeout and explicit merge gate. |
| SS04 | The workflow and handover rules agree on two independent reviews of one frozen SHA, no more than three rounds, four permanent reports per used round, preservation of failures and a blocked disposition after unresolved round three. |
| SS05 | The diff from the starting PR head is limited to this definition, its refactor and design navigation, the two authorized guarded amendments, Atlas and the actual review evidence. It preserves existing stage and milestone paths, active contracts, prior Drive-link removals and the proposed migration. |
| SS06 | Changed local navigation resolves. The Atlas regenerates and passes its freshness/reference check. Its new navigation points to the canonical workflow without presenting the draft PR's work as merged. |

## Review procedure

Apply the [Codex handover rules](../../governance/codex-handover-rules.md#roles-and-rounds) to this documentation change. The coder verifies SS01–SS06 and records the checks. The design-drift and test-gap reviewers work independently on the same frozen candidate SHA. The orchestrator consolidates findings. If corrections are required, both reviewers check the new candidate in the next round. Stop and report blocked if required findings remain after round three.

Keep `reviews/status.md` and the four reports `implementation.md`, `design-drift.md`, `test-gap.md` and `orchestrator.md` in each used round under this refactor. Preserve failed checks and prior findings with their dispositions. PR #59 stays draft and open for Sharon's review.
