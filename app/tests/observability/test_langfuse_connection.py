"""Langfuse settings and explicit check behavior, without a live service."""

from pathlib import Path
from unittest.mock import Mock, patch

import httpx
import pytest
from langfuse.api.core.api_error import ApiError
from pydantic import SecretStr

from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.loader import load_configuration
from agent_playbook.config.models import LangfuseSettings
from agent_playbook.observability.adapters.langfuse import connection
from tooling.observability.check_connection import main

BASE = Path(__file__).parents[1] / "fixtures/offline.yaml"


def config(tmp_path: Path, addition: str = "") -> Path:
    path = tmp_path / "application.yaml"
    path.write_text(BASE.read_text() + addition)
    empty_secrets = Path(__file__).parents[1] / "fixtures/empty-secrets.env"
    (tmp_path / empty_secrets.name).write_text(empty_secrets.read_text())
    return path


def test_old_yaml_defaults_to_disabled_without_client(tmp_path: Path) -> None:
    settings = load_configuration(str(config(tmp_path))).integrations.langfuse
    assert not settings.enabled
    with patch.object(connection, "LangfuseAPI", side_effect=AssertionError):
        assert connection.check_connection(settings).status == "skipped"


def test_local_and_environment_precedence_and_private_keys(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = config(tmp_path)
    path.with_name("application.local.yaml").write_text(
        "integrations:\n  langfuse:\n    enabled: true\n"
        "    base_url: http://localhost:3000\n"
        "    public_key: {env: TEST_PUBLIC_KEY}\n"
        "    secret_key: {env: TEST_SECRET_KEY}\n"
    )
    monkeypatch.setenv("TEST_PUBLIC_KEY", "pk-lf-private-marker")
    monkeypatch.setenv("TEST_SECRET_KEY", "sk-lf-private-marker")
    monkeypatch.setenv("AGENT_PLAYBOOK_LANGFUSE_BASE_URL", "http://localhost:33000")
    settings = load_configuration(str(path)).integrations.langfuse
    assert settings.enabled and settings.base_url == "http://localhost:33000"
    assert settings.secret_key is not None
    assert "private-marker" not in repr(settings)
    monkeypatch.setenv("AGENT_PLAYBOOK_LANGFUSE_ENABLED", "false")
    assert not load_configuration(str(path)).integrations.langfuse.enabled


@pytest.mark.parametrize(
    "addition",
    [
        "integrations:\n  langfuse:\n    enabled: true\n",
        "integrations:\n  langfuse:\n    enabled: true\n    public_key: marker\n",
        "integrations:\n  langfuse:\n    public_key: {name: marker}\n",
        "integrations:\n  langfuse:\n    base_url: ftp://marker\n",
        "integrations:\n  langfuse:\n    base_url: http://marker@localhost:3000\n",
        "integrations:\n  langfuse:\n    unknown: marker\n",
        "integrations:\n  langfuse:\n    enabled: 'true'\n",
    ],
)
def test_invalid_settings_are_sanitized(tmp_path: Path, addition: str) -> None:
    path = config(tmp_path)
    path.with_name("application.local.yaml").write_text(addition)
    with pytest.raises(ConfigurationError) as error:
        load_configuration(str(path))
    assert "marker" not in str(error.value)


def test_missing_enabled_key_reference_is_sanitized(tmp_path: Path) -> None:
    path = config(tmp_path)
    path.with_name("application.local.yaml").write_text(
        "integrations:\n  langfuse:\n    enabled: true\n"
        "    public_key: {env: SECRET_MARKER}\n"
    )
    with pytest.raises(ConfigurationError) as error:
        load_configuration(str(path))
    assert "SECRET_MARKER" not in str(error.value)


def enabled() -> LangfuseSettings:
    return LangfuseSettings(
        enabled=True,
        public_key=SecretStr("pk-lf-test"),
        secret_key=SecretStr("sk-lf-test"),
    )


def test_connection_statuses_and_cleanup() -> None:
    client = Mock()
    client.projects.get.return_value.data = [object()]
    with patch.object(connection, "LangfuseAPI", return_value=client):
        assert connection.check_connection(enabled()).status == "ok"
    client.projects.get.assert_called_once_with()

    for error, expected in (
        (ApiError(status_code=401, body="private-marker"), "auth_failed"),
        (httpx.ConnectError("private-marker"), "unreachable"),
        (RuntimeError("private-marker"), "failed"),
    ):
        client = Mock()
        client.projects.get.side_effect = error
        with patch.object(connection, "LangfuseAPI", return_value=client):
            result = connection.check_connection(enabled())
        assert result.status == expected
        assert "private-marker" not in repr(result)


def test_client_is_bounded_and_does_not_instrument() -> None:
    with patch.object(connection, "LangfuseAPI") as sdk:
        sdk.return_value.projects.get.return_value.data = [object()]
        assert connection.check_connection(enabled()).status == "ok"
    assert sdk.call_args.kwargs["httpx_client"].timeout.read == 5


def test_checker_exit_codes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = config(tmp_path)
    assert main(["--config", str(path)]) == 3
    assert "disabled" in capsys.readouterr().out

    with patch("tooling.observability.check_connection.check_connection") as check:
        check.return_value = connection.ConnectionResult("ok", "http://localhost:3000")
        assert main(["--config", str(path)]) == 0
        check.return_value = connection.ConnectionResult(
            "auth_failed", "http://localhost:3000"
        )
        assert main(["--config", str(path)]) == 1
    path.write_text("integrations: marker\n")
    assert main(["--config", str(path)]) == 2
    assert "marker" not in capsys.readouterr().out


def test_checker_reports_missing_selected_secrets_file_safely(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    path = config(tmp_path)
    path.with_name("application.local.yaml").write_text(
        "secrets:\n  file: missing-secrets.env\n"
    )
    assert main(["--config", str(path)]) == 2
    output = capsys.readouterr().out
    assert "Cannot read secrets file" in output
    assert "private-marker" not in output


def test_checker_reports_missing_required_key_without_values(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    path = config(tmp_path)
    path.with_name("application.local.yaml").write_text(
        "integrations:\n  langfuse:\n    enabled: true\n"
        "    public_key: {env: LANGFUSE_PUBLIC_KEY}\n"
        "    secret_key: {env: LANGFUSE_SECRET_KEY}\n"
    )
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-private-marker")
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    assert main(["--config", str(path)]) == 2
    output = capsys.readouterr().out
    assert "Required Langfuse secret_key environment variable is missing" in output
    assert "private-marker" not in output
