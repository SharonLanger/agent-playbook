"""Local management behavior without Docker or private settings."""

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tooling.observability import manage


@pytest.fixture(autouse=True)
def synthetic_project(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("COMPOSE_PROJECT_NAME", raising=False)
    monkeypatch.setattr(
        manage, "_resolve_project", MagicMock(return_value="observability")
    )
    monkeypatch.setattr(manage, "_inventory", MagicMock(return_value=set()))


def test_invalid_and_help_do_not_touch_docker_or_settings(tmp_path: Path) -> None:
    with (
        patch.object(manage, "_docker_ready", side_effect=AssertionError),
        patch.object(manage, "initialize", side_effect=AssertionError),
    ):
        for argv in (
            [],
            ["--start", "--stop"],
            ["--follow"],
            ["--check", "--env-file", str(tmp_path / "x")],
        ):
            with pytest.raises(SystemExit) as error:
                manage.main(argv)
            assert error.value.code == 2
        with pytest.raises(SystemExit) as error:
            manage.main(["--help"])
        assert error.value.code == 0


def test_first_repeat_start_and_stop_preserve_settings(tmp_path: Path) -> None:
    env_file = tmp_path / "private.env"
    calls: list[tuple[str, ...]] = []

    def compose(
        _env: Path, *args: str, **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        calls.append(args)
        return subprocess.CompletedProcess([], 0, "", "")

    with (
        patch.object(manage, "_docker_ready", return_value=True),
        patch.object(manage, "_compose", side_effect=compose),
        patch.object(
            manage, "_state", return_value=("running", "All six services are running.")
        ),
        patch.object(manage, "_health", return_value=True),
    ):
        assert manage.main(["--start", "--env-file", str(env_file)]) == 0
        initial = env_file.read_bytes()
        assert manage.main(["--start", "--env-file", str(env_file)]) == 0
        assert env_file.read_bytes() == initial
        assert manage.main(["--stop", "--env-file", str(env_file)]) == 0
        assert manage.main(["--stop", "--env-file", str(env_file)]) == 0
        assert env_file.read_bytes() == initial
    assert calls == [
        ("config", "--quiet"),
        ("up", "-d"),
        ("config", "--quiet"),
        ("up", "-d"),
        ("down",),
        ("down",),
    ]
    assert not any("-v" in call for call in calls)


def test_status_states_and_ports(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env_file = tmp_path / "private.env"
    env_file.write_text("LANGFUSE_PORT=33000\nMINIO_PORT=9191\n")
    with (
        patch.object(manage, "_docker_ready", return_value=True),
        patch.object(manage, "_health", return_value=True),
    ):
        with patch.object(manage, "_state", return_value=("running", "all running")):
            assert manage.main(["--status", "--env-file", str(env_file)]) == 0
            assert "http://localhost:33000" in capsys.readouterr().out
        for state in ("stopped", "starting", "unhealthy"):
            with patch.object(manage, "_state", return_value=(state, state)):
                assert manage.main(["--status", "--env-file", str(env_file)]) == 1


def test_compose_state_parses_json_array(tmp_path: Path) -> None:
    rows = [
        {
            "Service": service,
            "State": "running",
            "Health": "healthy"
            if service not in ("langfuse-web", "langfuse-worker")
            else "",
        }
        for service in manage.SERVICES
    ]
    with patch.object(
        manage,
        "_compose",
        return_value=subprocess.CompletedProcess([], 0, json.dumps(rows), ""),
    ):
        assert manage._state(tmp_path / "private.env", "observability")[0] == "running"  # pyright: ignore[reportPrivateUsage]


def test_missing_docker_and_browser_failure(tmp_path: Path) -> None:
    env_file = tmp_path / "private.env"
    env_file.write_text("LANGFUSE_PORT=3000\n")
    with (
        patch.object(manage, "_docker_ready", return_value=False),
        patch.object(manage, "_compose", side_effect=AssertionError),
    ):
        assert manage.main(["--status", "--env-file", str(env_file)]) == 1
    with patch.object(manage.webbrowser, "open", return_value=False):
        assert manage.main(["--open", "--env-file", str(env_file)]) == 1


def test_logs_follow_interrupt_does_not_stop(tmp_path: Path) -> None:
    env_file = tmp_path / "private.env"
    env_file.write_text("LANGFUSE_PORT=3000\n")
    process = MagicMock()
    process.stdout.__iter__.side_effect = KeyboardInterrupt
    with (
        patch.object(manage, "_docker_ready", return_value=True),
        patch.object(manage.subprocess, "Popen", return_value=process) as popen,
    ):
        assert manage.main(["--logs", "--follow", "--env-file", str(env_file)]) == 0
    assert popen.call_args.args[0][-4:] == ["logs", "--tail", "80", "--follow"]
    process.terminate.assert_called_once_with()


def test_service_logs_redact_secrets_and_auth_header(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env_file = tmp_path / "private.env"
    env_file.write_text("POSTGRES_PASSWORD=private-marker-123\nLANGFUSE_PORT=3000\n")
    result = subprocess.CompletedProcess(
        [], 0, "password private-marker-123 Authorization: Basic abc123\n", ""
    )
    with (
        patch.object(manage, "_docker_ready", return_value=True),
        patch.object(manage, "_compose", return_value=result),
    ):
        assert manage.main(["--logs", "--env-file", str(env_file)]) == 0
    output = capsys.readouterr().out
    assert "private-marker-123" not in output and "abc123" not in output


def test_missing_and_stopped_docker_engine_without_compose_start(
    tmp_path: Path,
) -> None:
    env_file = tmp_path / "private.env"
    env_file.write_text("LANGFUSE_PORT=3000\n")
    with (
        patch.object(manage.subprocess, "run", side_effect=FileNotFoundError),
        patch.object(manage, "_compose", side_effect=AssertionError),
    ):
        assert manage.main(["--start", "--env-file", str(env_file)]) == 1

    def stopped(
        command: list[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            command, 0 if command[-1] == "version" else 1
        )

    with (
        patch.object(manage.subprocess, "run", side_effect=stopped),
        patch.object(manage, "_compose", side_effect=AssertionError),
    ):
        assert manage.main(["--start", "--env-file", str(env_file)]) == 1


def test_start_timeout_and_unhealthy_are_failures(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    env_file = tmp_path / "private.env"
    env_file.write_text("LANGFUSE_PORT=3000\n")
    with (
        patch.object(manage, "_docker_ready", return_value=True),
        patch.object(
            manage, "_compose", return_value=subprocess.CompletedProcess([], 0, "", "")
        ),
        patch.object(manage, "_state", return_value=("unhealthy", "failed")),
    ):
        assert manage.main(["--start", "--env-file", str(env_file)]) == 1
    ticks = iter([0.0, 301.0])
    monkeypatch.setattr(manage.time, "monotonic", lambda: next(ticks, 302.0))
    with (
        patch.object(manage, "_docker_ready", return_value=True),
        patch.object(
            manage, "_compose", return_value=subprocess.CompletedProcess([], 0, "", "")
        ),
    ):
        assert manage.main(["--start", "--env-file", str(env_file)]) == 1


def test_fresh_checkout_status_and_stop_without_settings(tmp_path: Path) -> None:
    with (
        patch.object(manage, "DEPLOY", tmp_path),
        patch.object(manage, "_docker_ready", return_value=True),
        patch.object(
            manage.subprocess,
            "run",
            return_value=subprocess.CompletedProcess([], 0, "", ""),
        ),
        patch.object(manage, "_compose", side_effect=AssertionError),
    ):
        assert manage.main(["--status"]) == 1
        assert manage.main(["--stop"]) == 0
