"""Run one selected workflow through the common lifecycle."""

from pydantic import TypeAdapter, ValidationError

from agent_playbook.application.assembly import assemble_runtime
from agent_playbook.application.results import RunResult
from agent_playbook.application.workflow_factory import create_workflow
from agent_playbook.application.workflow_registry import workflow_registry
from agent_playbook.workflows.errors import WorkflowExecutionError, WorkflowInputError
from agent_playbook.workflows.lifecycle import WorkflowPhase

_INPUT = TypeAdapter(dict[str, object])


def run_workflow(
    workflow_id: str = "wf-01",
    raw_input: str | None = None,
    *,
    config_path: str | None = None,
) -> RunResult[object]:
    application = assemble_runtime(config_path)
    registry = workflow_registry()
    try:
        workflow = create_workflow(
            workflow_id, application, application.integrations.crewai, registry
        )
    except (WorkflowInputError, WorkflowExecutionError):
        raise
    except Exception as error:
        raise WorkflowExecutionError(f"{workflow_id} construction failed.") from error
    try:
        data = _INPUT.validate_json(
            "{}" if raw_input is None else raw_input, strict=True
        )
    except ValidationError as error:
        raise WorkflowInputError(f"Invalid {workflow_id} JSON object.") from error

    try:
        workflow.prepare(data)
    except WorkflowInputError:
        raise
    except Exception as error:
        raise WorkflowExecutionError(f"{workflow_id} PREPARE failed.") from error
    try:
        raw = workflow.execute()
        output = workflow.validate_output(raw)
        serialized = workflow.serialize_output()
    except Exception as error:
        phase = (
            workflow.failure.phase
            if workflow.failure is not None
            else WorkflowPhase.EXECUTE
        )
        raise WorkflowExecutionError(f"{workflow_id} {phase.name} failed.") from error
    return RunResult(workflow_id, output, serialized)
