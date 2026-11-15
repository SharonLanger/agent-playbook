# Stage 03 — Decision log

Updated: 2026-11-15. Companion specification: [README.md](README.md).

This record covers the agreements visible in this design conversation and the loaded repository authorities. It does not claim to reconstruct unseen discussions. Keep stable IDs, preserve superseded decisions and record changes with their source. A proposal becomes accepted only through an explicit decision; no implementation is authorized by this initial document creation.

## Current reading note

The initial register/checkpoint below is retained as history. The current decisions D12–D20 and source records U04–U07 later in this file supersede the initial application-path/tracing, permanent-test and per-recipe planning assumptions. The README presents the current specification. No frozen implementation handoff is active.

## Session sources

- U01: Sharon assigned this session as Stage 3 design agent and requested reading the roadmap, architecture, principles, charter, progress and governance; collect information first.
- U02: Sharon confirmed Stage 2 is done, assigned logging to another session, and requested alignment on the draft Stage Design PR and general working process.
- U03: Sharon said "Okay good" to that approach, requested two files covering agreements and every decision with what/why/where, and asked for grouped use-case proposals to begin scope discussion.
- B01: main `4ed7a318e25653d481705d9cb40c35de9ab649c7`; its progress records completed Stage 02 and separate logging ownership. Governing references are linked in the README.

## Initial agreement register — retained history

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

## Initial proposals and questions — dispositions below

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

## Initial alignment checkpoint — 2026-11-15

1. Goal/prerequisites: Stage 03 scope planning is authorized. Stage 01 is accepted; current main now records Stage 02 completed. Earlier conversation noted stale main progress; B01 resolves that status discrepancy.
2. Consistency: established boundaries match the roadmap. G1–G3 and the teaching example are new proposals, not prior agreements. No milestone baseline exists.
3. Research: the exploration index was consulted. It points to agent execution, observability and harness work; none authorizes Stage 03 scheduling semantics. No new research/probe or technical API guarantee is claimed. Selected concurrency/failure cases need focused inspection later.
4. Placement/dependencies: repository → designs → stages → 03-orchestration-patterns. README owns scope, requirements and stage index; decisions.md owns rationale/history. Inputs are session instructions and governing records; output is reviewable planning. No runtime component, state ownership or provider boundary changes.
5. Open questions: Q01–Q05 remain visible. There is no need to allocate milestones or select cancellation/retry semantics to publish this draft.
6. Outcome: ready for scope discussion; not ready for implementation handoff.

## Initial principle assessment — retained history

| Principles | Application |
|---|---|
| 1 explicit approvals; 3 no drift; 12 traceability; 15 honest status | New draft files preserve authorities, distinguish sources/status and record placement; no guarded amendments. |
| 2 security; 5 integrations; 6 configuration | No credentials, integration calls, runtime configuration or new provider dependency added; exact runtime policies await design. |
| 4 learning; 8 evidence; 9 incremental scope | Propose small teaching outcomes; distinguish predecessor acceptance from independent verification; no unapproved milestone commitment. |
| 7 quality gates | Documentation/link/scope verification applies; runtime tests do not establish anything new for this prose-only change. |
| 10 local-first | Candidate work uses deterministic local scenarios; no new service requirement. |
| 11 history; 13 personal sandbox | No historical files changed and no personal sandbox contents inspected. |
| 14 official documentation | No supported runtime behavior changes; app/docs has no update needed at this step. |

## Initial documentation impact — retained history

Initial scope is the two files requested in U03. Shared design indexes, global progress and Atlas registration are deferred to a later Stage 03 documentation update in this same design PR; this initial publication is not claimed fully indexed or ready for stage approval. No existing Atlas entry or generated artifact is changed. No Atlas build is claimed for this two-file seed. Preserve the mandatory maintenance checks when registering the stage.

Existing guarded authorities, other-stage documents, application sources/configuration/dependencies/tests and product guides remain unchanged. This package introduces no diagrams. Before publication, check relative link targets and confirm the diff contains exactly these two files; verify the published PR is draft. Runtime tests and application acceptance are not run for the seed.

