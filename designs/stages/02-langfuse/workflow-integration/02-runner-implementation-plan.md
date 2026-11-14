# M4.2 — Codex implementation and independent review plan

Status: **DRAFT FOR SHARON'S REVIEW — no application implementation authorized by this file.** Version 1, 2026-11-14.

**Current foundation, iteration 35:** M4.1 is accepted and merged in PR #44 at `942e59344c429454263319e783ea76ad297b7ea6`; PR #43 is merged. This branch incorporates main closeout `6a7b16f6e1947bf911de916b5ec2c1b76be58251`. The earlier pinned-source/handoff descriptions below retain drafting provenance; integration conflicts and duplicate D30 are resolved. M4.2 choices remain unapproved, and the current approved M4.1 contract is unchanged.

[Design](02-runner-design.md) · [RUN test cases](02-runner-test-cases.md) · [Runner discussion](history/runner-design-discussion.md) · [Shared requirements](requirements.md) · [Repository reconciliation](repository-updates.md)

## 1. Entry and authority

This is the future implementing Codex orchestrator's entry file after Sharon selects RUN-D01–05 and approves the exact M4.2 design/test/plan revision plus RUN-G01–08. It is a development procedure, not an application agent framework. Drafting/delegating this package does not authorize runtime code, dependency changes, guarded amendments or merge.

Load root/design instructions, design-contract/guard register, charter, principles, architecture, project structure, roadmap/progress and current Stage 02 authorities. Read this package's shared requirements/decisions, full context history, the entire standalone runner discussion, M4.1 design/test/plan, preserved research and this M4.2 trio. Reuse already-read unchanged revisions; refresh after handoff or base changes. Never inspect personal examples or historical sandbox.

Pin approval and input identities before work:

| Input | Record required |
|---|---|
| M4.2 approval | User instruction/reference; selected RUN-D01–05; authorization for each RUN-G01–08; exact full design/test/plan SHA |
| M4.1 foundation | Approved design `11bba581291c1b166973848ea8db6a9e2a142413`; actual final accepted code/test candidate and root's final-review disposition, not just the implementation agent's claim |
| M4.1 final review during drafting | PR #44 candidate `16c1580e96bd36945fa96b6ecfa8f9a563d53913`; published head `9392b39b1e556c1a36c7dfe1fa8574d65f8ce0e2`; release source `2e5d76dde2ec76b5a7ecae8ea0094286838229a9`. Root's [review](history/context-final-review.md), published at `68166c94497bf388eb05250c38cccc43f732a0f4`, records runtime/design PASS, independently 43 targeted tests and verified report-only delta. User acceptance/merge are separate; current documentation conflicts and duplicate D30 remain |
| Repository | Refreshed main, design PR/branch, M4.1 PR/base/merge state, implementation base and intended target; exact SHA/diff compatibility assessment |
| Runtime | Existing application Python/SDK lock; installed environment; effective startup/sampling settings without secret values |

The draft source check confirms that candidate 16c1580 creates ExecutionContext inside CONSTRUCTION immediately before construct_workflow and preserves assembly's settings return. Root's completed final review found no required runtime/contract correction; use its exact candidate/evidence and distinguish that verdict from user acceptance/merge. Incorporate later base changes and separate documentation integration without re-running an already completed review unnecessarily. A newly discovered context defect goes through a separate M4.1 follow-up; do not modify its accepted contract or reset its 2/3 review counter under this task.

Use a complete application checkout with repository instructions and installed pinned tooling. The partial documentation snapshot used to draft these files is unsuitable for coding, application tests or pushing local Git history. Do not reuse its local commit ancestry as remote ancestry.

Once approval covers this exact work, proceed without repeated permission requests. Identify a genuinely missing guarded item by RUN-G number/file and consequence; do not invent approval gates for reversible work already authorized. Do not quietly choose a different lifecycle/privacy/failure policy to make implementation easier.

## 2. Branch scope and Gate 0

Use one focused M4.2 implementation branch/PR. If the approved design and reviewed M4.1 foundation are merged, start from refreshed main. If not, record a deliberate base/target that contains the exact approved design and verified M4.1 candidate and yields a reviewable runner-only diff; do not merge either predecessor automatically or silently copy unreviewed branch heads. Root must reconcile outstanding design/M4.1 documentation overlap under the existing approval scope before publication/readiness. Preserve original research, M4.1 reports and all prior approval evidence.

