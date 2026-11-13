"""Selected YAML schema, overlays, defaults and redacted diagnostics."""

from pathlib import Path

import pytest

from agent_playbook.application.workflow_runner import run_workflow
from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.loader import load_configuration
from agent_playbook.workflows.errors import WorkflowInputError

FIXTURE = Path(__file__).parents[1] / "fixtures/offline.yaml"


def config_file(tmp_path: Path, entry: str = "{implementation: shared_state}") -> Path:
    selected = tmp_path / "application.yaml"
    selected.write_text(FIXTURE.read_text() + f"  customer-job: {entry}\n")
    return selected


@pytest.mark.parametrize(
    "entry",
    [
        "null",
        "[]",
        "3",
        "{}",
        "{implementation: null}",
        "{implementation: 3}",
        "{implementation: ''}",
        "{implementation: ' shared_state'}",
        "{implementation: unknown}",
        "{implementation: shared_state, enabled: 'false'}",
        "{implementation: shared_state, enabled: 0}",
        "{implementation: shared_state, enabled: null}",
        "{implementation: shared_state, name: ''}",
        "{implementation: shared_state, name: null}",
        "{implementation: shared_state, name: ' bad '}",
        "{implementation: shared_state, name: 4}",
        "{implementation: shared_state, config: null}",
        "{implementation: shared_state, config: []}",
        "{implementation: shared_state, config: 3}",
        "{implementation: shared_state, extra: 1}",
    ],
)
def test_invalid_selected_entry(tmp_path: Path, entry: str) -> None:
    selected = config_file(tmp_path, entry)
    with pytest.raises(ConfigurationError) as failure:
        run_workflow("customer-job", config_path=str(selected))
    assert "customer-job" in str(failure.value)


@pytest.mark.parametrize("workflow_id", ["", " ", " missing ", "missing"])
def test_invalid_or_missing_selected_id(tmp_path: Path, workflow_id: str) -> None:
    selected = config_file(tmp_path)
    with pytest.raises(WorkflowInputError):
        run_workflow(workflow_id, config_path=str(selected))


@pytest.mark.parametrize(
    "entry",
    [
        "{implementation: step_sequence, config: {extra: 1}}",
        "{implementation: shared_state, config: {defaults: null}}",
        "{implementation: shared_state, config: {defaults: []}}",
        "{implementation: shared_state, config: {defaults: 2}}",
        "{implementation: shared_state, config: {defaults: {initial: true}}}",
        "{implementation: shared_state, config: {defaults: {initial: 1.5}}}",
        "{implementation: shared_state, config: {defaults: {initial: '2'}}}",
        "{implementation: shared_state, config: {defaults: {initial: 1001}}}",
        "{implementation: shared_state, config: {defaults: {other: 1}}}",
        "{implementation: shared_state, config: {other: 1}}",
        "{implementation: conditional_route, config: {defaults: null}}",
        "{implementation: conditional_route, config: {defaults: []}}",
        "{implementation: conditional_route, config: {defaults: 2}}",
        "{implementation: conditional_route, config: {defaults: {score: true}}}",
        "{implementation: conditional_route, config: {defaults: {score: 1.5}}}",
        "{implementation: conditional_route, config: {defaults: {score: -1}}}",
        "{implementation: conditional_route, config: {defaults: {score: 101}}}",
        "{implementation: conditional_route, config: {defaults: {other: 1}}}",
    ],
)
def test_invalid_selected_implementation_settings(tmp_path: Path, entry: str) -> None:
    selected = config_file(tmp_path, entry)
    with pytest.raises(ConfigurationError) as failure:
        run_workflow("customer-job", '{"initial":2}', config_path=str(selected))
    assert "customer-job CONFIGURATION" in str(failure.value)
    assert "true" not in str(failure.value)
    if "initial: true" in entry:
        assert "defaults.initial (int_type)" in str(failure.value)


def test_overlays_and_alias_defaults_are_independent(tmp_path: Path) -> None:
    selected = config_file(
        tmp_path,
        "{implementation: shared_state, config: {defaults: {initial: 10, increment: -2, multiplier: 3}}}",
    )
    local = selected.with_name("application.local.yaml")
    local.write_text("workflows: {}\n")
    assert run_workflow("customer-job", config_path=str(selected)).output == 24
    assert (
        run_workflow("customer-job", '{"initial":2}', config_path=str(selected)).output
        == 0
    )
    assert run_workflow("customer-job", config_path=str(selected)).output == 24
    assert run_workflow("wf-02", config_path=str(selected)).output == 20
    local.write_text(
        "workflows:\n  customer-job:\n    config:\n      defaults:\n        increment: 0\n"
    )
    assert run_workflow("customer-job", config_path=str(selected)).output == 30
    local.write_text("workflows:\n  customer-job:\n    enabled: false\n")
    with pytest.raises(WorkflowInputError):
        run_workflow("customer-job", config_path=str(selected))
    local.write_text("workflows:\n  customer-job: null\n")
    with pytest.raises(ConfigurationError):
        run_workflow("customer-job", config_path=str(selected))


def test_score_alias_default_and_override(tmp_path: Path) -> None:
    selected = config_file(
        tmp_path, "{implementation: conditional_route, config: {defaults: {score: 59}}}"
    )
    assert (
        run_workflow("customer-job", config_path=str(selected)).output == "needs_work"
    )
    assert (
        run_workflow("customer-job", '{"score":60}', config_path=str(selected)).output
        == "pass"
    )
    assert (
        run_workflow("customer-job", config_path=str(selected)).output == "needs_work"
    )


@pytest.mark.parametrize(
    "fragment",
    [
        "root: 1\nroot: 2\n",
        "workflows:\n  unused: {config: {x: 1, x: 2}}\n",
        "workflows:\n  unused: {config: {<<: {x: 1}}}\n",
        "workflows:\n  [complex, key]: 1\n",
        "workflows:\n  3: 1\n",
        "workflows: [\n",
        "workflows: !!python/object/apply:os.system ['echo private']\n",
    ],
)
@pytest.mark.parametrize("local", [False, True])
def test_yaml_parse_rejects_keys_and_tags_in_both_files(
    tmp_path: Path, fragment: str, local: bool
) -> None:
    selected = config_file(tmp_path)
    target = selected.with_name("application.local.yaml") if local else selected
    target.write_text(fragment + (FIXTURE.read_text() if not local else ""))
    with pytest.raises(ConfigurationError):
        load_configuration(str(selected))


def test_unused_invalid_entries_are_inert(tmp_path: Path) -> None:
    selected = config_file(tmp_path)
    selected.write_text(
        selected.read_text()
        + "  unused: {implementation: unknown, config: {defaults: {initial: secret-marker}}}\n  broken: null\n"
    )
    assert (
        run_workflow("wf-01", config_path=str(selected)).output == "[Hello, workflow!]"
    )


def test_alias_configuration_error_redacts_source_values(tmp_path: Path) -> None:
    selected = config_file(
        tmp_path,
        "{implementation: shared_state, config: {defaults: {initial: secret-marker}}}",
    )
    with pytest.raises(ConfigurationError) as failure:
        run_workflow("customer-job", config_path=str(selected))
    message = str(failure.value)
    assert "customer-job CONFIGURATION" in message
    assert "defaults.initial (int_type)" in message
    assert "secret-marker" not in message
    assert "{initial:" not in message
