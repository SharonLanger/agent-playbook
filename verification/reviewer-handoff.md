# Reviewer handoff verification

Use this checklist for the first run under the updated reviewer guide and after relevant changes. Record actual results as pass, fail, or not run, with the review folder and code/playbook revisions. Do not alter unrelated Drive files or production code to manufacture a test.

## Minimal invocation check

Start a fresh session with only the PR URL and the playbook reviewer-guide URL, using the README prompt. Confirm that it discovers project/PR rules and the design, finds previous review folders/index without being given their links, checks evidence revisions, and chooses the next review number. Record unresolved design approval separately from successfully discovered inputs.

Repeat against a PR with an existing run. The new report must distinguish reused evidence from new checks, reassess findings affected by changed rules, and preserve the old run. Use an existing legacy run without a manifest to verify explicit limitations; do not deliberately damage completed artifacts.

## Before a review

- Resolve the configured agent-work folder and the exact project, repository, and PR.
- Read both reviews.json and existing review folders. Allocate the next number without overwriting a prior run. Legacy folders count even if absent from the index.
- Confirm there is no other active reviewer for that PR. Preserve previous index entries and completed files.
- Record design approval evidence if available. Missing approval remains a review blocker; do not mark the design approved as part of testing delivery.

## Delivery checks

- Main report and every referenced appendix/evidence file are uploaded inside the assigned run.
- Downloaded bytes match staged byte sizes and SHA-256 values.
- Report/appendix links open from Drive and use no session-only paths as handoff destinations.
- manifest.json parses, lists the artifacts by relative path and Drive ID/link, and identifies review number, repository, PR, reviewed commit, baseline, and instruction revisions.
- reviews.json parses, identifies the same run/commit/manifest, preserves previous entries, and shows complete delivery only after all checks pass.
- The final response includes report, run-folder, manifest, and index links. Review result and delivery result are distinct.

## Failure and sequencing cases

Exercise these only when encountered naturally or in an explicitly designated disposable test area. Otherwise mark not run.

| Case | Expected result |
| --- | --- |
| Review is blocked on design approval, but uploads succeed | review_status blocked; delivery_status complete; findings remain readable. |
| One upload or reference check fails | delivery blocked; list missing artifacts; do not mark the index complete. |
| Resume an interrupted upload | Use the recorded incomplete run ID; preserve earlier reviews; verify existing artifacts before updating. |
| Second review of the same commit | Allocate the next number; record the same hash without treating it as a collision. |
| PR or requirements change after review | Label the old review as applying to its recorded inputs; require a new review for the changed inputs. |
| Index changes during this invocation or another reviewer is active | Stop the competing write; do not overwrite it. |
| Missing legacy manifest | Preserve old artifacts; index delivery as blocked until a separately authorized repair or new complete run exists. |

## Fresh-session acceptance check

After delivery, open a fresh session and provide only the review-folder link plus this task:

> Read the review manifest and report in this folder. Verify you can retrieve every referenced artifact, match its size/checksum, and identify the repository, PR, reviewed commit, and review result. Explain any missing files or stale code/rules. Do not modify the files.

The receiver must not need the original session's workspace or pasted report contents. Record its observed outcome before saying cross-session delivery is verified. Reuse the prior successful cross-session report read as partial evidence, but not as proof that the newly required manifest/index protocol passed.
