"""Selected identity, setup, construction and deferred-import boundaries."""

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping
from unittest.mock import Mock, patch

import pytest
from pydantic import ValidationError

from agent_playbook.application.results import WorkflowExecutionError
from agent_playbook.application.workflow_runner import run_workflow
from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.models import (
    ApplicationSettings,
    CrewAISettings,
    IntegrationSettings,
)
from agent_playbook.workflows.contracts import Workflow
from agent_playbook.workflows.errors import WorkflowInputError, WorkflowOrderError

SETTINGS = CrewAISettings(
    usage_telemetry_enabled=False, tracing_enabled=False, show_framework_events=False
)
APPLICATION = ApplicationSettings(
    integrations=IntegrationSettings(crewai=SETTINGS),
    workflows={"customer-job": {"implementation": "test"}},
)
FIXTURE = Path(__file__).parents[1] / "fixtures/offline.yaml"


@dataclass(frozen=True)
class Review:
    details: tuple[int, ...]


class RichWorkflow(Workflow[Review]):
    def _prepare(self, data: Mapping[str, object]) -> None:
        self._value = Review((2, 3))

    def _execute(self) -> object:
        return self._value

    def _validate_output(self, output: object) -> Review:
        if not isinstance(output, Review):
            raise TypeError("review required")
        return output

    def _serialize_output(self) -> str:
        return str(sum(self.result.details))


def test_real_rich_result_through_arbitrary_registry_key() -> None:
    with (
        patch(
            "agent_playbook.application.workflow_runner.assemble_runtime",
            return_value=APPLICATION,
        ),
        patch(
            "agent_playbook.application.workflow_runner.workflow_registry",
            return_value={"test": RichWorkflow},
        ),
    ):
        result = run_workflow("customer-job")
    assert isinstance(result.output, Review)
    assert result.output.details == (2, 3) and result.serialized_output == "5"


@pytest.mark.parametrize(
    "error",
    [
        WorkflowInputError("private"),
        ValueError("private"),
        ValidationError.from_exception_data(
            "X", [{"type": "int_type", "loc": ("initial",), "input": True}]
        ),
    ],
)
def test_unexpected_constructor_errors_are_execution_failures(error: Exception) -> None:
    class Broken(RichWorkflow):
        def __init__(
            self, *, settings: CrewAISettings, config: Mapping[str, object]
        ) -> None:
            raise error

    with (
        patch(
            "agent_playbook.application.workflow_runner.assemble_runtime",
            return_value=APPLICATION,
        ),
        patch(
            "agent_playbook.application.workflow_runner.workflow_registry",
            return_value={"test": Broken},
        ),
    ):
        with pytest.raises(
            WorkflowExecutionError, match="customer-job CONSTRUCTION"
        ) as failure:
            run_workflow("customer-job")
    assert failure.value.__cause__ is error
    assert "private" not in str(failure.value)


def test_explicit_constructor_config_error_stays_configuration() -> None:
    class Broken(RichWorkflow):
        def __init__(
            self, *, settings: CrewAISettings, config: Mapping[str, object]
        ) -> None:
            raise ConfigurationError("defaults.initial (int_type)")

    with (
        patch(
            "agent_playbook.application.workflow_runner.assemble_runtime",
            return_value=APPLICATION,
        ),
        patch(
            "agent_playbook.application.workflow_runner.workflow_registry",
            return_value={"test": Broken},
        ),
    ):
        with pytest.raises(
            ConfigurationError, match="customer-job CONFIGURATION: defaults.initial"
        ):
            run_workflow("customer-job")


