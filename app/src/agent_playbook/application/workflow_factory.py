"""Resolve a selected YAML entry and construct a fresh workflow instance."""

from typing import Mapping

from pydantic import BaseModel, ConfigDict, Field, ValidationError

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


def create_workflow(
    workflow_id: str,
    application: ApplicationSettings,
    settings: CrewAISettings,
    registry: Mapping[str, type[Workflow[object]]],
) -> Workflow[object]:
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
        fields = "; ".join(
            ".".join(str(part) for part in item["loc"]) or "entry"
            for item in error.errors(
                include_input=False, include_context=False, include_url=False
            )
        )
        raise ConfigurationError(
            f"Invalid {workflow_id} configuration fields: {fields}."
        ) from None
    if isinstance(raw_entry, dict) and "name" in raw_entry and entry.name is None:
        raise ConfigurationError(
            f"Invalid {workflow_id} name; expected a nonempty string."
        )
    if entry.name is not None and (
        not entry.name.strip() or entry.name != entry.name.strip()
    ):
        raise ConfigurationError(
            f"Invalid {workflow_id} name; expected a nonempty string without surrounding whitespace."
        )
    if not entry.enabled:
        raise WorkflowInputError(f"Workflow {workflow_id!r} is disabled.")
    key = entry.implementation
    if key != key.strip() or key not in registry:
        raise ConfigurationError(f"Unknown implementation for {workflow_id!r}.")
    return registry[key](settings=settings, config=entry.config)