Gate 0 checklist, recorded in `reviews/runner/status.md`:

1. Exact approval/base/design/foundation SHAs and RUN-D/RUN-G decisions recorded; full M4.1 final-review findings resolved or explicitly separated without an affected-code dependency.
2. Inspect actual runner error boundaries, assembly/client helper, default enabled settings and actual tests at that base. Confirm scope can begin after context without moving its creation or reclassifying failures.
3. Compare shared-file overlap with active work: runner/assembly/connection, public docs, design status and Atlas. No zero-conflict assumption or changes to another agent's branch/reports.
4. Verify pinned Langfuse API/source behavior where needed: native active scope/propagation, public-key resource cache, disabled path, raw exception capture and native flush limits. A tiny isolated source/probe check is allowed if it resolves a named uncertainty; do not change the original research package.
5. Record current round 0, maximum rounds 3 and all role assignments. Run the relevant existing baseline tests/standard gate in the normal environment once; a preexisting failure is recorded, not hidden or automatically repaired outside scope.

Stop affected coding if the selected policies cannot be met with the native API without material design change. In particular, do not claim an attribute-only mask sanitizes exception events, invent a flush timeout, or use SDK private state to simulate per-run resource ownership. Return the smallest alternative and its concrete consequence to the design session.

## 3. Roles and implementation scope

| Role | Responsibility | Writes |
|---|---|---|
| Orchestrator | Verify authority/base, coordinate coder, freeze candidate SHA, collect both independent reviews, reconcile findings, enforce cap and hand back evidence | Status/orchestrator reports and authorized coordination/PR metadata; production/test fixes go to coder |
| Coder | Implement only approved runner/client policy, preserve existing contracts, add/reuse tests and maintain supported docs | Approved source/test/doc inventory and own implementation report |
| Design-drift reviewer | Independently compare the complete candidate against approved M4.2, governing contracts and boundaries | Own design-drift report; read-only candidate, scratch checks |
| Test-gap reviewer | Independently inspect assertions/evidence for all RUN-01–20 and regression preservation | Own test-gap report; read-only candidate, scratch checks |

There are TWO distinct independent reviewer agents, neither the coder. Prefer fresh reviewer sessions per round with the same approved baseline and prior reports. No particular model/effort is mandated. Both inspect the SAME immutable code/test candidate SHA; start review only after the coder finishes. Do not mutate that candidate while either reviewer is active. Reviewers do not patch source/tests or approve requirement changes. Orchestrator cannot replace a missing reviewer with its own pass.

Expected source scope: `application/workflow_runner.py`, narrow assembly setup support and existing `observability/adapters/langfuse/` client/lifecycle functions; tests under maintained application/observability boundaries. Existing `RunResult`, CLI flags/stdout, M4.1 context model/constructor route, factory/ABC lifecycle and deterministic Flow business code remain unchanged unless an explicit approved amendment names the needed change. No OpenInference package installation, dependency upgrade, new collector, per-step hooks, agent runtime or logging store in M4.2.

Routine test-file organization may follow repository conventions; record the actual inventory. It is not permission to move component responsibilities. Production typing remains strict and no unchecked casts/blanket suppressions may hide integration defects. Do not grow `observations.py`'s mock wrapper into a workflow broker.

## 4. Coder sequence

1. Apply only authorized RUN-G01–08 logical amendments against the actual post-M4.1 documents, preserving dated history. Mark the approved M4.2 trio with the real approval reference. Reconcile duplicate/stale decision IDs and navigation only through the coordinating branch's explicit scope; do not overwrite another task's records.
2. Implement smallest native-client acquisition/reuse/settings-consistency policy. `assemble_runtime` remains settings-only; the runner calls any separate acquisition helper only after context creation and metadata eligibility preflight. Preserve explicit enabled/disabled behavior, existing auth helper separation and configured local endpoint. No SDK private resource reset or duplicate exporter.
3. Place one native `start_as_current_observation(as_type="span", name="workflow.run", metadata=...)` at the reviewed post-context boundary. Enter `propagate_attributes(metadata=..., as_baggage=False)` immediately. Do not add ID allocation, trace-context plumbing or per-phase spans.
4. Preserve existing lifecycle/phase error boundaries and native RunResult. Implement exact metadata eligibility and the approved safe outcome/exception projection. Business work executes once; telemetry cleanup cannot replace its result or exception. Any helper must own real application policy rather than rename SDK methods.
5. Apply the selected flush/shutdown/diagnostic policy and repeated-call behavior, including settings changes and disabled calls. Use actual native APIs; measure pinned outage behavior rather than inventing a timeout guarantee.
6. Add meaningful RUN cases, reusing existing mock-transport/offline/error fixtures and preserving CTX/workflow regressions. Real SDK export, exception events, default filter and actual runner integration are essential; fakes alone are insufficient.
7. Update public guides for supported enabled behavior, data scope, repeated Python ownership, unavailable-service behavior and delivery limits. Maintain the relevant shared records, stage/progress and Atlas without claiming M4.3 or all Stage 02 complete. Record no-impact reasons for unrelated guides/configuration/dependencies.
8. Run focused tests, the existing full gate and documentation checks; fix within scope. Freeze a clean code/test candidate, then write the coder's first-round report and submit the same SHA to both reviewers.

