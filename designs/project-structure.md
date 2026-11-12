# Project structure

Status: **Approved structure / guarded baseline**. Approved by Sharon before the
pre-Stage 01 refactor. This file governs folder ownership; the target architecture
continues to govern behavior. Future component folders are reserved, not implemented.

## Change rules

Read this file before placing or moving code. Changes to the directory boundaries,
responsibilities, or dependency rules require presenting the exact proposed diff
and obtaining Sharon's approval before editing. Ordinary files added within an
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
| `app/configs/` | Shared external runtime YAML and ignored machine overrides; user guide in `app/docs/configuration.md` |
| `app/src/agent_playbook/` | Installed runtime Python package |
| `app/tooling/` | Bootstrap, quality checks, version changes, release build and verification |
| `app/examples/` | Learning exercises; excluded from the installed package |
| `app/examples/workflows/` | Eight self-contained workflow sandboxes; each owns its run.py, input, settings, tests and diagrams |
| `app/tests/` | Tests grouped by component, plus tooling and examples; workflow sandbox tests also live beside their examples |
| `app/docs/` | User-facing operating guides; index in `README.md`, CLI/build/release in `cli.md`, runtime settings in `configuration.md` |
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
| `cli/` | Parse arguments, display outcomes, delegate commands | Console/module entry points; checkout-tooling bridge |
| `application/` | Prepare and execute the selected application run | `runner.py` validates configuration/input and invokes a fresh selected workflow |
| `releases/` | Discover and launch completed local releases | `selection.py`; build logic stays in tooling |
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

- CLI delegates execution to application and release selection; it owns no workflow logic.
- The application layer assembles workflows and integrations using runtime configuration.
- Workflows own routing/state and invoke execution contracts; provider clients stay in adapters.
- Observability events are provider-neutral; only exporters depend on backend clients.
- Runtime modules must not import checkout-only tooling or learning examples.
- The CLI's development bridge may invoke checks, version and release scripts in `app/tooling/` as subprocesses
  only in a development checkout. Installed releases reject all developer commands clearly.
- Tooling may invoke the application CLI. Building a release and selecting a release
  are separate responsibilities.

```mermaid
flowchart TD
    CLI[CLI] --> APP[Application runner]
    CLI --> REL[Release selection]
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
Tests mirror runtime component folders and separately cover tooling and examples.
Validate the full local gate, clean bootstrap, wheel contents and isolated release
execution after structural moves. macOS PyCharm execution of changed paths requires local confirmation by Sharon.

