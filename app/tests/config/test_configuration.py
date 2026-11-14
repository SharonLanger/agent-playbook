"""Configuration precedence, validation, privacy and framework startup boundaries."""

import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from agent_playbook.cli import commands
from agent_playbook.config import paths
from agent_playbook.config.crewai import configure_crewai
from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.loader import load_configuration

FIXTURE = Path(__file__).parents[1] / "fixtures/offline.yaml"
EMPTY_SECRETS = Path(__file__).parents[1] / "fixtures/empty-secrets.env"


def copy_empty_secrets(directory: Path) -> None:
    (directory / EMPTY_SECRETS.name).write_text(EMPTY_SECRETS.read_text())


def copy_config(tmp_path: Path) -> Path:
    selected = tmp_path / "application.yaml"
    selected.write_text(FIXTURE.read_text())
    copy_empty_secrets(tmp_path)
    return selected


def test_explicit_secrets_file_resolves_references_and_reloads_without_mutation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    selected = copy_config(tmp_path)
    selected.with_name("application.local.yaml").write_text(
        "secrets:\n  file: secrets.env\n"
        "integrations:\n"
        "  crewai:\n"
        "    show_framework_events: {env: FLOW_EVENTS}\n"
        "  langfuse:\n"
        "    public_key: {env: LANGFUSE_PUBLIC_KEY}\n"
        "    secret_key: {env: LANGFUSE_SECRET_KEY}\n"
    )
    secrets = tmp_path / "secrets.env"
    marker = tmp_path / "must-not-be-created"
    secrets.write_text(
        "# private values are parsed, never executed\n"
        "\n"
        "FLOW_EVENTS = 'true' # single quoted\n"
        'LANGFUSE_PUBLIC_KEY="pk-\\"placeholder\\""\n'
        "LANGFUSE_SECRET_KEY=sk-placeholder\n"
        "AGENT_PLAYBOOK_LANGFUSE_ENABLED=true\n"
        "AGENT_PLAYBOOK_LANGFUSE_BASE_URL=http://localhost:3000\n"
        f"INERT=$(touch {marker})\n"
    )
    monkeypatch.delenv("FLOW_EVENTS", raising=False)
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    monkeypatch.delenv("AGENT_PLAYBOOK_LANGFUSE_ENABLED", raising=False)
    before = os.environ.copy()

    settings = load_configuration(str(selected))
    assert settings.integrations.crewai.show_framework_events
    assert settings.integrations.langfuse.enabled
    assert settings.integrations.langfuse.public_key is not None
    assert (
        settings.integrations.langfuse.public_key.get_secret_value()
        == 'pk-"placeholder"'
    )
    assert not marker.exists()
    assert os.environ == before

    secrets.write_text(
        secrets.read_text().replace("FLOW_EVENTS = 'true'", "FLOW_EVENTS = 'false'")
    )
    assert not load_configuration(
        str(selected)
    ).integrations.crewai.show_framework_events
    assert os.environ == before


