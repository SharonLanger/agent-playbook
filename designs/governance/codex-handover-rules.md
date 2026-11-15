# Codex handover rules

**Status: GUARDED — standing procedure requested and approved by Sharon on 2026-11-15.** Applies whenever preparing an implementation handoff. This does not approve an individual draft or authorize merging a PR.

Read this file before producing a Codex handoff. Follow the [design contract](design-contract.md) and [guarded-file register](guarded-files.md). A milestone plan supplies concrete paths and acceptance criteria; it must reference these rules rather than silently weaken them.

Read the [stage and milestone working method](stage-milestone-workflow.md) for requirements, decisions, alignment checkpoints and milestone folders. These rules apply to any stage or milestone, not only observability.

## Model selection

Use **Sol** for the orchestrator, coder, design-drift reviewer and test-gap reviewer. In this environment the current selectable Sol model is gpt-6.1-sol; record the exact model ID actually used for each role. Correctness takes priority over reducing effort. Do not silently substitute a cheaper model. If the orchestrator is already running in a session whose model cannot be selected, report its actual model rather than claiming Sol; assign the three delegated roles to Sol. If Sol is unavailable, report the limitation and ask for a replacement instead of claiming compliance. The originating design session remains responsible for the final review; it need not be replaced to satisfy the implementation role selection.

## Required package

Before delegation, provide a design, a separate test-cases document with stable IDs, and an implementation plan. Pin the approved document revision and the user's approval reference. Include relevant requirements, decisions, repository instructions, current main/base, implementation target and scope exclusions. If approval is missing, report the gap; never claim draft approval.

The design-session agent must deliver ONE complete copy-and-paste message for Sharon to give the implementing Codex. Resolve all placeholders before presenting a ready-to-run handoff. Use repository-relative paths AND immutable GitHub links at the pinned revision so another session can retrieve the files. Never rely on this session's scratch paths.

## Freeze while implementation is active

From Sharon saying Codex has started until its returned output is reviewed by the originating design session, do not edit, rename, move or replace the milestone design, test cases, implementation plan or shared requirements/decisions governing that handoff. Pin their exact revision in the outgoing prompt; the implementation team works against that revision, not a moving branch.

Record new requirements, corrections or discovered design gaps separately in the milestone's follow-ups.md (create only when needed). State the issue, affected contract/test, proposed change, and whether the active coder has received it. These notes are pending follow-up work, not silently added acceptance criteria. The active implementation team may change code/tests and append its review reports/status under the original contract.

If a change truly cannot wait, tell Sharon and the orchestrator, explicitly pause the affected work, and agree a new pinned baseline before resuming. Do not edit first or reset the three-round counter. Final review compares the result with the handed-off contract and reports later follow-ups separately.

## Roles and rounds

1. **Orchestrator:** reads the package, records the baseline and approval, delegates coding, freezes a candidate commit, assigns two independent reviewers, consolidates findings and routes corrections.
2. **Coder:** implements the approved design and agreed tests; records changed files, decisions, commands/results and limitations. Does not silently change the contract to make tests pass.
3. **Design-drift reviewer:** independently compares the actual diff and behavior against requirements, design and scope. Reviews guarded amendments, SDK reuse, public documentation and unauthorized additions. Reports PASS or CHANGES REQUIRED with evidence.
4. **Test-gap reviewer:** independently maps EVERY agreed test ID to actual tests, meaningful assertions and execution evidence. Checks missing/weak tests, false passes, skips, environment constraints and whether tested behavior matches the contract. Independently reruns relevant checks when feasible. Reports PASS or CHANGES REQUIRED.

Both reviewers review the SAME frozen code/test candidate SHA. Neither edits the candidate during review. They must be separate agents from the coder and from each other; neither reviewer substitutes for the other.

Maximum **three total rounds**: code/tests → both reviews → disposition is one round. After required findings, the orchestrator gives the coder the consolidated corrections and begins the next round on a new candidate. Both reviewers review that candidate, including regressions and previously open findings. Do not reset the count after compaction, agent replacement, final review or a report-only commit. If round three ends with required findings, STOP and report BLOCKED; no fourth coding/review round without a new explicit user decision.

A report-only addendum may clarify evidence for the same candidate; it must not hide a code/test change or erase a prior verdict. Additional final-review corrections after the cap require an explicit plan from Sharon.