## Conversation history

- 2026-11-15 / U01: read-only familiarization requested and completed; no PR created then.
- 2026-11-15 / U02: Stage 2 completion and separate logging ownership confirmed; working method explained.
- 2026-11-15 / U03: create two planning files and begin scope discussion with grouped proposals. This authorizes draft documentation, not implementation, milestone approval or merge.

## Follow-up sources — 2026-11-15

- U04: Sharon requested inspection of existing conditional/parallel examples and reframed Stage 03 as permanent, runnable, copyable building blocks rather than official application workflows. This specifically authorized inspection of the relevant personal examples.
- U05: Sharon limited the learning/testing objective to CrewAI capabilities and agreed that examples run independently of the application runner/configuration, registry, logging and Langfuse.
- U06: Sharon accepted the coverage map and recipe approach; deferred recovery; required a common README/flow/run/input shape with README as a learning guide and official-documentation links; rejected permanent tests and sequential per-recipe implementation cycles; allowed temporary checks removed before merge; requested one implementation batch/PR and two example subfolders.
- U07: Sharon explicitly accepted concepts/ and recipes/ and README as the learning guide. He requested broader candidates: combine/select parallel results, any-failure/threshold policies, conditional variations, fixed-count loops and a counter-based coder/reviewer feedback loop. Keep the explanation practical and copyable. Update this PR generally now; discuss the final batch later.

## Current decisions — what, why and where

| ID | Status / source | What | Why | Where / consequence |
|---|---|---|---|---|
| S03-D12 | Agreed; U04–U05 | Standalone CrewAI capability recipes; no official workflow registration, application runner/config/context or Langfuse/logging acceptance. | Learn and copy orchestration patterns without application integration work. | README R03–R06/R12; supersedes initial D08's assumed integration requirement, not the existence of Stage 02. |
| S03-D13 | Agreed; U06–U07 | Use concepts/ for existing examples and recipes/ for practical compositions within app/examples/workflows/. | Keep focused concepts and reusable compositions discoverable. | README organization. Future move includes link/path repairs; not executed now. |
| S03-D14 | Agreed; U06–U07 | Four core files: README.md, flow.py, run.py, input.json. README is the concise learning guide with drawing, tags, walkthrough and official links. | Uniform, low-friction copy/run experience. | Each future recipe; no mandatory separate learning file. |
| S03-D15 | Explicit scope instruction; U06 | No permanent new recipe tests. Temporary checks may verify intended behavior, then are removed before merge; retain evidence summary. | Avoid a maintained test project for a learning collection. | README R11; does not delete existing concept tests or weaken application gates. |
| S03-D16 | Agreed; U06 | Design and implement the selected batch together, in one implementation PR. | Previous one-example-at-a-time cycles cost unnecessary time. | Supersedes per-recipe cycles; PR #52 remains the separate design workspace under the explained process. |
| S03-D17 | Agreed; U06–U07 | Recovery/retry/fallback remains deferred. Include loop candidates as normal control flow. | Keep error recovery separate from repetition or reviewer-directed revision. | Candidate menu and exclusions; no durable recovery promise. |
| S03-D18 | Requested directions; U07 | Expand beyond the original three recipes to selection, threshold failures, conditional variations and bounded loops. | Provide a more useful reference collection. | C01–C08 are agent-proposed translations; final count, semantics and batch are not approved. |
| S03-D19 | Agreed; U04, U07 | Reuse existing evidence and allow a concept such as the revision loop to become a composed recipe. | Avoid needless duplication while providing practical copyable patterns. | Coverage map; revises the overly absolute interpretation of R02. |
| S03-D20 | Authorized; U07 | Update the two design files and PR description now; discuss the candidate batch later. | Preserve all agreements without starting premature implementation. | This update; no moves, code, tests or merge. |

## Proposal and question dispositions

