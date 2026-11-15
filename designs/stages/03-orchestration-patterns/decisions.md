# Stage 03 — Decision log

Updated: 2026-11-15. Companion specification: [README.md](README.md).

This record covers the agreements visible in this design conversation and the loaded repository authorities. It does not claim to reconstruct unseen discussions. Keep stable IDs, preserve superseded decisions and record changes with their source. A proposal becomes accepted only through an explicit decision; no implementation is authorized by this initial document creation.

## Session sources

- U01: Sharon assigned this session as Stage 3 design agent and requested reading the roadmap, architecture, principles, charter, progress and governance; collect information first.
- U02: Sharon confirmed Stage 2 is done, assigned logging to another session, and requested alignment on the draft Stage Design PR and general working process.
- U03: Sharon said "Okay good" to that approach, requested two files covering agreements and every decision with what/why/where, and asked for grouped use-case proposals to begin scope discussion.
- B01: main `4ed7a318e25653d481705d9cb40c35de9ab649c7`; its progress records completed Stage 02 and separate logging ownership. Governing references are linked in the README.

## Agreement register

| ID | Status / source | What | Why | Where / consequence |
|---|---|---|---|---|
| S03-D01 | Agreed; U01–U03 | This session owns Stage 3 design and eventual final design review. | Maintain continuity between chosen scope and reviewed implementation. | This stage package; does not take ownership of other stages. |
| S03-D02 | Confirmed; U02, B01 | Treat Stage 2 as completed. | The prerequisite foundation is accepted; later closeout is now on main. | README starting point; no rewrite of Stage 2 evidence. |
| S03-D03 | Agreed; U02, B01 | Leave logging to the separate session; no dependency on its completion. | Independent work should not block orchestration learning. | S03-R05; logging work remains outside this package. |
| S03-D04 | Agreed direction; U02–U03 and governance | Maintain one ongoing draft Stage Design PR with specifications, decisions, questions and progress. | Keep evolving design discoverable across milestones. | Stage PR and README; no auto-merge, explicit closeout merge gate. |
| S03-D05 | Authorized; U03 | Start with exactly two files: README.md and decisions.md. | Preserve agreements and rationale without creating premature milestone paperwork. | README doubles as specification and canonical milestone index; this file holds decision/history records. Filename choice is the design agent's implementation choice. |
| S03-D06 | Agreed process; U03, governance | Select scope first, then determine milestones; draft design/test/plan together and lock exact revisions incrementally. | Avoid approving undefined behavior or detailing every future milestone at once. | Future milestone folders; no milestone currently allocated or locked. |
| S03-D07 | Inherited boundary; roadmap and architecture | Cover a bounded set of branching, parallel work, joining and failure propagation; CrewAI owns scheduling/state. | Learn orchestration without introducing another execution engine. | S03-R01–R04; precise scenarios await selection. |
| S03-D08 | Inherited boundary; roadmap | Reuse Stage 01 evidence and Stage 02 context/tracing; no real-agent dependency or durable recovery framework. | Avoid duplicate learning and cross-stage scope expansion. | S03-R02, R04, R06; existing contracts remain authoritative. |
| S03-D09 | Inherited rule; governance | Implementation PRs and their acceptance are separate from the Stage Design PR; freeze approved handoff contracts. | Keep review evidence tied to the promised behavior. | Linked stage/handover procedures; separate design review, user acceptance and merge. |
| S03-D10 | Inherited rule; principles/design contract | Explain guarded logical changes per affected file and obtain approval before editing. | Preserve approved meanings and ownership. | No guarded file is changed in this initial package. |
| S03-D11 | Authorized; U03 | Present grouped use cases as proposals for discussion. | Let Sharon choose capabilities before implementation commitments. | README G1–G3 and optional additions; none accepted yet. |

## Proposals and open decisions

