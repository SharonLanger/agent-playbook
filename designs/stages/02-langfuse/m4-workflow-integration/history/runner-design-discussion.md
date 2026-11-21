# M4.2 runner tracing — preliminary discussion

**MERGE LAST — ONGOING DOCUMENTATION WORKSPACE.** Keep PR #47 open and draft while its implementation work is in progress. Merge it only after all implementation work covered by this workspace has been implemented and its implementation PRs merged, the documentation reflects the final results, and Sharon explicitly authorizes merging this documentation PR. Approval or merge instructions for an implementation PR do not authorize merging #47.

Status: **M4.2 DRAFT PREPARATION authorized; M4.1 final review completed in iteration 33, accepted and merged via PR #44; documentation integration completed. No M4.2 approved contract or implementation authorization.** Started 2026-11-14, discussion iteration 30; current iteration 43.

This file supplements the [complete discussion through iteration 29](context-discussion.md), [shared requirements](../requirements.md) and [decisions](../decisions.md). It records new instructions, proposals, open decisions and possible follow-ups while another Codex implements M4.1. It is not a competing application specification. Read this entire record on each new M4.2 discussion iteration and preserve earlier decisions when updating it.

## Baseline and active-work boundary

- M4.1's delegated design/test/implementation package is pinned to `11bba581291c1b166973848ea8db6a9e2a142413` in PR #43. Iteration 33 received and reviewed Codex's PR #44 handoff. Candidate 16c1580 passes this session's final runtime/design review and an independent 43-test rerun; current published head 9392b39 adds only reports. Documentation integration is pending; implementation, review, user acceptance and merge remain distinct.
- Shared records including D30/R31 were last published at `9aaf31e4b0e6345ed7162da765f37dbe94167f4b`. That is this discussion branch's starting point.
- New instruction, iteration 30: do not edit the implementing agent's parts. Save proposed changes separately for an explicit follow-up handoff. This session will not edit his code, tests, three M4.1 milestone documents, approval records or round reports.
- Separate branch `docs/m4-2-runner-discussion` owns this record and the three new M4.2 draft files authorized in iteration 32. Do not advance PR #43, its branch, the implementation branch or shared navigation/progress/Atlas during this parallel work. Reconcile discovery/status in the eventual M4.2 documentation PR after alignment. This isolation follows Sharon's explicit instruction and does not change guarded architecture meaning.
- No milestone boundary change is selected: M4.1 context/wiring; M4.2 runner tracing; M4.3 automatic CrewAI observations; logging later. Any proposed boundary change must be recorded and checked against shared requirements/decisions before adoption.

## Accepted instructions for the next package

1. Start with a simple preliminary design discussion; agree on broad behavior before adopting a detailed contract. Iteration 32 authorizes preparing a review draft in parallel while remaining policy choices are explicitly marked proposals.
2. Provide separate `02-runner-design.md`, `02-runner-test-cases.md` and `02-runner-implementation-plan.md`. A delegated design agent is preparing these new files; creation alone is not approval or implementation.
3. Use the same implementation procedure: orchestrator, coder, two independent reviewers for design drift and test gaps, permanent reports for each round, at most three total rounds, then stop if unresolved. Retain the final report back to this design session before user acceptance/merge.
4. An eventual M4.1 follow-up does not silently reset its existing three-round cap or instruct a fourth round. Coordinate it with the recorded round state and an explicit handoff. A requirement change needs its own recorded decision before code.

## Existing agreed requirements carried forward

- Native Langfuse SDK and existing configuration/client setup; no observability broker or replacement tracing framework.
- Use the existing ExecutionContext and nested ObservabilityContext. Do not change that model or add SDK objects/trace-ID allocation as a prerequisite here.
- Every workflow-associated observation carries the exact existing correlation_id, plus selected workflow/run metadata. Native propagation begins at the root before children. D30/R31 apply to later automatic CrewAI observations too.
- Future logs use correlation_id without requiring trace_id. Optional SDK trace/span IDs can narrow a search when several traces share one correlation group.
- Existing local Langfuse deployment only; no additional collector or logging service. Logging, agent runtime lifecycle and advanced scores/evaluations remain separately scoped.
- Keep current workflow outputs, validation, error classification and CrewAI scheduling. Telemetry handling must not erase the original workflow exception.