@pytest.mark.parametrize(
    "boundary",
    [
        "assembly",
        "registry",
        "selection",
        "construction",
        "json",
        "prepare",
        "execute",
        "validate_output",
        "serialize_output",
    ],
)
def test_failure_stops_before_success(boundary: str) -> None:
    original = ValueError("private failure")
    calls: list[str] = []
    workflow = Mock()
    output = Review((2, 3))

    def step(name: str, value: object) -> Mock:
        def invoke(*_args: object, **_kwargs: object) -> object:
            calls.append(name)
            if boundary == name:
                if name == "selection":
                    raise ConfigurationError("selected entry invalid")
                raise original
            return value

        return Mock(side_effect=invoke)

    assembly = step("assembly", APPLICATION)
    registry = step("registry", {"test": RichWorkflow})
    selection = step("selection", (RichWorkflow, dict[str, object]()))
    construction = step("construction", workflow)
    workflow.prepare = step("prepare", None)
    workflow.execute = step("execute", "raw")
    workflow.validate_output = step("validate_output", output)
    workflow.serialize_output = step("serialize_output", "5")
    result = step("result", object())
    with (
        patch("agent_playbook.application.workflow_runner.assemble_runtime", assembly),
        patch("agent_playbook.application.workflow_runner.workflow_registry", registry),
        patch("agent_playbook.application.workflow_runner.select_workflow", selection),
        patch(
            "agent_playbook.application.workflow_runner.construct_workflow",
            construction,
        ),
        patch("agent_playbook.application.workflow_runner.RunResult", result),
    ):
        if boundary == "selection":
            with pytest.raises(ConfigurationError, match="selected entry invalid"):
                run_workflow("customer-job")
        elif boundary == "json":
            with pytest.raises(
                WorkflowInputError, match="customer-job INPUT"
            ) as failure:
                run_workflow("customer-job", "[")
            assert isinstance(failure.value.__cause__, ValidationError)
        else:
            phase = {
                "assembly": "SETUP",
                "registry": "SETUP",
                "construction": "CONSTRUCTION",
                "prepare": "PREPARE",
                "execute": "EXECUTE",
                "validate_output": "VALIDATE_OUTPUT",
                "serialize_output": "SERIALIZE_OUTPUT",
            }[boundary]
            with pytest.raises(
                WorkflowExecutionError, match=f"customer-job {phase} failed"
            ) as failure:
                run_workflow("customer-job")
            assert failure.value.__cause__ is original
            assert "private failure" not in str(failure.value)
    sequence = [
        "assembly",
        "registry",
        "selection",
        "construction",
        "prepare",
        "execute",
        "validate_output",
        "serialize_output",
        "result",
    ]
    expected = (
        sequence[:4] if boundary == "json" else sequence[: sequence.index(boundary) + 1]
    )
    assert calls == expected
    result.assert_not_called()
    if boundary in {"construction", "json"}:
        workflow.prepare.assert_not_called()


def test_alias_input_phase_and_type_are_safe(tmp_path: Path) -> None:
    selected = tmp_path / "settings.yaml"
    selected.write_text(
        FIXTURE.read_text() + "  customer-job: {implementation: shared_state}\n"
    )
    with pytest.raises(WorkflowInputError) as failure:
        run_workflow("customer-job", '{"initial":true}', config_path=str(selected))
    message = str(failure.value)
    assert "customer-job PREPARE" in message and "initial (int_type)" in message
    assert "true" not in message and "wf-02" not in message


