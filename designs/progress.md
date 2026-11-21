# Progress and acceptance

## PR CI and local version tracking — 2026-11-21

The [approved package and final review](refactors/pr-ci/README.md) track issue #62. The originating session passed the corrected code on [implementation PR #64](https://github.com/SharonLanger/agent-playbook/pull/64) at `ba9a18a`. The implementation team recorded 483 passing tests and a verified 0.2.0 wheel on Linux. Private hosted jobs were skipped and main is unprotected. Owner acceptance, merges, public activation and the final coordinated fresh run remain pending.

## Logging M2 merged — 2026-11-18

Sharon authorized merging implementation PR #55 after the originating design-session final review passed with no required code corrections. PR #55 merged at `180b6e769d979015ed76e09128e25a32456ed5a4`; the reviewed code/test candidate remains `8770d076c5c586ff9f9830c43432dd127585033c` (reported full gate: 464 tests passed). M1 remains merged through PR #54.

**Required before finalizing logging design PR #51:** close LG-10's manual testing gap with a real local M2 workflow run against VictoriaLogs. Record the exact workflow/correlation identity, inspect stored lifecycle and DEBUG records plus native chained-exception details, check UI ordering, and observe shutdown behavior. LG-10 remains **NOT RUN**; merge authorization does not establish live ingestion or user acceptance. Keep design PR #51 draft/open until this gap is closed and Sharon separately authorizes its finalization/merge. See [M2 review status](refactors/logging/m2-application-logging/reviews/status.md).

## Stage 03 closeout — 2026-11-16

Stage 03 is complete and accepted by Sharon on 2026-11-16. He confirmed that he checked everything and that it was good, authorized removal of the temporary verification scripts, and explicitly authorized merging design PR #52. Implementation PR #53 merged at 529fe15895afc8211d833fc2544e98f0d18fb451. The eight temporary recipe verify.py files are removed in this closeout; existing concept tests and permanent recipe behavior are preserved. Review evidence remains at test-bearing revision 906e0e5921fae726f37c5bdbb61551578373c908. See [Stage 03](stages/03-orchestration-patterns/README.md). Logging and Stage 04 remain separately owned.

## Stage 02 closeout — 2026-11-15

Stage 02 is completed, accepted by Sharon and merged through Stage Design PR #47. Local Langfuse setup/mock work (PR #36), execution context (PR #44), and native runner plus automatic CrewAI tracing (PR #50) are delivered. PR #50 merged at `b08060f0acba74f19bc8a32aedb21316eed149c1`; its reviewed candidate passed 408 tests, static/lint/format checks and installed-release verification. Sharon completed local success, branch, correlation, input/output, readable-name and controlled-failure acceptance. Stage 03 can proceed under its own design approvals.

Application logging is separate work owned by a different agent under `designs/refactors/logging/`, with its own design and implementation PRs. It is outside completed Stage 02 and does not block Stage 03. Earlier logging requirements and research remain historical inputs; this closeout selects no logger, store, viewer or logging architecture and does not create or edit the logging agent’s files.

## Historical checkpoints


## Current acceptance — 2026-11-15

M4.2 + M4.3 native workflow tracing is implemented, final-reviewed and accepted by Sharon; PR #50 merged at b08060f0acba74f19bc8a32aedb21316eed149c1. The reviewed candidate is adbba215da77e1e618c3c699e1d84c1ba45c629e: 408 tests, static/lint/format checks and installed release passed. Sharon completed local success, routing, correlation, input/output, readable-name and controlled-failure checks. M1–M3 and M4.1 remain accepted/merged. Stage Design PR #47 stays open for documentation reconciliation and explicit stage closeout. Logging, real-agent cost/usage and scores/evaluations remain deferred. Earlier pending statements below are historical checkpoints, superseded by this acceptance.

## Earlier status and retained history

Updated 2026-11-15. This file owns current project status; [architecture.md](architecture.md)
describes the target system. Stage summaries own milestone detail and findings retain dated evidence.

## Current status after the PR #36 merge

| Stage | Implementation | Verification | Sharon's acceptance | Merge state |
|---|---|---|---|---|
| Stage 00 — development environment | Complete | Recorded in the [Stage 00 findings](stages/00-environment/findings.md) | Accepted | Merged through PR #26 |
| Stage 01 — CrewAI Flows | Completed and locked; three workflows, CLI/configuration, independent experiments, runtime structure refactor and workflow-contract refactor complete | Revision-specific checks in [Stage 01 findings](stages/01-crewai-flows/findings.md), [runtime refactor evidence](refactors/2026-11-12-runtime-structure/verification.md) and [workflow-contract evidence](refactors/workflow-contract/README.md) | Sharon confirmed Stage 01 completion after PR #38 and PR #40 merged | PR #30, #32, #34, #38 and #40 merged; workflow contract merge `a98e1041c0edb51a447472b6ebd78ab2a650150b` |
| Stage 02 — Langfuse | M1–M3, management CLI and YAML-selected external credentials implemented on PR #36; M4.1 implemented, final-reviewed and accepted; merged via PR #44 at 942e59344c429454263319e783ea76ad297b7ea6; M4.2/M4.3 combined design approved at ab3fab459c97eed44cc0b202402e559a827a71cf; unmerged implementation continues in round 02 under approved SDK-first amendment 82b967d; visible framework defaults enable automatic tracing, with verification/review and local acceptance pending | 363-test gate at `dafeaed`; Sharon confirmed local project access, synthetic traces, trace-ID inspection and stop/start persistence; delivery readback limitation retained | Local setup and mock-trace exercise accepted on 2026-11-14; whole stage remains in progress | PR #36 merged as `44d6919`; application version 0.1.3; final local-state test fix `0a5bf88` included |

