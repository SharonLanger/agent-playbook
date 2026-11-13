"""Coordinate one application run and normalize its outcome."""

from agent_playbook.application.assembly import assemble_runtime
from agent_playbook.application.results import (
    RunResult,
    WorkflowExecutionError,
    WorkflowInputError,
)
from agent_playbook.application.workflow_factory import (
    create_workflow,
    validate_workflow_id,
)


def run_workflow(
    workflow_id: str = "wf-01",
    raw_input: str | None = None,
    *,
    config_path: str | None = None,
) -> RunResult:
    selected = validate_workflow_id(workflow_id)
    settings = assemble_runtime(config_path)

    from pydantic import TypeAdapter, ValidationError

    try:
        data = TypeAdapter(dict[str, object]).validate_json(
            "{}" if raw_input is None else raw_input, strict=True
        )
        flow = create_workflow(selected, data, settings)
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
