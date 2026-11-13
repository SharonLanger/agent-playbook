# Project structure

Status: **GUARDED.** Existing protection is retained; follow the design contract.

Status: **Approved structure / guarded baseline**. Approved by Sharon before the
pre-Stage 01 refactor. This file governs folder ownership; the target architecture
continues to govern behavior. Future component folders are reserved, not implemented.

## Change rules

Read this file before placing or moving code. Changes to the directory boundaries,
responsibilities, or dependency rules require explaining the logical additions/removals and consequences for each affected guarded file
and obtaining Sharon’s explicit approval before editing; keep an inspectable diff. Ordinary files added within an
existing boundary do not require a new structural approval. Never hide new behavior
inside a folder-only refactor. Keep imports, CLI entry points, PyCharm configurations,
checks, packaging, tests and documentation aligned when a path changes.

This is the current layout authority. The layout in the locked Stage 00 architecture
is historical; it does not override this explicitly approved refactor. Its historical
approval wording and CrewAI acceptance discrepancy are tracked in progress.md.

## Repository and application

| Path | Responsibility |
|---|---|
| `designs/` | Architecture, guarded structure, stage plans and learning records |
| `designs/diagrams/` | Diagram sources, static/animated SVG and viewer |
| `.run/` | Shared portable PyCharm tasks |
| `app/pyproject.toml`, `app/uv.lock` | Package metadata, dependency pins and check configuration |
| `app/application.yaml`, `app/application.local.yaml` | Shared external runtime YAML and ignored machine overrides; user guide in `app/docs/configuration.md` |
| `app/src/agent_playbook/` | Installed runtime Python package |
| `app/tooling/` | Bootstrap, quality checks, version changes, release build and verification |
| `app/examples/` | Sharon’s personal sandbox; no unrequested access/maintenance; excluded from the maintained application boundary |
| `app/examples/workflows/` | Personal sandbox contents; not catalogued, inspected or maintained by agents without a specific request |
| `app/tests/` | Maintained application/tooling tests with independent fixtures; no dependency on personal examples |
| `app/docs/` | Maintained official product documentation; update affected guides/indexes in the same PR; no internal/temporary material |
| `app/dist/` | Generated local releases; ignored by Git |
| `sandbox/` | Historical experiments; outside active application work |

`src` is a packaging boundary. Put application code inside `agent_playbook`,
then inside its owning component. Keep only package entry points and build metadata
at the package root. Tooling is also code, but it is developer code and is not shipped
in the application Wheel. Deployment/CI helpers belong under tooling when introduced;
this refactor creates neither deployment infrastructure nor CI.

## Runtime components

All paths below are relative to `app/src/agent_playbook/`.

| Folder | Ownership | Current contents |
|---|---|---|
| `cli/` | Parse arguments, display outcomes, delegate commands | `parser.py` owns arguments; `commands.py` owns dispatch and presentation; checkout-tooling bridge |
| `application/` | Prepare and execute the selected application run | `assembly.py` initializes integrations; `workflow_factory.py` validates workflow choice and constructs a fresh flow; `workflow_runner.py` coordinates validation, kickoff and result/error normalization; `results.py` owns outcomes |
| `releases/` | Discover and launch completed local releases | `discovery.py` finds a compatible installation; `launcher.py` launches the selected interpreter; CLI owns messages; build logic stays in tooling |
| `config/` | Runtime settings and validation | YAML loader, validation, file selection and CrewAI startup mapping |
| `workflows/` | Named workflow packages with `flow.py`, `state.py`, `steps.py` | Stage 01 sequence, typed-state and conditional-route examples |
| `execution/` | Provider-independent agent execution contracts | Responsibility note |
| `execution/adapters/` | Separate SDK/provider implementations | Responsibility note |
| `observability/` | Provider-neutral events, correlation and redaction | Responsibility note |
| `observability/adapters/` | Exporters such as Langfuse | Responsibility note |