def test_process_environment_wins_even_when_explicitly_empty(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    selected = copy_config(tmp_path)
    selected.with_name("application.local.yaml").write_text(
        "secrets:\n  file: secrets.env\n"
        "integrations:\n"
        "  langfuse:\n"
        "    enabled: true\n"
        "    public_key: {env: LANGFUSE_PUBLIC_KEY}\n"
        "    secret_key: {env: LANGFUSE_SECRET_KEY}\n"
    )
    secrets = tmp_path / "secrets.env"
    secrets.write_text("LANGFUSE_PUBLIC_KEY=pk-file\nLANGFUSE_SECRET_KEY=sk-file\n")
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-process")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "")
    with pytest.raises(ConfigurationError, match="Required Langfuse secret_key"):
        load_configuration(str(selected))
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-process")
    settings = load_configuration(str(selected))
    assert settings.integrations.langfuse.public_key is not None
    assert settings.integrations.langfuse.public_key.get_secret_value() == "pk-process"
    assert settings.integrations.langfuse.secret_key is not None
    assert settings.integrations.langfuse.secret_key.get_secret_value() == "sk-process"


def test_missing_required_secret_reference_is_still_an_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    selected = copy_config(tmp_path)
    selected.write_text(
        selected.read_text().replace(
            "show_framework_events: false",
            "show_framework_events: {env: MISSING_FLOW_VALUE}",
        )
    )
    secrets = tmp_path / "empty-secrets.env"
    secrets.write_text("")
    monkeypatch.delenv("MISSING_FLOW_VALUE", raising=False)
    with pytest.raises(ConfigurationError, match="MISSING_FLOW_VALUE is missing"):
        load_configuration(str(selected))


@pytest.mark.parametrize(
    "contents",
    [
        "LANGFUSE_SECRET_KEY=secret-marker\nBROKEN_LINE\n",
        "LANGFUSE_SECRET_KEY='unterminated-secret-marker\n",
        "LANGFUSE_SECRET_KEY=first\nLANGFUSE_SECRET_KEY=secret-marker\n",
        "AGENT_PLAYBOOK_CONFIG=/tmp/redirect.yaml\n",
    ],
)
def test_secrets_file_errors_are_sanitized(tmp_path: Path, contents: str) -> None:
    selected = copy_config(tmp_path)
    secrets = tmp_path / "secrets.env"
    secrets.write_text(contents)
    selected.with_name("application.local.yaml").write_text(
        "secrets:\n  file: secrets.env\n"
    )
    with pytest.raises(ConfigurationError) as failure:
        load_configuration(str(selected))
    assert "secret-marker" not in str(failure.value)
    assert "BROKEN_LINE" not in str(failure.value)


def test_missing_secrets_file_path_is_clear(tmp_path: Path) -> None:
    selected = copy_config(tmp_path)
    missing = tmp_path / "missing-secrets.env"
    selected.with_name("application.local.yaml").write_text(
        f"secrets:\n  file: {missing.name}\n"
    )
    with pytest.raises(ConfigurationError, match="Cannot read secrets file"):
        load_configuration(str(selected))


def test_blank_secrets_file_path_is_clear(tmp_path: Path) -> None:
    selected = copy_config(tmp_path)
    selected.with_name("application.local.yaml").write_text("secrets:\n  file: '  '\n")
    with pytest.raises(ConfigurationError, match="secrets.file"):
        load_configuration(str(selected))


def test_secrets_path_expands_home_and_relative_paths_use_yaml_parent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    selected = copy_config(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("FLOW_VALUE", raising=False)
    # A stale selector from the previous implementation must have no effect.
    monkeypatch.setenv(
        "AGENT_PLAYBOOK_SECRETS_FILE", str(tmp_path / "must-not-be-read.env")
    )
    private = tmp_path / ".config/agent-playbook/secrets.env"
    private.parent.mkdir(parents=True)
    private.write_text("FLOW_VALUE=true\n")
    selected.with_name("application.local.yaml").write_text(
        "secrets:\n  file: ~/.config/agent-playbook/secrets.env\n"
        "integrations:\n  crewai:\n    show_framework_events: {env: FLOW_VALUE}\n"
    )
    assert load_configuration(str(selected)).integrations.crewai.show_framework_events

    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    selected.with_name("application.local.yaml").write_text(
        "secrets:\n  file: relative-secrets.env\n"
        "integrations:\n  crewai:\n    show_framework_events: {env: FLOW_VALUE}\n"
    )
    (tmp_path / "relative-secrets.env").write_text("FLOW_VALUE=false\n")
    assert not load_configuration(
        str(selected)
    ).integrations.crewai.show_framework_events


def test_selected_secrets_file_does_not_enable_disabled_langfuse(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    selected = copy_config(tmp_path)
    selected.with_name("application.local.yaml").write_text(
        "secrets:\n  file: secrets.env\n"
        "integrations:\n"
        "  langfuse:\n"
        "    public_key: {env: LANGFUSE_PUBLIC_KEY}\n"
        "    secret_key: {env: LANGFUSE_SECRET_KEY}\n"
    )
    secrets = tmp_path / "secrets.env"
    secrets.write_text(
        "LANGFUSE_PUBLIC_KEY=pk-placeholder\nLANGFUSE_SECRET_KEY=sk-placeholder\n"
    )
    monkeypatch.delenv("AGENT_PLAYBOOK_LANGFUSE_ENABLED", raising=False)
    settings = load_configuration(str(selected)).integrations.langfuse
    assert not settings.enabled
    assert settings.public_key is None and settings.secret_key is None


def test_nested_local_overlay_environment_precedence_and_reload(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    selected = copy_config(tmp_path)
    local = tmp_path / "application.local.yaml"
    local.write_text("integrations:\n  crewai:\n    show_framework_events: true\n")
    settings = load_configuration(str(selected)).integrations.crewai
    assert settings.show_framework_events
    assert not settings.tracing_enabled and not settings.usage_telemetry_enabled
    monkeypatch.setenv("AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS", "false")
    assert not load_configuration(
        str(selected)
    ).integrations.crewai.show_framework_events
    monkeypatch.delenv("AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS")
    local.write_text("integrations:\n  crewai:\n    show_framework_events: false\n")
    assert not load_configuration(
        str(selected)
    ).integrations.crewai.show_framework_events


def test_explicit_path_wins_and_development_default_ignores_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    selected = copy_config(tmp_path)
    monkeypatch.setenv("AGENT_PLAYBOOK_CONFIG", str(tmp_path / "missing.yaml"))
    load_configuration(str(selected))
    with pytest.raises(ConfigurationError, match="Cannot read"):
        load_configuration()
    monkeypatch.delenv("AGENT_PLAYBOOK_CONFIG")
    monkeypatch.chdir(tmp_path)
    assert (
        paths.configuration_path()
        == Path(paths.__file__).resolve().parents[3] / "application.yaml"
    )
    with patch.object(paths, "SOURCE_COMMIT", "installed-commit"):
        with pytest.raises(ConfigurationError, match="Select an external"):
            paths.configuration_path()


@pytest.mark.parametrize(
    "contents",
    [
        "[]",
        "null",
        "integrations: [",
        "integrations: {}",
        "integrations:\n  crewai:\n    tracing_enabled: secret-marker",
        FIXTURE.read_text() + "unknown: secret-marker\n",
        FIXTURE.read_text().replace("tracing_enabled: false", "tracing_enabled: 0"),
        FIXTURE.read_text().replace(
            "tracing_enabled: false", 'tracing_enabled: "false"'
        ),
        '!!python/object/apply:os.system ["touch should-not-exist"]',
    ],
)
def test_invalid_configuration_is_private_and_starts_no_steps(
    tmp_path: Path, contents: str, capsys: pytest.CaptureFixture[str]
) -> None:
    selected = tmp_path / "invalid.yaml"
    selected.write_text(contents)
    assert commands.main(["dev-run", "--config", str(selected)]) == 2
    captured = capsys.readouterr()
    assert "Configuration error" in captured.err
    assert "secret-marker" not in captured.err
    assert "started" not in captured.out
    assert not Path("should-not-exist").exists()


def test_environment_reference_and_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    selected = copy_config(tmp_path)
    selected.write_text(
        selected.read_text().replace(
            "show_framework_events: false",
            "show_framework_events: {env: MY_FLOW_EVENTS}",
        )
    )
    with pytest.raises(ConfigurationError, match="MY_FLOW_EVENTS is missing"):
        load_configuration(str(selected))
    monkeypatch.setenv("MY_FLOW_EVENTS", "true")
    assert load_configuration(str(selected)).integrations.crewai.show_framework_events
    monkeypatch.setenv("AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS", "false")
    assert not load_configuration(
        str(selected)
    ).integrations.crewai.show_framework_events
    monkeypatch.setenv("AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS", "secret-marker")
    with pytest.raises(ConfigurationError) as failure:
        load_configuration(str(selected))
    assert "secret-marker" not in str(failure.value)


def test_changed_import_settings_require_fresh_process(tmp_path: Path) -> None:
    selected = copy_config(tmp_path)
    selected.write_text(
        selected.read_text().replace("tracing_enabled: false", "tracing_enabled: true")
    )
    with pytest.raises(ConfigurationError, match="fresh process"):
        configure_crewai(load_configuration(str(selected)).integrations.crewai)


def test_invalid_configuration_precedes_framework_import(tmp_path: Path) -> None:
    selected = tmp_path / "missing.yaml"
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "from agent_playbook.cli.commands import main; "
            "import sys; code=main(['dev-run','--config',sys.argv[1]]); "
            "assert code == 2; assert 'crewai' not in sys.modules",
            str(selected),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_legacy_local_override_is_not_silently_ignored(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("AGENT_PLAYBOOK_CONFIG", raising=False)
    legacy = tmp_path / "configs/application.local.yaml"
    legacy.parent.mkdir()
    legacy.write_text("private-local-values")
    with patch.object(
        paths, "__file__", str(tmp_path / "src/agent_playbook/config/paths.py")
    ):
        with pytest.raises(ConfigurationError, match="Legacy local override"):
            paths.configuration_path()
        assert paths.configuration_path("explicit.yaml").name == "explicit.yaml"
        assert legacy.read_text() == "private-local-values"
        target = tmp_path / "application.local.yaml"
        target.write_text("current-local-values")
        with pytest.raises(ConfigurationError, match="Move or merge"):
            paths.configuration_path()
        assert target.read_text() == "current-local-values"
        legacy.unlink()
        assert paths.configuration_path() == tmp_path / "application.yaml"


def test_import_settings_are_applied_before_framework_import(tmp_path: Path) -> None:
    selected = copy_config(tmp_path)
    selected.write_text(
        selected.read_text().replace(
            "usage_telemetry_enabled: false", "usage_telemetry_enabled: true"
        )
    )
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "import os,sys; "
            "from agent_playbook.config.loader import load_configuration; "
            "from agent_playbook.config.crewai import configure_crewai; "
            "configure_crewai(load_configuration(sys.argv[1]).integrations.crewai); "
            "assert 'crewai' not in sys.modules; "
            "assert os.environ['CREWAI_DISABLE_TELEMETRY']=='false'; "
            "assert os.environ['CREWAI_TRACING_ENABLED']=='false'",
            str(selected),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_same_code_reads_edited_configuration_on_next_invocation(
    tmp_path: Path,
) -> None:
    selected = copy_config(tmp_path)
    env = os.environ.copy()
    env["AGENT_PLAYBOOK_CONFIG"] = str(selected)
    command = [sys.executable, "-I", "-m", "agent_playbook.cli", "dev-run"]
    first = subprocess.run(
        command, env=env, cwd=tmp_path, capture_output=True, text=True, timeout=60
    )
    selected.write_text(
        selected.read_text().replace(
            "show_framework_events: false", "show_framework_events: true"
        )
    )
    second = subprocess.run(
        command, env=env, cwd=tmp_path, capture_output=True, text=True, timeout=60
    )
    assert first.returncode == second.returncode == 0, first.stderr + second.stderr
    assert "result: [Hello, workflow!]" in first.stdout
    assert "result: [Hello, workflow!]" in second.stdout
    assert first.stdout != second.stdout


@pytest.mark.parametrize(
    "fragment",
    [
        "workflows:\n  wf-01: {}\n  wf-01: {}\n",
        "workflows:\n  unused:\n    config:\n      x: 1\n      x: 2\n",
        "workflows:\n  unused: {config: {x: 1, x: 2}}\n",
        "workflows:\n  unused: {config: {<<: {x: 1}}}\n",
        "workflows:\n  3: {}\n",
    ],
)
def test_invalid_yaml_keys_even_in_unused_entries(
    tmp_path: Path, fragment: str
) -> None:
    selected = copy_config(tmp_path)
    selected.write_text(selected.read_text().replace("workflows:\n", fragment, 1))
    with pytest.raises(ConfigurationError):
        load_configuration(str(selected))


def test_unused_invalid_entry_and_selected_alias(tmp_path: Path) -> None:
    selected = copy_config(tmp_path)
    selected.write_text(
        selected.read_text()
        + "  unused: {implementation: unknown, config: null}\n  custom: {implementation: shared_state, config: {defaults: {initial: 10, increment: -2, multiplier: 3}}}\n"
    )
    from agent_playbook.application.workflow_runner import run_workflow

    assert (
        run_workflow("wf-01", config_path=str(selected)).output == "[Hello, workflow!]"
    )
    result = run_workflow("custom", config_path=str(selected))
    assert result.output == 24 and result.serialized_output == "24"
    assert (
        run_workflow("custom", '{"initial":2}', config_path=str(selected)).output == 0
    )


@pytest.mark.parametrize(
    "suffix",
    [
        "",
        "workflows: null\n",
        "workflows: []\n",
        "workflows: 1\n",
    ],
)
def test_missing_or_nonmapping_workflow_catalog(tmp_path: Path, suffix: str) -> None:
    selected = tmp_path / "configuration.yaml"
    copy_empty_secrets(tmp_path)
    selected.write_text(FIXTURE.read_text().split("workflows:")[0] + suffix)
    with pytest.raises(ConfigurationError):
        load_configuration(str(selected))


def test_empty_catalog_is_valid_but_no_id_is_selected(tmp_path: Path) -> None:
    selected = tmp_path / "configuration.yaml"
    copy_empty_secrets(tmp_path)
    selected.write_text(FIXTURE.read_text().split("workflows:")[0] + "workflows: {}\n")
    assert load_configuration(str(selected)).workflows == {}
    from agent_playbook.application.workflow_runner import run_workflow
    from agent_playbook.workflows.errors import WorkflowInputError

    with pytest.raises(WorkflowInputError, match="Unknown workflow"):
        run_workflow("wf-01", config_path=str(selected))


def test_local_duplicate_keys_are_rejected(tmp_path: Path) -> None:
    selected = copy_config(tmp_path)
    selected.with_name("application.local.yaml").write_text(
        "workflows:\n  unused: {config: {x: 1, x: 2}}\n"
    )
    with pytest.raises(ConfigurationError):
        load_configuration(str(selected))


def test_invalid_default_cannot_be_hidden_by_input_override(tmp_path: Path) -> None:
    selected = copy_config(tmp_path)
    selected.write_text(
        selected.read_text()
        + "  bad: {implementation: shared_state, config: {defaults: {initial: 1001}}}\n"
    )
    from agent_playbook.application.workflow_runner import run_workflow

    with pytest.raises(ConfigurationError):
        run_workflow("bad", '{"initial":2}', config_path=str(selected))
