# Proposal: verify the current Langfuse branch in one pass

Status: **Docker usability direction agreed; newcomer requirements requested. Implementation details remain reviewable and execution is paused for joint conflict decisions.**

[Review: four open findings](review-2026-11-13.md) · [Stage entry](README.md)

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

Proposed entry point: a small standard-library helper at
`app/tooling/observability/manage.py`. **These are proposed commands, not commands
available at the reviewed SHA:**

```sh
python3 app/tooling/observability/manage.py start
python3 app/tooling/observability/manage.py status
python3 app/tooling/observability/manage.py logs
python3 app/tooling/observability/manage.py stop
```

| Action | Proposed behavior |
|---|---|
| `start` | Check Docker/Compose; on Mac, start installed Docker Desktop if needed and wait within a bound. Create private deployment settings only if missing, quietly validate Compose, start/apply configuration, wait for readiness, and print the correct UI URL. Running it again is safe. |
| `status` | Show the stack's service state, endpoint and readiness without starting anything or dumping configuration/secrets. |
| `logs` | Show a bounded tail for this stack; allow selecting a service for diagnosis. Do not print private configuration or authorization headers; treat underlying service logs as private. |
| `stop` | Stop this stack while preserving its settings and persistent volumes. Leave Docker Desktop and unrelated containers alone. Use `start` to run it again. |

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
| Host Python and application tools | Keep the helper standard-library-only and compatible with the existing bootstrap prerequisite, Python 3.10+. The application itself currently requires Python 3.13 and pins uv 0.13.6; use the existing bootstrap to provision its environment. Starting the UI must not require installing CrewAI or the Langfuse Python SDK. Reconfirm these values after integrating main. |
| Langfuse and storage images | Link to the exact versions/digest in the checked-out `compose.yaml`; keep them pinned. The helper must not silently upgrade the stack or use floating `latest` images. |

In the final public version table, distinguish a **tested combination**, a
**candidate awaiting platform verification**, and a **minimum requirement**.
Only claim a minimum if supported by the helper's actual features and checks.
Do not force an upgrade/downgrade of an existing working Docker installation
solely to match the candidate above. Refresh download/version links before
handoff; report a still-unverified Mac combination honestly.

The management script is a required deliverable, not a set of commands left for
newcomers to assemble. Keep one implementation for `start`, `stop`, `status` and
`logs`, with `--help` explaining each action and nonzero exits for operational
failures. `start` reuses the existing secret initializer and handles first use
and later runs. It may launch installed Docker Desktop on Mac, but must never
download/install Docker or change global Docker settings automatically. Do not
make the ordinary application bootstrap start Langfuse implicitly. Additional
thin launchers are justified only if needed for a verified platform; avoid a
collection of scripts with duplicated lifecycle logic.

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
| 1 | Install Docker Desktop if missing; run `start` | Services become ready and a UI URL is shown. No hand-written Compose sequence. |
| 2 | Open the UI; sign in or create the local account/project | Project opens. An existing M1 project is reused; an empty list is expected only for a new project. |
| 3 | Use the existing application setup command if needed; supply project API keys once in private local configuration and run the connection checker | Authenticated project access; no trace is created by the check. Copy the exact supported key/config commands into the final guide. |
| 4 | Run the success playground once and open its trace | One synthetic run with nested steps, actual input/output values and timings; delivery verification is explicit. |
| 5 | Change one input; choose a failed step and rerun | Separate run with changed data or an ERROR at the selected step. Earlier runs remain visible. The agent already covers both failure locations. |
| 6 | Run `stop`, then `start`; reopen the project and an earlier trace | Account/project/trace data survives normal stop/start. |

For a **no-mock check**, stop after step 3: this verifies service/UI/authentication.
For the full current PR acceptance, continue through the synthetic trace exercise
and persistence. Normal WF-01/02/03 execution can separately confirm unchanged
application behavior, but it will not produce Langfuse workflow traces until the
later workflow/context integration is implemented. No model call is needed.

Sharon should not have to rerun the agent's whole test suite. His essential work
is the Mac-specific startup/account check and seeing/understanding the traces.
Record his observed acceptance separately from automated evidence. Merging the
PR remains a later explicit decision.

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
