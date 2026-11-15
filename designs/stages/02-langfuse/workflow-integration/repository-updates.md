# Repository reconciliation checklist

Status: **M4.1 closeout: M4.1 implemented, independently reviewed and accepted by Sharon; merged via PR #44 at 942e59344c429454263319e783ea76ad297b7ea6. Combined M4.2 + M4.3 detailed design authorized; implementation awaits revised contract approval. Logging is deferred.** [README](README.md) · [Decisions](decisions.md) · [Requirements](requirements.md)

## Historical planning-PR checklist

- [x] Preserve requirements, decisions, complete discussion history and historical specification.
- [x] Preserve CrewAI research, the exact 13-file probe/results/dependencies and provenance.
- [x] Maintain permanent entry rules, Stage 02/exploration links and draft Atlas navigation.
- [x] Record D27 correlation, D28 permission to draft, D29 bounded implementation review, and R30 application correlation.
- [x] Draft [context design](m1-context/design.md), [test cases](m1-context/test-cases.md) and [Codex implementation/review plan](m1-context/implementation-plan.md).
- [x] Reconcile shared records, progress and Atlas with draft-review status; preserve implemented M1–M3 status.
- [x] Sharon reports sending the explicit M4.1/G01–G08 authorization pinned to 11bba58 to Codex. The implementing agent records the reference/applies those amendments; final evidence and review remain pending.

No product-guide update is needed yet: supported runtime behavior, CLI/configuration and dependencies do not change. No application test or probe rerun is claimed. app/examples/ remains excluded. The package gives the next Codex future commands and evidence requirements.

## M4.1 guarded amendments — approved implementation history