A service unavailable in the environment does not block deterministic SDK/loopback checks. Follow the [stage verification rule](../verification.md): inspect actual capabilities, attempt useful bounded live checks when feasible, and reserve a small UI exercise for Sharon. Do not provision extra services or build a browser test platform merely to avoid reporting a live limitation.

## 5. Exactly one counter, at most three rounds

A round is a coder candidate/fix pass, two independent reviews of that frozen candidate, and an orchestrator disposition. Local edits/tests before freezing a candidate belong to that candidate's preparation. Once reviewed, any production/test correction creates the next numbered round. Never reset after a handoff, rebase, reviewer replacement, renamed branch or new session.

| Round | Work and allowed disposition |
|---|---|
| 1 | Coder implements; both reviewers inspect complete diff. READY if required gates pass, NEXT ROUND 2 for in-scope findings, or STOP/BLOCKED for a real prerequisite |
| 2 | Coder addresses all first-round findings; both reviewers inspect the whole new candidate including regressions. READY, NEXT ROUND 3, or STOP/BLOCKED |
| 3 | Last correction candidate; both reviews still required. READY only with no unresolved required finding. Otherwise STOPPED AFTER ROUND 3 |

No fourth fix/review candidate disguised as final polish, a documentation handoff, or a “new first round.” A later extension requires a new explicit Sharon instruction and preserves the previous count/history. M4.1's counter is separate and must not be reset by M4.2 work or final review.

Each completed round retains coder, design-drift, test-gap and orchestrator reports, including when a role reports BLOCKED. Missing review, contradictory design authority or a material unavailable gate prevents a pass. Cosmetic suggestions without a contract/correctness effect are advisory and do not consume a correction round by themselves.

Release and live checks may initially be NOT RUN while reviewers inspect a candidate. When code/test reviews otherwise pass, complete those applicable checks on that same candidate and have the test reviewer append its evidence/verdict addendum. This is an evidence completion, not another code round. A code/test fix triggered by those checks consumes the next round; after round 3, stop. An unresolved live-only environment limit can produce the limited handoff status below but cannot mark RUN-20/acceptance complete.

Review disagreements are resolved through the exact contract and evidence, not majority vote. Keep stable findings; reviewers may withdraw one with a dated explanation. A true requirement change returns to Sharon before affected implementation; never edit approved tests/design to make the code pass retroactively.

## 6. Permanent reports

Create reports only as real rounds occur, under this workflow-integration package:

```text
reviews/runner/status.md
reviews/runner/round-01/implementation.md
reviews/runner/round-01/design-drift.md
reviews/runner/round-01/test-gap.md
reviews/runner/round-01/orchestrator.md
```

Use the same four filenames under round-02/round-03 only if needed. No empty pre-completed rounds or fictional PASS entries. Prior failed reports remain; corrections are dated addenda, not overwritten history.

Every report header includes role, round, date, implementation branch/PR, approved M4.2 SHA, M4.1 foundation SHA, implementation base SHA and reviewed code/test candidate SHA. A later published report-only head is distinct. Link permanent committed evidence; local scratch output alone is not a transferable handoff. Never record real credentials, raw private payloads or sensitive exception traces.

Coder report contains changed files/behavior mapped to design sections/RUN cases, exact commands/environment/exits, all known limitations, approved guarded amendments and public-doc/Atlas changes. Later reports address every prior finding ID with the fix or an evidence-backed dispute.

Design-drift report verdict is PASS / CHANGES REQUIRED / BLOCKED and covers the whole contract, including missing behavior and unplanned additions:

