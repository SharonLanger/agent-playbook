# Verification before handing a milestone to Sharon

Status: **Requested implementation/handoff requirement; no checks below are claimed as executed by this documentation update.**
[Milestones](milestones.md) · [Milestone 1 implementation brief](implementation-handoff.md)

## Working rule

The implementing agent does the practical verification available in its environment
before asking Sharon to test. Fix observed failures and rerun the affected checks.
Do not hand over configuration/code that has only been written or syntax-checked
when an actual execution is feasible.

Sharon does the small human-facing actions: open the UI, create his personal
account/project, confirm what he sees and experiment. Do not build a large browser
test framework merely to automate a few clicks. Prefer existing tools and small,
bounded checks; do not turn this stage into an infrastructure test platform.

Inspect available Docker/Compose, network access, platform and resources before
claiming live checks are unavailable. If blocked, record the attempted command,
specific reason and remaining local check. Do not spend disproportionate effort
adding cloud infrastructure, bypassing restrictions or reproducing Sharon's whole
machine to automate a trivial manual action. Complete independent checks anyway.
A skipped live check is unverified, not passed.

## Agent checks by milestone

| Milestone | Required practical verification before handoff | Small task left to Sharon |
|---|---|---|
| 1: local service | Validate resolved Compose quietly; check required settings, image pins, port bindings and persistent-volume declarations. Start the actual stack if supported; wait with a deadline for service readiness, inspect relevant service failures and request the UI page. Perform a normal stop/start without deleting volumes, then check readiness again. Test the documented start/stop instructions. | Open the UI, create his account/project, confirm the empty trace list; confirm the project survives a normal restart if no disposable project was used in the agent check. |
| 2: connection | Test settings parsing, missing/invalid settings, disabled/no-network mode and sanitized errors. With a live service, run valid authentication plus rejected authentication and unreachable-service cases using isolated test configuration. Confirm meaningful results/exit statuses and that the checker does not create traces. | Supply his own local project keys and run the already-verified checker once. Negative cases need not be repeated unless environment differences warrant it. |
| 3: playground | In the explicitly authorized new Langfuse example, run the default success scenario and deliberate failure at add and multiply. Confirm normal and failed observations, stopped downstream work, distinct run IDs and the returned trace links. Where live access is available, read back the observations to check structure/values; a flush is insufficient. Check the maintained integration separately with independent fixtures. | Open the traces, understand the UI, change the inputs/failing step and explore freely. |
| 4: real workflow | After its separate design review, run real success/failure paths, lifecycle/correlation tests, repeated-run isolation and the selected telemetry-outage behavior. Regress existing workflow results and current quality checks. | Run a normal workflow locally and inspect its trace. |

For M1, a service restart and a declared volume are not proof that an application
record survived. If feasible, use a disposable verification account/project in an
isolated instance and confirm its persistence. Otherwise explicitly leave the
short project-persistence check to Sharon. Never claim that account creation,
authentication, trace ingestion or the browser UI was verified solely from an
HTTP 200 response. Report exactly what the page/readiness probe establishes.

Keep normal application checks independent of Docker or a running Langfuse server.
Run the existing quality gate when maintained Python/runtime/tooling changes
require it. Validate Compose/deployment changes with their own checks. Run relevant
documentation links and Atlas build/check. Rebuild/retest release artifacts only
when packaging, installed behavior or dependency changes justify it. Explain any
not-applicable checks rather than generating busywork tests.

## Scope of the example smoke run

Sharon requested creation and verification of the Langfuse playground. During its
implementation, the agent may perform a targeted manual smoke run of that example.
This is not pytest discovery, coverage, an application gate or a release input.

Do not inspect or run `app/examples/workflows/` or other personal examples.
Do not add tests that read/import/execute `app/examples/langfuse/`. Maintained tests
own their fixtures under `app/tests/`. Preserve any later personal edits; use
explicit scenario options or an isolated copy of the authorized new example when
needed for a smoke run. Do not mass-format the sandbox.

Once the requested example is delivered, future access remains limited to specific
user requests. Its personal ownership does not remove the initial obligation to
check the new script before delivering it.

## Evidence and readiness

For each checkpoint, record in permanent stage findings (with a short PR summary):

| Field | Required record |
|---|---|
| Revision | Commit tested and any later changes that invalidate the result |
| Environment | OS/architecture, relevant tool/SDK/image versions; identify Linux-versus-Mac limits |
| Check | Exact executable command or concise reproducible procedure |
| Result | PASS / FAIL / BLOCKED / NOT RUN / NOT APPLICABLE, with observed output summary |
| Limitation | Specific missing capability or unverified behavior; no guessed success |
| User action | Only the remaining short local exercise, expected output and normal stop command |

Use these distinct handoff statuses:

- **Ready for Sharon's acceptance:** relevant available checks passed; remaining
  actions are the stated local/UI acceptance checks.
- **Ready for local verification, with limitations:** static/offline checks passed,
  but a material live check was blocked; name it prominently.
- **Not ready:** an observed failure remains unresolved.

Do not say everything is verified when only configuration validation ran. Also do
not require exhaustive tests of Langfuse itself: test our setup, configuration,
integration and the documented happy path plus selected useful failure cases.

## Short local handoff

Give Sharon the branch/revision, exact commands from the repository root, URL,
expected visible result and how to stop safely. Avoid dumping internal logs or
asking him to debug routine configuration mistakes the agent could reproduce.
Infrastructure restart checks preserve volumes; never reset his instance or
delete his data. Keep test credentials and resolved secret values out of commits,
logs, screenshots and the evidence record.
