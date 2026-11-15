# M4.1 — Codex implementation and review plan

Status: **APPROVED AND LOCKED at `11bba581`; implemented, verified, accepted and merged in PR #44 at `942e59344c429454263319e783ea76ad297b7ea6`.** The contract below is preserved; draft-era wording is historical. See [current status](reviews/status.md).

[Design](design.md) · [Test cases](test-cases.md) · [Shared entry point](../README.md) · [Repository reconciliation](../repository-updates.md)

## 1. Handoff and authority

This is the entry file for the Codex orchestrator implementing M4.1 after Sharon's review. It coordinates one coder and two separate reviewers. It is an instruction for this implementation task, not an application agent-orchestration feature to build.

First load repository/design instructions and guarded authorities, this package's README/requirements/decisions/full history, this design and its test cases. Refresh main and PR #43; locate the exact approved design revision. The inspected baseline is main `d12b5fc2867d3646b6fab2eb71f1447ff177d8c1`, with Python 3.13 and the existing dependency lock. A changed baseline needs an explicit compatibility/diff assessment, not blind cherry-picking.

Record Sharon's approval reference and the approved design/test/plan Git revision. Include authorization for G01–G08 from design section 9. A request to draft or review these documents is not implementation approval. Once authorized, proceed without asking again for the same scope. If a protected amendment lacks authorization, stop the affected work and identify that exact missing item; do not invent a blanket approval requirement for ordinary tasks.

Use one focused M4.1 implementation branch/PR. PR #43 holds the design package; if it remains unmerged when implementation is authorized, branch from its exact approved head and initially target that design branch so the implementation diff is reviewable. If it has merged, branch from the refreshed main. Record base/target in status.md and retarget after the design merge when applicable. Do not merge either PR automatically. M4.2/M4.3 remain separate work.

## 2. Roles and boundaries

| Role | Responsibility | Allowed writes |
|---|---|---|
| Codex orchestrator | Verify approval/base, dispatch scoped work, freeze candidate revision, collect both reviews, reconcile findings, enforce round cap, report final status | Status, combined round report, branch/PR metadata and approved coordination records; sends code/test fixes to coder |
| Coder | Implement approved context and wiring, update existing callers/tests/docs, run relevant checks, answer every finding in later rounds | M4.1 implementation/test/doc allowlist; own round implementation report |
| Design-drift reviewer | Compare actual implementation against approved design and guarded amendments; find missing requirements and unplanned behavior/abstractions | Own design-drift report; scratch/read-only verification, no production or test fixes |
| Test reviewer | Independently map all CTX cases to meaningful assertions/results, check regression preservation and test gaps | Own test-gap report; scratch/read-only verification, no production or test fixes |

Use two distinct reviewer agents, neither being the coder. Prefer fresh reviewer sessions each round with the same approved baseline and prior reports supplied. Do not require a specific model or reasoning setting beyond available task instructions. A reviewer cannot approve design changes on Sharon's behalf. The orchestrator cannot replace a missing review with its own pass.

The coder finishes before reviews start. Both reviewers inspect the same immutable candidate commit. Parallel reviews are allowed on detached read-only checkouts or equivalent snapshots. Do not edit the shared candidate while either review is running. Reviewers write only their separate reports; the orchestrator collects them without changing candidate source. No delegation or writes to unrelated sessions/services are required.

## 3. Implementation sequence

### Gate 0 — ready to implement

- Record approved design revision, approval reference, G01–G08 authorization, refreshed base and existing uncommitted-work handling. Do not discard other work.
- Review shared-file overlap: runner/factory/contracts, maintained Flow constructors/tests, official workflow guide, design records and Atlas. Do not assume concurrent agent-adapter work has no overlap.
- Ensure a normal pinned development environment via the existing bootstrap instructions. No new dependency or optional CrewAI instrumentation install is part of this milestone.
- Create `reviews/status.md` in this package, with current round 0, maximum rounds 3, branch/base/design references, roles and the gate state. This is a plain durable Markdown record.

### Coder work — first candidate

