# Local verification and retained milestone checklists

Status: **Sharon accepted the local setup and mock-trace exercise on 2026-11-14. PR #36 remains unmerged; M4 is deferred.**

The [acceptance record](acceptance-2026-11-14.md) distinguishes observed Mac/UI
results from automated verification and the remaining delivery-readback limitation.
Use the maintained [connection guide](../../../app/docs/langfuse-connection.md)
and [hands-on exercise](../../../app/docs/langfuse-hands-on.md) for current YAML-selected
credentials and runnable commands. The older Drive files below retain their original
SHAs and setup instructions; they are historical rather than current onboarding.

| Historical file | Checkpoint |
|---|---|
| [Combined acceptance checklist](https://drive.google.com/file/d/1vxH9napBHThAPX7ELtdTFoO0ONI8jBgE/view?usp=drivesdk) | Earlier combined final-head exercise before YAML-selected credentials |
| [M1 verification](https://drive.google.com/file/d/1ASuYt3GuwGhfnUJW2EvwhJVnKYxv5XEc/view?usp=drivesdk) | Local UI milestone checkpoint |
| [M2 verification](https://drive.google.com/file/d/18AgG1LrCXiag_cHG5QYev0dpwyrhMzoR/view?usp=drivesdk) | Project authentication checkpoint |
| [M3 verification](https://drive.google.com/file/d/1P2nLMatSnBhCBOMUUKpp5PRWzLAYSjvi/view?usp=drivesdk) | Explicit mock tracing checkpoint |

Historical checklist-preparation instructions and verification evidence follow.
They do not reopen accepted local setup or authorize M4.

## Historical checklist preparation instructions

Follow [the M2/M3 handoff](connection-playground-handoff.md). Update each file
only after its implementation exists. State the full pushed SHA, branch, platform,
checks and remaining local acceptance; include exact fetch/checkout commands,
working directories, dependency installation, private configuration, run command,
expected UI/output, safe stop and return-to-previous-branch instructions.
Do not use future placeholders in a ready-to-run file or relabel the existing
M1 commit as an M2/M3 implementation. Avoid committing a file that purports to
contain its own final commit hash: record the tested implementation revision in
a later documentation commit or directly in the Drive file.

Retain local secrets, Docker project identity and volumes between milestones.
Normal stop does not delete data. Later integration/mock code runs only on
explicit invocation, so merely checking out M2/M3 must not populate the empty
M1 UI. No automatic application instrumentation is part of these milestones.

If Drive is unavailable to Codex, produce complete plain-text checklists under
this permanent stage and report upload pending. Do not substitute an invented
Drive link or claim a successful update. A later review can update the existing
Drive files. M1 can be verified now; M2/M3 acceptance waits for implementation.

## Documentation decision record

This user-authorized preparation follows existing charter, principle and tooling/
configuration/adapter boundaries and the observability exploration. The stage
owns implementation instructions and acceptance records; app/docs remains the
guide for already implemented behavior. No runtime, dependencies, personal
examples or guarded files change in this update. The previous full principle
assessment remains applicable; principles 5/6 preserve isolation and external
settings, 7/8 require actual checks, and 12–15 require accurate status and records.
Atlas navigation, milestones, stage entry and progress are updated together.

Preparation verification: 39 relative links across changed Markdown files,
fences and trailing whitespace passed; Atlas build/check passed. All three Drive
files were read back and their Agent Playbook parent folder confirmed. No runtime
test or M2/M3 implementation is claimed by these documentation checks.