## First proposal: one observation around the workflow lifecycle

This is a recommendation for discussion, not an accepted detailed contract:

1. The existing application path loads configuration, selects the workflow and creates its execution context.
2. Start one native current Langfuse observation for that workflow invocation. Apply correlation_id, workflow_id and workflow_run_id through native attribute propagation immediately, before child work.
3. Within that observation, keep the existing workflow construction, input decoding/preparation, execution, output validation and serialization path.
4. End the observation when that path returns or raises. Preserve the actual workflow outcome. Later delivery/flush housekeeping is not part of the workflow's business execution duration.
5. Keep automatic CrewAI Flow/start/listen/router observations for M4.3; the M4.2 active scope supplies their future parent. No separate manual span for every lifecycle phase is proposed now.

Why this boundary: failures during preparation or output validation are part of the invocation the user is debugging, even if kickoff never runs or finishes successfully. Observing only kickoff would miss them. Configuration/selection/context-creation failures before this boundary cannot yet carry this invocation context; keep their existing diagnostics and decide any additional telemetry explicitly. Do not move M4.1's context creation earlier merely to expand coverage.

## Remaining decisions, in suggested order

| Order | Decision | Starting recommendation / unresolved detail |
|---|---|---|
| 1 | What does the workflow observation cover? | Whole existing lifecycle after context creation, as above; agree before exact code placement |
| 2 | Who owns the SDK client and delivery? | Reuse a client across invocations within one process; each invocation has its own observation. Flush before a short CLI exits; exact initialization, flush/shutdown and Python-call ownership remain to design |
| 3 | What happens when tracing is disabled or unavailable? | Disabled should create no exporter/contact. For telemetry delivery failure, recommend preserving the workflow outcome with a visible bounded diagnostic; distinguish delivery failure from invalid application configuration. Exact policy is not selected |
| 4 | What data is sent? | Required identity fields, stable operation name and safe outcome information. Input/output/exception payload exposure needs an explicit small allowlist/masking policy; never send the whole context/configuration automatically |
| 5 | What evidence proves it works? | Real SDK export assertions, repeat/error/disabled/outage behavior, correlation on every emitted observation, existing workflow regressions and explicit local-server/UI acceptance. Detailed cases follow agreed behavior |

Only the boundary proposal is being presented for agreement first. Do not turn the other recommendations into accepted decisions just because they appear in this table. Scores, sessions, client pools, async/process transport, generic field registries and new abstractions are not implicit additions.

## Potential M4.1 follow-ups

No runtime/context-contract follow-up was identified in the iteration-33 final review. Documentation integration does need the duplicate D30 decision identifier and reported target conflicts reconciled; see [the separate final review](../m4-1-context/reviews/context-final-review.md). Required correlation data and forwarding already exist; Langfuse metadata projection belongs to M4.2.

If a necessary M4.1 change is discovered, create a separate `context-followups.md` beside this file. Each entry must state the affected approved contract/file, concrete problem, smallest proposed change, why M4.2 cannot handle it locally, test impact, whether it changes a decision, and its pending/approved/handed-off status. Do not apply the change to active M4.1 work. No placeholder follow-up file is needed while there are no entries.

## Iteration 30 record and verification limits

Sharon confirms Codex is working, requests no changes to its parts, asks for proposed changes to be saved separately, and wants the same design/test/two-reviewer package for the next milestone after preliminary alignment. The same three-round maximum and final-review handoff remain applicable. This file captures those instructions without touching shared or delegated files.