1. Apply only the authorized G01–G08 documentation amendments, preserving dated historical evidence. Mark the reviewed M4.1 documents approved/locked with Sharon's reference; do not fabricate approval.
2. Add the context package and data-only for_agent helper. Implement UUID4 default correlation creation and preserve it during derivation. No broker/client or mutable metadata bag.
3. Add required keyword-only context forwarding through factory/ABC/all maintained wrappers. Runner creates it after selection inside CONSTRUCTION error handling. Keep public runner/RunResult/CLI behavior.
4. Add typed constructors/private context storage/read-only access to the three maintained CrewAI Flows. Preserve superclass initialization and decorated business methods. Keep settings/import order and business state unchanged.
5. Add meaningful new tests and update maintained direct callers/fakes/fixtures/typing examples. Search only explicit maintained paths; never inspect app/examples/. Complete the CTX mapping with existing cases reused where appropriate.
6. Update app/docs/workflows.md for implemented behavior, shared records, stage summary/progress and Atlas. A new package may need registry/packaging verification but no speculative new tooling. Record no-impact reasons for unaffected guides/configuration/dependencies.
7. Run focused tests, existing quality gate and documentation checks. Fix discovered issues within the candidate preparation; then commit a clean review candidate and write the implementation report. Do not claim application acceptance from research results.

Expected runtime changes are the exact source inventory in design section 7. Maintained tests, fixtures and constructor examples may also need signature updates. No dependency/lock/YAML/CLI option/release-policy change, no SDK/client lifecycle work, no app/examples or historical sandbox access. If a necessary fix would exceed this scope, report it for design review rather than bundling it silently.

## 4. Maximum three rounds

A round consists of one coder candidate/fix pass, both independent reviews of its frozen candidate SHA, and an orchestrator disposition. Small local edit/test iterations while preparing that one candidate do not create extra review rounds. Once reviewers have examined a candidate, any code/test correction goes into the next numbered round. Do not restart numbering after a handoff, rebase, reviewer replacement or new session.

| Round | Coder task | Review/disposition |
|---|---|---|
| 1 | Implement the approved contract and tests | Both reviewers report; orchestrator either verifies completion, assigns findings to round 2, or stops for a blocker |
| 2 | Address all round-1 findings within approved scope | Both reviewers inspect the whole updated diff and regression risks, not only claimed fixes; unresolved implementation gaps go to round 3 |
| 3 | Final correction pass | Both reviewers report again; ready only if every required condition passes. Otherwise STOP and hand back unresolved findings |

Stop earlier if a governing contradiction, missing approval, unavailable reviewer or environment prevents meaningful progress. Record BLOCKED honestly; do not treat it as a pass or use a fourth candidate under another name. A later restart beyond three rounds requires a new explicit instruction from Sharon and retains the earlier history.

Both review reports must exist for each completed round, even when one finds a blocker; the other may report its own completed work or clearly explain BLOCKED scope. Initial review may occur with CTX-17 release verification marked NOT RUN. If code/test reviews otherwise pass, the orchestrator runs the existing clean release gate on that exact candidate and appends its outcome before declaring the round ready. A code/test fix required by release failure consumes the next round; after round 3, stop.

The test reviewer checks that release evidence and adds a dated CTX-17/verdict addendum for the same candidate. This completes the current round's pending gate; it is not a new code-review round. The orchestrator must not convert the reviewer's pending or blocked verdict into PASS on their behalf.

Disagreements are not resolved by majority vote. Record each disputed finding, the cited contract/test and the proposed resolution. Reviewers may withdraw a finding with evidence. A true requirement change returns to Sharon; coder/orchestrator must not edit the baseline to make the implementation appear compliant.

## 5. Permanent round reports

Create these files as rounds actually happen; do not prefill fictional passes or empty completed rounds:

```yaml
reviews:
  context:
    status.md: current gate, approval, design/base/candidate SHAs and round count
    round-01:
      implementation.md: coder changes, commands and case mapping
      design-drift.md: independent implementation-versus-design review
      test-gap.md: independent CTX-01–17 assertion/evidence review
      orchestrator.md: consolidated findings, verification and disposition
    round-02: same four reports, only if needed
    round-03: same four reports, only if needed
```

