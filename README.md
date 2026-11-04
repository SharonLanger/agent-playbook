# Agent Playbook

Agent instructions, project rules, and workflows for coordinating coding, testing, and review.

## Structure

- `AGENTS.md`: short instructions for maintaining this repository.
- `agents/`: one Markdown file per role.
- `workflows/`: coordination steps, launch parameters, and explicit status routes.
- `projects/<project>/review-rules.md`: project review requirements.
- `projects/<project>/reviews/pr-<number>.md`: optional PR-specific requirements.

`project-a` and PR 14 are examples, not configured projects or tasks.

## Run one reviewer directly

Copy this into a Codex session and replace the bracketed fields:

> Use the playbook at https://github.com/SharonLanger/agent-playbook. Read `agents/reviewer.md` and review PR #[number] in [owner/repository] for project [project-key]. The approved design is [path or link, including revision]. Write the review report to [workspace path]. Follow the reviewer's file-discovery rules and return its structured status and report path. Do not edit code or post the review to GitHub.

The project key selects optional `projects/<project-key>/review-rules.md` and `projects/<project-key>/reviews/pr-<number>.md`. A missing file adds no extra rules. The approved design is required for a complete design-based review. You can read the report in the session from your phone.

## Agreed design

The orchestrator launches specialist agents using instruction file paths and task parameters. It does not read or paste specialist instructions, interpret reports, or decide how to fix problems. It follows explicit workflow routes based on structured results containing a status and artifact paths. Specialist agents interpret failures and prepare instructions for subsequent agents.

The reviewer reads its own instructions, the specified project's review rules if present, and the PR-specific file if present. Missing project or PR files mean there are no additional rules. Missing required instructions or unreadable files must be reported rather than silently ignored.

Role launches do not explicitly load the playbook's `AGENTS.md` as shared role instructions. It governs maintenance of this repository. Codex may also supply applicable repository instructions automatically, depending on the execution context; a role launch does not disable that behavior. Any future shared role defaults should be defined separately and loaded explicitly.

Workflows may specify additional parameters, available models, and reasoning effort. Exact role instructions, result formats, routing, retry limits, and model selections are still to be defined. Markdown files describe the behavior; execution requires a supporting agent runtime. A fresh sub-agent context does not restrict workspace access.

The reviewer guide is defined for a trial review once an approved design is available. The designer, implementer, orchestrator, and workflow files remain unimplemented and stop explicitly if invoked. Separate tester and replanner roles are deferred.