Stage 01 details and retained learning material are in the [stage summary](stages/01-crewai-flows/README.md). The [roadmap](roadmap.md) owns intended sequencing; later stages remain high-level.

## M4.1 current closeout — 2026-11-14

M4.1 implemented, independently reviewed and accepted by Sharon; merged via PR #44 at 942e59344c429454263319e783ea76ad297b7ea6. M4.2/M4.3 combined contract is approved; the unmerged `impl/m4-2-3-native-tracing` candidate implements native runner setup/scopes/CLI delivery, round 02 applies the approved visible-framework default and native input/output/naming amendment. Verification/review and local acceptance remain pending. Logging remains deferred. PR #43 merged as c8f129e. Reviewed candidate 16c1580 passed the reported 380-test quality gate/release and final reviewer's independent 43-test rerun. See [final review](stages/02-langfuse/workflow-integration/history/context-final-review.md). Documentation conflicts and duplicate D30 are reconciled without runtime/test changes; the merge was confirmed by GitHub at 942e59344c429454263319e783ea76ad297b7ea6.

## M4.2/M4.3 round-02 continuation — 2026-11-15

Sharon approved SDK-first continuation at `82b967dda1fbf942cc1067a3539328c74abc303a`, supplementing the frozen original `ab3fab459c97eed44cc0b202402e559a827a71cf` contract. The unmerged PR #50 candidate sets visible framework events by default while preserving explicit false, records validated business input/output using native SDK updates, gives maintained Flows native readable names, and suppresses the PyPI update check using CrewAI’s supported switch. Native public project-key scope metadata is the only payload-policy exception; secret/configuration exclusions remain. Round-02 evidence and remaining local checks are recorded in [follow-ups](stages/02-langfuse/workflow-integration/m2-3-workflow-tracing/follow-ups.md). PR #47 remains draft/open; no acceptance or merge is claimed.

## Historical M4.2/M4.3 round-01 checkpoint — 2026-11-15

Sharon approved the design/test/plan at `ab3fab459c97eed44cc0b202402e559a827a71cf` and narrow RUN-G01–08 amendments. Base: main `fefe4cc1065642b710a018ecb1088ececde852db`; governance `293fe88a404f9aa9bd37e897b6d65f0ef4d0ee1f` is included. Branch `impl/m4-2-3-native-tracing` is unmerged. The native setup, runner scopes/three-field propagation and CLI finally delivery are implemented; context/business Flow settings remain unchanged.

Actual runner integration reveals a blocker: OpenInference CrewAI 1.1.25 skips all automatic Flow/method observations under the maintained quiet setting. Tests preserve the expected hierarchy and fail rather than treating runner-only export as complete. See the [permanent follow-up](stages/02-langfuse/workflow-integration/m2-3-workflow-tracing/follow-ups.md) for released-source evidence and unapproved choices. The approved package remains frozen on draft PR #47. Automated verification, independent review, installed-release integration and live UI/user acceptance remain distinct; no completion or acceptance is claimed.

## Historical M4.1 handoff / M4.2 planning — 2026-11-14