All paths are relative to this workflow-integration package. Reports are permanent evidence, not temporary handoffs. Retain prior rounds; never overwrite an earlier failed review with a later pass. Append a dated correction/addendum if a factual report error is found. Keep secrets and raw private payloads out of reports.

Every report header identifies role, round, date, implementation PR/branch, base SHA, approved design SHA, reviewed candidate SHA and exact scope. Distinguish the runtime/test candidate from a later report-only commit. A new runtime/test commit invalidates previous pass status for those changed parts and requires the next round's two reviews; final report-only updates can be verified by diff without another code round.

### Implementation report template

- Changes by design section and CTX case; expected files versus actual diff.
- Commands, working directory, Python/dependency versions, exit codes and output summaries at the tested candidate.
- CTX mapping and known gaps; tests not run and why.
- For rounds 2/3: every earlier finding ID, fix or evidence-based dispute, affected files/tests and verification.
- Guarded amendments applied with approval reference; public-doc/progress/Atlas updates and unchanged-scope assessment.

### Design-drift report template

Verdict: PASS / CHANGES REQUIRED / BLOCKED.

| Finding ID | Design/requirement reference | Actual file:line and behavior | Impact | Required correction | Status |
|---|---|---|---|---|---|
| D-001, … | Exact section/R/D ID | Concrete mismatch, omission or unplanned behavior | Critical/major/minor; explain | Bounded fix or clarification | Open/fixed/disputed |

Also list reviewed sections and explicit confirmation of scope exclusions, constructor/Flow behavior, stable IDs, unchanged error/output contracts, typing and authorized guarded changes. PASS must cover the whole approved contract, not merely say no issues found. Missing features and accidental additions both count as drift. Cosmetic suggestions without a contract/correctness effect are advisory and do not force extra rounds.

### Test-gap report template

Verdict: PASS / CHANGES REQUIRED / BLOCKED. Include the complete CTX-01–17 mapping specified in the test-cases document, actual assertions and executed evidence.

| Finding ID | CTX ID | Missing/weak/wrong evidence | Regression that would slip through | Required correction | Status |
|---|---|---|---|---|---|
| T-001, … | One or more cases | Exact node/assertion/result gap | Concrete example | Meaningful test or execution | Open/fixed/disputed |

Check that changed fake constructors still fail for the intended reason; real Flow propagation is exercised; stored context is not serialized; no test relies on personal examples; baseline assertions were not weakened. A green mock-only test, an uncollected file or a skipped case cannot satisfy a required scenario. Independently rerun focused cases when practical and report precisely what was rerun. Do not repeat the full expensive gate solely to duplicate valid same-SHA evidence.

### Orchestrator report template

- Links to both reviews and coder report for this exact candidate.
- Union of open findings with owners; retain stable D-/T-IDs across rounds.
- Checks at the candidate, including CTX-17 when attempted; passed/failed/blocked/not run separately.
- Baseline drift/approval/overlap assessment; any justified report-only delta.
- Disposition: NEXT ROUND N, READY FOR SHARON'S ACCEPTANCE, or STOPPED AFTER ROUND N.
- If stopped: unresolved IDs, evidence, attempted fixes, why automatic work stopped and the precise decision/environment need. Preserve the branch/PR for inspection.

## 6. Commands and validation sequence

Use the repository's existing bootstrap and interpreter. From repository root, after the expected test files exist:

```sh
cd app
./.venv/bin/python -m pytest -q tests/context/test_models.py tests/application/test_context.py tests/workflows/test_context.py
./.venv/bin/python -m tooling.checks check
```

The full gate includes maintained tests and strict typing/lint/format. Existing offline runtime verification is already exercised by its maintained pytest case; do not repeat it without a new concern. If the coder splits test files differently, record actual node mapping and commands; changing the approved source boundaries is different from an ordinary test-file organization choice.

From repository root, for the documentation projection:

```sh
python3 designs/atlas/build.py
python3 designs/atlas/build.py --check
git diff --check
```

Run the repository-appropriate changed-link checks without traversing app/examples/. Freeze a clean committed candidate before isolated release verification. Then, from app/:

```sh
./.venv/bin/python -m tooling.release
```

