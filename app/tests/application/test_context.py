"""Actual runner, factory and wrapper context propagation."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agent_playbook.application.assembly import assemble_runtime
from agent_playbook.application.workflow_factory import (
    construct_workflow,
    create_workflow,
)
from agent_playbook.application.workflow_registry import workflow_registry
from agent_playbook.application.workflow_runner import run_workflow
from agent_playbook.context.models import ExecutionContext, ObservabilityContext
from agent_playbook.workflows.errors import WorkflowExecutionError

FIXTURE = Path(__file__).parents[1] / "fixtures/offline.yaml"


def test_runner_fresh_roots_and_alias(tmp_path: Path) -> None:
    config = tmp_path / "configuration.yaml"
    (tmp_path / "empty-secrets.env").write_text("")
    config.write_text(FIXTURE.read_text() + "  alias: {implementation: shared_state}\n")
    with patch(
        "agent_playbook.application.workflow_runner.construct_workflow",
        wraps=construct_workflow,
    ) as constructor:
        assert run_workflow("wf-02", config_path=str(config)).output == 20
        assert run_workflow("wf-02", config_path=str(config)).output == 20
        assert run_workflow("alias", config_path=str(config)).output == 20
    observed = [call.kwargs["context"] for call in constructor.call_args_list]
    assert all(isinstance(value, ExecutionContext) for value in observed)
    assert [x.observability.workflow_id for x in observed] == [
        "wf-02",
        "wf-02",
        "alias",
    ]
    assert len({id(x) for x in observed}) == 3
    assert len({x.correlation_id for x in observed}) == 3
    assert len({x.observability.workflow_run_id for x in observed}) == 3
    assert all(
        x.observability.agent_type is x.observability.agent_run_id is None
        for x in observed
    )


@pytest.mark.parametrize("selected", ["wf-01", "wf-02", "wf-03"])
def test_factory_forwarding(selected: str) -> None:
    application = assemble_runtime(str(FIXTURE))
    registry = workflow_registry()
    context = ExecutionContext(
        observability=ObservabilityContext(workflow_id=selected, workflow_run_id="run"),
        correlation_id="corr",
    )
    first = create_workflow(
        selected,
        application,
        application.integrations.crewai,
        registry,
        context=context,
    )
    assert first.context is context
    implementation = next(typ for typ in registry.values() if isinstance(first, typ))
    second = construct_workflow(
        selected, implementation, application.integrations.crewai, {}, context=context
    )
    assert second.context is context and second is not first


def test_context_construction_failure_has_existing_boundary() -> None:
    error = RuntimeError("injected")
    with patch(
        "agent_playbook.application.workflow_runner.ExecutionContext", side_effect=error
    ):
        with pytest.raises(
            WorkflowExecutionError, match="wf-01 CONSTRUCTION"
        ) as caught:
            run_workflow("wf-01", config_path=str(FIXTURE))
    assert caught.value.__cause__ is error
