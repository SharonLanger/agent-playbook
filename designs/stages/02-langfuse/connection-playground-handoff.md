# Codex handoff — connection and mock playground

Status: **Sharon requested this implementation handoff on 2026-11-13. M2/M3
are not implemented by this document. M1 still awaits his Mac/UI acceptance.**

## Scope and order

Implement milestone 2 (connection), then milestone 3 (editable mock traces) on
PR #36, branch `docs/stage-02-langfuse-setup`. Work may proceed while Sharon rests
and before his local M1 acceptance. This changes implementation scheduling, not
the acceptance gates: never mark a milestone accepted on his behalf.

Read root `AGENTS.md`, `designs/AGENTS.md`, governance, charter, principles,
architecture, project structure, roadmap/progress and this stage's README,
architecture, milestones, smoke plan and verification requirements. Reuse
unchanged already-loaded revisions. This request authorizes the scoped work
below, not unrelated guarded changes or a workflow/context implementation.

Use the existing integration/configuration/tooling boundaries. Register an
approved baseline as required by repository governance; do not infer approval
for unrelated changes or adopt exploratory event/harness designs.

1. Inspect the latest PR branch and preserve concurrent changes.
2. If still outstanding, complete the small M1 storage-port follow-up described
   in [the M1 brief](implementation-handoff.md), as a distinct commit/checkpoint.
   Preserve the existing M1 checkpoint below. Do not force Sharon to use the new
   setup revision to perform the original M1 test.
3. Implement and verify M2; commit/push a complete checkpoint and record its SHA.
4. Implement and verify M3 after M2's relevant available checks pass. A blocked
   live environment does not prevent offline development, but must remain
   explicitly BLOCKED, including dependent ingestion checks.
5. Update separate user verification files with actual commands and hashes.
   Stop before M4 and do not merge the PR.

The current fixed M1 checkpoint is
`fad8a4f119cab5316529b3ad9239d01b8347368c`. Keep it reachable; do not rewrite
history. Separate milestone commits/checkpoints are required, not one new PR per
milestone. Each milestone may need several commits. Record its final tested
implementation SHA before beginning the next milestone; a later evidence-only
commit may link to that SHA without claiming to test itself.

## Concurrent-work assessment

At preparation, workflow implementation PR #40 (`feat/workflow-contract`) overlaps
`config/models.py`, `config/loader.py`, configuration tests, official guides,
progress and Atlas. The proposals are behaviorally separable, not conflict-free.
Recheck open PRs and main before editing or integrating. Make additive config
changes, preserve existing configuration-selection/merge/validation semantics,
and do not import or cherry-pick unfinished workflow lifecycle work. If another
branch merges, reconcile its configuration changes and rerun affected checks.
Never hand-merge generated Atlas HTML; rebuild from reconciled sources.

## Milestone 2 — connection only

Deliver validated external settings, a narrow Langfuse-specific integration and
an explicitly invoked standalone checker. Follow the configuration proposal in
[architecture](architecture.md); choose concrete names consistent with the current
loader and document them. Existing YAML files that omit Langfuse must still load
with Langfuse disabled. Do not create a second application configuration loader.

- Config responsibility: endpoint, enabled flag, environment label and references
  to externally supplied project keys. Preserve file/local/environment precedence,
  strict validation, unknown-field handling and sanitized errors. Missing keys are
  relevant when enabled; disabled mode requires neither keys nor network access.
- Adapter responsibility: instantiate the compatible client only on explicit use,
  check project authentication, own bounded requests/cleanup and report a small
  structured result. SDK/provider details stay inside the adapter. No global
  instrumentation, import-time client construction or automatic export.
- Tooling responsibility: load settings, invoke the check and print a safe result
  with documented exit codes for success, disabled/skipped and failure. A skipped
  check must not say authenticated. No traces are emitted by this checker.
- Use current official SDK/server documentation before selecting an exact SDK pin
  compatible with the deployed Langfuse version. Update dependency metadata and
  lockfile consistently. Document installation/packaging choice and verify it;
  do not introduce a broad optional-plugin system for this task.
- Reject unsupported/malformed endpoints safely. Do not print key values, raw SDK
  exceptions or URL credentials in errors. Distinguish invalid configuration,
  failed authentication and network/timeout errors where the SDK exposes them;
  otherwise report an honest general connection failure.

