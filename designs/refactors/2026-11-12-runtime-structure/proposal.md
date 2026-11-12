# Agent Playbook — Future Architecture and Refactor Proposal

Date: 12 November 2026  
Status: Design proposal for review; not an implementation or replacement of the guarded baseline.  
Repository: [SharonLanger/agent-playbook](https://github.com/SharonLanger/agent-playbook)  
Inspected baseline: [`6f16508d9f36da66edec04ddb055d8954f0f7c70`](https://github.com/SharonLanger/agent-playbook/tree/6f16508d9f36da66edec04ddb055d8954f0f7c70), after PR #33.

## 1. Recommended direction

Build one modular Python application, organized by responsibility, with explicit contracts and adapters. Keep one application package and release process. Give workflows, agent roles, execution setup, provider adapters, tools, and observability clear owners.

This recommendation follows the intended completed system, not merely the size of Stage 01. The target is a reusable local environment for defining, executing, observing, and testing workflows. CrewAI coordinates workflow transitions; compatible agent executors perform agent work; Langfuse receives correlated execution evidence.

The immediate refactor should:

1. Keep `releases/` and split `selection.py` into `discovery.py` and `launcher.py`.
2. Separate the application layer into `assembly.py`, `workflow_factory.py`, and `workflow_runner.py`, retaining `results.py`.
3. Move the shared configuration to `app/application.yaml` and its optional ignored override to `app/application.local.yaml`.
4. Preserve the existing workflow packages, checkout-only tooling, independent examples, and permanent learning material.

The future structure should additionally give reusable agent roles a home in `agents/`, harness setup in `execution/harnesses/`, custom agent tools in `tools/`, external harness profiles in `app/harnesses/`, and provider-neutral observation logic in `observability/`.

These last additions extend the documented target. Their responsibilities are proposed here; detailed schemas, SDK behavior, and implementations remain decisions for their respective stages.

## 2. What exists, what is documented, and what is new

| Area | State at the inspected baseline | Treatment in this proposal |
|---|---|---|
| CLI, releases, configuration, application runner | Implemented | Refactor ownership and naming while preserving behavior |
| Three integrated CrewAI workflows | Implemented | Retain their separate packages and contracts |
| Eight independent workflow examples | Implemented | Retain their self-contained setup and colocated tests |
| Execution contracts and provider adapters | Responsibilities documented; implementation deferred | Preserve these boundaries and illustrate their eventual files |
| Observability and Langfuse exporter | Responsibilities documented; implementation deferred | Preserve these boundaries and illustrate their eventual files |
| Reusable reviewer/coder roles | No dedicated component in the current target or structure document | Propose `agents/` |
| Harness profiles, shared customization, and custom tool ownership | Not concretely defined; harness engineering remains a future direction | Propose the boundaries described below |
| Exact final filesystem | Not fully specified by the current target architecture | Provide a proposed hierarchy, distinguishing current files from future candidates |

`designs/architecture.md` describes intended system responsibilities. `designs/project-structure.md` is the guarded authority for current placement and dependencies. Neither has been changed by this document. The earlier proposal to move release launching under `cli/` is superseded here by keeping a dedicated `releases/` component.

## 3. Component ownership in the completed system

Runtime paths in this table are relative to `app/src/agent_playbook/`, except paths beginning with `app/`.

| Location | Owns | Boundary |
|---|---|---|
| `cli/` | Arguments, command dispatch, messages, exit statuses | Delegates work; does not own workflow decisions |
| `application/` | Configuration-driven assembly, workflow construction, run lifecycle and outcome | Coordinates components without containing their provider internals |
| `releases/` | Discovery and process launch of completed local installations | Separate from executing a workflow inside the chosen installation |
| `config/` | Reading, resolving and validating external settings; current CrewAI startup mapping | Configuration data remains external to the installed wheel |
| `workflows/<name>/` | Typed workflow state, steps, routes, joins, declared retry/completion rules | CrewAI executes the graph; business decisions remain in the workflow |
| `agents/<role>/` | Role instructions, task preparation, role inputs/results and validation | Uses the execution contract rather than a provider SDK directly |
| `execution/contracts.py` | Provider-independent agent request/outcome and execution interface | Exact types and capability semantics are defined at integration time |
| `execution/harnesses/` | Reusable execution setup, context preparation, tool selection and shared hook policies | Does not implement a second workflow scheduler or assume all providers behave identically |
| `execution/adapters/<provider>/` | Provider invocation, sessions, supported native options and hook translation | SDK-specific behavior stays here |
| `tools/` | Implementations of custom tools available to agents | Separate implementation from tool enablement and provider registration |
| `observability/` | Normalized events, run/step/session correlation and redaction | Provider-neutral evidence; not authoritative workflow state |
| `observability/adapters/langfuse/` | Mapping and exporting observations to Langfuse | Langfuse types and client stay behind this boundary |
| `app/application.yaml` | Shared application settings and eventual profile selections | External runtime settings, not build metadata |
| `app/harnesses/` | External, named harness profiles | Declarative selections; no committed credentials or executable Python |
| `app/tooling/` | Bootstrap, checks, version changes, builds and release verification | Developer code excluded from the application wheel |
| `app/examples/` | Independent learning experiments | Do not make them depend on the integrated application runner |

### Dependencies and decisions

- Application assembly connects implementations to their consumers. Configured choices do not require workflows to import SDK clients.
- A workflow invokes a role and decides what happens after the role returns. A role prepares a request and interprets its result through the execution contract.
- Ordinary Python workflow steps remain ordinary Python; they need not become agents.
- The provider adapter owns session details. The workflow owns its business state. Observation correlates them with the run identity.
- The observation boundary normalizes and redacts evidence before exporter-specific handling.
- Runtime modules do not import checkout-only tooling or independent examples. The existing development CLI bridge may invoke tooling as subprocesses in a checkout.
- New modules must not force CrewAI or agent SDK imports during CLI help, version, release discovery, or developer command dispatch.

## 4. Releases: discover an installation, then launch it

The current `releases/selection.py` combines manifest discovery, selection, presentation, environment preparation, and subprocess execution. Its name only describes part of its behavior.

Keep the dedicated package and separate its responsibilities:

| Proposed file | Responsibility |
|---|---|
| `releases/discovery.py` | Inspect release manifests and installation files; select the requested or newest completed installation; return its executable and version |
| `releases/launcher.py` | Launch a selected installation with the correct arguments, isolated interpreter flags and environment; return the subprocess outcome |
| `cli/commands.py` | Present the selected release or the missing-release message and map the operation to the CLI contract |

Discovery should not print messages or launch a process. Launching should not decide which release is newest. A small value object is reasonable if it clarifies the returned installation metadata; a generic release-management framework is unnecessary.

`app/tooling/release.py` remains responsible for building, installing and verifying releases. The workflow runner operates inside the already selected interpreter and must not search for virtual environments.

### Preserve during the split

- Exact requested-version filtering and the existing newest-installation ordering. The current implementation orders by manifest modification time with a folder-name tie-breaker; it does not select the highest semantic version.
- Existing checks for installation files, incomplete releases, and the manifest's verification field. The current legacy behavior accepts a missing `verified` field; changing that requires a separate behavioral decision.
- Argument boundaries, including JSON and paths with spaces; no shell interpolation.
- Isolated execution using `-I`, removal of `PYTHONPATH` and `PYTHONHOME`, and propagation of the child exit status.
- Explicit configuration and environment precedence, plus the current compatibility mechanism for older releases through environment forwarding.
- The difference between source `run`, which selects an installation, installed `run`, which executes that installation, and `dev-run`, which executes editable source.

Do not silently change error handling or release-selection policy while moving code. Record any desired behavior change separately.

## 5. Application: assembly, factory and runner

These files have separate purposes even though they all participate in one run.

| File | Immediate responsibility | Later responsibility |
|---|---|---|
| `application/assembly.py` | Load validated configuration and apply CrewAI startup settings using the existing configuration code | Select and connect role executors, harness profiles and observation adapters |
| `application/workflow_factory.py` | Choose a workflow, validate its specific input, construct fresh state and a fresh flow | Supply the selected workflow with its required role and integration dependencies |
| `application/workflow_runner.py` | Coordinate preparation, common input handling, execution, failure translation and `RunResult` | Own run identity, overall lifecycle, observation boundaries and final outcome |
| `application/results.py` | Keep the existing immutable result and error contracts | Evolve only when an approved stage needs a concrete change |

Assembly decides which implementations are connected. The factory constructs a particular workflow. The runner controls the application-level lifecycle of one run. CrewAI continues to own workflow scheduling.

### Immediate extraction rules

- Preserve `run_workflow(workflow_id, raw_input, *, config_path=None) -> RunResult` as the callable contract, although its module moves.
- Keep the existing early rejection of unknown workflow IDs and the current validation/error categories.
- Apply validated CrewAI startup settings **before importing CrewAI or workflow modules that import it**. Factory imports must remain appropriately lazy.
- Create fresh flow and state instances per invocation. Do not introduce cached mutable workflow instances.
- Keep the three-workflow selector explicit. A simple selection function is enough; no dynamic plugin discovery, base-class hierarchy, dependency container or second execution engine is required.
- Assembly can initially be a small function using existing settings. Do not add placeholder SDK clients, invented context objects or empty provider abstractions merely to fill the future layout.
- Preserve workflow output formatting and CLI exit behavior through the existing presentation boundary.

## 6. Agent roles: reviewer and coder

A role describes the work and how its outcome is interpreted. It is independent of the compatible provider used to execute it.

Proposed reusable roles:

| File pattern | Responsibility |
|---|---|
| `agents/reviewer/agent.py` | Prepare a review request, invoke the execution contract and validate/interpret findings |
| `agents/reviewer/instructions.md` | Reusable reviewer instructions |
| `agents/reviewer/models.py` | Role-specific input and result types |
| `agents/coder/agent.py` | Prepare an implementation request, invoke execution and interpret the result |
| `agents/coder/instructions.md` | Reusable coder instructions |
| `agents/coder/models.py` | Role-specific input and result types |

For example, a reviewer produces findings. The workflow decides whether those findings require another coding attempt, whether a revision limit has been reached, and which step comes next. The adapter handles SDK invocation and sessions.

If a role is genuinely specific to one workflow, keep it inside that workflow first. Promote it to the shared `agents/` component when reuse is intended. Avoid a common-role framework before concrete shared behavior exists.

Role instructions packaged with the application must be included in the wheel and read as package resources, independently of the caller's working directory. Machine settings and secrets remain external.

## 7. Harness customization and tools

Here, harness customization means configuring and extending an execution environment: available tools, context preparation, hooks and provider-supported settings. It does not imply implementing our own agent loop.

| Concern | Proposed owner |
|---|---|
| Application chooses the role, executor and harness profile | `application/assembly.py` using external configuration |
| Validated profile data and shared setup rules | `execution/harnesses/` |
| Reading and validating profile files | The configuration boundary, with exact loader modules determined during design |
| Shared context preparation and hook behavior | `execution/harnesses/`, only where genuinely reusable |
| Provider-specific hook registration, event payloads and native settings | `execution/adapters/<provider>/` |
| Custom tool implementation | `tools/<tool>.py` or a focused tool package |
| Tool selection, enablement and execution settings | External harness profiles under `app/harnesses/` |
| Provider tool schemas and registration wrappers | The relevant provider adapter |

Illustrative profiles are `app/harnesses/review.yaml` and `app/harnesses/coding.yaml`. Their schemas are not defined or supported today. They might select tool references, hook policies and execution settings, but exact fields and precedence must be designed before implementation.

For example, a reviewer role can use a review profile enabling repository inspection and test execution. Its role instructions define what to review; the profile selects capabilities; the provider adapter applies a supported configuration.

### Important distinctions

- **Tool implementation versus selection:** a custom diff-inspection implementation belongs in `tools/`; the profile selects it. Provider-built-in tools need supported configuration, not copied implementations.
- **Tools versus tooling:** agents invoke `tools/`; developers use `app/tooling/` to bootstrap, check, build and release the project.
- **Shared versus native behavior:** preserve common semantics where possible, and keep provider-specific behavior explicit. An adapter must report unsupported required capabilities rather than silently weakening the requested setup.
- **Role needs versus permission:** a role can declare needed capabilities; its request does not grant itself additional authority. Effective setup must respect the applicable policy and supported execution boundary.
- **MCP declaration versus service implementation:** a profile can refer to external tool services; it does not imply their implementation belongs in this repository. Integrate a service's client or registration details at the relevant boundary when that integration is designed.
- **Configuration versus a new runtime:** replacing a provider's agent loop, compaction system or recovery behavior is a separate executor/harness design, not a configuration-only refactor.

Future filenames in the appendix, such as `profiles.py` and `prepare.py`, illustrate ownership. They do not prescribe a finished hook API or promise identical provider capabilities.

## 8. Configuration placement

Move the currently shared YAML out of the single-file `configs/` directory:

| Current | Proposed |
|---|---|
| `app/configs/application.yaml` | `app/application.yaml` |
| Optional ignored `app/configs/application.local.yaml` | Optional ignored `app/application.local.yaml` |
| `app/src/agent_playbook/config/` | Retained: Python loading and validation code |

One application YAML can group settings for several integrations. More providers do not automatically require more configuration files. Named harness profiles have a specific reusable purpose, so a later `app/harnesses/` folder is compatible with keeping the main application YAML at the application root.

Preserve `--config`, `AGENT_PLAYBOOK_CONFIG`, local overrides, documented environment overrides and startup validation. Update the default path in `config/paths.py`, path-sensitive tests, relevant PyCharm tasks, ignore rules and documentation. Preserve developer-created local overrides during migration; do not overwrite them or commit their values.

Configuration remains outside the installed wheel and versioned release artifacts. Source launches forward the selected external path to an installation. Direct installed invocations continue to require an explicit selector under the existing contract. The location change does not introduce live reload, a settings server or automatic fallback policies.

## 9. Execution and observability in the target

Execution contracts describe provider-independent requests and outcomes. Separate Claude, Codex and deterministic adapters satisfy those contracts only to the extent supported by their capabilities. Native transports and process/language boundaries remain open until their integrations are designed.

The deterministic executor supplies controlled results or failures while the actual workflow still runs its real transitions and branches. It must not replace the workflow with a simulated success path.

Observability owns normalized events, correlation and redaction. The Langfuse adapter maps those observations into its backend representation. Workflow code and role code must not depend on Langfuse-specific client types.

Run IDs, step IDs and agent session references are distinct. Traces correlate them but do not become the authoritative workflow state or control the next step. Telemetry failure policy, flush behavior, payload limits and retention remain explicit integration-stage decisions.

## 10. Concrete refactor plan

The following is a suggested sequence of reviewable changes, not work already performed.

| Step | Change | Completion evidence |
|---|---|---|
| 1. Reconcile design boundaries | Present exact proposed edits to the guarded architecture/structure where required; distinguish immediate refactor from future additions | Reviewed component ownership, dependency rules and retained stage contracts |
| 2. Release split | Extract `releases/discovery.py` and `releases/launcher.py`; move presentation into CLI; retire `selection.py` after updating consumers | Existing selection, forwarding and installed-release behavior preserved |
| 3. Application split | Rename runner; extract assembly and workflow construction; update imports and tests | Existing workflow outputs, input failures, fresh state, startup ordering and exit statuses preserved |
| 4. Configuration move | Move shared YAML to the app root; update default selection, tests, docs and any affected tasks | Source and isolated installed runs use the intended external settings |
| 5. Optional CLI cleanup | Extract argument declarations to `cli/parser.py` only if the separation improves navigation | Identical commands, flags, help and dispatch behavior |

Release construction already has focused functions in `app/tooling/release.py`. Keep them unless a concrete responsibility problem appears. This proposal does not introduce a `ReleaseManager`, global utilities bucket, generic framework or new CI service.

### Move and extraction inventory

| Existing location | Destination or action |
|---|---|
| `releases/selection.py::find_release` | `releases/discovery.py` |
| `releases/selection.py::run_release` | Split process/environment handling into `releases/launcher.py` and presentation into `cli/commands.py` |
| `application/runner.py` | `application/workflow_runner.py` |
| Configuration/startup preparation within the runner | `application/assembly.py`, using existing `config/` functions |
| Workflow-specific construction within the runner | `application/workflow_factory.py` |
| `tests/application/test_runner.py` | `tests/application/test_workflow_runner.py`; divide existing cases further only where meaningful |
| Existing release tests | Keep under `tests/releases/`; update imports and mock boundaries, retaining behavior assertions |
| Shared application YAML and optional override | `app/` root, as described above |
| `cli/commands.py::build_parser` | Optional `cli/parser.py` extraction |

Runtime paths in this table are relative to `app/src/agent_playbook/`; test paths are relative to `app/`.

### Verification required for implementation

- Run the repository's local quality gate: strict typing, linting, formatting and deterministic tests.
- Check source/module/console entry points, `run`, `run --version`, `dev-run`, `version`, `test`, `check`, formatting and release commands.
- Verify fresh-process startup ordering, configuration precedence, workflow inputs/results/failures and isolation between consecutive runs.
- Verify release selection, incomplete/unverified handling, argv preservation and child exit propagation.
- Build from a clean committed snapshot; inspect the wheel for excluded tooling, examples, tests and active configuration; verify installation and workflows in isolation.
- Check release behavior from another working directory, external configuration forwarding and source-edit isolation.
- Update all path-dependent imports, checks, task definitions and documentation links. Test bootstrap where structural path changes affect it; retain separate local macOS/PyCharm confirmation when necessary.
- Preserve the user's version changes; do not introduce or reverse a version bump as a side effect of moving files.

Reuse existing meaningful behavior tests. Add coverage for uncovered risks introduced by an extraction, rather than tests that merely repeat the new file layout.

## 11. What to introduce later

| Work | Timing |
|---|---|
| Observation events, correlation/redaction and Langfuse exporter | Stage 02 design and implementation |
| More complex branching, parallelism and workflow failure policies | Relevant orchestration stage |
| Agent execution contracts and a first concrete adapter | Agent SDK study/integration stages |
| Reusable reviewer/coder roles and deterministic execution | When the corresponding agent workflows are designed |
| Harness profiles, reusable hooks/context setup and custom tool integrations | Explicitly scoped harness/integration work; the current roadmap leaves this open |

Do not create empty implementations of these components in the immediate refactor. Their future paths communicate intended ownership. Existing responsibility notes can remain until approved implementations replace or expand them.

Keep detailed request/result fields, provider capability mapping, cancellation, timeouts, session reuse, tool authorization, bounded retries, idempotency, persistence and resume semantics open until there is enough integration evidence. No exactly-once, crash-recovery or full provider-parity guarantee is implied by this structure.

## 12. Why this structure, rather than the alternatives

| Approach | Fit for the intended project |
|---|---|
| One application, grouped by responsibility, with explicit contracts/adapters | Recommended: preserves local execution and gives reusable components clear ownership |
| Global technical layers such as `interfaces/`, `domain/`, `infrastructure/` | Possible, but scatters each capability across more folders without a demonstrated benefit here |
| Independently packaged runtime, CLI and integrations | Consider when independent consumers, dependency sets or release cycles justify separate packages |

The target explicitly describes logical components within a local application. It does not currently require a REST service, queue service, custom dashboard or independently deployed services. An SDK's necessary process boundary can remain behind its adapter without turning the whole repository into a service monorepo.

The external examples discussed were references for ownership, not templates to copy wholesale:

- [CrewAI contribution guide](https://github.com/crewAIInc/crewAI/blob/main/.github/CONTRIBUTING.md): separate framework, CLI, integration and release-tooling packages.
- [Langfuse contribution guide](https://github.com/langfuse/langfuse/blob/main/CONTRIBUTING.md): separate web/worker applications and shared packages.
- [LangGraph contribution guide](https://github.com/langchain-ai/docs/blob/main/src/oss/contributing/code.mdx): framework, SDK/CLI and checkpoint-interface/implementation packages.
- [Prefect runner source](https://github.com/PrefectHQ/prefect/tree/main/src/prefect/runner): focused runner responsibilities extracted into dedicated modules.

These patterns support separation by responsibility. They do not establish that a large project's package count or deployment topology is appropriate for Agent Playbook.

## 13. Source documents and implementation handoff

The following baseline files were reviewed. Links are pinned to the inspected commit:

- [Target architecture](https://github.com/SharonLanger/agent-playbook/blob/6f16508d9f36da66edec04ddb055d8954f0f7c70/designs/architecture.md)
- [Guarded project structure](https://github.com/SharonLanger/agent-playbook/blob/6f16508d9f36da66edec04ddb055d8954f0f7c70/designs/project-structure.md)
- [Charter](https://github.com/SharonLanger/agent-playbook/blob/6f16508d9f36da66edec04ddb055d8954f0f7c70/designs/charter.md)
- [Engineering principles](https://github.com/SharonLanger/agent-playbook/blob/6f16508d9f36da66edec04ddb055d8954f0f7c70/designs/principles.md)
- [Roadmap](https://github.com/SharonLanger/agent-playbook/blob/6f16508d9f36da66edec04ddb055d8954f0f7c70/designs/roadmap.md)
- [Architecture walkthrough](https://github.com/SharonLanger/agent-playbook/blob/6f16508d9f36da66edec04ddb055d8954f0f7c70/designs/learning/architecture-walkthrough.md)
- [Approved Stage 01 architecture](https://github.com/SharonLanger/agent-playbook/blob/6f16508d9f36da66edec04ddb055d8954f0f7c70/designs/stages/01-crewai-flows/architecture.md)
- [Current release selection](https://github.com/SharonLanger/agent-playbook/blob/6f16508d9f36da66edec04ddb055d8954f0f7c70/app/src/agent_playbook/releases/selection.py)
- [Current application runner](https://github.com/SharonLanger/agent-playbook/blob/6f16508d9f36da66edec04ddb055d8954f0f7c70/app/src/agent_playbook/application/runner.py)
- [Current CLI commands](https://github.com/SharonLanger/agent-playbook/blob/6f16508d9f36da66edec04ddb055d8954f0f7c70/app/src/agent_playbook/cli/commands.py)

Before implementing, refresh the repository state and read applicable repository instructions. Reconcile this proposal with the guarded architecture and structure through their exact-diff approval process. Preserve the approved Stage 01 behavioral contracts, security and external-configuration requirements, learning material, source/release separation and historical sandbox.

This document records the requested proposal. No runtime refactor, protected-document edit, new integration, build or test execution is claimed as completed by writing it.

## Appendix: Complete proposed source hierarchy

The hierarchy below starts from every tracked file at the inspected baseline, applies the proposed moves, and adds clearly marked candidates. It retains historical and learning files so that the proposal does not hide deletions.

- **Existing:** currently tracked; location retained. An existing file may still need import, documentation or configuration-reference updates.
- **Moved / Renamed / Split:** current implementation relocated or separated by the immediate proposal.
- **Extracted:** new file holding existing behavior.
- **Optional:** a discretionary cleanup or a local override, as labeled.
- **Future:** illustrative file placement for a later component, not an existing implementation or a locked schema.
- **Generated:** machine-local output; dependency and release-instance contents are not enumerated.

Future test cases and additional provider-specific files are not knowable yet. Existing tests are fully listed; their future additions should follow the same component ownership when their stages are designed. The future filenames below are a concrete navigation proposal, not a claim that the final system's file list is frozen.

<details>
<summary>Expand the complete proposed hierarchy</summary>

- **`agent-playbook/`**
  - **`.run/`**
    - **`Bump Patch.run.xml`** — Existing
    - **`Check.run.xml`** — Existing
    - **`Dev Run.run.xml`** — Existing
    - **`Format Check.run.xml`** — Existing
    - **`Format.run.xml`** — Existing
    - **`Lint.run.xml`** — Existing
    - **`Release.run.xml`** — Existing
    - **`Run.run.xml`** — Existing
    - **`Setup.run.xml`** — Existing
    - **`Test WF-01.run.xml`** — Existing
    - **`Test WF-02.run.xml`** — Existing
    - **`Test WF-03.run.xml`** — Existing
    - **`Tests.run.xml`** — Existing
    - **`Types.run.xml`** — Existing
    - **`Version.run.xml`** — Existing
    - **`WF-01 Sequence.run.xml`** — Existing
    - **`WF-02 State.run.xml`** — Existing
    - **`WF-03 Route.run.xml`** — Existing
  - **`app/`**
    - **`.venv/`** — Generated. Generated environment; dependency files omitted.
    - **`dist/`** — Generated. Generated local releases; machine-specific contents omitted.
    - **`docs/`**
      - **`cli.md`** — Existing
      - **`configuration.md`** — Existing
      - **`README.md`** — Existing
      - **`troubleshooting.md`** — Existing
      - **`workflows.md`** — Existing
    - **`examples/`**
      - **`workflows/`**
        - **`ex_01_step_sequence/`**
          - **`.gitignore`** — Existing
          - **`diagram-animated.svg`** — Existing
          - **`diagram.html`** — Existing
          - **`diagram.svg`** — Existing
          - **`flow.py`** — Existing
          - **`input.json`** — Existing
          - **`README.md`** — Existing
          - **`run.py`** — Existing
          - **`settings.py`** — Existing
          - **`settings.toml`** — Existing
          - **`test_ex_01.py`** — Existing
          - **`THIRD-PARTY-NOTICES.txt`** — Existing
        - **`ex_02_method_completion/`**
          - **`.gitignore`** — Existing
          - **`diagram-animated.svg`** — Existing
          - **`diagram.html`** — Existing
          - **`diagram.svg`** — Existing
          - **`flow.py`** — Existing
          - **`input.json`** — Existing
          - **`README.md`** — Existing
          - **`run.py`** — Existing
          - **`settings.py`** — Existing
          - **`settings.toml`** — Existing
          - **`test_ex_02.py`** — Existing
          - **`THIRD-PARTY-NOTICES.txt`** — Existing
        - **`ex_03_router_labels/`**
          - **`.gitignore`** — Existing
          - **`diagram-animated.svg`** — Existing
          - **`diagram.html`** — Existing
          - **`diagram.svg`** — Existing
          - **`flow.py`** — Existing
          - **`input.json`** — Existing
          - **`README.md`** — Existing
          - **`run.py`** — Existing
          - **`settings.py`** — Existing
          - **`settings.toml`** — Existing
          - **`test_ex_03.py`** — Existing
          - **`THIRD-PARTY-NOTICES.txt`** — Existing
        - **`ex_04_name_collision/`**
          - **`.gitignore`** — Existing
          - **`diagram-animated.svg`** — Existing
          - **`diagram.html`** — Existing
          - **`diagram.svg`** — Existing
          - **`flow.py`** — Existing
          - **`input.json`** — Existing
          - **`README.md`** — Existing
          - **`run.py`** — Existing
          - **`settings.py`** — Existing
          - **`settings.toml`** — Existing
          - **`test_ex_04.py`** — Existing
          - **`THIRD-PARTY-NOTICES.txt`** — Existing
        - **`ex_05_revision_loop/`**
          - **`.gitignore`** — Existing
          - **`diagram-animated.svg`** — Existing
          - **`diagram.html`** — Existing
          - **`diagram.svg`** — Existing
          - **`flow.py`** — Existing
          - **`input.json`** — Existing
          - **`README.md`** — Existing
          - **`run.py`** — Existing
          - **`settings.py`** — Existing
          - **`settings.toml`** — Existing
          - **`test_ex_05.py`** — Existing
          - **`THIRD-PARTY-NOTICES.txt`** — Existing
        - **`ex_06_nested_conditions/`**
          - **`.gitignore`** — Existing
          - **`diagram-animated.svg`** — Existing
          - **`diagram.html`** — Existing
          - **`diagram.svg`** — Existing
          - **`flow.py`** — Existing
          - **`input.json`** — Existing
          - **`README.md`** — Existing
          - **`run.py`** — Existing
          - **`settings.py`** — Existing
          - **`settings.toml`** — Existing
          - **`test_ex_06.py`** — Existing
          - **`THIRD-PARTY-NOTICES.txt`** — Existing
        - **`ex_07_chained_routers/`**
          - **`.gitignore`** — Existing
          - **`diagram-animated.svg`** — Existing
          - **`diagram.html`** — Existing
          - **`diagram.svg`** — Existing
          - **`flow.py`** — Existing
          - **`input.json`** — Existing
          - **`README.md`** — Existing
          - **`run.py`** — Existing
          - **`settings.py`** — Existing
          - **`settings.toml`** — Existing
          - **`test_ex_07.py`** — Existing
          - **`THIRD-PARTY-NOTICES.txt`** — Existing
        - **`ex_08_persisted_routing/`**
          - **`.gitignore`** — Existing
          - **`diagram-animated.svg`** — Existing
          - **`diagram.html`** — Existing
          - **`diagram.svg`** — Existing
          - **`flow.py`** — Existing
          - **`input.json`** — Existing
          - **`README.md`** — Existing
          - **`run.py`** — Existing
          - **`settings.py`** — Existing
          - **`settings.toml`** — Existing
          - **`test_ex_08.py`** — Existing
          - **`THIRD-PARTY-NOTICES.txt`** — Existing
        - **`README.md`** — Existing
      - **`README.md`** — Existing
      - **`typing_example.py`** — Existing
    - **`harnesses/`**
      - **`coding.yaml`** — Future. Illustrative external coding profile; not a supported schema yet.
      - **`review.yaml`** — Future. Illustrative external review profile; not a supported schema yet.
    - **`src/`**
      - **`agent_playbook/`**
        - **`agents/`**
          - **`coder/`**
            - **`__init__.py`** — Future
            - **`agent.py`** — Future. Implementation task preparation, execution-contract invocation and result validation.
            - **`instructions.md`** — Future. Reusable role instructions; packaged resource.
            - **`models.py`** — Future. Role-specific request/result types.
          - **`reviewer/`**
            - **`__init__.py`** — Future
            - **`agent.py`** — Future. Review task preparation, execution-contract invocation and result validation.
            - **`instructions.md`** — Future. Reusable role instructions; packaged resource.
            - **`models.py`** — Future. Role-specific request/result types.
          - **`__init__.py`** — Future
        - **`application/`**
          - **`__init__.py`** — Existing
          - **`assembly.py`** — Extracted. Now: configuration and CrewAI startup. Later: integration and harness assembly.
          - **`results.py`** — Existing
          - **`workflow_factory.py`** — Extracted. Choose and construct a fresh workflow.
          - **`workflow_runner.py`** — Renamed; from `app/src/agent_playbook/application/runner.py`
        - **`cli/`**
          - **`__init__.py`** — Existing
          - **`__main__.py`** — Existing
          - **`commands.py`** — Existing
          - **`development.py`** — Existing
          - **`parser.py`** — Optional. Argument declarations extracted from commands.py.
        - **`config/`**
          - **`__init__.py`** — Existing
          - **`crewai.py`** — Existing
          - **`errors.py`** — Existing
          - **`loader.py`** — Existing
          - **`models.py`** — Existing
          - **`paths.py`** — Existing
          - **`README.md`** — Existing
        - **`execution/`**
          - **`adapters/`**
            - **`claude/`**
              - **`__init__.py`** — Future
              - **`executor.py`** — Future. Claude invocation and session lifecycle; transport remains undecided.
            - **`codex/`**
              - **`__init__.py`** — Future
              - **`executor.py`** — Future. Codex invocation and session lifecycle; transport remains undecided.
            - **`deterministic/`**
              - **`__init__.py`** — Future
              - **`executor.py`** — Future. Controlled results and failures for workflow regression tests.
            - **`__init__.py`** — Future
            - **`README.md`** — Existing
          - **`harnesses/`**
            - **`hooks/`**
              - **`README.md`** — Future. Placement for shared hook policies when reuse is demonstrated; native hooks stay in adapters.
            - **`__init__.py`** — Future
            - **`prepare.py`** — Future. Reusable context and capability preparation.
            - **`profiles.py`** — Future. Validated setup/profile concepts; exact schema deferred.
          - **`__init__.py`** — Future
          - **`contracts.py`** — Future. Provider-independent requests, outcomes and execution interface; exact fields deferred.
          - **`README.md`** — Existing
        - **`observability/`**
          - **`adapters/`**
            - **`langfuse/`**
              - **`__init__.py`** — Future
              - **`exporter.py`** — Future. Map observations to Langfuse; outage policy deferred.
            - **`__init__.py`** — Future
            - **`README.md`** — Existing
          - **`__init__.py`** — Future
          - **`contracts.py`** — Future. Provider-neutral observation/export boundary.
          - **`correlation.py`** — Future. Associate run, step and agent-session identities.
          - **`events.py`** — Future. Normalized execution observations.
          - **`README.md`** — Existing
          - **`redaction.py`** — Future. Remove sensitive information before export.
        - **`releases/`**
          - **`__init__.py`** — Existing
          - **`discovery.py`** — Split; from `app/src/agent_playbook/releases/selection.py`
          - **`launcher.py`** — Extracted. Process launch and environment forwarding from selection.py; CLI owns presentation.
        - **`tools/`**
          - **`__init__.py`** — Future
          - **`inspect_diff.py`** — Future. Illustrative custom tool for inspecting a target repository diff.
          - **`run_checks.py`** — Future. Illustrative custom tool for target-project checks; distinct from application developer tooling.
        - **`workflows/`**
          - **`wf_01_step_sequence/`**
            - **`__init__.py`** — Existing
            - **`flow.py`** — Existing
            - **`steps.py`** — Existing
          - **`wf_02_shared_state/`**
            - **`__init__.py`** — Existing
            - **`flow.py`** — Existing
            - **`state.py`** — Existing
            - **`steps.py`** — Existing
          - **`wf_03_conditional_route/`**
            - **`__init__.py`** — Existing
            - **`flow.py`** — Existing
            - **`state.py`** — Existing
            - **`steps.py`** — Existing
          - **`__init__.py`** — Existing
          - **`README.md`** — Existing
        - **`__init__.py`** — Existing
        - **`__main__.py`** — Existing
        - **`_build_info.py`** — Existing
    - **`tests/`**
      - **`application/`**
        - **`README.md`** — Existing
        - **`test_offline_runtime.py`** — Existing
        - **`test_workflow_runner.py`** — Renamed; from `app/tests/application/test_runner.py`
      - **`cli/`**
        - **`test_cli.py`** — Existing
        - **`test_workflow_commands.py`** — Existing
      - **`config/`**
        - **`README.md`** — Existing
        - **`test_configuration.py`** — Existing
      - **`examples/`**
        - **`test_greeting.py`** — Existing
      - **`execution/`**
        - **`README.md`** — Existing
      - **`fixtures/`**
        - **`offline.yaml`** — Existing
      - **`observability/`**
        - **`README.md`** — Existing
      - **`releases/`**
        - **`test_release_selection.py`** — Existing
        - **`test_workflow_launch.py`** — Existing
      - **`tooling/`**
        - **`test_cli_tasks.py`** — Existing
        - **`test_development.py`** — Existing
        - **`test_release_completion.py`** — Existing
        - **`test_release_dependencies.py`** — Existing
        - **`test_release_destination.py`** — Existing
        - **`test_release_preflight.py`** — Existing
        - **`test_toolchain.py`** — Existing
        - **`test_wheel_hash.py`** — Existing
      - **`workflows/`**
        - **`wf_01_step_sequence/`**
          - **`__init__.py`** — Existing
          - **`test_flow.py`** — Existing
          - **`test_steps.py`** — Existing
        - **`wf_02_shared_state/`**
          - **`__init__.py`** — Existing
          - **`test_flow.py`** — Existing
          - **`test_state.py`** — Existing
          - **`test_steps.py`** — Existing
        - **`wf_03_conditional_route/`**
          - **`__init__.py`** — Existing
          - **`test_flow.py`** — Existing
          - **`test_state.py`** — Existing
          - **`test_steps.py`** — Existing
        - **`__init__.py`** — Existing
        - **`conftest.py`** — Existing
        - **`README.md`** — Existing
      - **`__init__.py`** — Existing
      - **`conftest.py`** — Existing
      - **`README.md`** — Existing
    - **`tooling/`**
      - **`__init__.py`** — Existing
      - **`bootstrap.py`** — Existing
      - **`checks.py`** — Existing
      - **`README.md`** — Existing
      - **`release.py`** — Existing
      - **`toolchain.py`** — Existing
      - **`verify_runtime.py`** — Existing
      - **`verify_wheel.py`** — Existing
      - **`version.py`** — Existing
    - **`.gitignore`** — Existing
    - **`.python-version`** — Existing
    - **`application.local.yaml`** — Optional local file. Ignored local override; migrate existing local values carefully.
    - **`application.yaml`** — Moved; from `app/configs/application.yaml`
    - **`pyproject.toml`** — Existing
    - **`README.md`** — Existing
    - **`uv.lock`** — Existing
  - **`designs/`**
    - **`diagrams/`**
      - **`01-system.animated.svg`** — Existing
      - **`01-system.svg`** — Existing
      - **`02-execution.animated.svg`** — Existing
      - **`02-execution.svg`** — Existing
      - **`03-observability.animated.svg`** — Existing
      - **`03-observability.svg`** — Existing
      - **`AUTHORING.md`** — Existing
      - **`build_viewer.py`** — Existing
      - **`index.html`** — Existing
      - **`README.md`** — Existing
      - **`render.py`** — Existing
    - **`learning/`**
      - **`architecture-walkthrough.md`** — Existing
      - **`README.md`** — Existing
    - **`stages/`**
      - **`00-environment/`**
        - **`learning/`**
          - **`00-1-python-environment.md`** — Existing
          - **`00-2-application-cli.md`** — Existing
          - **`00-3-pyright.md`** — Existing
          - **`00-4-pytest.md`** — Existing
          - **`00-5-ruff.md`** — Existing
          - **`00-6-unified-checks.md`** — Existing
          - **`00-7-wheel-release.md`** — Existing
        - **`architecture.md`** — Existing
        - **`findings.md`** — Existing
        - **`plan.md`** — Existing
      - **`01-crewai-flows/`**
        - **`diagrams/`**
          - **`00-architecture-animated.svg`** — Existing
          - **`00-architecture.html`** — Existing
          - **`00-architecture.svg`** — Existing
          - **`01-sequence-animated.svg`** — Existing
          - **`01-sequence.html`** — Existing
          - **`01-sequence.svg`** — Existing
          - **`02-state-animated.svg`** — Existing
          - **`02-state.html`** — Existing
          - **`02-state.svg`** — Existing
          - **`03-route-pass-animated.svg`** — Existing
          - **`03-route-pass.html`** — Existing
          - **`03-route-pass.svg`** — Existing
          - **`04-route-needs-work-animated.svg`** — Existing
          - **`04-route-needs-work.html`** — Existing
          - **`04-route-needs-work.svg`** — Existing
          - **`index.html`** — Existing
          - **`README.md`** — Existing
          - **`THIRD-PARTY-NOTICES.txt`** — Existing
        - **`learning/`**
          - **`00-reading-the-code.md`** — Existing
          - **`01-flow-basics.md`** — Existing
          - **`02-sequence-and-values.md`** — Existing
          - **`03-typed-state.md`** — Existing
          - **`04-routing.md`** — Existing
          - **`05-failures-and-tests.md`** — Existing
          - **`06-running-and-releasing.md`** — Existing
          - **`08-independent-sandboxes.md`** — Existing
        - **`workflows/`**
          - **`wf-01-step-sequence.md`** — Existing
          - **`wf-02-shared-state.md`** — Existing
          - **`wf-03-conditional-route.md`** — Existing
        - **`architecture.md`** — Existing
        - **`configuration-findings.md`** — Existing
        - **`coordination.md`** — Existing
        - **`file-structure.md`** — Existing
        - **`findings.md`** — Existing
        - **`plan.md`** — Existing
        - **`README.md`** — Existing
        - **`sources.md`** — Existing
        - **`test-plan.md`** — Existing
    - **`architecture.md`** — Existing
    - **`charter.md`** — Existing
    - **`principles.md`** — Existing
    - **`progress.md`** — Existing
    - **`project-structure.md`** — Existing
    - **`README.md`** — Existing
    - **`roadmap.md`** — Existing
  - **`sandbox/`**
    - **`agents/`**
      - **`code-writer.md`** — Existing
      - **`designer.md`** — Existing
      - **`orchestrator.md`** — Existing
      - **`replanner.md`** — Existing
      - **`reviewer.md`** — Existing
      - **`tester.md`** — Existing
    - **`projects/`**
      - **`agent-playbook/`**
        - **`features/`**
          - **`f-01-reviewer-trial/`**
            - **`design.md`** — Existing
          - **`f-02-implementer-handoff/`**
            - **`design.md`** — Existing
          - **`f-03-design-deviations/`**
            - **`design.md`** — Existing
      - **`project-a/`**
        - **`reviews/`**
          - **`pr-14.md`** — Existing
        - **`review-rules.md`** — Existing
      - **`system-one-harness/`**
        - **`features/`**
          - **`f-01-offline-test-suite/`**
            - **`design.md`** — Existing
        - **`reviews/`**
          - **`pr-46.md`** — Existing
    - **`verification/`**
      - **`reviewer-handoff.md`** — Existing
    - **`workflows/`**
      - **`implement-change.md`** — Existing
    - **`AGENTS.md`** — Existing
    - **`README.md`** — Existing
  - **`.gitignore`** — Existing
  - **`AGENTS.md`** — Existing
  - **`README.md`** — Existing

</details>
