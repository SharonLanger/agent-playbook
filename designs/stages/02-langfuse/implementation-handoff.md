# Codex brief — implement milestone 1 only

Status: **Handoff instructions to use when Sharon requests implementation.**
This documentation update does not itself start implementation or approve unrelated
guarded changes. [Milestones](milestones.md) · [Verification requirements](verification.md)

## Read and align before editing

1. Fetch the latest state of PR #36 and its branch
   `docs/stage-02-langfuse-setup`; inspect local changes and concurrent work.
   Preserve existing work. Do not force-push or overwrite another agent's edits.
2. Read root `AGENTS.md`, `designs/AGENTS.md`, charter, principles, target
   architecture, project structure, roadmap/progress, design contract/guard register
   and relevant approved stage material as those instructions require.
3. Read this stage's README, milestones, architecture and verification documents.
   Consult the observability exploration. M1 is independent of the workflow refactor.
4. Treat Sharon's explicit instruction to implement M1 as authorization for that
   milestone's stated scope, not M2–M4 or unrelated protected changes. Record the
   approval scope. Follow required approval/registration procedures for a baseline;
   if guarded meaning must change beyond that scope, present the concrete logical
   change first. Do not invent extra approval gates for already-authorized work.

## Implement

**Goal:** Sharon can start local self-hosted Langfuse, open the UI, create his
project and retain it after a normal restart. An empty trace list is expected.

- Add a minimal reproducible deployment under the existing
  `app/tooling/observability/` ownership boundary. Use upstream Langfuse Compose
  as a reference and verify current release compatibility before choosing exact
  pins. Record the upstream reference and tested versions.
- Provide external/ignored local secret configuration and a safe template. Explain
  initialization, ordinary start, readiness check and stop. Avoid overwriting
  existing local files. Keep published services local and preserve named volumes.
- Keep helpers small. Add only the setup/readiness support M1 actually needs.
  There is no need to create a diagnostic framework.
- Add maintained official setup/troubleshooting instructions under `app/docs/`
  and link them from its index. Update affected stage findings/progress and Atlas
  accurately, preserving the distinction between implemented, verified and accepted.

No Langfuse Python SDK wiring, application YAML schema extension, CLI doctor,
mock script, examples access, workflow/context edits or milestone 2–4 work.
The Python integration/configuration is M2; the personal example is M3.

## Verify before handing over

Follow [verification.md](verification.md), including real stack startup and
readiness/restart checks when the environment supports them. Use an isolated
verification instance and never touch Sharon's existing volumes. Check the
documented commands. Do not expose resolved Compose secrets in diagnostic output;
prefer quiet validation and sanitized summaries.

If Docker, downloads or required resources are unavailable, diagnose and report
the actual blocker, complete static checks, and provide the minimum remaining
local commands. Do not claim live verification. Do not spend substantial effort
provisioning a new environment just to automate Sharon's few UI clicks.

Run relevant repository/documentation checks; fix failures within scope. Record
actual commands, results, versions and tested revision in the stage findings.
Do not create tests for upstream behavior or tests that merely repeat the config.

## Deliver and stop

Commit/push the M1 work to the existing PR branch after checking its latest head;
keep the PR unmerged. Do not create one new PR per milestone or start later
milestones automatically. If branch status changed, reconcile deliberately rather
than overwrite or silently choose a different integration target.

Report the milestone's verification status, exact checkout/run/stop commands,
expected URL/UI result and any remaining limitation. Leave Sharon only the short
manual acceptance exercise; do not mark it completed on his behalf.
