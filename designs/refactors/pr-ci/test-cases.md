# Acceptance cases

| ID | Requirement | Expected evidence |
|---|---|---|
| T1 | R1, R5 | Public code and docs-only PRs emit the same named check. Private runs allocate no runner. When a selected gate fails, its failure propagates. No path filter, live-service fixture, secrets or personal examples are required. Inspect actual hosted outcomes after activation. |
| T2 | R1, R5 | Existing checks report type, lint, format and maintained tests once. Atlas --check passes on current output and rejects stale output. Collect failure and skip evidence honestly. |
| T3 | R1, R3 | Build in a clean checkout, install in runner temp, and run the installed console script there. Confirm metadata, wheel contents, imported module location inside its clean environment, version/SHA, hash, known workflow output and existing negative cases. Record exact commands and environment. |
| T4 | R2 | GitHub readback shows the specified rules. A failing check blocks an ordinary merge, admin has an explicit PR-only override, fixing the PR enables ordinary merge when otherwise eligible. Do not actually merge or force-push to prove enforcement. |
| T5 | R3 | Exercise all three arithmetic examples, bare version, explicit input compatibility and invalid input. Test clean failure without mismatched TOML/lock. Bumping leaves Git refs unchanged; installed packages reject checkout-only bumps. |
| T6 | R4 | At a version boundary, compare the dated entry to all merged PRs in the recorded interval. Include docs-only and maintenance PRs, de-duplicate Unreleased entries, and record a needed breaking-change upgrade note. An empty interval, first baseline or standalone offline clone must not fabricate GitHub history. |