Project API keys are created inside Langfuse; they are different from Docker
service secrets in `app/tooling/observability/.env`. Do not automatically source
that file as application settings. Use ignored local configuration/environment
references and document an exact Mac-friendly way to supply keys without putting
their values in committed files or command history.

Do not change application assembly, runner, workflow factory, workflow/context
classes or CrewAI tracing. Do not implement CLI doctor (#37); this checker should
be small enough to reuse there later. Preserve Docker-only M1 usage without a
Python environment install. Normal application operations must still work when
Langfuse is disabled/stopped, and normal checks require no live server.

### M2 verification

Follow [verification.md](verification.md). Use maintained fixtures under
`app/tests/` to verify old YAML compatibility, precedence, valid/invalid enabled
settings, missing/invalid key references, disabled/no-client/no-network behavior,
sanitized diagnostic output, bounded failure handling and documented exit codes.
Test behavior, not a copy of the implementation.

With a feasible isolated service/project, check correct keys, rejected keys and
an unreachable endpoint. Verify the check produces no trace writes. A public
health response is insufficient authentication evidence. The agent may create
disposable local test credentials, but must not require Sharon's personal keys
or touch his existing volumes. Report live blockers rather than substitute mock
results for live evidence. Run current type/lint/format/test gates. Since SDK
metadata changes, perform relevant lock/install/wheel checks using existing
project tooling; no release/version bump or publication is requested.

## Milestone 3 — personal mock playground

Implement the specifically requested `app/examples/langfuse/run.py` and README,
using M2's configuration/connection and a small observation interface in the
Langfuse adapter. Follow [smoke-plan.md](smoke-plan.md): initialize → add →
multiply → finish, defaults `(3 + 2) * 4 = 20`, editable inputs and a choice of
failure at add or multiply. Use fresh run/trace identifiers, actual timings,
small synthetic payloads and explicit mock labels. No actual CrewAI/model calls.

The script runs only when Sharon invokes it. Creating/importing the integration,
starting Docker or running the normal application must not seed traces. On a
simulated failure, mark the failed step/root as errors and do not report later
steps as completed. Distinguish simulation errors from export/configuration
failures. Flush/cleanup and print the actual trace ID/link without secrets.
Do not claim persisted success merely from returning a link or flushing.

This explicitly permits creating, reading, editing and manually smoke-running
only the new Langfuse playground during implementation. If it already exists,
inspect and preserve Sharon's edits. Do not access `app/examples/workflows/` or
other personal examples. Do not import/run/inspect examples from automated tests,
coverage, quality checks, bootstrap or releases. Maintained tests own independent
fixtures and cover the adapter/configuration; the personal README explains
installation, working directory, settings, editable values and commands.

### M3 verification

Manually smoke-run the requested new script's success, add-failure and
multiply-failure scenarios. With live access, read observations back with a
bounded wait and check parent/child relationships, result 20, errors, absent
completed downstream steps, distinct run IDs and correct trace links. Separately
exercise maintained adapter behavior with independent fixtures. Check ordinary
workflow results and checks remain unaffected without touching other examples.
Record blocked ingestion checks honestly if the service is unavailable.

## Deliverables and user verification files

Maintain public `app/docs/` setup/configuration guides for implemented behavior,
the example README, stage findings/progress and Atlas. Preserve earlier test
results with their original revisions. Report PASS/FAIL/BLOCKED/NOT RUN rather
than implying that all checks ran. Keep M1/M2/M3 acceptance pending until Sharon
reports his respective local checks. M4 is out of scope even if its refactor
merges during this task.

See [user-verification.md](user-verification.md) for the existing Drive files.
After each milestone, update its own text file in place with the exact tested
full commit SHA and literal fetch/checkout/install/configure/run/stop commands.
Keep the M1 file pinned; don't replace its hash with an M2/M3 revision. Include
working directories, expected visible result, safe return instructions and
platform/check limitations. No placeholders may remain in a file marked ready.

If Drive tools are unavailable in the implementing Codex environment, deliver
one complete plain-text checklist per milestone in a permanent stage-owned
handoff location and identify the intended Drive file. Report that Drive upload
is pending; do not claim it happened or block coding on account access. A later
review can upload those exact files. Never put real keys in those checklists.

At final handoff, report the M1 follow-up (if any), M2 SHA, M3 SHA, actual checks,
remaining local tasks and Drive update status. Leave the existing PR unmerged.
