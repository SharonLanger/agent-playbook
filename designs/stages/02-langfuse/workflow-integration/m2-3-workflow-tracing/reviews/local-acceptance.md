# Local acceptance — design-session checkpoint

2026-11-15. Implementation code/test candidate adbba215da77e1e618c3c699e1d84c1ba45c629e; reviewed published head 59282c9a18e6807149ca8337d2b4bea3463ba15c. This report adds evidence only.

Sharon completed Setup on his Mac and ran the maintained workflows against local Langfuse. WF-01 console/result/exit and local hierarchy were inspected; its screenshot showed runner, kickoff and produce/decorate/finish. Sharon confirmed shared correlation_id and workflow_run_id. He ran WF-02 and both WF-03 routes. After the round-02 update, he explicitly confirmed the requested score-60 checks and then the score-59 checks: outer input/output, readable names, selected branch and absence of the other branch. His final confirmation was “Everything is there.” These are user-reported live checks, not independently queried backend exports.

Design session reviewed round-02 runtime/test changes and both reports, and verified candidate-to-published-head changes were report-only. No new implementation blocker found. Reported full gate: 408 passed, Pyright/Ruff passed; installed release passed. Design session did not independently rerun that suite. Existing reviewer verdicts remain historical and are not rewritten.

Remaining RUN-18 evidence: a controlled failed step reaching local Langfuse has not been run/reported in this session. Automated failure tests passed according to candidate reports, but they do not prove live failure ingestion. This item must be completed or explicitly deferred by Sharon before claiming the full acceptance checklist closed.

Sharon requested merging implementation PR #50 and updating stage progress. Merge preparation is awaiting the remaining manual item's disposition; this is not evidence it passed. Stage Design PR #47 stays open/draft. No third coding round is consumed by this report.
