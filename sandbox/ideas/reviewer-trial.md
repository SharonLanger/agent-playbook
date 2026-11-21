# f-01-reviewer-trial — Verify the reviewer and its handoff

**Draft idea.** This preserves the trial as proposed, including the design-approval and persistence-test questions observed at inspection. The [archived PR 46 requirements](../../designs/refactors/project-refactor/archive/system-one-harness/reviews/pr-46.md) record the later persistence-test clarification and the remaining design approval condition. [Original location at the migration base](https://github.com/SharonLanger/agent-playbook/blob/ef7b22492d6091c8c4b47c4226a24550a9b23ccb/sandbox/projects/agent-playbook/features/f-01-reviewer-trial/design.md).

- Project: `agent-playbook`
- Source repository: https://github.com/SharonLanger/agent-playbook
- Status: Draft; not approved for implementation.
- Revision: Draft 1
- Inspection baseline: `9c674a76ee2dec04e5f05e5bdd6b8c564e761c86`
- Feature identifier: `f-01-reviewer-trial`

## Problem and intended outcome

The reviewer guide is written, but we have not evaluated a completed review from a fresh session. Establish whether it finds useful issues, loads the right rules, and reports evidence honestly before building coordination around it.

## Scope and approach

Use the already requested review of system-one-harness PR 46 as the first real trial. If that review is already running or finished, inspect its report rather than launch a duplicate. Record the source head actually reviewed, playbook revision, design revision, and model/effort used. Evaluate findings against source evidence; do not equate a long report or a passing status with a good review.

Check whether the report follows the [historical reviewer guide](../references/reviewer.md) and the [archived PR 46 requirements](../../designs/refactors/project-refactor/archive/system-one-harness/reviews/pr-46.md) (formerly `projects/system-one-harness/reviews/pr-46.md`). The design was marked draft at inspection, and dedicated persistence tests conflict with the stricter PR rules. Obtain the user's actual decision about those points; never manufacture approval to make a trial pass.

Add a short reusable verification checklist for future reviewer changes. Use small disposable examples only for cases the real trial does not exercise. Real source edits are outside this feature. No permanent testing framework is needed.

## Acceptance criteria

- A fresh reviewer receives paths and explicit task inputs, without needing this conversation.
- It identifies all loaded rules and revisions, including missing optional rules.
- Findings include evidence and distinguish introduced problems from existing gaps.
- Optional suggestions alone do not prevent a pass; missing essential evidence prevents a trustworthy pass.
- The report and structured status agree. A blocked report preserves concrete findings already established.
- PR 46's experiment inventory, replacement-scenario mapping, and file-assertion audit are evaluated for completeness.
- No implementation changes or GitHub review submission occur during the review.

## Verification scenarios

| Scenario | Expected behavior |
| --- | --- |
| Real PR 46 trial | Report traces removed/deferred coverage to replacement scenarios, including one-to-many mappings; no claim that deferred checks passed. |
| No project or PR rules file | Continue with general rules; do not invent requirements. |
| Existing rules file is unreadable | Report the access problem and block rather than ignore it. |
| Specific rule conflicts with a required general rule | Explain the conflict; block if it prevents a sound conclusion. An explicitly overridable default may be specialized. |
| Draft design without approval evidence | Report the approval gap; preserve useful inspection findings without issuing a complete design-compliance pass. |
| Test results refer to an older code revision | Label evidence stale and obtain relevant evidence or report the limitation. |
| Known defect versus cosmetic preference in a small example | Request changes for the defect; label the preference optional. |
| PR head changes during review | Identify the reviewed revision and avoid presenting the report as approval of unreviewed changes. |

For each exercised scenario, record expected and observed behavior, artifact/revision references, and pass/fail/not-run. Mark unexercised scenarios not-run. Ask the user to assess the real report's usefulness; do not treat the reviewer's self-assessment as independent validation.

## Delivery and evidence

1. Collect and evaluate the real review report.
2. Exercise only the remaining critical cases with small examples.
3. Correct demonstrated guide or handoff problems in a separate implementation PR.
4. Save a concise outcome record with limitations and links to durable evidence.

Keep temporary reports in the workspace during evaluation. Preserve selected final evidence in the playbook through a PR when completing the feature; avoid committing every log.

## Dependencies and open decisions

Needs the real reviewer report and the user's resolution of design approval and file-test scope. A blocked trial can validate blocker behavior, but cannot demonstrate a successful approved-design review. Implementation and execution are pending approval of this design.