[Design section 9](m1-context/design.md#9-guarded-logical-amendments-to-approve-with-this-design) is the canonical file-specific G01–G08 list. It proposes data-only context placement, runner/factory/ABC/Flow routing, dated workflow-contract amendments, M4 checkpoints and registration of the approved design/test/implementation documents. No guarded file is edited in this draft.

The orchestrator records the approved revision and Sharon's approval reference, applies only authorized amendments and does not ask again for that scope. Identify missing approval by G-number and file before affected work. Preserve prior acceptance and PR #40's lifecycle history. M4.1 needs no provider-isolation exception: its shared model uses the standard library and contains no SDK/client handles; Flow integration uses existing CrewAI/Pydantic within workflow code.

## Later tracing reconciliation — before M4.2

| File / surface | Logical change to present | Limit |
|---|---|---|
| designs/principles.md, principle 5 | Narrow exception for native Langfuse instrumentation at reviewed call sites | Preserve centralized configuration and agent-provider contracts; data-only M4.1 does not need this |
| designs/architecture.md | Reconcile the neutral observation/exporter path with native tracing | Preserve scheduling, application outcomes/errors, redaction and agent adapters |
| designs/project-structure.md | Specify reviewed SDK import/initialization locations | Do not multiply the shared context or allow unrestricted SDK imports |
| AGENTS.md engineering boundary | Reconcile adapter-only instructions conflicting with the approved tracing exception | Explain exact protected logical changes before editing |
| Stage 02 architecture/milestones and maintained views | Record native scope/client/instrumentation contracts and acceptance | Preserve M1–M3 evidence and M4.1's approved data contract |

D11 already accepts no broker. These changes reconcile implementation with guarded sources, without reopening that direction or reversing agent-provider isolation.

## At each implementation milestone's closeout

- [ ] Refresh main/concurrent PRs; assess shared-file overlap, particularly runner/factory/context signatures, settings and Atlas. Do not assume zero conflicts.
- [ ] Map implementation and meaningful assertions/results to the approved design/tests. Preserve outputs/errors, imports, typing and personal-sandbox isolation.
- [ ] For M4.1, retain coder, design-drift, test-gap and orchestrator reports for each used round, with exact design/candidate SHAs; enforce three total rounds maximum.
- [ ] Record passed/failed/blocked/unrun checks at the tested revision. Research success is not application completion; flush/trace URLs are not ingestion proof.
- [ ] Update app/docs when supported behavior changes; otherwise record no impact. M4.1 updates internal Python construction/context instructions, not CLI flags.
- [ ] Reconcile progress, stage summaries, shared records, authorized guarded changes and Atlas. Preserve historical evidence and do not mark M4.2/M4.3 complete after context work.
- [ ] After explicitly authorized merge, inspect resulting main and record acceptance/merge status. Drafting or approving a design is not merge authorization.

designs/roadmap.md needs no change: stage order is unchanged. designs/README.md already leads to stage/exploration navigation; add only useful links. The workflow-contract status marker N02 remains a dated reconciliation item; use explicit amendments rather than rewrite historical acceptance.

M4.1 closeout proves context identity/propagation/isolation and existing behavior. M4.2 adds root correlation and client/disabled/outage/shutdown behavior. M4.3 adds real automatic Flow observations, masking/startup checks and local-server/UI acceptance. Agent lifecycle, logs and scores remain separate.

## Documentation validation

Iteration 21 opening checks passed at their recorded revision: Atlas build/freshness, 67 relative links, prior record/probe preservation and unchanged guarded baselines. This is historical evidence, not validation of the new draft.

Iteration 27 checks passed: Atlas build/freshness and its reference/guard/sandbox checks; 140 relative Markdown links; balanced fences and current-edit whitespace; R01–R30, D01–D29 and Q01–Q25 retained; all CTX-01–17/G01–G08 entries present; complete prior discussion and all 13 probe files preserved; guarded baselines unchanged. No application code, dependencies or guarded sources changed; no application tests, research rerun or live Langfuse verification claimed.

Iteration 28 added the exact final-review return template and preserved the three-round cap. Atlas freshness, 140 relative links, record/CTX/G IDs, historical discussion/probe preservation, unchanged guarded baselines and current-edit whitespace checks passed. Runtime design/test cases and application code remain unchanged.

Preservation detail: the opening PR copied eight unchanged Flow fixture modules with blank-at-EOF warnings. Keep their bytes/hashes unchanged. Check current edits normally; for the full preserved snapshot only, disabling that warning category is acceptable and must not conceal other whitespace errors.

## Approved M4.1 implementation update — 2026-11-14

Sharon's implementation instruction explicitly approved G01–G08 at
`11bba581291c1b166973848ea8db6a9e2a142413`. The implementation branch adds
the approved guarded amendments, updates official workflows documentation,
progress and Stage 02 summary, and preserves the earlier records. Runtime
settings, CLI options, dependencies and YAML are unchanged, so the other public
guides have no user-facing change. Atlas navigation is refreshed for the context
package and implementation review status. Candidate-specific checks and review
findings are recorded in `m1-context/reviews/` rather than claimed here.

Iteration 29 records D30/R31 metadata correlation and starts M4.2 preliminary design without editing the three pinned M4.1 milestone documents. The focused SDK-only metadata check is recorded in research/history with its limits; it is not an application or live-server acceptance result. Documentation checks passed: Atlas build/freshness, 140 relative links, R01–R31/D01–D30/Q01–Q25 retention, prior discussion and 13-file probe preservation, unchanged guarded baselines/current-edit whitespace. The three pinned M4.1 files were also compared byte-for-byte to the published handoff and remain unchanged.

## Iteration 35 integration

Sharon authorized conflict resolution and merge. PR #43 is merged as c8f129e. Both documentation streams are retained; D30 is correlation and the implementation approval entry is a dated unnumbered heading. Runtime/tests stay identical to reviewed candidate 16c1580. G01–G08 and all round reports remain. Generated Atlas is rebuilt from reconciled sources; PR #44 merged at 942e59344c429454263319e783ea76ad297b7ea6. M4.2 drafts remain separate and unapproved.


## Iteration 40 reconciliation

- Standing handover rules published and linked from both READMEs; combined milestone accepted, detailed version-2 package is for review.
- Before implementation: retain accepted PAYLOAD-01 and obtain the specific RUN-G approvals in the revised design. Do not apply old catch/project/rethrow or custom cache proposals.
- After approved implementation: reconcile Stage 02 milestone/architecture and global status against actual results; coordinate broader stage alignment work separately. No unrelated stage renumbering here.
- After each implementation PR merges: update this ongoing PR's evidence/status. Merge #47 LAST, only with separate explicit authorization.
- No application product documentation changes now: only a design/process revision, with no supported behavior change. Public guides change with implementation. Atlas reflects draft scope, not implementation.