[Draft PR #43](https://github.com/SharonLanger/agent-playbook/pull/43) contains the
[context design](stages/02-langfuse/workflow-integration/m1-context/design.md),
[separate test cases](stages/02-langfuse/workflow-integration/m1-context/test-cases.md)
and [Codex implementation/review plan](stages/02-langfuse/workflow-integration/m1-context/implementation-plan.md).
Sharon authorized drafting, accepted a stable application correlation_id and requested
one coder plus independent design-drift/test reviewers, with permanent reports and
at most three total rounds. Sharon now reports sending the explicit M4.1 implementation
authorization at design revision 11bba581291c1b166973848ea8db6a9e2a142413 to Codex.
Implementation results and final review remain pending; the implemented/verified
Stage 02 status above is unchanged. M4.2 preliminary design starts in parallel,
including correlation_id on every workflow-associated Langfuse observation. CrewAI research is bounded
isolated evidence, not real-application or local-UI acceptance.

## Local acceptance and merge — 2026-11-14

The [local acceptance record](stages/02-langfuse/acceptance-2026-11-14.md)
records Sharon's Mac/UI results and the remaining `delivery: unconfirmed`
readback limitation despite visible ingestion. PR #40 is already merged and
accepted; its dated review findings below remain historical. Sharon authorized
merging PR #36 after his planned enable/version push and this reconciliation.
The 0.1.3 enable/version push `dafeaed` passed the complete 363-test gate.
Real workflow/context tracing remains a separate deferred step.

PR #36 was explicitly authorized and merged on 2026-11-14 as `44d69194f6add6f646795b14f7c3f43c656baeda`.
The resulting main was inspected. The isolated local-state regression passed
at `0a5bf88`; the complete 363-test gate remains pinned to `dafeaed`.
The next agent should start from the [acceptance/handoff record](stages/02-langfuse/acceptance-2026-11-14.md).
M4 and logging/context design remain separate work; the delivery-readback
limitation is retained. This merge does not complete all of Stage 02.

## Historical snapshots and revision-specific evidence

The records below preserve the status, decisions and verification known at their dated checkpoints. Statements about open PRs, pending acceptance and next actions within these snapshots are historical, not the current project status above.

## Langfuse branch detail (earlier integration checkpoint)

Sharon approved combining all six conflict resolutions on 2026-11-13.
This branch incorporates main `53764abeb9402d596ee26bef19872fc2ebd7d888`,
including the merged workflow-contract refactor and application version 0.1.2.
PR #36 remains draft and unmerged. Langfuse M1–M3 and the management
helper/CLI are implemented and independently checked. Live ingestion and Sharon's
Mac/UI acceptance remain pending; real workflow/context tracing is deferred.

The histories below retain their original revisions and earlier pending/merged
wording. They are historical evidence, not the current state. Integration
verification and the approved conflict choices are in the
[Stage 02 reconciliation record](stages/02-langfuse/main-reconciliation.md).
The [follow-up resolution](stages/02-langfuse/resolution-2026-11-13.md) records
the SDK/reporting fixes, current checks and live blocker.


| Work | Verified state |
|---|---|
| 00.1 environment | PR #17 merged after user ran main |
| 00.2 CLI | PR #18 merged after user ran help and run |
| 00.3 Pyright | PR #19 merged; user ran Pyright in PyCharm and observed a type error |
| 00.4 pytest | PR #20 merged; user ran Tests in PyCharm and reported four passing tests |
| 00.5 Ruff | PR #21 merged; local IDE configuration was the latest user task |
| 00.6 local gate | PR #22 merged after user accepted the improved check output |
| 00.7 Wheel release | PR #23 merged after user built a release and accepted 00.7 |
| Shared IDE tasks | PR #26 merged; user restored configurations and accepted Stage 00 |
| Target architecture and visuals | PR #25 merged; diagrams and architecture are in main |
| Stage 01 implementation | PR #30 merged after user acceptance; WF-01/02/03, runtime configuration and release verification |
| Principles and compliance | PR #31 merged; security, external settings and principle-review rules |
| Independent workflow examples | PR #32 merged after Sharon reported everything working, including resized diagrams; 132 tests plus type/lint/format checks passed |

The user authorized preparing 00.3–00.7 sequentially. Their review and merge remain
one at a time. After each predecessor merges, retarget its successor to main and
carry any accepted corrections forward. Later stage branches contain older copies
of progress documents; reconcile them instead of restoring obsolete status text.

## Architecture documentation

The target architecture now separates components, execution/failure flow, and
observation flow. Static and animated SVGs share one generator; a local browser
viewer provides playback controls. PR #25 is merged; browser animation verification
remains pending.

Earlier Stage 00 approval is recorded by merged PR #15. Its architecture/plan still
contain historical approval wording, and its acceptance list retains a CrewAI import
item despite excluding CrewAI. Those protected stage files are unchanged in this
visual-documentation PR; their exact correction requires separate review.

## Earlier Stage 01 planning and acceptance

Sharon accepted Stage 00 and approved the pre-Stage 01 folder refactor.
`project-structure.md` records the guarded layout. The refactor separates runtime
components from checkout-only tooling and examples, with reserved future folders.
PR #28 (CLI/tooling refactor) and PR #29 (Stage 01 design) are merged. Sharon approved
implementing all three workflows together and learning them sequentially. Stage 01 code
implements WF-01 sequence, WF-02 typed state and WF-03 exclusive routing, with strict inputs,
shared CLI dispatch and dependency-aware releases. See the permanent Stage 01 findings for
verification evidence and the code-reading guide for the learning order. Sharon accepted the
implementation and independent examples, reporting that everything works. The learning
material remains available for continued experiments; acceptance does not claim every topic
has been studied exhaustively.

Historical examples were delivered under `app/examples/workflows/`. Sharon now designates `app/examples/` as his personal sandbox; it is outside maintained agent work and application testing. Do not inspect it without a specific request. Historical example test counts below/above are retained only as historical evidence. User-facing configuration instructions live in
`app/docs/configuration.md`; YAML is `app/application.yaml`. Documentation navigation is in
`app/docs/README.md`.

Next: discuss Stage 02 (Langfuse observability), agree on the first visible run/step/error
experiment, and approve its design before implementation. No Stage 02 integration has been built.


## Historical Atlas/governance update — PR #35

Sharon approved the logical changes to charter, principles, architecture and project structure, the new guarded design contract, preservation of every existing guard, mandatory placement/reading flow, official-doc maintenance and permanent Current/Explorations Atlas on 2026-11-13. This approval authorizes the documentation work; PR #35 remains a draft for merge review. Detailed reviewer/event-adapter/harness designs remain explorations.

Current implementation snapshot: main `96cb1f8`, merging accepted PR #34. Runtime discovery/launcher, assembly/factory/runner, CLI parser, app-root YAML and examples isolation are implemented. Sharon reported that Verify Refactor passed after a formatting correction and a normal 0.1.1 release completed; those local results precede the final cleanup commit. Earlier 137-test/release evidence applies to its recorded earlier revision, not automatically to the final head.

PR #35 reconciles these facts with the approved guarded governance and permanent Atlas. All existing stage files remain unchanged and protected. Personal examples remain outside unrequested agent work. The deleted internal public-doc review guide and temporary handoff stay deleted; Sharon also authorized removing the temporary review helper and PyCharm task. Application tests and normal quality checks remain.

Stage 02 Langfuse design/research may proceed; implementation requires its approved stage design. Role/event/adapter/harness details remain optional explorations. PR #35 is unmerged pending Sharon's review.

## Historical Langfuse branch record


## Stage 02 milestones — documentation review

On 2026-11-13 Sharon agreed to four checkpoints: local Langfuse UI, a connection check, editable mock runs in his requested app/examples/langfuse playground, and real workflow integration last. The [milestone plan](stages/02-langfuse/milestones.md) replaces the earlier blanket dependency on the workflow refactor: milestones 1–3 are independent; only milestone 4 waits for the merged workflow/context design. Milestones are not mandatory separate PRs; reuse the existing PR/review thread and assess actual overlap before splitting work.

The personal playground is for manual UI learning and scenario edits, not automated acceptance fixtures. Application tests remain independent under app/tests. [Doctor #37](https://github.com/SharonLanger/agent-playbook/issues/37) tracks the requested future diagnostic command. No Stage 02 runtime, deployment, credentials, playground or live telemetry is implemented or verified by this documentation update. Existing stage acceptance and guarded baselines remain unchanged.

### Agent verification and implementation handoff

Sharon requested practical sanity checks before an implementation reaches his manual review, while leaving simple UI/account steps to him when automation would be disproportionate. The stage now has [verification requirements](stages/02-langfuse/verification.md) and a [milestone 1 Codex brief](stages/02-langfuse/implementation-handoff.md). They require actual available checks, explicit blocked/unrun results, targeted smoke runs of the specifically requested new Langfuse playground during M3, and independent automated fixtures. This update is documentation only; no milestone implementation or live verification has been performed.

## Stage 02 milestone 1 — implementation on PR #36

Sharon authorized milestone 1 only. The PR branch now includes a pinned local
Langfuse Compose stack, one-time ignored secret generation and an official UI
setup guide. See [M1 findings](stages/02-langfuse/findings.md) for live
verification, limits and remaining manual acceptance. This pending PR is
implemented and agent-verified, not yet accepted or merged. No Python
integration, playground, workflow or context change is included.

## Stage 02 next implementation assignment

On 2026-11-13 Sharon requested [M2/M3 implementation instructions](stages/02-langfuse/connection-playground-handoff.md) for Codex to work while his M1 local check is pending. M2 connects/authenticates without traces; M3 explicitly sends editable synthetic traces. Separate tested commits and per-milestone Drive text checklists preserve independent verification. Shared configuration files overlap workflow PR #40 and must be reconciled; no zero-conflict claim is made. This handoff update implements neither milestone, changes no guarded meaning, and does not accept M1 or authorize M4. [Verification file status](stages/02-langfuse/user-verification.md).

## Stage 02 milestone 2 — pending PR #36 checkpoint

The branch implements an explicit Langfuse project authentication checker with
disabled-by-default external settings and SDK 5.2.0. Existing workflows are not
instrumented. [M2 findings](stages/02-langfuse/findings.md) record offline and
packaging checks plus the blocked live-auth check. Sharon's local acceptance is
pending. M3 and M4 are not implemented at this checkpoint.

## Stage 02 milestone 3 — pending PR #36 checkpoint

The branch now includes the explicitly invoked personal
`app/examples/langfuse/run.py` mock playground and a narrow observation writer.
No ordinary workflow emits traces. [M3 findings](stages/02-langfuse/findings.md)
record independent adapter tests, targeted personal-script smoke runs and the
blocked live ingestion/readback check. Sharon's M1, M2 and M3 local acceptance
remain pending; M4 is not implemented.


## PR #36 independent review and verification proposal — 2026-11-13

Sharon requested a permanent record of the four review findings and a simpler
manual exercise before implementation resumes. The [review](stages/02-langfuse/review-2026-11-13.md)
applies to PR head `5bfcb889215d000d76629c3d4198d33bea99398d`: a real-SDK
connection/tracing lifecycle defect prevents mock export; rejected export can
still print submission success; latest-main integration remains unresolved;
and some canonical stage status is stale. The review independently passed
Pyright, Ruff and 133 tests, but its actual-SDK HTTP probes reproduced the two
delivery defects. No live server ingestion, Mac UI or persistence acceptance is
claimed. Prior checkpoint results above remain revision-specific history.

Read-only comparison with main `53764abeb9402d596ee26bef19872fc2ebd7d888`
found conflicts in the three configuration files, progress, Atlas catalog and
generated HTML. No merge or resolution was applied. The [proposed follow-up](stages/02-langfuse/verification-simplification-plan.md)
starts with updating from main and agreeing on conflict choices with Sharon,
then delivery fixes, a small lifecycle helper, agent verification and one
current-revision Drive checklist. It awaits agreement; its commands are proposed,
not implemented. Workflow/context integration remains separate.

This update saves review/proposal documents and updates navigation/progress/Atlas
only. It changes no runtime, dependency, guarded baseline or supported product
command; official product guides therefore remain unchanged at this proposal
stage. PR #36 remains draft and unmerged, with all four review items open.

Documentation-only verification: Atlas build/freshness/reference checks passed;
39 relative Markdown links, fenced blocks, whitespace and the six-file change
scope passed. Hash comparison confirmed other copied source files unchanged.
Application tests were not rerun for this documentation-only update; the 133-test
result above belongs to the independent review of `5bfcb889`.


## Langfuse newcomer setup requirements — 2026-11-13

Sharon agreed with the simple Docker operation/verification direction and asked
for the design to include complete newcomer installation guidance and the needed
management scripts. The [follow-up plan](stages/02-langfuse/verification-simplification-plan.md)
now assigns public-guide updates, a first-use walkthrough, exact version/evidence
labels, prerequisite checks, repeated-start/stop behavior, helpful failures and
existing-installation preservation. Official Docker/Langfuse references were
checked; Docker Desktop 4.99.0 is recorded as a candidate, not a tested Mac result.

This change documents the requested requirements and updates navigation/Atlas.
No application or script implementation, main merge, conflict resolution or
public supported-command change was made. Official guides will be updated with
working commands alongside implementation; currently proposed commands remain
explicitly labeled in the design. Main integration with conflict choices agreed
with Sharon is still the first execution step. All four review findings remain
open. Existing charter, ownership, secrets, sandbox and evidence rules apply; no
guarded baseline or broader event/harness design changes.


## Langfuse CLI agreement and Codex handoff — 2026-11-13

Sharon selected double-dash action flags under `agent-playbook langfuse`:
`--start`, `--stop`, `--status`, `--logs`, `--open`, `--check`, with `--follow`
only for logs and normal `--help`. He requested the Markdown update and complete
Codex context before starting. The [plan and handoff](stages/02-langfuse/verification-simplification-plan.md)
now define exclusive actions, responsibilities, exits, existing configuration
selectors, development-checkout dispatch, direct-script fallback, newcomer
guides and independent verification. A fresh Codex instruction starts with
reading and conflict presentation; resolving conflicts still requires Sharon's
agreement. No execution, conflict resolution, main merge or runtime change was
performed by this update. PR #36 remains draft and all four review findings open.

The existing CLI on main was inspected to make the handoff concrete: its
development bridge defaults to checks.py, so the new command needs an explicit
tooling mapping. Main's source-checkout boundary and lazy workflow execution
remain in force. Root `agent-playbook check` stays the quality gate; the planned
Langfuse `--check` reuses project authentication. No general doctor, workflow
context or agent runtime was added. Public guides will document working commands
when implemented; this change updates permanent design/navigation/Atlas only.

## Historical workflow-contract branch record

## Historical workflow contract refactor design — 2026-11-13

Main was read at `a4264ac985005b6e9c104bf8a8c4c1f1492abfb1`, the merge of PR #35; the older unmerged wording above is retained as historical review context. The runtime still has the PR #34 direct-flow factory/runner.

Sharon requested the [workflow contract design package](refactors/workflow-contract/README.md) before Langfuse integration: final public ABC lifecycle methods with abstract hooks, per-instance status, explicit error phases, stable implementation registry and selected YAML validation. He authorized the narrow Stage 01 base-class restriction update. Other guarded changes are enumerated for final review in the implementation plan.

This update contains documentation and generated Atlas navigation only. Application code, tests, dependencies, configuration and releases are unchanged. No runtime verification result is claimed for the proposed refactor. Implementation remains explicitly stopped pending Sharon's go-ahead. Context/Langfuse follows separately; child workflows and recovery are future feature requests.

## Historical workflow-contract review follow-up — 2026-11-13

PR #40 (feat/workflow-contract) implements the approved PR #38 contract and enumerated guarded changes. It was reviewed at b3d279b6826284cd9a0e1aba6f559525e8358f31. The reviewer independently reran the standard check: Pyright and Ruff lint/format passed; pytest reported 166 passed. Fourteen temporary additional probes passed but are not committed regression tests. Existing real workflow tests remain; planned coverage is incomplete. The reviewer did not rebuild the release independently; PR #40 contains the implementer's release evidence.

The review reproduced eager unused-flow import failure, constructor WorkflowInputError misclassification and alias/type information missing from validation diagnostics. The import finding was qualified: the existing release smoke checks should catch that deterministic defect before a release is marked verified. Sharon nevertheless chose lazy dependency imports now, together with exhaustive built-in release verification, and asked for all test gaps and corrections to be handed to the next implementation agent.

[review-follow-up.md](refactors/workflow-contract/review-follow-up.md) is the current task specification and evidence matrix. This commit changes documentation and Atlas only. PR #40 must incorporate the updated design branch and implement/verify the follow-up before the next review. Both PRs remain unmerged. Context/Langfuse, children, recovery and optional-package installation profiles remain separate. Earlier initial-stop statements above are retained as dated history, not current authorization status.

## Historical workflow contract implementation PR (2026-11-13)


Sharon approved the PR #38 design and the enumerated guarded-file changes. `feat/workflow-contract` starts at design head `cf62b80` while PR #38 remains open. This branch adds the final-method ABC, per-instance lifecycle/failure records, stable class registry, selected YAML configuration, strict YAML key handling, typed native results, and CLI adaptation. CrewAI retains decorated step orchestration. Children (#39), recovery, and context/Langfuse remain separate.

Baseline at `cf62b80`: Pyright, Ruff lint and format passed. Pytest collection failed in the sandbox because CrewAI attempted to create per-user storage in a read-only home directory. Full tests subsequently ran in the approved execution context. Final checks and current-release evidence are recorded below when complete.

### Verification at implementation commit `465a09754dcd3201dbaf925c7b243877141083a8`

- `app/.venv/bin/python -m tooling.checks check`: PASS, Pyright 0 errors/warnings, Ruff lint/format PASS, pytest 166 passed. The release command repeated the same full gate on the committed tree.
- `python3 designs/atlas/build.py --check` and `git diff --check`: PASS before the implementation commit; Atlas rebuilt from the updated catalog.
- `app/.venv/bin/python tooling/verify_runtime.py dev-run`: PASS for WF-01, WF-02, both WF-03 routes and zero Python socket/DNS attempts. This is a Python audit, not an OS network sandbox.
- `app/.venv/bin/python -m tooling.release` with a workspace uv cache: PASS on CPython 3.13.5. Locked dependency export/install with hashes, `uv pip check` (138 installed packages), isolated installed imports, default WF-01, WF-02, WF-03 pass/needs_work and the fresh-process offline audit passed. Verified wheel SHA-256 `2c99ec87c0f2c52faf783c47fbc3194ad6124a950c104f3dc1e1cafc29d2eb19`; requirements SHA-256 `99fb1fc30d3c3b63e7a4b5464eab05a3fc9364f9631edcf6bffd5afbf4779840`; lock SHA-256 `5bb830f9eaf61fb9b67d3d6c6cf07a2084279cb64fa03a26968cb36e4ec36d04`.
- A configured `wf-02-custom` alias using defaults 10, -2, 3 returned 24 in source and the installed release. The final installed release returned 0 when JSON overrode `initial` with 2.

The Linux verification does not certify Sharon's Mac/PyCharm setup. The release artifact is local and intentionally untracked. Existing releases using an older configuration schema were not tested with this new YAML. No Langfuse or model service was required.

For a manual review from `app/`, run `./.venv/bin/agent-playbook dev-run`, then WF-02 with `--workflow wf-02 --input '{"initial":10,"increment":-2,"multiplier":3}'` and with `--input '{"initial":3,"increment":2,"multiplier":4}'`. Try WF-03 with scores 59 and 60. Add the documented `wf-02-custom` entry to a temporary YAML file and select it with `--config PATH --workflow wf-02-custom`. Try score 101 (exit 2) and an injected step exception through `tests/cli/test_workflow_commands.py` (exit 1); there is no public failure flag.

## Historical workflow contract follow-up implementation — PR #40 (2026-11-13)

The PR #38 design head `5d6a770` was merged into the implementation branch without resetting its earlier work. The follow-up implementation at `9f75544c47c1b2356a547f54a634c00262edbdc0` defers concrete CrewAI flow imports until the selected wrapper prepares. Selection and actual construction have separate error boundaries; constructor defects exit 1 while explicit invalid settings remain exit 2. Diagnostics identify the configured alias, phase, field and safe validation type. The CLI suppresses CrewAI's raw step-error log while presenting its classified error. CrewAI still owns decorated step execution and routing. No existing regression tests were removed; application tests and gates exclude `app/examples/`.

The exact A1–F6 maintained test mapping is in [review-follow-up.md](refactors/workflow-contract/review-follow-up.md#pr-40-maintained-test-mapping). Focused follow-up suites passed, including 62 lifecycle/boundary cases, 56 selected-YAML cases and 41 concrete-wrapper/real-flow cases. The negative Pyright probe passed by asserting the final-override, incompatible-hook and assignment diagnostics.

Final verification at application commit `9f75544c47c1b2356a547f54a634c00262edbdc0`:

- `cd app && ./.venv/bin/python -m tooling.checks check`: PASS — Pyright 0 errors/warnings, Ruff lint/format PASS, pytest 314 passed. The release command repeated the full gate on the committed tree with the same result.
- `python3 designs/atlas/build.py --check` and `git diff --check`: PASS after the status/evidence update.
- `cd app && ./.venv/bin/python tooling/verify_runtime.py dev-run`: PASS — all three built-ins, both configured alias defaults/overrides, execution exit 1 and zero Python socket/DNS attempts.
- `cd app && UV_CACHE_DIR=/workspace/.uv-cache ./.venv/bin/python -m tooling.release`: PASS on CPython 3.13.5. Locked hash-verified dependency closure installed, `uv pip check` confirmed 138 compatible installed packages, installed imports stayed in the isolated environment, and every built-in plus both aliases passed the installed smoke audit. The installed CLI rejected invalid input with exit 2 and the injected execution failure with exit 1. The release manifest records `verified: true`. Wheel SHA-256: `b4fb6593f02fc000b15f99fcc5262a531e0296e27f1fe3d554bcd2f9b1b12326`; requirements SHA-256: `99fb1fc30d3c3b63e7a4b5464eab05a3fc9364f9631edcf6bffd5afbf4779840`; lock SHA-256: `5bb830f9eaf61fb9b67d3d6c6cf07a2084279cb64fa03a26968cb36e4ec36d04`.

The offline audit is Python socket/DNS auditing, not an OS network sandbox. Linux checks do not establish Mac/PyCharm behavior. The release is local and untracked. Older installed releases were not tested with the new YAML. Optional dependency packaging, context/Langfuse, children and recovery remain outside this PR. Both PRs remain unmerged.

## Historical workflow-contract second review and test-quality handoff — 2026-11-13

PR #40 at f61683c8e2a089b2dc4f008d193dd83618322adf incorporates design head 5d6a770 and implements I-1–I-4. The second independent review passed Pyright, Ruff lint/format, 314 tests and Atlas checks. A wheel rebuilt from the hash-checked application snapshot at 9f75544 matched the implementation agent's SHA-256 and passed isolated installed built-in/alias/failure verification. This reviewer check did not rerun the original Git clean-check/archive release entrypoint; PR #40 records that separate implementer evidence. No Mac/PyCharm or old-release/new-YAML compatibility claim is made; socket/DNS auditing covers Python attempts, not all OS networking.

Four temporary in-memory probes showed ineffective assertions/fixtures: E3 does not observe early flow construction/kickoff; C6 inherits already-correct startup settings; D4 base YAML can reject an unrelated duplicate root workflows key; B2 replaces a hook with an exception object and accidentally raises TypeError. These are test-evidence gaps, not a finding that all four production behaviors are broken.

Sharon requested another detailed Markdown handoff. [review-test-quality.md](refactors/workflow-contract/review-test-quality.md) specifies Q1–Q4 fixes, focused negative controls, replacement/consolidation rules, per-case evidence and next-agent instructions. This update adds the plan and reconciles status/navigation only. Runtime, tests, dependencies and public behavior are unchanged; no new application test/release run is claimed for this documentation update. The implementation agent must preserve the existing A1–F6 mapping and fill the new completion evidence on PR #40. Both PRs remain unmerged.

Documentation verification: Atlas build and freshness/reference checks passed; 64 relative document links were checked against the repository inventory, with the existing historical-sandbox link left untraversed. Changed files passed a trailing-whitespace check. This is documentation evidence only.

## Workflow-contract test-quality corrections — PR #40 (2026-11-13; historical verification)

The latest PR #38 design head `9edca5f` was merged into `feat/workflow-contract` as `50d5001`, resolving overlapping progress/status prose while preserving the existing implementation and A1–F6 evidence. Sharon authorized Q1–Q4 and the guarded documentation updates. The governing ABC/YAML contract stays in `designs/refactors/workflow-contract/`; maintained regression tests stay beside their application owners. Relevant exploration topics were already consulted in the design follow-up; no exploration changes this test-quality pass. CrewAI still owns flow steps and routing.

At application commit `4775cbea7b3b86dda76de015cbfd282e43df6cf9`, Q1 observes each concrete flow constructor/kickoff across 11 invalid wrapper inputs; Q2 seeds conflicting framework settings and checks both before the first CrewAI import; Q3 uses 14 independently valid base/local YAML controls and asserts the specific loader reason; Q4 injects callable failures across nine boundaries and checks exact cause/call prefix. Temporary negative controls made each corrected test fail on its intended assertion, then were restored. The former exception-object test injection was replaced. Q3 exposed one narrow production fix: merge keys now report their explicit `StrictLoader` reason instead of a generic invalid-key reason. Public errors remain redacted. See [Q1–Q4 evidence](refactors/workflow-contract/review-test-quality.md#completion-evidence--pr-40) and the [A1–F6 maintained mapping](refactors/workflow-contract/review-follow-up.md#pr-40-maintained-test-mapping).

- `cd app && ./.venv/bin/python -m pytest -q tests/workflows/test_wrappers.py tests/application/test_followup_boundaries.py tests/application/test_runner_contract.py tests/config/test_workflow_matrix.py`: **119 passed**.
- `cd app && ./.venv/bin/python -m tooling.checks check`: **PASS**, Pyright 0 errors/warnings, Ruff lint/format passed, **315 tests passed**. The clean release repeated this gate on the committed tree.
- `cd app && ./.venv/bin/python tooling/verify_runtime.py dev-run`: **PASS**, every built-in, both configured aliases with default/override cases, execution failure exit 1, zero Python socket/DNS attempts.
- `cd app && UV_CACHE_DIR=/workspace/.uv-cache ./.venv/bin/python -m tooling.release`: **PASS** from clean source commit `4775cbea7b3b86dda76de015cbfd282e43df6cf9` on CPython 3.13.5. Hash-checked locked installation and `uv pip check` passed for 138 installed packages. The isolated installed verifier passed every built-in, both aliases/defaults/overrides, failure exit and offline audit. `release.json` records `verified: true`. Wheel SHA-256 `150b5d67638642232931b54ac838751fa967edb25c6d1e6cb8451b4f8a3f3fb8`; requirements SHA-256 `99fb1fc30d3c3b63e7a4b5464eab05a3fc9364f9631edcf6bffd5afbf4779840`; lock SHA-256 `5bb830f9eaf61fb9b67d3d6c6cf07a2084279cb64fa03a26968cb36e4ec36d04`.
- `python3 designs/atlas/build.py --check` and `git diff --check`: **PASS** after the evidence and Atlas update.

The existing public configuration guide already states that merge keys reject and source values are hidden; the new internal `StrictLoader` reason has no user-facing documentation impact. The refactor package, progress, Atlas and PR evidence are updated. No regression scenarios were removed, and maintained gates exclude `app/examples/`. The release artifact remains local and untracked. Python socket/DNS auditing does not provide an OS network sandbox; Linux results do not establish Mac/PyCharm behavior. Compatibility of older installed releases with the new YAML remains untested. Context/Langfuse, optional dependency packaging, children and recovery remain outside PR #40. Both PRs remain open for review.

## PR #36 Langfuse review follow-up — 2026-11-13

The draft branch implements the R1/R3 fixes, R4 factual status correction, optional management helper/CLI and newcomer guides. [Resolution evidence](stages/02-langfuse/resolution-2026-11-13.md) records 350 passing maintained tests and actual-SDK loopback regressions. An isolated Linux Docker start was stopped because its `vfs` driver consumed nearly all free workspace disk before the six services were created. Live ingestion/persistence and Sharon's Mac acceptance remain pending. No M4 or workflow instrumentation is included; PR #36 is unmerged.

The current combined Drive checklist supersedes the historical M1–M3 checkout guides for local acceptance, while retaining their original tested SHAs. The code commit passed isolated release verification; the later documentation commit is rechecked separately.

## PR #41 main reconciliation — 2026-11-14

Sharon approved the four documentation/Atlas conflict resolutions and the stale
PR #40 status correction in the guarded Stage 01 architecture. Main `9e464014`
is incorporated; Stage 01 is completed, accepted and locked, with historical
material retained. Stage 02 remains pending local acceptance on draft PR #36.
The charter, principles, design contract, guarded register and relevant stage
baselines were consulted; no new context/event architecture is adopted.
Only status/navigation and generated Atlas change. Application behavior and
public guides are unchanged, so no application test rerun is required. Atlas
build/freshness and changed-document link/scope checks accompany this update.

## Historical M4.1 implementation branch — 2026-11-14

Sharon's implementation instruction approved the M4.1 design, test cases and
implementation plan at `11bba581291c1b166973848ea8db6a9e2a142413`, including
G01–G08. The focused `feat/m4-1-context` branch implements data-only context
identity and runner/factory/Workflow/CrewAI Flow forwarding. The branch is under
its capped independent review; candidate and check evidence belong in
[permanent review status](stages/02-langfuse/workflow-integration/m1-context/reviews/status.md).
This is unmerged implementation evidence, not Stage 02 acceptance. M4.2 tracing,
M4.3 instrumentation and local logging remain later work.

## Roadmap and reusable governance alignment — 2026-11-15

Sharon approved applying PR #46's broad roadmap direction through PR #48, the Stage 04-only sequencing exception, deferred logging, incremental milestone approval and the Stage Design PR convention. This is an approved documentation/governance change; it does not mark Stage 02 complete or Stage 04 implemented. Stage-specific files, their PR titles and detailed design reconciliation remain with their owners.

The permanent [roadmap approval record](roadmap.md#approval-and-scope-record) preserves the handover's lasting decisions. [Stage working method](governance/stage-milestone-workflow.md) and [Codex handover rules](governance/codex-handover-rules.md) own the reusable process, including frozen handoff contracts. Runtime architecture/structure, application behavior and existing stage acceptance are unchanged. C01/Q12 ownership reconciliation remains with Stage 04's owner and is not resolved by this roadmap change.