## Permanent evidence

Under the milestone's designated reviews directory, retain:

- status.md: approved revision, base/target, candidates, rounds used, current findings and test-ID mapping.
- round-01/implementation.md, design-drift.md, test-gap.md, orchestrator.md.
- The same four reports for round-02 and round-03 ONLY if used.

Every report identifies author role, candidate SHA, scope, checks and limitations. Findings have stable IDs, severity, expected versus observed behavior, file/line or test references and disposition. Keep earlier findings and failed checks visible; record fixes rather than replacing history with a final PASS. Treat missing evidence as missing, not passed.

Distinguish code/test candidate from published head. If later commits only add reports, verify and report that exact diff. Any runtime/test change invalidates the claim that the old candidate reviews cover the new head.

Passing implementation reviews means READY FOR FINAL REVIEW, not accepted or merged. Return the handoff to the originating design session. Do not merge without explicit authorization. Any ongoing documentation PR marked MERGE LAST stays open until all work it covers is implemented/merged, its final records reconciled and Sharon authorizes that documentation PR separately.

## Outgoing message template — design session to implementing Codex

The design-session agent fills this template and gives the whole message to Sharon in one copyable block:

```text
You are the implementation orchestrator for <milestone> in <repository URL>.

Read <pinned link to these rules> and follow them.
Approved contract revision: <full SHA>.
Approval reference: <exact user instruction/reference and scope>.
Read these files at that revision:
- Design: <path + immutable link>
- Test cases: <path + immutable link>
- Implementation plan: <path + immutable link>
- Requirements/decisions/relevant research: <paths + immutable links>

Refresh repository instructions and inspect current main. Implementation base/target: <intended base and target>. Assess intervening changes before coding. Work only within <scope>; preserve <exclusions>. Apply only the specifically approved guarded changes listed in the design.

Use Sol for implementation roles and record exact model IDs. Delegate to one coder and two independent reviewers: design drift and test gaps.
Both reviewers must assess the same candidate commit. Keep the permanent per-round reports under <review path>. Maximum three total rounds; stop if unresolved after round three. Preserve all findings and evidence. Complete the milestone's agreed checks, explicitly identifying anything unrun or blocked.

Open/update the separate implementation PR as specified. Do not merge it.
Documentation PR <number/link> is MERGE LAST and must remain open.

When finished, return ONE self-contained copyable final-review handoff using the required return template in the rules. The originating design session will perform the final review.
```

## Return message template — implementing Codex to Sharon

Return the following as ONE copyable text block with all fields filled; use NOT RUN/UNKNOWN/BLOCKED when applicable, never omit limitations:

```text
<MILESTONE> — FINAL REVIEW HANDOFF

Outcome: READY FOR FINAL REVIEW / BLOCKED
Repository and implementation PR:
Design/documentation PR:
Approved design/test/plan revision and approval reference:
Implementation branch, target and base commit:
Final code/test candidate reviewed by BOTH reviewers:
Final published head:
Candidate-to-head comparison and whether runtime/tests changed:

Implemented:
Design deviations and approvals (or none):
Guarded amendments applied and approval references:
Models actually used (orchestrator/coder/design reviewer/test reviewer):
Rounds used: N/3

For EACH round:
- Candidate SHA
- Coder report link
- Design-drift report link and verdict
- Test-gap report link and verdict
- Orchestrator disposition link
- Findings fixed/carried/open

Test coverage:
- Every agreed test ID mapped to pytest node/assertions/evidence (inline or permanent table link)
- Passed/failed/missing/weak/skipped/blocked/unrun cases
- Exact commands, results and tested revision
- Environment qualifications and prior failures
- Release/documentation checks where required
- Local/manual acceptance still needed

Open findings/blockers/risks:
Base/target drift and conflicts:
Scope confirmation:
Merge state: <state; identify any authorized merge explicitly>

Please review the actual diff and linked evidence. Implementation reviews do not replace the design session's final review or authorize merging.
```

## Completion and changes

The design session performs its own final review against the actual candidate and reports its verdict to Sharon. Final review, user acceptance and merge are distinct. Keep these rules available across milestones through README links. Changes to the approved review count, independent roles or acceptance process require an explicit recorded user decision.
