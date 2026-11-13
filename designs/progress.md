# Progress and acceptance

Updated 2026-11-13. This file records implemented behavior; architecture.md describes
the target system.

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

## Next actions

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


## Atlas/governance update — PR #35

Sharon approved the logical changes to charter, principles, architecture and project structure, the new guarded design contract, preservation of every existing guard, mandatory placement/reading flow, official-doc maintenance and permanent Current/Explorations Atlas on 2026-11-13. This approval authorizes the documentation work; PR #35 remains a draft for merge review. Detailed reviewer/event-adapter/harness designs remain explorations.

Current implementation snapshot: main `96cb1f8`, merging accepted PR #34. Runtime discovery/launcher, assembly/factory/runner, CLI parser, app-root YAML and examples isolation are implemented. Sharon reported that Verify Refactor passed after a formatting correction and a normal 0.1.1 release completed; those local results precede the final cleanup commit. Earlier 137-test/release evidence applies to its recorded earlier revision, not automatically to the final head.

PR #35 reconciles these facts with the approved guarded governance and permanent Atlas. All existing stage files remain unchanged and protected. Personal examples remain outside unrequested agent work. The deleted internal public-doc review guide and temporary handoff stay deleted; Sharon also authorized removing the temporary review helper and PyCharm task. Application tests and normal quality checks remain.

Stage 02 Langfuse design/research may proceed; implementation requires its approved stage design. Role/event/adapter/harness details remain optional explorations. PR #35 is unmerged pending Sharon's review.


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