References already checked in iteration 29: [Langfuse metadata](https://langfuse.com/docs/observability/features/metadata), [Python API](https://python.reference.langfuse.com/langfuse), installed SDK 5.2.0 and the [research record](../research/crewai-langfuse.md). The bounded metadata check does not prove application or server integration. No new SDK/API claim, runtime probe, application test or implementation is added in this iteration.

Before approving the detailed design: reconcile actual M4.1 implementation findings, settle the decisions above and present required tracing-specific guarded changes. A draft can proceed in parallel with that review under iteration 32. Do not edit global principles/architecture or SDK import boundaries during drafting. No roadmap or stage renumbering is requested.

## Iteration 31 — trace versus observation clarification

Sharon asks whether the hierarchy shares the same observation. Clarified that the runner opens the enclosing workflow observation; instrumented CrewAI operations and later agent/tool/model calls have distinct child observation/span IDs within the same trace. They share trace identity and application correlation_id; their timing and outcomes remain separate. A failed child does not require a failed parent when recovery succeeds. Passing ExecutionContext alone does not create observations or establish SDK active scope. This clarification does not select the unresolved client, outage or payload policies.

## Iteration 32 — parallel design delegation and forthcoming M4.1 review

Sharon reports that the M4.1 Codex finished and wants to supply its result for root's final review while a sub-agent starts the next design. He asks whether everything is agreed or whether the review should precede drafting. Answer: enough is agreed to draft in parallel, but not every M4.2 policy is settled. Client ownership/flush/shutdown, telemetry-disabled/unavailable/error behavior and safe payload/exception projection remain explicit decisions; the precise lifecycle placement must be checked against the completed context code. Do not label all choices approved.

Started /root/m42_runner_design, authorized to create only the three new M4.2 draft documents in this package. It must follow repository authorities, inspect actual SDK behavior, propose minimal solutions, identify unresolved decisions, and include separate tests plus coder/two-reviewer/max-three-round implementation instructions. It cannot modify M4.1, shared records, guarded documents, application source, PRs or branch refs; root owns publishing. Any needed context change is reported separately rather than applied.

Root will inspect the actual M4.1 PR/diff and permanent reports once Sharon supplies the handoff and requests that review. Its findings feed the M4.2 draft before approval. Delegation is not proof that the new design is finished, and M4.1's reported completion is not proof of passed acceptance. Keep both tasks separate and preserve the no-automatic-merge/no-round-reset rules.

## Iteration 33 — M4.1 final review

Sharon supplied the full implementation handoff and requested review of the actual diff and linked evidence, plus the parallel design agent's status. Inspected PR #44 candidate 16c1580 against approved 11bba581 and published head 9392b39. [Final review](../m4-1-context/reviews/context-final-review.md): runtime/design PASS, independent targeted 43 tests PASS; full 380-test/release evidence inspected rather than repeated. Prior two-reviewer rounds remain 2/3; no merge or implementation edit authorized by this review.

One new documentation integration finding: both branches use D30 for different decisions (correlation requirement versus M4.1 approval/status). Preserve both meanings and reconcile the identifier/references when combining streams. GitHub also reports the known target documentation merge conflicts. These do not require a context redesign; neither branch was modified. The separate review records the exact revisions, limitations and proposed integration correction.

The M4.2 design agent finished all three review drafts: [design](../m4-2-3-workflow-tracing/design.md), [test cases](../m4-2-3-workflow-tracing/test-cases.md) and [implementation/review plan](../m4-2-3-workflow-tracing/implementation-plan.md). It validated 27 relative links/anchors, stable RUN-01–20/RUN-D01–05/RUN-G01–08 identifiers, fences/whitespace and Atlas freshness. Root also checked the review/discussion links and Atlas. No application tests or SDK probe were run for drafting. The drafts cite the completed M4.1 final review; their five explicit policy choices remain proposals for Sharon, not an approved implementation contract. All new documents remain on the separate discussion branch; PRs #43 and #44 are untouched.

## Iterations 34–35 — correlation clarification and authorized merges

Clarified that correlation_id generation and context propagation already exist in M4.1; export to Langfuse belongs to M4.2, with automatic CrewAI coverage in M4.3. Duplicate D30 was document numbering, not a runtime identity conflict.

Sharon explicitly authorized resolving the documentation conflicts, pushing/merging PRs #43/#44, recording acceptance and merge status, and refreshing this design branch from main. This supersedes the temporary no-edit/isolation restrictions above solely for authorized integration. No M4.2 policy is approved.

PR #43 merged as c8f129ee8c978067bf576b0ab563bfab74c9d6fe; PR #44 merged as 942e59344c429454263319e783ea76ad297b7ea6. Main closeout commit 6a7b16f6e1947bf911de916b5ec2c1b76be58251 records M4.1 accepted and merged. Both streams and all previous reports are preserved; D30 remains correlation, with a dated unnumbered approval entry. Atlas checks passed; application tree remains 0789b6bfd7ffe2248afbe9b3cd735cb908125571, identical to reviewed head 9392b39. No repeated application gate was needed for documentation-only integration.

This branch now incorporates that main. Its three M4.2 files remain drafts for discussion and carry no implementation authorization. Next: agree the pending runner policies and then approve the exact design/test/plan revision.

## Iteration 36 — documentation PR must merge last

Sharon clarified that the documentation PR is an ongoing workspace and was not intended to close alongside the M4.1 implementation. The earlier iteration-35 wording describes the assistant's interpretation and actions; it does not establish a standing authorization to merge documentation with implementation. PR #43 is already merged; PR #47 is the continuing workspace.

**MERGE LAST — ONGOING DOCUMENTATION WORKSPACE.** Keep PR #47 open and draft while its implementation work is in progress. Merge it only after all implementation work covered by this workspace has been implemented and its implementation PRs merged, the documentation reflects the final results, and Sharon explicitly authorizes merging this documentation PR. Approval or merge instructions for an implementation PR do not authorize merging #47.

Continue updating this PR throughout design, implementation and review. Keep implementation PRs separate. This rule changes merge sequencing only; it does not approve M4.2 design choices or implementation.

## Iteration 37 — simplify M4.2 around native SDK behavior

Sharon explicitly prioritizes low code/no code: use Langfuse's existing free SDK capabilities and do not recreate behavior it already implements. This is the governing direction for revising the unapproved M4.2 drafts. The existing context and correlation_id remain the starting point, followed by a native current observation and native metadata propagation. No broker, custom tracing lifecycle or additional logging is requested.

CrewAI scope: Sharon explicitly says not to add anything to CrewAI, while also considering whether its integration could move earlier. No milestone consolidation is selected. Keep CrewAI instrumentation out of this implementation proposal unless he subsequently chooses to combine it.

The earlier detailed policies RUN-D01–05 are still unapproved proposals. In particular, custom client caching/configuration-change handling, payload/error projection machinery and application-level metadata-limit handling must not become implementation requirements merely because the draft describes them. Reassess against a real current need; retain existing application behavior and credential protections without inventing a generic framework. The three draft documents require simplification before approval or handoff.

Recommendation for discussion: use a native SDK context manager around the existing workflow lifecycle after context creation, and propagate correlation_id, workflow_id and workflow_run_id using propagate_attributes. Native decorators are an alternative; choose the least intrusive placement in the existing runner. SDK behavior supplies observation IDs, nesting, timing and lifecycle. Do not manually reproduce those mechanisms.

Delivery recommendation, not a new approved policy: leave batching to the SDK and call flush once at the short-lived CLI's exit boundary, including failure paths after observation closure. Do not flush at every workflow junction. This is ordinary delivery wiring, not a custom queue, retry policy, client pool or shutdown framework. Advanced delivery/performance decisions are deferred; tests should verify the chosen minimal wiring and preserve existing workflow behavior.

Official documentation checked this iteration:
- https://langfuse.com/docs/observability/get-started — native observation context managers and flush for short-lived applications.
- https://langfuse.com/docs/observability/features/metadata — native propagated metadata.
- https://langfuse.com/docs/observability/features/metadata notes the SDK's metadata size limits; these are SDK behavior, not authorization to build a new application-level policy.

No application code, M4.1 contract, CrewAI instrumentation or implementation authorization changes in this iteration. PR #47 remains draft and must merge last. Next step: revise the detailed M4.2 package to the minimal scope, with its tests and review process retained and any truly necessary unresolved choices explicit.

## Iteration 38 — native scope isolation and final flush verified

Sharon agrees to native SDK usage and the final flush direction, explicitly requiring exception-path coverage. He requests verification of runner/factory/workflow propagation and future agent-specific attributes before proceeding; CrewAI instrumentation remains out of scope. This approves the direction, not the superseded detailed draft policies.

Inspected the merged M4.1 review snapshot: application/workflow_runner.py creates context after configuration/selection, constructs through workflow_factory.py, then prepares, executes, validates and serializes. Factory forwards the same context; Workflow retains it; maintained Flow constructors receive it as a private attribute outside business state. for_agent uses dataclasses.replace for a separate outer and observability context, preserving parent fields. No M4.1 modification is needed.

Verified Langfuse 5.2.0 locally with an in-memory exporter: workflow → A → A-tool → workflow checkpoint → B → B-tool → workflow checkpoint, in success and controlled exception cases. Both cases exported seven observations; every observation retained correlation_id, A and its tool retained only A-run, B and its tool only B-run, and workflow/checkpoints had no agent_run_id. Root status was UNSET on success and ERROR on escaping exception. Finally invoked flush once in each case. This is native SDK behavior verification, not implemented runner tests or live server ingestion acceptance.

Important ordering: enter the child agent observation FIRST, then propagate its agent fields. propagate_attributes updates the active observation as well as future children; entering agent propagation while the workflow is active would stamp the workflow. SDK scope exit restores propagation for subsequent work; existing span attributes are not retroactively erased. CrewAI does not automatically translate our ExecutionContext or invent our application agent_run_id; future integration must provide these values at the actual agent invocation boundary, using native SDK propagation, without duplicating auto-created observations.

Use try/finally at the selected short-lived CLI delivery boundary, outside completed observation scopes. Catch is not required merely to run finally; retain existing application exception handling. A flush failure must not replace the workflow's original exception. “Always” means an attempt on normal returns and Python stack-unwinding paths; hard process termination/power loss cannot run finally, and attempted flush is not guaranteed server delivery.

Probe setup notes: initial attempts were blocked by inherited SOCKS proxy configuration and disabled tracing environment. The passing isolated run removed proxy variables and explicitly enabled tracing/ALWAYS_ON sampling with the in-memory exporter; dummy keys and localhost URL only. No application/CrewAI code was changed. No current-main refresh or full application suite was claimed.

References: https://python.reference.langfuse.com/langfuse and https://langfuse.com/docs/observability/features/metadata. Native SDK propagation source confirmed context detach in finally. Next: simplify the design/test/implementation package using this verified behavior. PR #47 stays draft and merges last.

## Iteration 39 — propose combining runner and automatic CrewAI integration

Sharon reopens the milestone boundary and suggests doing M4.2 and M4.3 together. He asks for a recommendation, remains open to alternatives, and reiterates that application code must not reproduce SDK behavior. This supersedes the assumption that CrewAI must remain excluded from discussion; formal milestone consolidation and implementation are not yet approved.

Recommendation: combine runner tracing and automatic instrumentation of the existing deterministic CrewAI Flows in one implementation milestone/PR, with two independently testable acceptance sections. No real agents or new workflows are required. Keep M4.1 complete. Agent-runtime integration, application agent_run_id binding, model-specific generation/usage instrumentation, scores and logging remain later work.

Reviewed the preserved research and the current official Langfuse CrewAI guide: https://langfuse.com/integrations/frameworks/crewai. The guide uses openinference-instrumentation-crewai, initialized once, plus a native Langfuse enclosing observation. This is an in-process integration package, not another service. The existing research tested CrewAI 1.15.40 / Langfuse 5.2.0 / instrumentor 1.1.25, eight scenarios and 44 exported spans including start/listen/router, both conditional branches, failure, repeats and async. These are prior isolated results, not new application or live-server acceptance. No version upgrade is demonstrated necessary.

Small application responsibilities: initialize the configured local SDK and released instrumentor before workflow execution; create the existing application context; open the runner observation; project selected application identities via propagate_attributes; invoke the existing lifecycle; attempt flush after scopes close on exit paths. SDK/instrumentor responsibilities: trace/span IDs, active-parent propagation/restoration, step observations, timing, exception recording, batching and export. No per-step decorators, span loop, custom event listener, separate exporter, broker or custom tracing framework.

Combined acceptance must use the actual runner/factory/ABC and all maintained workflows: one runner root, one Flow child, correct executed steps with no duplicates, correlation_id on every observation, repeat/disabled/failure behavior and final flush. Verify local ingestion/UI separately. Avoid claiming automatic model cost/token coverage before an actual model integration exists. Preserve the current local-only configuration and credential protections; research limitations concerning captured payloads and framework update checks remain verification items, not license to implement a generic platform.

Next recommended action: revise the three M4.2 drafts into one minimal combined design/test/implementation package once the proposed consolidation is accepted; retain coder, two independent reviewers, max three rounds and final handoff. Reconcile milestone references explicitly rather than silently deleting M4.3 history. PR #47 remains draft and merges last.

## Iteration 40 — standing handover procedure and combined design authorized

On 2026-11-15 Sharon explicitly accepts merging M4.2/M4.3 scope and requests a reusable Codex handover rules document, README discovery and exact copyable outgoing/return instructions. He authorizes starting the simplified detailed design. Preserve M4.1 and its accepted evidence; no application implementation or merge is authorized here.

Published designs/governance/codex-handover-rules.md and linked it from the design and package READMEs. It formalizes one orchestrator/coder, two independent reviewers (design drift and test gaps), one frozen candidate per round, permanent four-report round folders, maximum three total rounds, explicit blocked stop and final design-session review. It requires filled immutable-link outgoing prompts and a complete return report that Sharon can copy back. Generic templates are not a ready-to-run approval for an unapproved draft.

Updated milestone table and D12/shared requirements to the accepted combined scope, preserving historical M4.3 identity and evidence. Replaced the three unapproved version-1 drafts with concise version-2 combined design/test/plan. Prior drafts remain in Git history at 7ffa9228a1e131f9f252d7d5def3abdde144f793. No custom client cache, generic tracing framework or manual per-step instrumentation is proposed.

One substantive review choice remains PAYLOAD-01: whether native input/output/exception capture is accepted for existing deterministic workflows. Default capture is proposed, not assumed approved; explicit configuration credentials/full context are never projected. Comprehensive suppression is not promised by attribute-only masking. Guarded RUN-G amendments remain proposed and must be approved with the final revision; milestone consolidation does not silently approve unseen protected-file edits.

The detailed package is ready for discussion, not implementation. Next: settle payload policy, review/approve exact design/tests/plan and narrow guarded amendments, then generate the filled copyable Codex handoff. PR #47 stays draft and MERGE LAST. No new application tests or live Langfuse acceptance claimed for documentation work.

## Iterations 41–42 — payload approval, milestone folders and reusable governance

Sharon accepts default native workflow input/output/exception capture, requires configuration and credentials never to become trace payloads, and asks whether capture can later change. PAYLOAD-01 is resolved with that scope; supported SDK/instrumentor controls can change capture later, but defaults are not a universal secret detector. Validate automatic capture paths as well as explicit mappings. No new generic redaction platform is authorized.

Sharon approved reorganizing milestone-specific files into m1-context/ and m2-3-workflow-tracing/, each with README/design/test-cases/implementation-plan and its own reviews. Shared requirements, decisions, research and history stay at the package root. A cheaper delegated agent performs mechanical moves/link repairs; root reviews the result. Approved context semantics, evidence and immutable historical links remain protected.

He requests generalized stage/milestone governance in a NEW independent PR, superseding the tentative request to use PR #46 or #45. PR #48 now contains the reusable working method and Codex handover rules, discovery links in agent instructions/README, guard registration and Atlas refresh. It specifies Sol implementation roles, pre-design contradiction checks, milestone packages, two independent reviewers, three rounds maximum and copyable outgoing/return reports. The design session retains final review. No charter/runtime architecture change is needed. PR #48 is open, unmerged and independent; PR #47 stays draft and MERGE LAST. Refresh #47 against the canonical governance after #48 merges so the earlier copy cannot overwrite it.

No application code or acceptance tests are changed; this work is documentation organization and recorded decisions. Exact combined design/guarded amendment approval still precedes implementation handoff.

## Iteration 43 — implementation freeze and requested start handoff

Sharon requests a simple freeze from the moment he says Codex is working until this design session reviews its returned output. Do not edit/move the handed-off contract or governing requirements/decisions during that window. Record new issues/corrections separately in milestone follow-ups.md with explicit pending/sent status. Only a coordinated explicit pause and rebaseline can change an active contract; no automatic review-round reset.

Added the reusable rule to PR #48 and its earlier copy in PR #47, plus a milestone README entry. The implementation team's code/tests and progress/review reports may evolve under the fixed contract. Corrected the implementation plan's report location to the milestone-local reviews/ directory, consistent with the accepted reorganization.

Sharon asks for the exact text to start Codex. The outgoing pinned instruction states the scope, design/tests/plan, narrow RUN-G01–08 authorization, Sol roles, three-round limit, freeze rule and final-review return format. Forwarding it serves as explicit authorization of that package; publishing it alone does not claim execution has started. Both PRs remain unmerged, with #47 last. No new application code or tests here.
