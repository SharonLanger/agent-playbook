# Codex brief — milestone 1 setup

For the newly authorized connection/playground work, follow the
[M2/M3 brief](connection-playground-handoff.md). The stop-at-M1 instructions below
apply to the original setup assignment, not to that later assignment.

Status: **Handoff instructions to use when Sharon requests implementation.**
This documentation update does not itself start implementation or approve unrelated
guarded changes. [Milestones](../../milestones.md) · [Verification requirements](../verification.md)

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

Follow [verification.md](../verification.md), including real stack startup and
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

## Follow-up: simple operation and replaceability

M1 is now implemented on PR #36; inspect the latest branch and findings before
working. Sharon's follow-up requests easy install/start/stop/rerun and externally
configurable, removable deployment. The official guide is
`app/docs/langfuse-local.md`; retain that existing canonical file rather than
create a competing `langfuse.md`.

Use the guide's short native Compose commands from the deployment folder. Do not
add a custom Dockerfile or wrapper framework just to wrap `up`, `down` and `ps`.
The existing prebuilt images and Compose already supply those operations.

The remaining implementation gap is the hard-coded MinIO host port. Expose it as
one external setting (default 9090), applying it consistently to the host binding
and the web browser's media endpoint. Keep container-internal endpoints on the
service network. Update the template, first-time settings generation and official
guide together; preserve existing `.env` files and default old configurations
correctly. Keep image pins explicit and reviewed; do not use floating versions
merely to make them configurable.

Verify first setup, repeated setup without overwriting secrets, repeated start,
normal stop/start, restart, and applying a UI/storage-port change with `up -d`.
Check that both published ports stay on loopback and use an isolated verification
project. If possible on the available platform, check image architecture support
for Sharon's Mac; report Linux-only testing honestly. Confirm normal application
checks require neither Docker nor this stack. Keep the existing CLI, bootstrap,
workflow/context and Python dependency graph unchanged in this follow-up.

Disabling/removing local deployment must leave application execution intact;
ordinary stop never deletes stored data. Later SDK/configuration milestones must
keep endpoint/credentials external and a disabled mode without network access.
Do not implement those later milestones in this follow-up. These instructions
record requested work, not evidence that the port change or Mac check has run.