| Finding | Contract/RUN-D/R/RUN-G reference | Actual file:line/behavior | Impact | Required correction | State |
|---|---|---|---|---|---|
| RD-001 … | Precise approved reference | Concrete evidence | Critical/major/minor with reason | Bounded fix or design decision | Open/fixed/disputed/withdrawn |

Check exact root boundary, SDK APIs/propagation, context preservation, client reuse/config semantics, privacy limits, telemetry/business exception precedence, native filter/provider, deferred CrewAI/logging/agent boundaries, guarded authority and honest status.

Test-gap report verdict uses the same statuses and includes all RUN-01–20 rows from the [test specification](02-runner-test-cases.md#per-round-evidence-mapping). Read actual assertions, fixture realism and test execution, not just filenames/counts:

| Finding | RUN case | Weak/missing/wrong evidence | Regression that could pass | Required correction | State |
|---|---|---|---|---|---|
| RT-001 … | Exact ID(s) | Assertion/node/output location | Concrete failure example | Meaningful test or execution | Open/fixed/disputed/withdrawn |

Independently rerun focused checks where useful. Do not duplicate the entire expensive gate/release solely to repeat trustworthy same-SHA evidence. Any claimed report-only or release-source delta must be checked, not taken on trust.

Orchestrator report links both reviews/coder report, preserves the union of findings and owners, records gate outcomes and final disposition. Disposition is NEXT ROUND N, READY FOR FINAL REVIEW, READY FOR LOCAL VERIFICATION WITH LIMITATIONS, or STOPPED/BLOCKED AFTER ROUND N. It explains unresolved IDs and the exact decision/environment need. An orchestrator cannot convert a reviewer's pending verdict into PASS.

## 7. Validation sequence and release evidence

Use current repository bootstrap/interpreter and actual test node names. Expected focused entry after files exist, from `app/`:

```sh
./.venv/bin/python -m pytest -q tests/application/test_runner_observability.py
./.venv/bin/python -m tooling.checks check
```

Add the actual SDK/lifetime/loopback test nodes to the focused command; do not invent an already-existing filename. The full gate supplies maintained pytest, Pyright and Ruff. Existing offline runtime coverage should not be rerun redundantly without a new concern, but new enabled-path no-network assertions need their own collected case. Report environment/proxy/OTel sampling controls used in isolated tests; never silently alter application credentials or global settings to manufacture a pass.

From repository root after canonical documentation changes:

```sh
python3 designs/atlas/build.py
python3 designs/atlas/build.py --check
git diff --check
```

Run changed-document link checks and preserve unrelated/guarded content. Check personal-example independence by scope/import/gate configuration, not by scanning or deleting the sandbox.

After both reviews otherwise pass, freeze the clean candidate and use existing release tooling from `app/`:

```sh
./.venv/bin/python -m tooling.release
```

Record artifact/version/source SHA, installed imports, dependency/hash verification and actual results. If a report-only source delta is used for a release, prove the runtime/test/tooling/dependency content matches the reviewed candidate; include the comparison and limitations. Do not change release/version policy to evade a blocker. RUN-19 requires enabled installed-path evidence too when it is absent from the normal offline verifier; use a small independent maintained in-memory/loopback fixture, no backend requirement for the wheel gate.

RUN-20 is explicitly configured local integration, separate from ordinary offline pytest. Give the actual tested invocation/controlled-failure commands, expected UI fields and readback deadline after implementing them; this draft does not claim those commands already exist. Use the existing local stack only, preserve volumes, and never reset Sharon's data. A flushed/exported trace URL is not evidence of stored observations. Mark Linux/Mac and readback/UI limits precisely.

No commands in this plan have been executed against an M4.2 application candidate during drafting. Documentation checks are recorded separately by the drafting session.

## 8. Completion and final-review handoff

READY FOR FINAL REVIEW requires an approved reconciled baseline/amendments, implementation within scope, no unresolved required review findings, both reviews on the same final candidate, required automated/release evidence and committed reports. Actual live checks/remaining Sharon UI acceptance must be separately explicit; a material agent live-check block uses READY FOR LOCAL VERIFICATION WITH LIMITATIONS instead. Neither status means accepted or merged. M4.3 does not start automatically.

Publish used reports/status in the focused implementation PR before handing back. Root/design session performs its own final review of actual diff/evidence, after the two independent implementation reviewers. It does not reset the three-round cap or authorize merging. No automatic merge is permitted. If pushing/publication fails, report the exact blocker and available evidence rather than claiming a transferable ready handoff.

Return one copyable report in this exact structure. Replace every placeholder with actual evidence, explicit none, or NOT RUN/BLOCKED and reason. Use GitHub links pinned to actual commits; distinguish candidate, release-source and report-only head.

```text
M4.2 RUNNER OBSERVABILITY — FINAL REVIEW HANDOFF

Outcome: READY FOR FINAL REVIEW / READY FOR LOCAL VERIFICATION WITH LIMITATIONS / STOPPED / BLOCKED
Implementation PR: <URL; draft/open/unmerged state>
Design package PR/branch: <actual URL and branch>
Approved M4.2 design/test/plan revision: <full SHA and commit URL>
Sharon approval reference: <instruction/reference; RUN-D01–05 and RUN-G01–08 decisions>
Verified M4.1 foundation: <full code/test SHA; final-review/acceptance reference; merge state>
Implementation branch and PR target: <branch; target>
Implementation base commit: <full SHA>
Final code/test candidate reviewed by BOTH reviewers: <full SHA and commit URL>
Final published head including reports: <full SHA and commit URL>
Candidate-to-head differences: <comparison URL; proved report-only or exact changes>

Implemented: <actual native runner/client/correlation/outcome behavior and files>
Selected policies: <root boundary; client reuse/config changes; flush/shutdown; disabled/outage; payload/exception projection>
Design deviations: <none or precise approved/unapproved differences and references>
RUN-G01–08 amendments: <applied/blocked; approval/diff/evidence links>
M4.1 changes/follow-ups: <none or separately authorized reference; no silent round reset>

Rounds used: <N>/3
For EACH used round:
- Candidate SHA: <full SHA>
- Coder report: <permanent URL>
- Design-drift review: <verdict; permanent URL>
- Test-gap review: <verdict; permanent URL>
- Orchestrator report: <permanent URL; findings fixed/carried forward>
Final status and complete RUN-01–20 mapping: <permanent URLs>

Verification at <candidate SHA>:
- Focused native SDK/runner tests: <exact commands; counts/results; evidence URLs>
- Existing workflow/context regression and full quality gate: <commands; pytest/type/lint/format results>
- Disabled/enabled-fixture network audit: <attempt counts and scope; blocked destinations if any>
- Repeated calls/outage/flush/exception/payload checks: <actual assertions/results; limits>
- RUN-01–20: <passed / missing / weak / failed / blocked / not-run cases>
- RUN-19 installed release: <command; artifact/version/source SHA; enabled/disabled evidence>
- Release-source-to-candidate differences: <comparison URL; exact equivalence or limits>
- Documentation/Atlas/links/whitespace: <commands and results>
- RUN-20 local ingestion: <server/version; actual stored trace evidence; observed fields or blocker>
- Sharon UI acceptance: <pending or exact user acceptance reference>
- Checks not run and remaining local/manual steps: <exact commands/expected result and reasons, or none>

Open findings/blockers/risks: <stable RD/RT IDs; impact; next action, or none>
Scope confirmation: <M4.2 only; no automatic CrewAI/logger/agent/dependency additions, or explicit approved exception>
Merge state: <unmerged; no merge performed>

Please perform the final design-session review of the actual diff and linked evidence.
The two implementation reviews do not replace your final review or authorize merging.
The three-round counter remains in force; no automatic fourth correction round is requested.
```

After an explicit acceptance/merge instruction, inspect resulting main and reconcile status/evidence as required by the design contract. Retain all rounds and local-ingestion limits. Prepare M4.3 only under its own design/authorization; preserve the automatic-instrumentation priority without bundling it into this runner PR.

## Draft documentation verification — 2026-11-14

The drafting session checked all three new files: 27 relative links/anchors, balanced fenced blocks, final newlines/trailing whitespace, exact RUN-01–20 case rows, RUN-D01–05 choices and RUN-G01–08 amendment rows. Atlas `--check` passed its existing references/hierarchy/guards/sandbox/freshness checks; its navigation was intentionally unchanged under the parallel-work boundary. Git tracked-file diff was empty and `git diff --check` passed; the three new files also received direct whitespace checks because they were untracked. No existing M4.1/history/guarded/research file was edited by this drafting agent. No application test, SDK runtime probe, release build or live Langfuse verification was run for these drafts.
