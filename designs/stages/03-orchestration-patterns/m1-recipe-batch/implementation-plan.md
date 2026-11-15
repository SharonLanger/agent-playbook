# S03.M1 — Implementation plan and handoff rules

Read [the repository handoff procedure](../../../governance/codex-handover-rules.md) in full. This plan supplies batch paths and scope; it does not weaken the one-coder/two-reviewer model or three-round cap.

## Approval and revision

Sharon approved the eight visual walkthroughs and requested implementation by another Codex session, with diagrams at README tops, official footer links and temporary tests for his own use. Source U09 and decisions D21–D25 in [decisions.md](../decisions.md) retain his instruction. The outgoing prompt pins this package's full SHA. Treat that SHA, not PR #52's moving head, as the contract. Forwarding the concrete prompt authorizes implementation of its stated scope.

Stage Design PR: #52, [Stage 03 Design] Orchestration patterns. Keep draft/open; no auto-merge. Its merge requires Sharon's separate explicit authorization.

## Base and branch strategy

Inspected main: 4ed7a318e25653d481705d9cb40c35de9ab649c7.
Create impl/stage-03-recipe-batch from current main after inspecting intervening changes, with implementation PR title [Stage 03 · M1] Standalone CrewAI recipe cookbook targeting main.

Read the design from its immutable links; do not merge/cherry-pick the whole Stage Design branch into implementation. Keep the implementation PR focused on examples, necessary navigation/path repairs and permanent implementation reports. The design session integrates returned evidence/status into PR #52. Report base drift or conflicts before changing agreed semantics.

The temporary test files are intentionally in the implementation PR during review. No implementation merge is authorized.

## Work order — one batch

1. Load root/design instructions, design-contract, guarded register, approved stage specification/decisions, this design and test cases, authoring rules and the existing examples needed for this task. Read current dependency pins and examples run/settings patterns. Relevant personal-example access is explicitly authorized; this is not permission to inspect unrelated sandbox material.
2. Record baseline and approval. Compare the graph reference with all eight recipe contracts. Check needed native behavior with focused temporary probes, especially exceptions, joins and router re-arming. Prefer published/pinned source and concise probes over a broad audit. If core behavior conflicts, report it; do not redesign silently.
3. Move the eight concept folders as approved, preserve behavior and repair navigation/path references. Identify exact path-only guarded repairs before editing; no other guarded meaning changes.
4. Implement all eight recipe folders, diagrams, README guides and temporary verify.py scripts. New Python code stays inside recipe folders. Use no shared helper/package or official workflow registration.
5. Run the mapped checks, direct/copy runs and appropriate documentation/diagram/lint checks. Honor Sharon's CrewAI-only verification scope: do not run unrelated application regression tests for unchanged runtime. Keep its gate configuration untouched and explain this narrow user-directed exception to the default full-gate instruction.
6. Freeze a code/test candidate. Run independent design-drift and test-gap/behavior reviews against THAT SAME SHA.
7. Consolidate findings, give one correction list to the coder, freeze a new candidate and repeat both reviews if needed. Maximum three rounds total.
8. Push the implementation PR with temporary scripts still present. Return a self-contained final-review handoff and exact commands for Sharon. Do not merge, do not delete the tests early and do not edit the pinned design to match implementation.
9. After design-session final review and Sharon's hands-on check, temporary-script cleanup follows test-cases.md. No merge until explicitly authorized.

## Delegated roles

Use gpt-6.1-sol for coder and both independent reviewers, with fork_turns=none and a complete task containing pinned links and candidate SHA. The orchestrator should use Sol when selectable; otherwise report its actual model honestly, per repository rules.

- Coder implements the entire batch and records commands/results/limits.
- Design-drift reviewer compares every recipe's code, diagram and README against its approved contract, verifies isolation/placement and identifies unauthorized behavior. Does not edit the candidate.
- Test-gap/behavior reviewer maps every test ID to actual assertions and evidence, independently runs relevant direct/copy/verification checks, and examines false passes, failures, loops and diagram/guide accuracy. Does not edit the candidate.
- Orchestrator freezes candidates, consolidates results and preserves all prior findings and rounds.
- Originating design session performs final review after the handoff. User acceptance and merge remain separate.

Do not replace these with a single combined reviewer. No fourth round after a failed third, no reset after compaction/agent replacement, and no self-approved merge.

## Permanent reports

Create reports only as work occurs under:
designs/stages/03-orchestration-patterns/m1-recipe-batch/reviews/

- status.md: pinned contract, approval reference, base/target, actual models, candidates, published head, round count, all test-ID mappings, open findings and pending cleanup/manual acceptance.
- round-01/implementation.md, design-drift.md, test-gap.md, orchestrator.md.
- Corresponding round-02 and round-03 files only when used.

Preserve failed checks and their dispositions. A PASS must identify what was inspected/run and limitations. Any report-only commit after candidate must be proven not to alter runtime/tests. Initial handoff status is READY FOR FINAL REVIEW, not accepted/merge-ready; temporary cleanup and Sharon's review are still pending.

Use the complete return template in the repository handoff rules. Include direct run commands, the command to run all verify.py scripts, intentionally failing demonstrations, Linux versus Mac/PyCharm limits, every review report link, exact candidate/published-head SHAs and no-merge confirmation.

## Documentation and remaining owner work

README diagrams/source links and moved-folder references are part of implementation. Do not edit frozen design/requirements/decisions during implementation; put discovered design gaps in follow-ups.md and notify the design session.

Stage 03 global roadmap/status/Atlas semantic reconciliation remains owned by the design session before stage closeout. For implementation-induced path-only Atlas changes, preserve statuses and regenerate/check output using existing tooling; do not manually edit generated HTML or add application behavior. This split avoids concurrent unreviewed semantic edits.

No Docker, application logging, real agent work, application API refactor, new dependency or permanent recipe tests. Do not mark Stage 03 complete merely because the examples run.
