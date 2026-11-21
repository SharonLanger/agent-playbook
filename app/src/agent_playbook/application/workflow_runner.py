"""Run one selected workflow through the common lifecycle."""

from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager, nullcontext
from typing import Any
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
from agent_playbook.config.models import ApplicationSettings, LangfuseSettings
from agent_playbook.context.models import ExecutionContext, ObservabilityContext
from agent_playbook.observability.adapters.otel_logging.runtime import logging_scope
from agent_playbook.observability.logging import log_debug, log_error, log_info, warn
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
    with logging_scope(application.integrations.logging):
        try:
            return _run_configured(workflow_id, raw_input, application)
        finally:
            try:
                from agent_playbook.observability.adapters.langfuse.runtime import (
                    flush_tracing,
                )

                flush_tracing()
            except Exception:
                warn("Langfuse delivery attempt failed.")


@contextmanager
def _telemetry_scope(factory: Callable[[], Any]) -> Iterator[None]:
    """Contain native scope operations without catching the workflow body."""
    manager = None
    try:
        manager = factory()
        manager.__enter__()
    except Exception:
        warn("Langfuse observation setup failed.")
        manager = None
    try:
        yield
    except BaseException as error:
        if manager is not None:
            try:
                manager.__exit__(type(error), error, error.__traceback__)
            except Exception:
                warn("Langfuse observation cleanup failed.")
        raise
    else:
        if manager is not None:
            try:
                manager.__exit__(None, None, None)
            except Exception:
                warn("Langfuse observation cleanup failed.")


def _run_configured(
    workflow_id: str, raw_input: str | None, application: ApplicationSettings
) -> RunResult[object]:
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

    def scope():
        return (
            get_client(
                public_key=settings.public_key.get_secret_value()
            ).start_as_current_observation(as_type="span", name=workflow_id)
            if settings.enabled and settings.public_key is not None
            else nullcontext()
        )

    with _telemetry_scope(scope):

        def attributes():
            return (
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

        with _telemetry_scope(attributes):
            log_info(context, "Workflow started")
            log_debug(
                context,
                "Workflow selected",
                fields={
                    "implementation": implementation.__name__,
                    "component": "runner",
                },
            )
            try:
                result = _run_selected(
                    workflow_id, raw_input, application, implementation, config, context
                )
            except Exception as error:
                # Configuration diagnostics deliberately omit potentially secret-bearing causes.
                log_error(
                    context,
                    "Workflow failed",
                    fields={
                        "phase": next(
                            (
                                phase
                                for phase in (
                                    "CONSTRUCTION",
                                    "INPUT",
                                    "PREPARE",
                                    "EXECUTE",
                                    "VALIDATE_OUTPUT",
                                    "SERIALIZE_OUTPUT",
                                )
                                if f"{workflow_id} {phase}" in str(error)
                            ),
                            "UNKNOWN",
                        )
                    },
                    exception=None
                    if isinstance(error, (ConfigurationError, WorkflowInputError))
                    else error,
                )
                raise
            log_info(context, "Workflow completed")
            return result


def _run_selected(
    workflow_id: str,
    raw_input: str | None,
    application: ApplicationSettings,
    implementation: type[Workflow[object]],
    config: Mapping[str, object],
    context: ExecutionContext,
) -> RunResult[object]:
    log_debug(context, "Workflow phase started", fields={"phase": "construction"})
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

    log_debug(context, "Workflow phase started", fields={"phase": "prepare"})
    try:
        workflow.prepare(data)
    except WorkflowInputError as error:
        raise WorkflowInputError(f"{workflow_id} PREPARE: {error}") from error
    except Exception as error:
        raise WorkflowExecutionError(f"{workflow_id} PREPARE failed.") from error
    settings = application.integrations.langfuse
    _update_span(settings, input=data)
    log_debug(context, "Workflow phase started", fields={"phase": "execute"})
    try:
        raw = workflow.execute()
    except Exception as error:
        raise WorkflowExecutionError(f"{workflow_id} EXECUTE failed.") from error
    log_debug(context, "Workflow phase started", fields={"phase": "validate_output"})
    try:
        output = workflow.validate_output(raw)
    except Exception as error:
        raise WorkflowExecutionError(
            f"{workflow_id} VALIDATE_OUTPUT failed."
        ) from error
    log_debug(context, "Workflow phase started", fields={"phase": "serialize_output"})
    try:
        serialized = workflow.serialize_output()
    except Exception as error:
        raise WorkflowExecutionError(
            f"{workflow_id} SERIALIZE_OUTPUT failed."
        ) from error
    if settings.enabled and settings.public_key is not None:
        try:
            _update_span(settings, output=_OUTPUT.dump_python(output, mode="json"))
        except Exception:
            warn("Langfuse observation update failed.")
    return RunResult(workflow_id, output, serialized)


def _update_span(settings: LangfuseSettings, **attributes: Any) -> None:
    if settings.enabled and settings.public_key is not None:
        try:
            get_client(
                public_key=settings.public_key.get_secret_value()
            ).update_current_span(**attributes)
        except Exception:
            warn("Langfuse observation update failed.")