| ID | Proposal / question | Reason and affected scope | Owner / state |
|---|---|---|---|
| S03-P01 | Use one deterministic document-check example throughout. | Makes patterns comparable without introducing agent behavior or another integration. | Sharon to choose; proposed |
| S03-P02 | Select G1 parallel/join, G2 conditional convergence, G3 failure propagation as the initial scope. | Covers the roadmap with a small connected set; may be grouped differently into milestones. | Sharon to choose; proposed |
| S03-P03 | Keep retries and variable-size fan-out optional for later selection. | Both add semantics beyond the simplest fixed-branch cases. | Proposed exclusion from initial selection, not a permanent rejection |
| S03-Q01 | Which groups and example domain are useful? | Blocks exact scope/milestone approval, not discussion. | Sharon |
| S03-Q02 | What happens to active siblings after a required branch fails? | Decide wait/cancel behavior only after inspecting native support; failure propagation alone does not settle this. | Design agent investigates after scope selection; Sharon approves policy |
| S03-Q03 | How do negative findings differ from execution failures? | Determines result versus exception semantics and honest overall outcome. | Design discussion |
| S03-Q04 | What join/convergence and context propagation behavior does the pinned runtime actually provide? | Must verify on selected cases before promising implementation behavior. | Design agent; not yet researched |
| S03-Q05 | Should G1–G3 be separate milestones or fewer combined outcomes? | Choose boundaries by learning and acceptance value, not file count. | Sharon and design session; unresolved |

No policy from Stage 04's separate agent-event design is silently imported into Stage 03.

## Alignment checkpoint — 2026-11-15

1. Goal/prerequisites: Stage 03 scope planning is authorized. Stage 01 is accepted; current main now records Stage 02 completed. Earlier conversation noted stale main progress; B01 resolves that status discrepancy.
2. Consistency: established boundaries match the roadmap. G1–G3 and the teaching example are new proposals, not prior agreements. No milestone baseline exists.
3. Research: the exploration index was consulted. It points to agent execution, observability and harness work; none authorizes Stage 03 scheduling semantics. No new research/probe or technical API guarantee is claimed. Selected concurrency/failure cases need focused inspection later.
4. Placement/dependencies: repository → designs → stages → 03-orchestration-patterns. README owns scope, requirements and stage index; decisions.md owns rationale/history. Inputs are session instructions and governing records; output is reviewable planning. No runtime component, state ownership or provider boundary changes.
5. Open questions: Q01–Q05 remain visible. There is no need to allocate milestones or select cancellation/retry semantics to publish this draft.
6. Outcome: ready for scope discussion; not ready for implementation handoff.

## Principle assessment for this documentation change

| Principles | Application |
|---|---|
| 1 explicit approvals; 3 no drift; 12 traceability; 15 honest status | New draft files preserve authorities, distinguish sources/status and record placement; no guarded amendments. |
| 2 security; 5 integrations; 6 configuration | No credentials, integration calls, runtime configuration or new provider dependency added; exact runtime policies await design. |
| 4 learning; 8 evidence; 9 incremental scope | Propose small teaching outcomes; distinguish predecessor acceptance from independent verification; no unapproved milestone commitment. |
| 7 quality gates | Documentation/link/scope verification applies; runtime tests do not establish anything new for this prose-only change. |
| 10 local-first | Candidate work uses deterministic local scenarios; no new service requirement. |
| 11 history; 13 personal sandbox | No historical files changed and no personal sandbox contents inspected. |
| 14 official documentation | No supported runtime behavior changes; app/docs has no update needed at this step. |

## Documentation impact and verification boundary

Initial scope is the two files requested in U03. Shared design indexes, global progress and Atlas registration are deferred to a later Stage 03 documentation update in this same design PR; this initial publication is not claimed fully indexed or ready for stage approval. No existing Atlas entry or generated artifact is changed. No Atlas build is claimed for this two-file seed. Preserve the mandatory maintenance checks when registering the stage.

Existing guarded authorities, other-stage documents, application sources/configuration/dependencies/tests and product guides remain unchanged. This package introduces no diagrams. Before publication, check relative link targets and confirm the diff contains exactly these two files; verify the published PR is draft. Runtime tests and application acceptance are not run for the seed.

## Conversation history

- 2026-11-15 / U01: read-only familiarization requested and completed; no PR created then.
- 2026-11-15 / U02: Stage 2 completion and separate logging ownership confirmed; working method explained.
- 2026-11-15 / U03: create two planning files and begin scope discussion with grouped proposals. This authorizes draft documentation, not implementation, milestone approval or merge.
