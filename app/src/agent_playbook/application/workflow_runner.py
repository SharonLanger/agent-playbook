"""Run one selected workflow through the common lifecycle."""

from collections.abc import Mapping
from contextlib import nullcontext
from uuid import uuid4

from langfuse import get_client, propagate_attributes
from pydantic import TypeAdapter, ValidationError

from agent_playbook.application.assembly import assemble_runtime
from agent_playbook.application.results import RunResult
from agent_playbook.application.workflow_factory import (
    construct_workflow,
    select_workflow,
)
from agent_playbook.application.workflow_registry import workflow_registry
from agent_playbook.config.diagnostics import validation_fields
from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.models import ApplicationSettings
from agent_playbook.context.models import ExecutionContext, ObservabilityContext
from agent_playbook.workflows.contracts import Workflow
from agent_playbook.workflows.errors import WorkflowExecutionError, WorkflowInputError

_INPUT = TypeAdapter(dict[str, object])
_OUTPUT = TypeAdapter(object)


def run_workflow(
    workflow_id: str = "wf-01",
    raw_input: str | None = None,
    *,
    config_path: str | None = None,
) -> RunResult[object]:
    try:
        application = assemble_runtime(config_path)
    except ConfigurationError:
        raise
    except Exception as error:
        raise WorkflowExecutionError(f"{workflow_id} SETUP failed.") from error
    try:
        registry = workflow_registry()
    except Exception as error:
        raise WorkflowExecutionError(f"{workflow_id} SETUP failed.") from error
    implementation, config = select_workflow(
        workflow_id, application, application.integrations.crewai, registry
    )
    try:
        context = ExecutionContext(
            observability=ObservabilityContext(
                workflow_id=workflow_id, workflow_run_id=str(uuid4())
            )
        )
    except Exception as error:
        raise WorkflowExecutionError(f"{workflow_id} CONSTRUCTION failed.") from error
    settings = application.integrations.langfuse
    scope = (
        get_client(
            public_key=settings.public_key.get_secret_value()
        ).start_as_current_observation(as_type="span", name=workflow_id)
        if settings.enabled and settings.public_key is not None
        else nullcontext()
    )
    with scope:
        attributes = (
            propagate_attributes(
                metadata={
                    "correlation_id": context.correlation_id,
                    "workflow_id": context.observability.workflow_id,
                    "workflow_run_id": context.observability.workflow_run_id,
                }
            )
            if settings.enabled
            else nullcontext()
        )
        with attributes:
            return _run_selected(
                workflow_id, raw_input, application, implementation, config, context
            )


def _run_selected(
    workflow_id: str,
    raw_input: str | None,
    application: ApplicationSettings,
    implementation: type[Workflow[object]],
    config: Mapping[str, object],
    context: ExecutionContext,
) -> RunResult[object]:
    try:
        workflow = construct_workflow(
            workflow_id,
            implementation,
            application.integrations.crewai,
            config,
            context=context,
        )
    except ConfigurationError:
        raise
    except Exception as error:
        raise WorkflowExecutionError(f"{workflow_id} CONSTRUCTION failed.") from error
    try:
        data = _INPUT.validate_json(
            "{}" if raw_input is None else raw_input, strict=True
        )
    except ValidationError as error:
        raise WorkflowInputError(
            f"{workflow_id} INPUT: {validation_fields(error)}."
        ) from error

    try:
        workflow.prepare(data)
    except WorkflowInputError as error:
        raise WorkflowInputError(f"{workflow_id} PREPARE: {error}") from error
    except Exception as error:
        raise WorkflowExecutionError(f"{workflow_id} PREPARE failed.") from error
    settings = application.integrations.langfuse
    if settings.enabled and settings.public_key is not None:
        get_client(
            public_key=settings.public_key.get_secret_value()
        ).update_current_span(input=data)
    try:
        raw = workflow.execute()
    except Exception as error:
        raise WorkflowExecutionError(f"{workflow_id} EXECUTE failed.") from error
    try:
        output = workflow.validate_output(raw)
    except Exception as error:
        raise WorkflowExecutionError(
            f"{workflow_id} VALIDATE_OUTPUT failed."
        ) from error
    try:
        serialized = workflow.serialize_output()
        if settings.enabled and settings.public_key is not None:
            get_client(
                public_key=settings.public_key.get_secret_value()
            ).update_current_span(output=_OUTPUT.dump_python(output, mode="json"))
    except Exception as error:
        raise WorkflowExecutionError(
            f"{workflow_id} SERIALIZE_OUTPUT failed."
        ) from error
    return RunResult(workflow_id, output, serialized)