def test_real_runner_import_order_and_unused_flows_in_fresh_process() -> None:
    script = """
import builtins, os, sys
for key in ('AGENT_PLAYBOOK_CREWAI_USAGE_TELEMETRY_ENABLED', 'AGENT_PLAYBOOK_CREWAI_TRACING_ENABLED', 'AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS'):
    os.environ.pop(key, None)
os.environ['CREWAI_DISABLE_TELEMETRY'] = 'false'
os.environ['CREWAI_TRACING_ENABLED'] = 'true'
original = builtins.__import__
framework_attempts = []
def guard(name, *args, **kwargs):
    if name in ('agent_playbook.workflows.wf_02_shared_state.flow', 'agent_playbook.workflows.wf_03_conditional_route.flow'):
        raise AssertionError('unused flow imported: ' + name)
    if name == 'crewai' or name.startswith('crewai.') or name == 'crewai_core' or name.startswith('crewai_core.'):
        framework_attempts.append(name)
        assert os.environ['CREWAI_DISABLE_TELEMETRY'] == 'true', 'telemetry not configured before framework import'
        assert os.environ['CREWAI_TRACING_ENABLED'] == 'false', 'tracing not configured before framework import'
    return original(name, *args, **kwargs)
builtins.__import__ = guard
from agent_playbook.application.workflow_registry import workflow_registry
assert set(workflow_registry()) == {'step_sequence', 'shared_state', 'conditional_route'}
assert not framework_attempts
assert not any(name == 'crewai' or name.startswith('crewai.') or name == 'crewai_core' or name.startswith('crewai_core.') for name in sys.modules)
from agent_playbook.application.workflow_runner import run_workflow
assert run_workflow(config_path=sys.argv[1]).serialized_output == '[Hello, workflow!]'
assert framework_attempts, 'framework import guard was never reached'
assert 'agent_playbook.workflows.wf_02_shared_state.flow' not in sys.modules
assert 'agent_playbook.workflows.wf_03_conditional_route.flow' not in sys.modules
"""
    result = subprocess.run(
        [sys.executable, "-I", "-c", script, str(FIXTURE)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_blocked_selected_flow_is_prepare_error_and_cli_exit_one(
    tmp_path: Path,
) -> None:
    script = """
import builtins, sys
original = builtins.__import__
def guard(name, *args, **kwargs):
    if name == 'agent_playbook.workflows.wf_03_conditional_route.flow':
        raise ModuleNotFoundError('private package')
    return original(name, *args, **kwargs)
builtins.__import__ = guard
from agent_playbook.cli.commands import main
assert main(['dev-run','--config',sys.argv[1],'--workflow','wf-03']) == 1
"""
    result = subprocess.run(
        [sys.executable, "-I", "-c", script, str(FIXTURE)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert (
        "wf-03 PREPARE failed" in result.stderr
        and "private package" not in result.stderr
    )
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize(
    "method", ["prepare", "execute", "validate_output", "serialize_output"]
)
def test_order_error_at_public_boundary_is_execution_category(method: str) -> None:
    workflow = RichWorkflow(settings=SETTINGS, config={})
    original = WorkflowOrderError("wrong order")
    with (
        patch.object(workflow, method, side_effect=original),
        patch(
            "agent_playbook.application.workflow_runner.assemble_runtime",
            return_value=APPLICATION,
        ),
        patch(
            "agent_playbook.application.workflow_runner.workflow_registry",
            return_value={"test": RichWorkflow},
        ),
        patch(
            "agent_playbook.application.workflow_runner.construct_workflow",
            return_value=workflow,
        ),
    ):
        with pytest.raises(
            WorkflowExecutionError, match=f"customer-job {method.upper()}"
        ) as failure:
            run_workflow("customer-job")
    assert failure.value.__cause__ is original


def test_unused_implementation_constructor_never_runs() -> None:
    from agent_playbook.workflows.wf_03_conditional_route.workflow import (
        ConditionalRouteWorkflow,
    )

    fixture_application = ApplicationSettings(
        integrations=IntegrationSettings(crewai=SETTINGS),
        workflows={
            "wf-01": {"implementation": "step_sequence"},
            "unused": {"implementation": "conditional_route"},
        },
    )
    with (
        patch(
            "agent_playbook.application.workflow_runner.assemble_runtime",
            return_value=fixture_application,
        ),
        patch.object(
            ConditionalRouteWorkflow,
            "__init__",
            side_effect=AssertionError("unused constructed"),
        ) as constructor,
    ):
        assert run_workflow("wf-01").output == "[Hello, workflow!]"
    constructor.assert_not_called()


def test_execute_input_named_exception_is_execution_failure() -> None:
    workflow = RichWorkflow(settings=SETTINGS, config={})
    original = WorkflowInputError("private")
    with (
        patch.object(workflow, "_execute", side_effect=original),
        patch(
            "agent_playbook.application.workflow_runner.assemble_runtime",
            return_value=APPLICATION,
        ),
        patch(
            "agent_playbook.application.workflow_runner.workflow_registry",
            return_value={"test": RichWorkflow},
        ),
        patch(
            "agent_playbook.application.workflow_runner.construct_workflow",
            return_value=workflow,
        ),
    ):
        with pytest.raises(
            WorkflowExecutionError, match="customer-job EXECUTE"
        ) as failure:
            run_workflow("customer-job")
    assert failure.value.__cause__ is original
    assert "private" not in str(failure.value)


def test_prepare_state_construction_validation_error_is_execution_failure() -> None:
    workflow = RichWorkflow(settings=SETTINGS, config={})
    original = ValidationError.from_exception_data(
        "State", [{"type": "int_type", "loc": ("value",), "input": True}]
    )
    with (
        patch.object(workflow, "_prepare", side_effect=original),
        patch(
            "agent_playbook.application.workflow_runner.assemble_runtime",
            return_value=APPLICATION,
        ),
        patch(
            "agent_playbook.application.workflow_runner.workflow_registry",
            return_value={"test": RichWorkflow},
        ),
        patch(
            "agent_playbook.application.workflow_runner.construct_workflow",
            return_value=workflow,
        ),
    ):
        with pytest.raises(
            WorkflowExecutionError, match="customer-job PREPARE"
        ) as failure:
            run_workflow("customer-job")
    assert failure.value.__cause__ is original


@pytest.mark.parametrize(
    "hook,phase",
    [
        ("_validate_output", "VALIDATE_OUTPUT"),
        ("_serialize_output", "SERIALIZE_OUTPUT"),
    ],
)
def test_alias_output_phase_is_safe_and_precise(
    tmp_path: Path, hook: str, phase: str
) -> None:
    from agent_playbook.workflows.wf_02_shared_state.workflow import SharedStateWorkflow

    selected = tmp_path / "settings.yaml"
    selected.write_text(
        FIXTURE.read_text() + "  customer-job: {implementation: shared_state}\n"
    )
    original = ValueError("private-result")
    with patch.object(SharedStateWorkflow, hook, side_effect=original):
        with pytest.raises(
            WorkflowExecutionError, match=f"customer-job {phase} failed"
        ) as failure:
            run_workflow("customer-job", config_path=str(selected))
    assert failure.value.__cause__ is original
    assert "private-result" not in str(failure.value)
