"""Resolve a selected YAML entry and construct a fresh workflow instance."""

from typing import Mapping

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from agent_playbook.config.diagnostics import validation_fields
from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.models import ApplicationSettings, CrewAISettings
from agent_playbook.workflows.contracts import Workflow
from agent_playbook.workflows.errors import WorkflowInputError


class WorkflowEntry(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)
    implementation: str = Field(min_length=1)
    name: str | None = Field(default=None, min_length=1)
    enabled: bool = True
    config: dict[str, object] = Field(default_factory=dict)


def select_workflow(
    workflow_id: str,
    application: ApplicationSettings,
    settings: CrewAISettings,
    registry: Mapping[str, type[Workflow[object]]],
) -> tuple[type[Workflow[object]], dict[str, object]]:
    if not workflow_id or workflow_id != workflow_id.strip():
        raise WorkflowInputError(
            "Workflow ID must be a nonempty string without surrounding whitespace."
        )
    if workflow_id not in application.workflows:
        raise WorkflowInputError(f"Unknown workflow {workflow_id!r}.")
    raw_entry = application.workflows[workflow_id]
    try:
        entry = WorkflowEntry.model_validate(raw_entry)
    except ValidationError as error:
        raise ConfigurationError(
            f"{workflow_id} CONFIGURATION: {validation_fields(error)}."
        ) from error
    if isinstance(raw_entry, dict) and "name" in raw_entry and entry.name is None:
        raise ConfigurationError(
            f"{workflow_id} CONFIGURATION: invalid name; expected a nonempty string."
        )
    if entry.name is not None and (
        not entry.name.strip() or entry.name != entry.name.strip()
    ):
        raise ConfigurationError(
            f"{workflow_id} CONFIGURATION: invalid name; expected a nonempty string without surrounding whitespace."
        )
    if not entry.enabled:
        raise WorkflowInputError(f"Workflow {workflow_id!r} is disabled.")
    key = entry.implementation
    if key != key.strip() or key not in registry:
        raise ConfigurationError(
            f"{workflow_id} CONFIGURATION: unknown implementation."
        )
    return registry[key], entry.config


def construct_workflow(
    workflow_id: str,
    implementation: type[Workflow[object]],
    settings: CrewAISettings,
    config: Mapping[str, object],
) -> Workflow[object]:
    try:
        return implementation(settings=settings, config=config)
    except ConfigurationError as error:
        raise ConfigurationError(f"{workflow_id} CONFIGURATION: {error}") from error


def create_workflow(
    workflow_id: str,
    application: ApplicationSettings,
    settings: CrewAISettings,
    registry: Mapping[str, type[Workflow[object]]],
) -> Workflow[object]:
    implementation, config = select_workflow(
        workflow_id, application, settings, registry
    )
    return construct_workflow(workflow_id, implementation, settings, config)
