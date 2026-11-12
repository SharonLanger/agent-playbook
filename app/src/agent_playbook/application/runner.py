"""Validate input, select a fresh flow, invoke CrewAI and normalize its result."""

from agent_playbook.application.results import (
    RunResult,
    WorkflowExecutionError,
    WorkflowInputError,
)


def run_workflow(
    workflow_id: str = "wf-01",
    raw_input: str | None = None,
    *,
    config_path: str | None = None,
) -> RunResult:
    if workflow_id not in ("wf-01", "wf-02", "wf-03"):
        raise WorkflowInputError(
            f"Unknown workflow {workflow_id!r}; use wf-01, wf-02 or wf-03."
        )

    # Keep help, version, tooling and release selection free of framework imports.
    from pydantic import TypeAdapter, ValidationError

    from agent_playbook.config.crewai import configure_crewai
    from agent_playbook.config.loader import load_configuration

    settings = load_configuration(config_path).integrations.crewai
    configure_crewai(settings)

    from agent_playbook.workflows.wf_01_step_sequence.flow import StepSequenceFlow
    from agent_playbook.workflows.wf_02_shared_state.flow import SharedStateFlow
    from agent_playbook.workflows.wf_02_shared_state.state import (
        NumberInput,
        NumberState,
    )
    from agent_playbook.workflows.wf_03_conditional_route.flow import (
        ConditionalRouteFlow,
    )
    from agent_playbook.workflows.wf_03_conditional_route.state import (
        ScoreInput,
        ScoreState,
    )

    try:
        data = TypeAdapter(dict[str, object]).validate_json(
            "{}" if raw_input is None else raw_input, strict=True
        )
        if workflow_id == "wf-01":
            if data:
                raise WorkflowInputError(
                    "wf-01 accepts no input fields; use {} or omit --input."
                )
            flow = StepSequenceFlow(
                tracing=settings.tracing_enabled,
                suppress_flow_events=not settings.show_framework_events,
            )
        elif workflow_id == "wf-02":
            numbers = NumberInput.model_validate(data)
            flow = SharedStateFlow(
                initial_state=NumberState(
                    initial=numbers.initial,
                    increment=numbers.increment,
                    multiplier=numbers.multiplier,
                ),
                tracing=settings.tracing_enabled,
                suppress_flow_events=not settings.show_framework_events,
            )
        else:
            score = ScoreInput.model_validate(data)
            flow = ConditionalRouteFlow(
                initial_state=ScoreState(score=score.score),
                tracing=settings.tracing_enabled,
                suppress_flow_events=not settings.show_framework_events,
            )
    except ValidationError as error:
        raise WorkflowInputError(f"Invalid {workflow_id} input: {error}") from error

    try:
        output: object = flow.kickoff()
        if not isinstance(output, (str, int)) or isinstance(output, bool):
            raise TypeError("Workflow returned an unsupported result.")
    except Exception as error:
        raise WorkflowExecutionError(
            f"{workflow_id} execution failed: {error}"
        ) from error
    return RunResult(workflow_id, str(output))
