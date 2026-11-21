# M3 follow-ups after capped design review

Historical scope note. The [current design](design.md) keeps the existing Docker names and generated Langfuse deployment settings. Routine M3 verification uses the existing installation. Renaming belongs to issue #56.

## Approved scope change — fresh deployment, 2026-11-18

Sharon explicitly approved discarding the existing local Langfuse and VictoriaLogs deployment data and starting fresh. His clarification: “I called it sandbox. But I mean, we can delete all and start fresh.” This is a fresh-install decision for these two project stacks, not a reference to the repository's excluded app/examples/ or sandbox/ directories.

Approval follows the explicit question about discarding existing traces/logs from these two stacks. Cleanup may remove their identified containers and volumes; project images may be removed when not used by unrelated containers. It does not authorize global Docker pruning, deleting unrelated projects, source files, or the shared secrets file.

### Consequences for the next contract revision

- Replace legacy data migration, old-volume adoption/reconstruction, recovery manifests and legacy rollback with a documented explicit clean-start prerequisite.
- No requirement to preserve old traces, logs, Langfuse accounts or projects across this one-time reset. Recreate Langfuse onboarding/project credentials as needed after database reset; retained application API keys must not be assumed valid against a new database.
- Keep the selected shared secrets file and unrelated credentials. Provision new deployment credentials there as needed through the agreed setup; no copying/equivalence validation of old infrastructure credentials is required for a fresh database.
- Routine start/stop after initialization still preserves data. Destructive reset is an explicit manual verification action, never implicit in normal startup.
- Retain independent act-logs / act-langfuse operations, configuration-driven selection, shared YAML/secret ownership, controlled Compose environment, canonical Langfuse origin, bounded readiness, Docker-free default tests, opt-in live checks and honest Atlas/docs status.
- Broader naming remains issue #56. No source/package/CLI/path rename or personal examples access.

### Manual Mac acceptance sequence

1. Identify the Docker context and exact old/new project resources; remove only those stacks' containers/volumes and optionally unused project images.
2. Start logging independently, run a real workflow and inspect records, then verify ordinary restart retains them.
3. Start Langfuse independently, complete fresh onboarding/project-key setup, run a workflow and inspect traces, then verify restart retains them.
4. Explicitly clean the two test stacks and their data again.
5. Start both through the shared entry according to enabled settings; repeat fresh Langfuse onboarding if its database was removed, and verify actual workflow logs and traces.
6. Stop/start each independently while the other remains usable; verify new data persists through ordinary operations.
7. Include M2 LG-10 lifecycle/DEBUG/chained-exception, identity query, UI ordering and shutdown observation in the final .txt guide. Record actual evidence; instructions are not a PASS.

## Review and implementation status

This decision supersedes the old-data-preservation requirement for the one-time transition. The old three rounds and their findings remain historical evidence; migration-specific findings become superseded by changed scope, not fixed or passed. Relevant non-migration findings still need correction.

The blocked candidate design/test/plan has not been rewritten by this note. No new review round, runtime implementation, deletion or live test has run. The implementation agent has not yet received a revised handoff. The three-round cap remains exhausted until Sharon authorizes a new bounded continuation. Prepare a simpler revised concrete contract from this scope before implementation approval.