- P01: original document-check domain is superseded as the leading suggestion. Simple numbers/counters are now proposed to keep business logic small; exact domains remain open.
- P02: original G1–G3 are retained as capability groups and expanded into C01–C08. This is not approval of every candidate.
- P03: retry/fallback is explicitly deferred. Variable-size fan-out remains unselected.
- Q01: capability directions are agreed; exact batch/example choices remain open.
- Q02: sibling failure/cancellation behavior remains to inspect on the pinned version; no promise of immediate cancellation.
- Q03: negative results, captured failure outcomes and uncaught exceptions must be distinguished when designing C05/C06.
- Q04: inspect native CrewAI join/routing behavior as needed; application context propagation is no longer a learning objective.
- Q05: resolved for delivery direction: one batch implementation PR, not separate per-recipe cycles. Formal batch ID remains unallocated.
- Q06 (new): C02 result selection must choose between best-after-all, first-completed and first-acceptable; they have different completion/loser semantics.
- Q07 (new): C06 threshold needs branch count, counting rules and early-versus-final evaluation.
- Q08 (new): C07/C08 need bounded termination and explicit exhaustion behavior. A revision loop is not exception retry.
- Q09 (new): final batch may combine/remove overlapping candidates; Sharon decides in the next discussion.

## Current alignment checkpoint — 2026-11-15

1. Goal: practical CrewAI cookbook with accepted organization and format. Final recipe batch is deliberately pending.
2. Existing coverage: inspected main 4ed7a318e25653d481705d9cb40c35de9ab649c7 and its existing examples index; read code for official WF-03 and examples 05/06/08, the example-06 tests, example-08 README and Stage 01 sandbox findings. Other coverage-map rows are supported by the collection guide. No examples were run. Historical gate claims in Stage 01 findings do not override the later sandbox exclusion.
3. Dependencies: project interpreter/dependencies only; no new runtime application integration. Main is unchanged since the previous inspection. Current authorities already loaded remain applicable.
4. Authority reconciliation: user instructions deliberately narrow initial R03 and alter test/delivery expectations. Record those instructions explicitly; do not pretend main's correlated-trace evidence wording was already changed. Shared roadmap/status/Atlas alignment is still required before final approval/closeout. Existing architecture ownership is preserved.
5. Placement: design records remain in designs/stages/03-orchestration-patterns. Future example moves stay within the existing examples boundary, preserve prior history and update affected links. No move now.
6. Research limits: this update chooses no native API or scheduler semantics. Threshold policies/selection may require ordinary Python logic; label it accurately. Official source links and readable diagrams are deliverables for the actual recipe guides.
7. Outcome: ready to discuss the expanded batch; not an implementation handoff or completion claim.

## Current principle and documentation impact

All fifteen principles were reconsidered against this update. Approvals/traceability/status (1/3/12/15) are supported by sourced decisions and explicit pending reconciliation. Security/integrations/configuration (2/5/6) have no runtime changes. Learning/evidence/incremental scope (4/8/9) use a coverage map and unapproved candidate list. Quality gates (7) apply to this documentation update; future temporary recipe verification follows U06 without altering application gates. Local-first/history/sandbox isolation (10/11/13) are preserved; U04 specifically authorized relevant example inspection. Official documentation (14) has no supported-application behavior change to describe.

Only the two Stage 03 Markdown files and PR metadata change. No guarded file, existing example, application test, source, dependency or configuration changes. No diagram is created. Main progress and Atlas discovery registration remain pending in this draft; no Atlas build/freshness pass is claimed. Check the new links and published scope; do not claim a fully reconciled or approved stage package.

## Follow-up history

- U04–U05: shift from integrated workflows/traces to standalone CrewAI examples; inspect existing coverage.
- U06: batch implementation, common four-file format, README learning guide, no permanent new tests, temporary checks permitted, recovery deferred.
- U07: approve concepts/recipes names and expand recipe directions. Update this design PR only; final batch discussion follows.
