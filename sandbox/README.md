# Agent Playbook

Agent instructions, project rules, and workflows for coordinating coding, testing, and review.

## Structure

- `AGENTS.md`: short instructions for maintaining this repository.
- `agents/`: one Markdown file per role.
- `workflows/`: coordination steps, launch parameters, and explicit status routes.
- `projects/<project>/review-rules.md`: project review requirements.
- `projects/<project>/reviews/pr-<number>.md`: optional PR-specific requirements.

`project-a` and PR 14 are examples, not configured projects or tasks.

## Design a new feature

Project folder names match the exact supplied project name. For System One Harness, use `system-one-harness`. Features are numbered within each project and use lowercase names with a slug of at most three words, such as `f-01-session-recovery`.

A design is saved at `projects/system-one-harness/features/f-01-session-recovery/design.md`. This is an example path; create a feature folder only for a real feature.

Copy this into a new session and replace the bracketed fields:

> Use https://github.com/SharonLanger/agent-playbook and read `agents/designer.md`. Help me design a new feature for project `system-one-harness`, source repository [repository URL]: [feature request]. Follow the guide to choose the next feature number and save the draft design. Return its exact path so I can review it.

To resume, supply the exact feature identifier or design path. The designer reads its save and lookup conventions from its own guide, so it does not depend on this chat's memory.

## Run one reviewer directly

Copy this into a new Codex session:

> Review [PR URL] using `agents/reviewer.md` in https://github.com/SharonLanger/agent-playbook on main.

Use the same prompt for the first review and every follow-up. The reviewer discovers the exact project, applicable rules, linked design, prior runs, and valid reusable evidence. It allocates the next number, writes and verifies the shared handoff, and returns the links automatically. Supply extra context only for something that cannot be discovered or an intentional change of scope. Missing approval is reported rather than invented.

## Share a review between sessions

The reviewer publishes ordinary Markdown reports and JSON evidence to Google Drive:

```text
agent-work/
└── system-one-harness/
    └── pr-46/
        ├── reviews.json
        └── review-01/
            ├── pr-46-review.md
            ├── manifest.json
            ├── [review appendices]
            └── evidence/
                └── [supporting files]
```

Each invocation owns its sequential review directory and may maintain its own entry in that PR's `reviews.json`. The index records exact commits, design/rules revisions, times, results, delivery status, and links. Run one reviewer per PR at a time; Drive file updates are not atomic appends. Preserve completed reviews and earlier index entries. The reviewer can create required project/PR folders but cannot write into another project or PR, delete shared files, or change Drive sharing. These instructions do not change Drive's technical permissions.

A local workspace is temporary staging, not shared storage. A blocked review still saves its available findings and evidence. The final response reports review status and delivery status separately. If uploads fail, the reviewer must say the handoff is incomplete rather than present a local path as a shared result.

In another session, paste:

> Read the review and its evidence from this Agent Work review folder: [folder link]. Start with manifest.json, confirm the source repository, PR, and reviewed revision, then inspect the report and linked evidence. Explain the findings to me.

The reviewer verifies uploaded bytes and all artifact references, then finalizes the manifest and PR index. A new numbered review is required even when reviewing the same commit again. A recent passing report applies only to the code and requirements it actually reviewed.

Use the [handoff verification checklist](verification/reviewer-handoff.md) to exercise successful, blocked, and incomplete deliveries and a fresh-session readback. A checklist describes checks to perform; it is not evidence that they ran.

This workflow requires both sessions to have access to the same connected Drive folder. It does not require committing review artifacts to GitHub.

## Agreed design

The orchestrator launches specialist agents using instruction file paths and task parameters. It does not read or paste specialist instructions, interpret reports, or decide how to fix problems. It follows explicit workflow routes based on structured results containing a status and artifact paths. Specialist agents interpret failures and prepare instructions for subsequent agents.

The reviewer reads its own instructions, the specified project's review rules if present, and the PR-specific file if present. Missing project or PR files mean there are no additional rules. Missing required instructions or unreadable files must be reported rather than silently ignored.

Role launches do not explicitly load the playbook's `AGENTS.md` as shared role instructions. It governs maintenance of this repository. Codex may also supply applicable repository instructions automatically, depending on the execution context; a role launch does not disable that behavior. Any future shared role defaults should be defined separately and loaded explicitly.

Workflows may specify additional parameters, available models, and reasoning effort. Exact role instructions, result formats, routing, retry limits, and model selections are still to be defined. Markdown files describe the behavior; execution requires a supporting agent runtime. A fresh sub-agent context does not restrict workspace access.

The reviewer guide is defined for a trial review once an approved design is available. The designer guide supports initial design creation and discovery; autonomous replanning is still deferred. The implementer, orchestrator, and workflow files remain unimplemented and stop explicitly if invoked. Separate tester and replanner roles are deferred.
