# Proposal: verify the current Langfuse branch in one pass

Status: **Main conflict resolutions approved and applied; remaining Langfuse/CLI implementation is next. See the reconciliation record for verification and remaining issues.**

[Review: four open findings](review-2026-11-13.md) · [Stage entry](README.md)

**Codex: first read [main-reconciliation.md](main-reconciliation.md), then the
[implementation handoff](#codex-implementation-handoff). The six recorded
conflicts have been agreed and reconciled. Start steps 2–5 when Sharon supplies
the implementation instruction; only new conflicts require another decision.**

Requested on 2026-11-13. Planning starts from PR #36 head
`5bfcb889215d000d76629c3d4198d33bea99398d`; inspected main is
`53764abeb9402d596ee26bef19872fc2ebd7d888`.

## Goal and scope

Give Sharon one short, copyable acceptance guide for the final tested state of
the current PR. No switching among old milestone commits during normal manual
verification. Keep the original checkpoint SHAs and evidence as history.

The existing UI, connection checker and mock playground are implemented, but
the review found delivery defects. Fix and verify them before asking Sharon to
judge the trace UI. Real CrewAI workflow/context integration remains a separate,
later change; its prerequisite refactor is now on main. No Claude/Codex runtime,
general log platform or full CLI doctor is introduced by this plan.

Sharon agreed with the simple Docker start/stop and verification direction, then
requested explicit newcomer documentation, installation/version requirements
and the scripts needed to make setup easy. This update records those requirements
only. The main update remains the first execution step, with conflict choices
discussed before any resolutions. No script implementation or conflict resolution
is authorized to bypass that discussion. Wider trace-delivery follow-up remains
as proposed below; Docker-only verification comes first in the manual exercise.

Sharon subsequently selected `agent-playbook langfuse --start`-style flags,
including `--follow` for logs, and requested this Codex handoff before starting.
The CLI clarification was recorded from PR head
`c8640a8d95dcfc0e823d7495488725d4ac0138b6`; main remained at the SHA above.

The instructions below preserve the original plan. Step 1 is now completed as
recorded in the reconciliation document; earlier statements about waiting on
these six conflict choices are superseded by that dated update. Other scope and
verification requirements remain in force.

## Execution order after agreement

### 1. Update from main, resolving conflicts together

Refresh both branch heads and the common ancestor first. Present every conflict
with a short explanation of what main adds, what the PR adds, and the proposed
combined result. The current six-file preview is recorded under review R2.

**Stop for Sharon's decisions before applying resolutions.** Agreement to this
plan is not blanket authorization to choose conflict resolutions. Do not use an
automatic ours/theirs choice or discard either branch's work. Do not resolve
generated HTML independently of its source metadata.

After the choices are agreed, integrate main into the existing PR branch,
preserving workflow lifecycle/configuration changes, strict YAML, lazy imports,
current package version/lock consistency and both histories. Rebuild Atlas from
the agreed sources. Run the combined baseline checks and distinguish pre-existing
review defects from new integration regressions. Keep the PR draft and unmerged.

### 2. Fix trace delivery and honest result reporting

Resolve R1's connection/tracing resource lifetime and R3's misleading submission
message. Keep implementation inside the existing config/adapter/tooling owners.

Add small maintained tests with the actual pinned SDK and independent HTTP
fixtures: successful preflight followed by an export in the same process, and
rejected export without a false delivery-success result. Verify disabled mode
still makes no connection. Tests belong under `app/tests/` and must not consume
the personal example. Use the specifically requested Langfuse playground only
for its targeted manual smoke/learning exercise; leave other examples alone.

Define bounded readback or a supported export-result check. A mock calculation
passing, the exporter accepting a batch and the server returning the trace are
three different observations. Report rejected, unconfirmed and verified states
accurately. Do not silently retry a whole mock run and create duplicate traces.

### 3. Make local operation one command

Keep the existing pinned Compose definition and prebuilt images. A Dockerfile
builds an image; it does not replace the coordination of Langfuse's web, worker,
database, queue and storage services. No custom image build is needed here.

The agreed public interface is a `langfuse` command with **double-dash action
flags**. These commands are specified for implementation; they are **not yet
available** at the reviewed revision:

```sh
agent-playbook langfuse --start
agent-playbook langfuse --stop
agent-playbook langfuse --status
agent-playbook langfuse --logs
agent-playbook langfuse --logs --follow
agent-playbook langfuse --open
agent-playbook langfuse --check
agent-playbook langfuse --help
```

| Action | Required behavior |
|---|---|
| `--start` | Check Docker/Compose; on Mac, start installed Docker Desktop if needed and wait within a bound. Create private deployment settings only if missing, quietly validate Compose, start/apply configuration, wait for readiness, and print the correct UI URL. Running it again is safe. |
| `--stop` | Stop this stack while preserving its settings and persistent volumes. Leave Docker Desktop and unrelated containers alone. Use `--start` to run it again. |
| `--status` | Show this stack's service state, UI URL and readiness. Distinguish stopped, starting, unhealthy and ready. Do not start services or authenticate to a project. |
| `--logs` | Show a bounded recent tail of this stack's Docker service logs. `--follow` streams new lines until interrupted. Do not print private configuration or authorization headers; underlying service logs remain private. |
| `--open` | Print the effective local UI URL and open it in the default browser. Do not start services, collect traces or require project keys. If the browser cannot open, keep the URL visible and report the failure clearly. |
| `--check` | Reuse the maintained application-config/project-authentication check. Report disabled as skipped, not success. Do not start Docker, emit a trace or claim ingestion from authentication. This can target a configured hosted endpoint without local Docker. |

#### CLI contract and ownership

- Require exactly one of the six action flags. Reject no action, multiple actions
  such as `--start --stop`, unknown options, and `--follow` without `--logs`
  before invoking Docker, configuration writes, SDK calls or browser actions.
- `--help` succeeds without Docker, keys or side effects. Do not introduce
  positional action aliases or `--info`/`--observe` aliases in this change.
- Preserve the existing checker's `--config PATH` selector for `--check`; reject
  it with unrelated actions. Preserve explicit `--env-file PATH` for local
  deployment actions, with the adjacent private `.env` as the default. The two
  files have different owners; do not interpret deployment secrets as project
  keys. Resolve caller-supplied relative paths before a subprocess changes cwd.
- Use exit 0 for a completed action or ready status, 1 for operational failure or
  non-ready status, and 2 for invalid invocation/configuration. Preserve exit 3
  for a disabled/skipped connection check. A successful `--stop` against an
  already stopped/absent stack is safe; an unreachable engine is not proof of a
  successful stop. Ctrl-C during `--logs --follow` ends the log stream, not the
  containers; report the normal interruption status without a traceback.
- Docker logs describe services. The UI displays traces that were actually sent.
  Neither `--logs` nor `--open` enables workflow instrumentation. Keep root
  `agent-playbook check` as the existing application quality gate; it is distinct
  from `agent-playbook langfuse --check`.

Keep the CLI thin: `cli/parser.py` owns public arguments, `cli/commands.py` owns
dispatch/presentation, and `cli/development.py` uses the existing subprocess
bridge to checkout-only tooling. A standard-library management helper at
`app/tooling/observability/manage.py` owns Docker/process/browser operations;
project authentication stays in the existing connection checker and adapter.
The bridge currently defaults unrecognized developer commands to `checks.py`:
add an explicit Langfuse mapping rather than relying on that fallback.

For this scope, the CLI is a **development-checkout command**. Preserve the
existing clear exit-2 rejection when invoked from an installed release without
checkout tooling. Do not ship deployment assets in the runtime wheel, import
tooling from the runtime package, eagerly initialize Langfuse, or load CrewAI
flows merely to use management/help commands. Status and connection checks may
later be reused by doctor #37; do not implement a doctor framework now.

Direct script use remains a documented fallback, using the same action flags:

```sh
python3 app/tooling/observability/manage.py --start
python3 app/tooling/observability/manage.py --status
python3 app/tooling/observability/manage.py --logs --follow
python3 app/tooling/observability/manage.py --stop
```

Keep Docker operations standard-library-only so this fallback can start the UI
before the application environment is installed. The public CLI requires the
existing application bootstrap/entry point. `--check` requires that application
environment; delegate to its maintained checker rather than reimplementing
authentication or installing SDK packages implicitly. Document the exact Python
invocation for the check after bootstrap. Share management behavior between CLI
and script; do not maintain two lifecycle implementations.

First use still requires installing Docker Desktop. The helper should clearly
explain missing installation, unavailable engine, occupied ports, startup timeout
and service failures. Use bounded waits with progress output; no endless polling.
It must not install software or change Docker's global settings automatically.

Reuse the existing deployment directory/project identity, including existing M1
volumes. Preserve the current private `.env` and credentials across runs; never
reset data or rotate secrets as an ordinary start/stop action. Keep configurable
ports and explicit private environment-file support. Resolve deployment paths
from the helper location, so internals do not depend on the caller's directory.
Keep application project keys separate from deployment credentials.

The helper delegates to Compose; it is not a new deployment framework, CLI doctor
or application startup hook. Agent Playbook must still run while Langfuse is
stopped. Choosing a hosted endpoint later remains an application configuration
change; this local helper stays optional.

#### Newcomer setup documentation and script requirements

Deliver a complete first-use path alongside the helper, not just an internal
design or a Drive checklist. Use the existing guides instead of creating a
second competing installation manual:

| File | Required implementation-time change |
|---|---|
| `README.md` and `app/README.md` | Link the optional local Langfuse setup from the application setup section. Explain that Docker is needed for local Langfuse, not ordinary workflow execution or a hosted Langfuse endpoint. |
| `app/docs/langfuse-local.md` | Canonical newcomer guide: prerequisites/downloads, version table, first launch, ready-state output, account/project creation, everyday commands, configuration, persistent data and troubleshooting. |
| `app/docs/README.md` and `app/docs/troubleshooting.md` | Make setup discoverable and link actionable Docker/Langfuse troubleshooting to the canonical guide. |
| `app/docs/cli.md` | Document all six action flags, `--follow`, help, configuration selectors, exit meanings and the development-checkout requirement. Distinguish the root quality gate from the Langfuse connection check. |
| `app/tooling/observability/README.md` | Explain the management helper and existing `setup.py`/Compose ownership; link the public guide rather than duplicate the full procedure. |
| `app/docs/langfuse-connection.md` | Continue from a working UI to application bootstrap, project keys and connection verification, then point to the separately requested trace exercise. |

The beginner sequence must say exactly what to install, where to download it,
which directory to run commands from, the command to run, expected output, and
what to do if that step fails. Include Apple silicon versus Intel selection,
supported macOS requirements, first Docker Desktop launch/permissions, a stated
resource budget, and first-start image-download/network/disk requirements.
Distinguish Docker being installed from its engine being ready; the missing
Docker socket in Sharon's screenshot is a case the guide/helper must explain.
Do not require a separate local PostgreSQL, ClickHouse, Redis or MinIO install.

Record versions precisely without inventing compatibility evidence:

| Component | Design input and publication rule |
|---|---|
| Docker Desktop for Mac | Official release notes checked 2026-11-13 list **4.99.0**, released 2026-11-09. This is a candidate installation baseline, **not a project-tested Mac version**. Before the final guide, recheck availability and record the version actually used for the acceptance exercise. |
| Bundled Docker Engine / Compose plugin | That Desktop release lists **Engine 29.9.3** and **Compose 5.7.0**. Use the bundled `docker compose` plugin; no separate legacy `docker-compose` install. Record actual detected versions and test results. Earlier Linux Engine 29.9.2 / Compose 2.40.3 evidence does not establish Mac support. |
| Host Python and application tools | Keep the Docker management helper standard-library-only and compatible with the existing bootstrap prerequisite, Python 3.10+. The application currently requires Python 3.13 and pins uv 0.13.6; use the existing bootstrap to provision the CLI/check environment. The direct script must support UI-only startup without CrewAI or the Langfuse Python SDK. Reconfirm these values after integrating main. |
| Langfuse and storage images | Link to the exact versions/digest in the checked-out `compose.yaml`; keep them pinned. The helper must not silently upgrade the stack or use floating `latest` images. |

In the final public version table, distinguish a **tested combination**, a
**candidate awaiting platform verification**, and a **minimum requirement**.
Only claim a minimum if supported by the helper's actual features and checks.
Do not force an upgrade/downgrade of an existing working Docker installation
solely to match the candidate above. Refresh download/version links before
handoff; report a still-unverified Mac combination honestly.

The management script is a required deliverable, not a set of commands left for
newcomers to assemble. Keep one management implementation behind the six agreed
CLI actions, with `--help` explaining each action and nonzero exits for operational
failures. `--start` reuses the existing secret initializer and handles first use
and later runs. It may launch installed Docker Desktop on Mac, but must never
download/install Docker or change global Docker settings automatically. Do not
make the ordinary application bootstrap start Langfuse implicitly. Additional
thin launchers are justified only if needed for a verified platform; avoid a
collection of scripts with duplicated lifecycle logic.

Lead with CLI commands in the guides. From a fresh checkout, show the existing
`python3 app/tooling/bootstrap.py` command, then either activate `app/.venv` or
use `app/.venv/bin/agent-playbook` explicitly. Do not assume a global executable
or create shell aliases automatically. Explain the direct management-script
fallback for someone who only wants to open Langfuse before installing the app.

Require a fresh-checkout walkthrough before handoff: no existing generated
deployment `.env`, no project keys for UI-only startup, explicit prerequisites,
and the documented single start command. Also verify an existing M1 installation
keeps its private settings, project identity and volumes. Repeated start, stop
when already stopped, and start after stop must be safe. Leave account/project
clicks and final Mac UI acceptance to Sharon; report any agent-side live blocker.

Official references checked for this documentation proposal:
[Docker Mac installation](https://docs.docker.com/desktop/setup/install/mac-install/),
[Docker Desktop 4.99.0 release notes](https://docs.docker.com/desktop/release-notes/#4990),
and [Langfuse local Compose deployment](https://langfuse.com/self-hosting/deployment/docker-compose).
These are upstream requirements/release evidence, not project acceptance results.

### 4. Agent verification and documentation before handoff

Do the practical checks before handing Sharon another checklist:

- Combined branch: locked environment, Pyright, Ruff and maintained tests;
  preserve main's built-in/alias/failure checks and release verification where
  changed packaging/configuration affects it. Do not rely on the old 133 count.
- Helper: missing/stopped engine, stable paths/project identity, repeated setup,
  preserved private settings, port configuration, bounded readiness failure and
  non-destructive stop/start. Mock subprocess boundaries in offline unit tests;
  use actual Docker for live claims.
- CLI: all six dispatch paths, argument validation before side effects,
  `--logs --follow` interruption, selected config/environment-file paths across
  cwd changes, browser failure, disabled check exit 3, installed-release
  rejection, and unchanged root commands. Help and Docker-only management must
  not initialize an exporting SDK client or execute a workflow.
- SDK: the independent R1/R3 regressions, connection error handling and sanitized
  diagnostics. Normal application checks must not require a live server.
- When Docker is available: isolated stack startup, real valid/rejected project
  authentication, real success/failure trace readback, changed-port recreation
  and normal stop/start persistence. Use disposable agent-owned data only.
- Smoke-run the specifically requested playground's success and two selected
  failure cases separately from the maintained suite. Verify inputs, hierarchy,
  error status and absence of later successful steps after a deliberate failure.

If a live check is blocked, report the exact blocker and leave it unverified.
Loopback HTTP fixtures prove SDK behavior, not Langfuse ingestion or Mac behavior.
Do not add expensive browser automation merely to replace Sharon's few clicks.

Correct R4's stale current-status prose without rewriting historical evidence or
altering guarded meaning. Update the official local/connection guides for actual
supported commands, stage records, navigation and Atlas. Add a prominent pointer
from the old per-milestone verification instructions to the new combined guide
once it exists; retain their original SHAs and results as history.

### 5. One short manual acceptance guide for Sharon

Create one new text file in Google Drive's **Agent Playbook** folder after the
implementation is tested. Link it from the existing verification files so the
three older checklists are clearly historical. Include the exact final tested
SHA, branch update instructions, required working directory, copyable commands,
expected output and a short recovery instruction for each likely local blocker.
Do not overwrite private local settings or changes during checkout/update.
If the branch moves after testing, either verify the new revision or keep the
guide pinned to its tested SHA; never call an untested moving head verified.

Proposed manual order, all on that same revision:

| Order | Sharon does | Visible acceptance |
|---|---|---|
| 1 | Install Docker Desktop if missing; prepare the application CLI as documented (or choose the direct-script fallback); run `--start` | Services become ready and a UI URL is shown. No hand-written Compose sequence. |
| 2 | Run `--open`; sign in or create the local account/project | Project opens. An existing M1 project is reused; an empty list is expected only for a new project. |
| 3 | Supply project API keys once in private local configuration and run `--check` | Authenticated project access; no trace is created by the check. Copy the exact supported key/config commands into the final guide. |
| 4 | Run the success playground once and open its trace | One synthetic run with nested steps, actual input/output values and timings; delivery verification is explicit. |
| 5 | Change one input; choose a failed step and rerun | Separate run with changed data or an ERROR at the selected step. Earlier runs remain visible. The agent already covers both failure locations. |
| 6 | Run `--stop`, then `--start`; reopen the project and an earlier trace | Account/project/trace data survives normal stop/start. |

For a **no-mock check**, stop after step 3: this verifies service/UI/authentication.
For the full current PR acceptance, continue through the synthetic trace exercise
and persistence. Normal WF-01/02/03 execution can separately confirm unchanged
application behavior, but it will not produce Langfuse workflow traces until the
later workflow/context integration is implemented. No model call is needed.

Sharon should not have to rerun the agent's whole test suite. His essential work
is the Mac-specific startup/account check and seeing/understanding the traces.
Record his observed acceptance separately from automated evidence. Merging the
PR remains a later explicit decision.

## Codex implementation handoff

### Entry, current state and authority

Work on **PR #36**, branch `docs/stage-02-langfuse-setup`, in
`SharonLanger/agent-playbook`. Keep this PR draft and unmerged. Do not create a
replacement PR, rewrite branch history, discard local work or revert main's
package version to the older version still on this branch.

This document records agreed CLI direction and the implementation specification;
it was requested **before starting work**. Unless Sharon has separately asked
you to execute it, read it and discuss the next step. Once execution is requested,
the first task is a fresh main/branch comparison and conflict presentation.
**Do not resolve conflicts or proceed to implementation until Sharon has agreed
on the conflict choices.** Record that agreement and the exact main SHA used.
Any fresh conflict discovered later must also be surfaced. Nothing in this
handoff authorizes an automatic PR merge.

Read in this order, using actual files at the fetched revisions:

1. Root `AGENTS.md`, `designs/AGENTS.md`, the design contract/guard register and
   their required core documents. Preserve personal-sandbox boundaries.
2. This plan and [the four findings](review-2026-11-13.md), including the actual
   SDK reproductions and six-file conflict inventory. Do not infer delivery
   correctness from the earlier 133-test pass.
3. Stage [architecture](architecture.md), [verification](verification.md),
   [implementation evidence](findings.md) and relevant observability exploration.
   Old milestone SHAs are historical; the combined acceptance approach and CLI
   spelling in this plan supersede their separate-checkout instructions for the
   new handoff. Existing approved boundaries and all four review items remain.
4. Main's merged workflow-contract design and current code before integrating
   shared configuration. Refresh after the merge. Do not start M4 just because
   its prerequisite refactor has merged.

At the recorded starting point: M1 deployment, M2 connection and M3 example code
exist; `manage.py` and the `langfuse` CLI command **do not**. No Mac UI acceptance
has been reported. Review R1 (real SDK lifecycle), R2 (main integration), R3
(false submission success) and R4 (stale status) are all open. Docker was not
available in the review environment; previous implementation live checks also
hit Docker storage exhaustion. These are limitations to reassess, not a reason
to skip checks that your execution environment can now perform.

### Implementation map and constraints

| Owner | Work and limits |
|---|---|
| `app/src/agent_playbook/cli/parser.py`, `commands.py`, `development.py` | Add the six mutually exclusive action flags, help/options and explicit tooling dispatch. Preserve existing run/dev-run/check/release behavior and source-checkout restrictions. |
| `app/tooling/observability/manage.py` | Implement local lifecycle/readiness/status/log/browser management. Reuse `setup.py` and existing Compose assets; use argument-list subprocess calls without shell interpolation. Only `--start` may initialize missing deployment settings or start installed Docker Desktop. |
| `app/tooling/observability/check_connection.py` | Reuse the existing configuration/check interface and exit meanings. Allow `--check` to work without local Docker. Do not duplicate SDK authentication in the CLI or helper. |
| `app/src/agent_playbook/config/` | Preserve main's strict YAML, workflow registry and selected configuration behavior while retaining Langfuse settings. Do not create a competing config loader. |
| `app/src/agent_playbook/observability/adapters/langfuse/` | Resolve SDK resource ownership and delivery reporting using the pinned SDK's real behavior. No workflow/context wiring or global automatic instrumentation. |
| `app/tests/cli/`, `app/tests/tooling/`, `app/tests/observability/` | Independent maintained fixtures and meaningful regression tests. Normal checks need no Docker, project keys or network service. No dependency on examples. |
| Existing public docs and Stage 02 records | Update supported commands alongside implementation, record exact evidence and unresolved limits, rebuild Atlas, and preserve historical findings. |

Keep Docker project identity stable so an existing M1 user's volumes stay
visible. Resolve the selected ports and URL consistently with Compose and its
environment-file/override rules. Do not rotate credentials, rename the project,
run volume deletion/pruning, or touch unrelated containers as a convenience
fix. No destructive reset action is part of this scope. Preserve prebuilt pinned
images; a custom Dockerfile is not a deliverable.

Do not add real agents, workflow contexts, event/harness abstractions, general
application logging, cloud migration, recovery or CLI doctor. `--logs` means
Docker service logs; `--open` means the UI; `--check` means authenticated project
access. They are not automatic instrumentation. Preserve provider isolation and
keep configuration/key values out of command output, trace metadata and evidence.

Access to the specifically requested `app/examples/langfuse/` is limited to
review-directed corrections and explicit smoke runs needed for this task. Do
not access other personal examples. Never make maintained tests, application
checks, bootstrap or release inputs import, scan or run personal examples.

### Verification and stopping conditions

Complete each applicable check and record PASS, FAIL, BLOCKED or NOT RUN, with
command, source SHA, environment, expected observation and actual result:

| Gate | Required evidence |
|---|---|
| A — integration | Exact main SHA and agreed conflict choices; both branches' intended behavior preserved; Atlas regenerated from reconciled sources. |
| B — CLI | Real parser/dispatch exercised for all six actions. Invalid combinations and help cause no external side effects. Config/env paths survive spaces and cwd changes. Existing commands and installed-release rejection remain correct. |
| C — lifecycle | Offline tests cover actionable missing/stopped-engine errors, ready/unhealthy/timeout states, first/repeated start, non-destructive stop, effective ports/URL, browser failure and log follow interruption. Ensure failure tests actually observe the prohibited operation, not only a returned message. |
| D — actual SDK | Same-process project preflight followed by a real export request; rejected export cannot claim verified delivery. Use an independent local HTTP fixture and actual pinned SDK, not a fake client or the personal example. Reproduce failures before the fix or record an equivalent negative control. |
| E — combined application | Run the maintained quality gate on the reconciled implementation. Preserve main's workflow/alias/failure verification; validate wheel isolation and checkout-only tooling behavior when packaging/CLI changes affect them. Earlier test counts are not targets. |
| F — live and example | Where supported, run actual stack/authentication/export/readback and normal stop/start persistence checks against disposable agent-owned data. Separately smoke the requested example's success and two deliberate failures. Trace URLs or flush returns alone are not delivery proof. |
| G — handoff | Working guide commands, help text, version evidence, links/Atlas and the final Drive checklist agree with the exact tested revision. Report the remaining simple Mac/UI tasks. |

The existing full-gate entry point from the repository root is
`app/.venv/bin/python app/tooling/checks.py check`; verify it against the merged
checkout. The Atlas check is `python3 designs/atlas/build.py --check`. Use the
repository's existing runtime/release verification tools after reading their
current instructions. Do not replace meaningful tests with assertions that only
mirror implementation, or expand testing beyond the changes without a reason.

If Docker, disk, network or Mac access blocks a check, record the observed
limitation. Do not represent static Compose validation, mocked subprocesses or
an HTTP fixture as a live Langfuse/Mac result. Preserve local data; do not clean
up user volumes to unblock your environment. Pause on unresolved design conflicts
or required guarded logical changes and explain the specific decision needed.

### Final delivery to Sharon

Update this stage's evidence with fix commits for R1–R4, commands/results and
remaining limitations. Keep the original review as dated evidence; add a linked
resolution record instead of erasing what was reproduced. Update PR #36's body
so it describes the actual final state. Do not mark it accepted or merge it.

Publish the single copyable Drive checklist only after testing the implementation.
Keep the existing [M1](https://drive.google.com/file/d/1ASuYt3GuwGhfnUJW2EvwhJVnKYxv5XEc/view),
[M2](https://drive.google.com/file/d/18AgG1LrCXiag_cHG5QYev0dpwyrhMzoR/view) and
[M3](https://drive.google.com/file/d/1P2nLMatSnBhCBOMUUKpp5PRWzLAYSjvi/view)
files as history and link the new combined guide from them. Use the Agent Playbook
folder; no private keys or generated `.env` contents belong in those documents.
Include the exact tested commit, safe checkout/update instructions, CLI setup,
commands, expected results and remaining manual tasks. Read the saved file back.
If Drive access is unavailable, report it rather than claim delivery.

Keep user updates short and frequent. At completion, say what changed, what was
actually verified, what was blocked, the PR/head, and exactly what Sharon should
try. Avoid another long milestone-by-milestone exercise. The first visible
acceptance remains Docker start/UI/project/stop/start; connection and synthetic
traces follow on the same tested revision. Real workflow traces remain later.

Suggested first instruction for a fresh Codex session:

> Continue PR #36 on docs/stage-02-langfuse-setup. Read repository instructions,
> main-reconciliation.md, the dated review and this complete implementation plan.
> The six approved main conflicts are resolved and verified; do not repeat that
> approval step. Implement steps 2–5: R1/R3 fixes, R4 status correction, the agreed
> helper/CLI, newcomer guides and independent verification. Refresh refs first;
> report any new conflicts to Sharon without resolving them. Keep M4 out of scope
> and PR #36 draft and unmerged. Publish the combined Drive checklist at the final
> tested revision, with honest live/Mac limitations.

## Placement, principles and approval boundary

This permanent proposal and review live with Stage 02; official runnable guides
will stay under `app/docs/`. Proposed helper code stays in checkout-only tooling,
provider details in the Langfuse adapter, and regression fixtures in tests.
No new component boundary or workflow context is approved by this proposal.

| Principles | Application |
|---|---|
| 1, 3 | Plan agreement and collaborative conflict choices before execution; preserve approved architecture. |
| 2, 6 | External endpoints/keys, no secret dumps or automatic credential rotation. |
| 4, 9, 10 | One understandable local exercise; independent workflow integration later. |
| 5 | Keep Langfuse client details behind the adapter; local deployment optional. |
| 7, 8 | Locked dependencies, independent SDK regression evidence, explicit live blockers. |
| 11, 13 | Preserve historical evidence and personal examples; no example-dependent gates. |
| 12, 14, 15 | Permanent review/plan, official guides after implementation, accurate status and Atlas links. |

The observability exploration informs the trace/log distinction, but no logging
backend, event schema, recovery or harness design is adopted. Saving these
documents changes no supported product behavior, so official product guides are
unchanged at this proposal stage. Navigation/progress/Atlas expose the proposal
without presenting it as implemented or accepted. Any later guarded logical
change must be explained and agreed before editing.
