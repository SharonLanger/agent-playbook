"""Registry keys, constructor compatibility, aliases and boundaries."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agent_playbook.application.assembly import assemble_runtime
from agent_playbook.application.workflow_factory import create_workflow
from agent_playbook.application.workflow_registry import workflow_registry
from agent_playbook.config.errors import ConfigurationError
from agent_playbook.workflows.contracts import Workflow
from agent_playbook.workflows.errors import WorkflowInputError
from agent_playbook.workflows.lifecycle import WorkflowStatus

FIXTURE = Path(__file__).parents[1] / "fixtures/offline.yaml"


def test_every_registered_class_is_concrete_and_constructible() -> None:
    application = assemble_runtime(str(FIXTURE))
    registry = workflow_registry()
    assert set(registry) == {"step_sequence", "shared_state", "conditional_route"}
    for implementation in registry.values():
        workflow = implementation(settings=application.integrations.crewai, config={})
        assert isinstance(workflow, Workflow)
        assert workflow.status is WorkflowStatus.CREATED


def test_aliases_create_fresh_instances(tmp_path: Path) -> None:
    selected = tmp_path / "configuration.yaml"
    selected.write_text(
        FIXTURE.read_text() + "  second: {implementation: shared_state}\n"
    )
    application = assemble_runtime(str(selected))
    registry = workflow_registry()
    first = create_workflow(
        "wf-02", application, application.integrations.crewai, registry
    )
    second = create_workflow(
        "second", application, application.integrations.crewai, registry
    )
    assert first is not second and type(first) is type(second)
    assert first.status is second.status is WorkflowStatus.CREATED


@pytest.mark.parametrize(
    "entry,error",
    [
        ("{implementation: unknown}", ConfigurationError),
        ("{implementation: shared_state, enabled: false}", WorkflowInputError),
        ("{implementation: shared_state, config: null}", ConfigurationError),
        ("{implementation: shared_state, surprise: 1}", ConfigurationError),
        (
            "{implementation: shared_state, config: {defaults: {initial: 1001}}}",
            ConfigurationError,
        ),
    ],
)
def test_selected_entry_fails_before_steps(
    tmp_path: Path, entry: str, error: type[Exception]
) -> None:
    selected = tmp_path / "configuration.yaml"
    selected.write_text(FIXTURE.read_text() + f"  selected: {entry}\n")
    application = assemble_runtime(str(selected))
    with patch(
        "agent_playbook.workflows.wf_02_shared_state.flow.SharedStateFlow.kickoff"
    ) as kickoff:
        with pytest.raises(error):
            create_workflow(
                "selected",
                application,
                application.integrations.crewai,
                workflow_registry(),
            )
        kickoff.assert_not_called()
