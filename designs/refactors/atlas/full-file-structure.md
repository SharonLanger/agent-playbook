# Candidate file structure

The PR #34 snapshot provides runtime context. Personal examples contents are intentionally excluded; `app/examples/` is an opaque boundary. Existing examples tests are excluded from the maintained target. This inventory is a future proposal, not current main.

| Path | Status | Responsibility |
|---|---|---|
| `.gitignore` | PR baseline | Retained repository or application configuration/documentation. |
| `.run/Bump Patch.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/Check.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/Dev Run.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/Format Check.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/Format.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/Lint.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/Release.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/Run.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/Setup.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/Test WF-01.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/Test WF-02.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/Test WF-03.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/Tests.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/Types.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/Verify Refactor.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/Version.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/WF-01 Sequence.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/WF-02 State.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `.run/WF-03 Route.run.xml` | PR baseline | Shared PyCharm run configuration. |
| `AGENTS.md` | PR baseline | Retained repository or application configuration/documentation. |
| `README.md` | PR baseline | Retained repository or application configuration/documentation. |
| `app/.gitignore` | PR baseline | Retained repository or application configuration/documentation. |
| `app/.python-version` | PR baseline | Retained repository or application configuration/documentation. |
| `app/README.md` | PR baseline | Retained repository or application configuration/documentation. |
| `app/application.local.yaml` | Generated / illustrative | Optional ignored local override; not committed. |
| `app/application.yaml` | PR baseline | External shared runtime settings relocated by PR #34. |
| `app/dist/<version>/<package>.whl` | Generated / illustrative | Illustrative generated wheel path; actual version and layout follow release tooling. |
| `app/dist/<version>/<release-metadata>` | Generated / illustrative | Illustrative release metadata artifact, not a source file. |
| `app/docs/README.md` | PR baseline | User-facing operating guide. |
| `app/docs/cli.md` | PR baseline | User-facing operating guide. |
| `app/docs/configuration.md` | PR baseline | User-facing operating guide. |
| `app/docs/troubleshooting.md` | PR baseline | User-facing operating guide. |
| `app/docs/workflows.md` | PR baseline | User-facing operating guide. |
| `app/examples/` | Excluded sandbox | Personal sandbox boundary only. Do not inspect contents without a specific request. |
| `app/pyproject.toml` | PR baseline | Retained repository or application configuration/documentation. |
| `app/src/agent_playbook/__init__.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/__main__.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/_build_info.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/agents/README.md` | Proposed | Shared role ownership and provider-neutral boundary. |
| `app/src/agent_playbook/agents/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/agents/coder/README.md` | Proposed | Coder role contract and capability requirements. |
| `app/src/agent_playbook/agents/coder/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/agents/coder/agent.py` | Proposed | Orchestrate one coding task using the execution contract. |
| `app/src/agent_playbook/agents/coder/context.py` | Proposed | Prepare coding scope and context references. |
| `app/src/agent_playbook/agents/coder/event_handler.py` | Proposed | React to canonical events for coding; no native SDK imports. |
| `app/src/agent_playbook/agents/coder/instructions.md` | Proposed | Stable coding role rules. |
| `app/src/agent_playbook/agents/coder/models.py` | Proposed | Typed coding inputs, evidence and domain results. |
| `app/src/agent_playbook/agents/coder/prompts/system.md` | Proposed | Coder prompt resource. |
| `app/src/agent_playbook/agents/coder/tools.py` | Proposed | Role-specific deterministic operations when needed; reuse shared runtime tools. |
| `app/src/agent_playbook/agents/coder/validation.py` | Proposed | Validate coding output and required evidence. |
| `app/src/agent_playbook/agents/contracts.py` | Proposed | Only shared role concepts used by more than one role. |
| `app/src/agent_playbook/agents/reviewer/README.md` | Proposed | Reviewer role contract and capability requirements. |
| `app/src/agent_playbook/agents/reviewer/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/agents/reviewer/agent.py` | Proposed | Orchestrate one review task using the execution contract. |
| `app/src/agent_playbook/agents/reviewer/context.py` | Proposed | Prepare review scope and context references. |
| `app/src/agent_playbook/agents/reviewer/event_handler.py` | Proposed | React to canonical events for review; no native SDK imports. |
| `app/src/agent_playbook/agents/reviewer/instructions.md` | Proposed | Stable review role rules. |
| `app/src/agent_playbook/agents/reviewer/models.py` | Proposed | Typed review inputs, evidence and domain results. |
| `app/src/agent_playbook/agents/reviewer/prompts/system.md` | Proposed | Reviewer prompt resource. |
| `app/src/agent_playbook/agents/reviewer/tools.py` | Proposed | Role-specific deterministic operations when needed; reuse shared runtime tools. |
| `app/src/agent_playbook/agents/reviewer/validation.py` | Proposed | Validate review output and required evidence. |
| `app/src/agent_playbook/agents/verifier/README.md` | Proposed | Verifier role contract and capability requirements. |
| `app/src/agent_playbook/agents/verifier/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/agents/verifier/agent.py` | Proposed | Orchestrate one verification task using the execution contract. |
| `app/src/agent_playbook/agents/verifier/context.py` | Proposed | Prepare verification scope and context references. |
| `app/src/agent_playbook/agents/verifier/event_handler.py` | Proposed | React to canonical events for verification; no native SDK imports. |
| `app/src/agent_playbook/agents/verifier/instructions.md` | Proposed | Stable verification role rules. |
| `app/src/agent_playbook/agents/verifier/models.py` | Proposed | Typed verification inputs, evidence and domain results. |
| `app/src/agent_playbook/agents/verifier/prompts/system.md` | Proposed | Verifier prompt resource. |
| `app/src/agent_playbook/agents/verifier/tools.py` | Proposed | Role-specific deterministic operations when needed; reuse shared runtime tools. |
| `app/src/agent_playbook/agents/verifier/validation.py` | Proposed | Validate verification output and required evidence. |
| `app/src/agent_playbook/application/__init__.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/application/assembly.py` | PR baseline | Dependency construction split out by PR #34. |
| `app/src/agent_playbook/application/results.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/application/workflow_factory.py` | PR baseline | Selected workflow construction split out by PR #34. |
| `app/src/agent_playbook/application/workflow_runner.py` | PR baseline | Run lifecycle split out by PR #34. |
| `app/src/agent_playbook/cli/__init__.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/cli/__main__.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/cli/commands.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/cli/development.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/cli/parser.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/config/README.md` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/config/__init__.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/config/crewai.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/config/errors.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/config/loader.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/config/models.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/config/paths.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/execution/README.md` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/execution/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/execution/adapters/README.md` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/execution/adapters/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/execution/adapters/claude/README.md` | Proposed | Claude transport choice, mapping rules and capability gaps. |
| `app/src/agent_playbook/execution/adapters/claude/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/execution/adapters/claude/capabilities.py` | Proposed | Version/transport-specific supported features and limits. |
| `app/src/agent_playbook/execution/adapters/claude/controls.py` | Proposed | Translate supported permission, input or cancellation controls. |
| `app/src/agent_playbook/execution/adapters/claude/event_mapper.py` | Proposed | Translate native messages with required mapping state. |
| `app/src/agent_playbook/execution/adapters/claude/executor.py` | Proposed | Claude native invocation, consumption and cleanup. |
| `app/src/agent_playbook/execution/adapters/claude/request_mapper.py` | Proposed | Map our request to native runtime options. |
| `app/src/agent_playbook/execution/adapters/claude/tool_bindings.py` | Proposed | Expose runtime tools to this provider when introduced. |
| `app/src/agent_playbook/execution/adapters/codex/README.md` | Proposed | Codex transport choice, mapping rules and capability gaps. |
| `app/src/agent_playbook/execution/adapters/codex/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/execution/adapters/codex/capabilities.py` | Proposed | Version/transport-specific supported features and limits. |
| `app/src/agent_playbook/execution/adapters/codex/controls.py` | Proposed | Translate supported permission, input or cancellation controls. |
| `app/src/agent_playbook/execution/adapters/codex/event_mapper.py` | Proposed | Translate native messages with required mapping state. |
| `app/src/agent_playbook/execution/adapters/codex/executor.py` | Proposed | Codex native invocation, consumption and cleanup. |
| `app/src/agent_playbook/execution/adapters/codex/request_mapper.py` | Proposed | Map our request to native runtime options. |
| `app/src/agent_playbook/execution/adapters/codex/tool_bindings.py` | Proposed | Expose runtime tools to this provider when introduced. |
| `app/src/agent_playbook/execution/adapters/codex/transport.py` | Proposed | Own the selected Codex SDK/process protocol; selection deferred to experiment. |
| `app/src/agent_playbook/execution/adapters/deterministic/README.md` | Proposed | Deterministic executor behavior and limits. |
| `app/src/agent_playbook/execution/adapters/deterministic/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/execution/adapters/deterministic/executor.py` | Proposed | Offline execution using canonical fixtures. |
| `app/src/agent_playbook/execution/capabilities.py` | Proposed | Capability profiles and requirement compatibility. |
| `app/src/agent_playbook/execution/contracts.py` | Proposed | Provider-neutral executor and live invocation interfaces. |
| `app/src/agent_playbook/execution/errors.py` | Proposed | Execution-level errors and unsupported feature reporting. |
| `app/src/agent_playbook/execution/events.py` | Proposed | Canonical event envelope and discriminated payload union. |
| `app/src/agent_playbook/execution/harness/README.md` | Proposed | Provisional shared-policy boundary; internal files deferred. |
| `app/src/agent_playbook/execution/requests.py` | Proposed | Instructions, output requirements, limits and required capabilities. |
| `app/src/agent_playbook/execution/results.py` | Proposed | Technical outcomes, output, usage and typed failure details. |
| `app/src/agent_playbook/execution/service.py` | Proposed | Preflight and local invocation coordination; not another model loop. |
| `app/src/agent_playbook/observability/README.md` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/observability/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/observability/adapters/README.md` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/observability/adapters/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/observability/adapters/langfuse/README.md` | Proposed | Exporter behavior and outage policy. |
| `app/src/agent_playbook/observability/adapters/langfuse/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/observability/adapters/langfuse/exporter.py` | Proposed | Langfuse client integration. |
| `app/src/agent_playbook/observability/adapters/noop.py` | Proposed | Offline no-op exporter. |
| `app/src/agent_playbook/observability/contracts.py` | Proposed | Telemetry sink interface. |
| `app/src/agent_playbook/observability/correlation.py` | Proposed | Relate run, step, execution and provider-session references. |
| `app/src/agent_playbook/observability/events.py` | Proposed | Telemetry records; does not duplicate execution AgentEvent. |
| `app/src/agent_playbook/observability/projection.py` | Proposed | Convert workflow, role and execution facts into telemetry. |
| `app/src/agent_playbook/observability/redaction.py` | Proposed | Payload filtering and retention policy. |
| `app/src/agent_playbook/releases/__init__.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/releases/discovery.py` | PR baseline | Completed-release discovery split out by PR #34. |
| `app/src/agent_playbook/releases/launcher.py` | PR baseline | Selected-release launch split out by PR #34. |
| `app/src/agent_playbook/tools/README.md` | Proposed | Runtime tools, distinct from developer tooling. |
| `app/src/agent_playbook/tools/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/tools/contracts.py` | Proposed | Typed tool definitions and invocation boundaries. |
| `app/src/agent_playbook/tools/repository/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/tools/repository/read_diff.py` | Proposed | Read repository changes as a reusable deterministic operation. |
| `app/src/agent_playbook/tools/verification/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/tools/verification/models.py` | Proposed | Typed verification command evidence. |
| `app/src/agent_playbook/tools/verification/run_tests.py` | Proposed | Capture test process outcome and artifacts directly. |
| `app/src/agent_playbook/workflows/README.md` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/workflows/__init__.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/workflows/policies/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/workflows/policies/retry.py` | Proposed | Shared retry policy only once real cross-workflow reuse exists. |
| `app/src/agent_playbook/workflows/wf_01_step_sequence/__init__.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/workflows/wf_01_step_sequence/flow.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/workflows/wf_01_step_sequence/steps.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/workflows/wf_02_shared_state/__init__.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/workflows/wf_02_shared_state/flow.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/workflows/wf_02_shared_state/state.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/workflows/wf_02_shared_state/steps.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/workflows/wf_03_conditional_route/__init__.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/workflows/wf_03_conditional_route/flow.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/workflows/wf_03_conditional_route/state.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/workflows/wf_03_conditional_route/steps.py` | PR baseline | Existing runtime package source or responsibility note. |
| `app/src/agent_playbook/workflows/wf_code_review/README.md` | Proposed | Illustrative future workflow; identifier subject to stage approval. |
| `app/src/agent_playbook/workflows/wf_code_review/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/workflows/wf_code_review/artifacts.py` | Proposed | Workflow-specific artifact naming and references. |
| `app/src/agent_playbook/workflows/wf_code_review/flow.py` | Proposed | CrewAI transitions through coding, review, bounded revision and report. |
| `app/src/agent_playbook/workflows/wf_code_review/inputs.py` | Proposed | Public workflow input validation. |
| `app/src/agent_playbook/workflows/wf_code_review/routing.py` | Proposed | Decide the next step from validated domain results. |
| `app/src/agent_playbook/workflows/wf_code_review/state.py` | Proposed | Typed workflow state and outcomes. |
| `app/src/agent_playbook/workflows/wf_code_review/steps/__init__.py` | Proposed | Python package marker; no behavior. |
| `app/src/agent_playbook/workflows/wf_code_review/steps/code.py` | Proposed | Invoke coder from this workflow. |
| `app/src/agent_playbook/workflows/wf_code_review/steps/report.py` | Proposed | Build the final report deterministically. |
| `app/src/agent_playbook/workflows/wf_code_review/steps/review.py` | Proposed | Invoke reviewer from this workflow. |
| `app/tests/README.md` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/__init__.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/agents/coder/test_coding_result.py` | Proposed | Validate coder output and artifact references. |
| `app/tests/agents/reviewer/test_event_handler.py` | Proposed | Review behavior driven by canonical event fixtures. |
| `app/tests/agents/reviewer/test_review_result.py` | Proposed | Validate review verdict, findings and evidence requirements. |
| `app/tests/agents/verifier/test_required_evidence.py` | Proposed | Verifier fails explicitly when required evidence is unavailable. |
| `app/tests/application/README.md` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/application/test_offline_runtime.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/application/test_workflow_runner.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/cli/test_cli.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/cli/test_workflow_commands.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/config/README.md` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/config/test_configuration.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/conftest.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/execution/README.md` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/execution/adapters/claude/test_event_mapper.py` | Proposed | Claude fixture mapping, partial text and terminal failures. |
| `app/tests/execution/adapters/codex/test_event_mapper.py` | Proposed | Codex fixture mapping, snapshots and command evidence. |
| `app/tests/execution/adapters/deterministic/test_executor.py` | Proposed | Offline executor conformance. |
| `app/tests/execution/contracts/test_capabilities.py` | Proposed | Same requirement checks against every adapter profile. |
| `app/tests/execution/contracts/test_controls.py` | Proposed | Control semantics only for adapters advertising the capability. |
| `app/tests/execution/contracts/test_lifecycle.py` | Proposed | Common adapter suite: ordering, terminal outcomes and cleanup. |
| `app/tests/execution/test_service.py` | Proposed | Preflight, dispatch ownership and invocation failures. |
| `app/tests/fixtures/execution/canonical/reviewer.jsonl` | Proposed | Provider-neutral event fixture for role tests. |
| `app/tests/fixtures/execution/claude/failure.jsonl` | Proposed | Sanitized failure fixture; no invented claim of live capture today. |
| `app/tests/fixtures/execution/claude/success.jsonl` | Proposed | Sanitized native fixture, captured during SDK experiment. |
| `app/tests/fixtures/execution/codex/failure.jsonl` | Proposed | Sanitized native transport/turn failure fixture. |
| `app/tests/fixtures/execution/codex/success.jsonl` | Proposed | Sanitized fixture for the chosen Codex transport. |
| `app/tests/fixtures/offline.yaml` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/integration/test_claude_smoke.py` | Proposed | Opt-in live provider smoke test, outside offline gates. |
| `app/tests/integration/test_codex_smoke.py` | Proposed | Opt-in live provider smoke test, outside offline gates. |
| `app/tests/observability/README.md` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/observability/test_export_failure.py` | Proposed | Configured telemetry outage behavior. |
| `app/tests/observability/test_projection.py` | Proposed | Correct trace correlation without leaking native types. |
| `app/tests/observability/test_redaction.py` | Proposed | Sensitive payload filtering. |
| `app/tests/releases/test_release_selection.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/releases/test_workflow_launch.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/tooling/test_cli_tasks.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/tooling/test_development.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/tooling/test_release_completion.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/tooling/test_release_dependencies.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/tooling/test_release_destination.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/tooling/test_release_preflight.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/tooling/test_toolchain.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/tooling/test_wheel_hash.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/tools/test_run_tests.py` | Proposed | Capture real subprocess exit status and bounded output. |
| `app/tests/workflows/README.md` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/workflows/__init__.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/workflows/conftest.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/workflows/wf_01_step_sequence/__init__.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/workflows/wf_01_step_sequence/test_flow.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/workflows/wf_01_step_sequence/test_steps.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/workflows/wf_02_shared_state/__init__.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/workflows/wf_02_shared_state/test_flow.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/workflows/wf_02_shared_state/test_state.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/workflows/wf_02_shared_state/test_steps.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/workflows/wf_03_conditional_route/__init__.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/workflows/wf_03_conditional_route/test_flow.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/workflows/wf_03_conditional_route/test_state.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/workflows/wf_03_conditional_route/test_steps.py` | PR baseline | Existing test or test fixture retained from PR baseline. |
| `app/tests/workflows/wf_code_review/test_routing.py` | Proposed | Approve, revise, fail and exhausted-budget outcomes. |
| `app/tooling/README.md` | PR baseline | Development/build/verification code, excluded from installed runtime. |
| `app/tooling/__init__.py` | PR baseline | Development/build/verification code, excluded from installed runtime. |
| `app/tooling/bootstrap.py` | PR baseline | Development/build/verification code, excluded from installed runtime. |
| `app/tooling/checks.py` | PR baseline | Development/build/verification code, excluded from installed runtime. |
| `app/tooling/release.py` | PR baseline | Development/build/verification code, excluded from installed runtime. |
| `app/tooling/toolchain.py` | PR baseline | Development/build/verification code, excluded from installed runtime. |
| `app/tooling/verify_refactor.py` | PR baseline | Temporary review helper in PR #34; later removal is an explicit decision. |
| `app/tooling/verify_runtime.py` | PR baseline | Development/build/verification code, excluded from installed runtime. |
| `app/tooling/verify_wheel.py` | PR baseline | Development/build/verification code, excluded from installed runtime. |
| `app/tooling/version.py` | PR baseline | Development/build/verification code, excluded from installed runtime. |
| `app/uv.lock` | PR baseline | Retained repository or application configuration/documentation. |
| `designs/README.md` | PR baseline | Retained architecture, governance or design material. |
| `designs/architecture.md` | PR baseline | Retained architecture, governance or design material. |
| `designs/charter.md` | PR baseline | Retained architecture, governance or design material. |
| `designs/diagrams/01-system.animated.svg` | PR baseline | Retained architecture, governance or design material. |
| `designs/diagrams/01-system.svg` | PR baseline | Retained architecture, governance or design material. |
| `designs/diagrams/02-execution.animated.svg` | PR baseline | Retained architecture, governance or design material. |
| `designs/diagrams/02-execution.svg` | PR baseline | Retained architecture, governance or design material. |
| `designs/diagrams/03-observability.animated.svg` | PR baseline | Retained architecture, governance or design material. |
| `designs/diagrams/03-observability.svg` | PR baseline | Retained architecture, governance or design material. |
| `designs/diagrams/AUTHORING.md` | PR baseline | Retained architecture, governance or design material. |
| `designs/diagrams/README.md` | PR baseline | Retained architecture, governance or design material. |
| `designs/diagrams/build_viewer.py` | PR baseline | Retained architecture, governance or design material. |
| `designs/diagrams/index.html` | PR baseline | Retained architecture, governance or design material. |
| `designs/diagrams/render.py` | PR baseline | Retained architecture, governance or design material. |
| `designs/learning/README.md` | PR baseline | Retained architecture, governance or design material. |
| `designs/learning/architecture-walkthrough.md` | PR baseline | Retained architecture, governance or design material. |
| `designs/principles.md` | PR baseline | Retained architecture, governance or design material. |
| `designs/progress.md` | PR baseline | Retained architecture, governance or design material. |
| `designs/project-structure.md` | PR baseline | Retained architecture, governance or design material. |
| `designs/refactors/2026-11-12-runtime-structure/README.md` | PR baseline | Retained architecture, governance or design material. |
| `designs/refactors/2026-11-12-runtime-structure/proposal.md` | PR baseline | Retained architecture, governance or design material. |
| `designs/refactors/2026-11-12-runtime-structure/verification.md` | PR baseline | Retained architecture, governance or design material. |
| `designs/refactors/atlas/README.md` | Proposed | Entry point, status and navigation levels. |
| `designs/refactors/atlas/THIRD-PARTY-NOTICES.txt` | Proposed | Diagram renderer attribution and license. |
| `designs/refactors/atlas/architecture-atlas.html` | Proposed | Offline drill-down block viewer and file explorer. |
| `designs/refactors/atlas/architecture-guide.md` | Proposed | Detailed ownership, contracts, worked scenario and research. |
| `designs/refactors/atlas/diagrams/01-source.animated.svg` | Proposed | Architecture view with accessible text and static/animated alternatives. |
| `designs/refactors/atlas/diagrams/01-source.html` | Proposed | Architecture view with accessible text and static/animated alternatives. |
| `designs/refactors/atlas/diagrams/01-source.svg` | Proposed | Architecture view with accessible text and static/animated alternatives. |
| `designs/refactors/atlas/diagrams/02-execution.animated.svg` | Proposed | Architecture view with accessible text and static/animated alternatives. |
| `designs/refactors/atlas/diagrams/02-execution.html` | Proposed | Architecture view with accessible text and static/animated alternatives. |
| `designs/refactors/atlas/diagrams/02-execution.svg` | Proposed | Architecture view with accessible text and static/animated alternatives. |
| `designs/refactors/atlas/diagrams/03-events.animated.svg` | Proposed | Architecture view with accessible text and static/animated alternatives. |
| `designs/refactors/atlas/diagrams/03-events.html` | Proposed | Architecture view with accessible text and static/animated alternatives. |
| `designs/refactors/atlas/diagrams/03-events.svg` | Proposed | Architecture view with accessible text and static/animated alternatives. |
| `designs/refactors/atlas/diagrams/04-observability.animated.svg` | Proposed | Architecture view with accessible text and static/animated alternatives. |
| `designs/refactors/atlas/diagrams/04-observability.html` | Proposed | Architecture view with accessible text and static/animated alternatives. |
| `designs/refactors/atlas/diagrams/04-observability.svg` | Proposed | Architecture view with accessible text and static/animated alternatives. |
| `designs/refactors/atlas/diagrams/05-release.animated.svg` | Proposed | Architecture view with accessible text and static/animated alternatives. |
| `designs/refactors/atlas/diagrams/05-release.html` | Proposed | Architecture view with accessible text and static/animated alternatives. |
| `designs/refactors/atlas/diagrams/05-release.svg` | Proposed | Architecture view with accessible text and static/animated alternatives. |
| `designs/refactors/atlas/full-file-structure.md` | Proposed | Complete candidate file inventory with status. |
| `designs/refactors/atlas/verification.md` | Proposed | Artifact checks and limits of evidence. |
| `designs/roadmap.md` | PR baseline | Retained architecture, governance or design material. |
| `designs/stages/00-environment/architecture.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/00-environment/findings.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/00-environment/learning/00-1-python-environment.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/00-environment/learning/00-2-application-cli.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/00-environment/learning/00-3-pyright.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/00-environment/learning/00-4-pytest.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/00-environment/learning/00-5-ruff.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/00-environment/learning/00-6-unified-checks.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/00-environment/learning/00-7-wheel-release.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/00-environment/plan.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/README.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/architecture.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/configuration-findings.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/coordination.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/00-architecture-animated.svg` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/00-architecture.html` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/00-architecture.svg` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/01-sequence-animated.svg` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/01-sequence.html` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/01-sequence.svg` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/02-state-animated.svg` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/02-state.html` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/02-state.svg` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/03-route-pass-animated.svg` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/03-route-pass.html` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/03-route-pass.svg` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/04-route-needs-work-animated.svg` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/04-route-needs-work.html` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/04-route-needs-work.svg` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/README.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/THIRD-PARTY-NOTICES.txt` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/diagrams/index.html` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/file-structure.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/findings.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/learning/00-reading-the-code.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/learning/01-flow-basics.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/learning/02-sequence-and-values.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/learning/03-typed-state.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/learning/04-routing.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/learning/05-failures-and-tests.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/learning/06-running-and-releasing.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/learning/08-independent-sandboxes.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/plan.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/sources.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/test-plan.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/workflows/wf-01-step-sequence.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/workflows/wf-02-shared-state.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `designs/stages/01-crewai-flows/workflows/wf-03-conditional-route.md` | PR baseline | Retained stage design, lesson, diagram or verification record. |
| `sandbox/AGENTS.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/README.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/agents/code-writer.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/agents/designer.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/agents/orchestrator.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/agents/replanner.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/agents/reviewer.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/agents/tester.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/projects/agent-playbook/features/f-01-reviewer-trial/design.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/projects/agent-playbook/features/f-02-implementer-handoff/design.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/projects/agent-playbook/features/f-03-design-deviations/design.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/projects/project-a/review-rules.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/projects/project-a/reviews/pr-14.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/projects/system-one-harness/features/f-01-offline-test-suite/design.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/projects/system-one-harness/reviews/pr-46.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/verification/reviewer-handoff.md` | PR baseline | Retained historical experiment; outside active application work. |
| `sandbox/workflows/implement-change.md` | PR baseline | Retained historical experiment; outside active application work. |
