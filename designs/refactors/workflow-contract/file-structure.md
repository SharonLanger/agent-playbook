# Proposed file structure

Status: **Design only. The paths marked new below are not implemented.**

Keep the accepted component boundaries. Add the shared contract within workflows, the registry within application, and a wrapper beside each existing CrewAI flow. No code moves to a generic framework package.

```yaml
designs:
  refactors:
    workflow-contract:
      README.md: entry point, decisions and authorization status
      design.md: lifecycle, types, configuration and errors
      file-structure.md: this placement proposal
      test-plan.md: acceptance scenarios by test layer
      implementation-plan.md: milestones, risks, guarded changes and handoff

app:
  application.yaml: add configured workflow entries
  src:
    agent_playbook:
      application:
        assembly.py: return loaded settings and configure integrations
        workflow_registry.py: NEW stable implementation keys to class references
        workflow_factory.py: resolve selected configuration and construct wrapper
        workflow_runner.py: call the common ABC methods and normalize outcomes
        results.py: immutable generic RunResult with typed output and display text
      config:
        models.py: shared settings plus raw workflow catalog and selected-entry model
        loader.py: safe YAML, duplicate-key checks, overlays and shared validation
        errors.py: existing ConfigurationError
      workflows:
        contracts.py: NEW Workflow ABC and typed validated-result access
        lifecycle.py: NEW WorkflowStatus, WorkflowPhase and WorkflowFailure record
        errors.py: NEW shared input, execution and invalid-order errors
        wf_01_step_sequence:
          workflow.py: NEW wrapper; empty input/configuration rules and string output
          flow.py: existing CrewAI graph
          steps.py: existing computations
        wf_02_shared_state:
          workflow.py: NEW wrapper; prepare flow and validate/serialize integer
          config.py: NEW strict workflow defaults schema using existing input model
          flow.py: existing CrewAI graph
          state.py: existing NumberInput and NumberState
          steps.py: existing computations
        wf_03_conditional_route:
          workflow.py: NEW wrapper; prepare flow and validate allowed output
          config.py: NEW strict score-defaults schema using existing input model
          flow.py: existing CrewAI graph and threshold
          state.py: existing ScoreInput and ScoreState
          steps.py: existing computations
      cli:
        parser.py: general workflow help; no hardcoded allowed-ID list
        commands.py: print serialized_output and preserve exit categories
      releases:
        discovery.py: existing installation selection
        launcher.py: existing argv forwarding and interpreter isolation
  tests:
    workflows:
      test_contract.py: NEW shared lifecycle and rich-result contract tests
      wf_01_step_sequence:
        test_workflow.py: NEW wrapper tests; retain existing flow/step tests
      wf_02_shared_state:
        test_workflow.py: NEW wrapper/config tests; retain existing flow/state/step tests
      wf_03_conditional_route:
        test_workflow.py: NEW wrapper/config tests; retain existing flow/state/step tests
    application:
      test_workflow_registry.py: NEW registry compatibility and construction tests
      test_workflow_factory.py: NEW selected-entry resolution and fresh instances
      test_workflow_runner.py: adapt; isolate runner with mocked collaborators
      test_offline_runtime.py: retain real fresh-process coverage
    config:
      test_configuration.py: extend selection, strict YAML and overlay cases
    cli:
      test_workflow_commands.py: adapt presentation; add configured aliases
    releases:
      test_workflow_launch.py: retain forwarding and isolation scenarios
  tooling:
    verify_runtime.py: adapt maintained configuration fixtures, preserve real runs
  docs:
    configuration.md: update with implemented workflow schema in implementation PR
    workflows.md: update with implemented selection/configuration behavior
    cli.md: update workflow selection and result/error guidance
    troubleshooting.md: update failure phases and configuration diagnostics
```

Package markers and unrelated files are omitted from this focused tree. No new dependency or framework is required. Implementation may keep a tiny declaration beside its owner rather than add a helper module, provided the approved responsibilities remain unchanged and the final layout is recorded.

## Dependency and placement rules

- Workflow contracts/lifecycle/errors do not import application, CLI, release tooling or Langfuse. Concrete wrappers can use config model types and their own flow/state modules.
- Application imports the common workflow contract; only its registry names concrete wrapper classes.
- The registry stores class references, not shared instances. Its imports must preserve assembly-before-CrewAI initialization.
- Lifecycle methods and transition guards live in the ABC once. The enum/data records live in lifecycle.py; that file is not an execution engine.
- Each wrapper owns strict implementation configuration; shared config only understands the common entry envelope.
- Public guides describe supported behavior after implementation. This proposal remains under designs.
- Personal `app/examples/` and historical `sandbox/` remain outside this change. Tests use independent fixtures.

## Guarded structure relationship

This tree proposes files within existing application/config/workflows boundaries. The top-level project structure still describes the current direct-flow factory and runner; its exact future wording change is listed in the implementation plan. That guarded file is not silently rewritten to claim this refactor already exists.
