"""Selected YAML schema, overlays, defaults and redacted diagnostics."""

from pathlib import Path

import pytest
import yaml

from agent_playbook.application.workflow_runner import run_workflow
from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.loader import StrictLoader, load_configuration
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


_YAML_DEFECTS = (
    ("root_duplicate", "Duplicate YAML key"),
    ("unused_nested_duplicate", "Duplicate YAML key"),
    ("unused_merge", "YAML merge keys are unsupported"),
    ("unused_complex_key", "Invalid YAML key"),
    ("unused_numeric_key", "Invalid YAML key"),
    ("malformed", None),
    ("unsupported_tag", "could not determine a constructor"),
)


def yaml_pair(kind: str, *, local: bool) -> tuple[str, str]:
    prefix = "workflows:\n" if local else FIXTURE.read_text()
    if kind == "root_duplicate":
        return (
            ("workflows: {}\nworkflows: {}\n", "workflows: {}\n")
            if local
            else (prefix + "workflows: {}\n", prefix)
        )
    if kind == "unused_nested_duplicate":
        return (
            prefix + "  unused: {config: {x: 1, x: 2}}\n",
            prefix + "  unused: {config: {x: 1}}\n",
        )
    if kind == "unused_merge":
        return (
            prefix + "  unused: {config: {<<: {x: 1}}}\n",
            prefix + "  unused: {config: {x: 1}}\n",
        )
    if kind == "unused_complex_key":
        return (
            prefix + "  unused: {config: {[complex, key]: 1}}\n",
            prefix + "  unused: {config: {x: 1}}\n",
        )
    if kind == "unused_numeric_key":
        return (
            prefix + "  unused: {config: {3: 1}}\n",
            prefix + "  unused: {config: {x: 1}}\n",
        )
    if kind == "malformed":
        return prefix + "  unused: [\n", prefix + "  unused: []\n"
    if kind == "unsupported_tag":
        return (
            prefix + "  unused: !!python/tuple [1, 2]\n",
            prefix + "  unused: [1, 2]\n",
        )
    raise AssertionError(f"Unknown fixture kind: {kind}")


@pytest.mark.parametrize("kind,reason", _YAML_DEFECTS)
@pytest.mark.parametrize("local", [False, True], ids=["base", "local"])
def test_yaml_parse_rejects_keys_and_tags_in_both_files(
    tmp_path: Path, kind: str, reason: str | None, local: bool
) -> None:
    selected = tmp_path / "application.yaml"
    overlay = selected.with_name("application.local.yaml")
    defect, control = yaml_pair(kind, local=local)
    selected.write_text(FIXTURE.read_text() if local else control)
    if local:
        overlay.write_text(control)
    assert load_configuration(str(selected)).workflows
    target = overlay if local else selected
    target.write_text(defect)
    with pytest.raises(yaml.YAMLError) as parser_failure:
        yaml.load(defect, Loader=StrictLoader)
    if reason is not None:
        assert reason in str(parser_failure.value)
    with pytest.raises(ConfigurationError) as public_failure:
        load_configuration(str(selected))
    assert "Cannot read configuration" in str(public_failure.value)
    assert "unused:" not in str(public_failure.value)
    target.write_text(control)
    assert load_configuration(str(selected)).workflows


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