Create named workflows and provider subfolders as their stages introduce them.
Do not create speculative classes or empty implementations. Keep each workflow's
state and steps with that workflow rather than in global `models` or `utils` folders.

## Dependency rules

- CLI delegates execution to the workflow runner or release discovery/launcher; it owns no workflow logic.
- The workflow runner calls assembly before the factory imports a selected flow. Assembly owns
  integration setup; the factory owns construction; the runner owns execution and result/error handling.
- Release discovery does not start a process; the launcher does not select a release or print messages.
  Neither module imports the application runner. Launching a release crosses an interpreter boundary.
- Workflows own routing/state and invoke execution contracts; provider clients stay in adapters.
- Observability events are provider-neutral; only exporters depend on backend clients.
- Runtime modules must not import checkout-only tooling or learning examples.
- The CLI's development bridge may invoke checks, version and release scripts in `app/tooling/` as subprocesses
  only in a development checkout. Installed releases reject all developer commands clearly.
- Tooling may invoke the application CLI. Building a release and selecting a release
  are separate responsibilities.

```mermaid
flowchart TD
    CLI[CLI] --> APP[Application assembly and runner]
    CLI --> REL[Release discovery and launcher]
    CLI -. Development checkout .-> TOOLS[Tooling subprocess]
    APP --> WF[Workflows]
    APP --> CFG[Runtime configuration]
    WF --> EXEC[Execution contracts]
    EXEC --> SDK[SDK adapters]
    APP --> OBS[Observability]
    OBS --> EXPORT[Export adapters]
```

The graph expresses ownership and intended runtime flow; execution/observability
integrations remain future work. Stage 01 adds external integration configuration; future provider contracts remain deferred.

## Compatibility and validation

Preserve `agent-playbook` and `python -m agent_playbook.cli`, including `run`,
`run --version`, `dev-run`, `version`, `test`, and `check`. Preserve the direct
`python -m agent_playbook` entry point. Update shared Setup/Release paths to tooling.
Tests mirror runtime component folders and separately cover tooling. The maintained target excludes the personal examples sandbox; track implementation of exclusion separately from this ownership rule.
Validate the full local gate, clean bootstrap, wheel contents and isolated release
execution after structural moves. macOS PyCharm execution of changed paths requires local confirmation by Sharon.



## Permanent design ownership

| Path | Responsibility |
|---|---|
| `designs/AGENTS.md` | Mandatory design instructions, explicitly loaded from root instructions |
| `designs/governance/design-contract.md` | Guarded change/placement/maintenance contract |
| `designs/governance/guarded-files.md` | Minimum guarded-file register; existing protection is never silently removed |
| `designs/atlas/` | Permanent generated Current/Explorations viewer, catalog, builder, diagrams and viewing instructions |
| `designs/explorations/` | Indexed non-binding research, alternatives, POCs and unresolved discussions |
| `designs/refactors/` | Refactor-specific rationale, approval/review records and verification |
| `designs/stages/` | Permanent stage contracts, lessons and evidence; existing guards retained |

The Atlas is maintained from canonical Markdown and a navigation catalog. It does not authorize candidate folders. Reviewer/event-adapter/harness details are discoverable explorations, not additions to the approved runtime file tree.

## Accepted runtime structure

PR #34 was accepted and merged at `96cb1f8`. The current paths above include the application assembly/factory/runner split, release discovery/launcher split, extracted CLI parser and app-root YAML. Personal examples are excluded from default application tests, types, lint, formatting and release source inputs; explicit manual sandbox lint/format remains possible on request.

The earlier [runtime proposal](refactors/2026-11-12-runtime-structure/proposal.md) preserves optional role/harness/tool thinking; consult the exploration index before extending it. Those candidate paths are not approved implementation contracts. The temporary Verify Refactor task/helper are removed with Sharon's approval; standard application check/test commands remain the maintained verification entry points.