This follows the current release tool, which verifies the installed runtime. Record the actual artifact/version/source SHA and output; do not invent a release success. Do not publish/upload/delete releases or change version policy solely because the command has a blocker. Resolve only authorized implementation issues; otherwise report the concrete blocker. A later source change requires appropriate revalidation.

No application tests have been run for this design draft. Commands here are future implementation instructions based on the inspected tooling, not evidence of completion. Mac/PyCharm behavior is not proved by Linux checks; record any platform-specific remaining verification separately.

## 7. Completion and handoff

Ready for Sharon's acceptance requires: approved baseline/amendments, implementation within scope, both reviews without unresolved required findings on the final candidate, CTX-01–17 satisfied, relevant documentation/Atlas reconciled, and every used round's reports committed. Exact code/test revision and report revision must be clear. Do not mark M4.2/M4.3 or all Stage 02 complete.

The final message uses section 8's exact return-report structure. Sharon will paste it into the design session for an additional final review after both implementation reviewers finish. That final review does not automatically authorize a fourth correction round or merge. If the three-round cap is reached without success, explicitly say STOPPED and list unresolved findings. No automatic merge or next-milestone implementation.

After Sharon explicitly accepts/authorizes merge, reconcile the resulting main and preserved evidence under the repository contract. Logging/agent runtimes and later tracing remain separate assignments.

## 8. Required return report for the design session

Commit and push all used round reports and final status to the implementation PR before the handoff. Use GitHub links pinned to actual commits, not agent-local or scratch paths. The next reviewer must be able to inspect the source and reports without access to this Codex session. If pushing or a check is blocked, say so and provide whatever verified evidence is available; do not claim readiness.

Return one copyable report using this structure. Replace every placeholder with actual evidence, an explicit none, or NOT RUN/BLOCKED plus the reason. Keep commands/results concise and link detailed output in permanent reports. A report-only head must be distinguished from the candidate actually reviewed/tested; provide the comparison and confirm whether runtime/test files differ.

```text
M4.1 CONTEXT — FINAL REVIEW HANDOFF

Outcome: READY FOR FINAL REVIEW / STOPPED / BLOCKED
Implementation PR: <URL; draft/open/unmerged state>
Design PR: https://github.com/SharonLanger/agent-playbook/pull/43
Approved design revision and approval reference: <full SHA; user instruction/reference>
Implementation branch and PR target: <branch; base branch>
Implementation base commit: <full SHA>
Final code/test candidate reviewed by both reviewers: <full SHA and commit URL>
Final published head including reports: <full SHA and commit URL>
Candidate-to-head differences: <comparison URL; report-only or list actual changes>

Implemented: <short summary of actual behavior and important files>
Design deviations: <none, or exact approved/unapproved differences and references>
G01–G08 amendments: <applied/blocked status; approval and diff/report links>

Rounds used: <N>/3
For EACH round:
- Candidate SHA: <full SHA>
- Coder report: <permanent URL>
- Design-drift review: <verdict; permanent URL>
- Test-gap review: <verdict; permanent URL>
- Orchestrator report: <permanent URL; findings fixed/carried forward>
Final status and CTX-01–17 mapping: <permanent status and test-gap report URLs>

Verification at <candidate SHA>:
- Focused context tests: <exact command; result and count; evidence URL>
- Full quality gate: <exact command; pytest/type/lint/format outcomes; evidence URL>
- CTX-01–17: <passed / missing / weak / failed / skipped / blocked / not-run cases>
- CTX-17 installed release: <command; artifact/version/source SHA; outcome/evidence>
- Documentation/Atlas/whitespace: <commands and outcomes>
- Checks not run and remaining local/manual verification: <list with reasons, or none>

Open findings/blockers/risks: <stable IDs, impact and next action, or none>
Scope confirmation: <M4.1 only; any exceptions explicitly listed>
Merge state: <unmerged; no merge performed>

Please perform the final design-session review of the actual diff and linked evidence.
The two implementation reviews do not replace your final review or authorize merging.
```

Use READY FOR FINAL REVIEW only when section 7's implementation, test and review conditions pass. This means ready to inspect, not already accepted by Sharon or merged. For STOPPED/BLOCKED, preserve the same report structure and explain what prevents completion. Do not reset the round counter when handing work back.
