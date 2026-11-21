"""Fake-Docker checks for service identity, guarded settings and work budgets."""

import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from agent_playbook.observability.adapters.otel_logging.connection import (
    ConnectionResult,
)
from tooling import service_runtime, services
from tooling.logging import manage as logs
from tooling.observability import manage as langfuse


def finished(
    code: int = 0, stdout: str = "", stderr: str = ""
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess([], code, stdout, stderr)


@pytest.mark.parametrize("container_state", ["stopped", "running", "unhealthy"])
def test_logging_uses_one_fixed_project_and_preserves_compose_contract(
    monkeypatch: pytest.MonkeyPatch,
    container_state: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    project = "agent-playbook-logging-smoke"
    monkeypatch.setenv("COMPOSE_PROJECT_NAME", "unrelated")
    document: dict[str, object] = yaml.safe_load(
        (logs.DEPLOY / "compose.yaml").read_text()
    )
    assert document == {
        "name": project,
        "services": {
            "victorialogs": {
                "image": "victoriametrics/victoria-logs:v1.54.0",
                "command": [
                    "-storageDataPath=/victoria-logs-data",
                    "-retentionPeriod=7d",
                ],
                "ports": ["127.0.0.1:9428:9428"],
                "volumes": ["logs-data:/victoria-logs-data"],
                "networks": ["logs-local"],
                "logging": {"driver": "local"},
            },
        },
        "networks": {"logs-local": {"driver": "bridge"}},
        "volumes": {"logs-data": {"driver": "local"}},
    }
    state = (
        []
        if container_state == "stopped"
        else [
            {
                "Service": "victorialogs",
                "State": "running",
                "Health": "unhealthy" if container_state == "unhealthy" else "",
            }
        ]
    )
    with (
        patch.object(logs, "docker_ready", return_value=True),
        patch.object(
            service_runtime.subprocess,
            "run",
            side_effect=[
                finished(stdout=json.dumps(state)),
                finished(),
                finished(),
            ],
        ) as docker,
        patch.object(
            logs, "check_connection", return_value=ConnectionResult("ok")
        ) as health,
    ):
        assert logs.main(["--status"]) == int(container_state != "running")
        assert logs.main(["--stop"]) == logs.main(["--stop"]) == 0
    prefix = [
        "docker",
        "compose",
        "--project-directory",
        str(logs.DEPLOY),
        "-p",
        project,
        "-f",
        str(logs.DEPLOY / "compose.yaml"),
    ]
    assert [call.args[0] for call in docker.call_args_list] == [
        prefix + ["ps", "--all", "--format", "json"],
        prefix + ["down"],
        prefix + ["down"],
    ]
    assert health.call_count == int(container_state == "running")
    assert project in capsys.readouterr().out


@pytest.mark.parametrize("override", [False, True])
def test_explicit_logging_start_is_independent_and_preserves_configuration(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, override: bool
) -> None:
    selected = tmp_path / "app.yaml"
    selected.write_text(
        "secrets: {file: test.env}\nintegrations: {logging: {enabled: false}}"
    )
    secrets = tmp_path / "test.env"
    secrets.write_text("AGENT_PLAYBOOK_LOGGING_ENABLED=true\n" if override else "")
    local = tmp_path / "app.local.yaml"
    local.write_text("integrations: {langfuse: {enabled: false}}")
    for key in ("AGENT_PLAYBOOK_LOGGING_ENABLED", "AGENT_PLAYBOOK_LANGFUSE_ENABLED"):
        monkeypatch.delenv(key, raising=False)
    if override:
        monkeypatch.setenv("AGENT_PLAYBOOK_LOGGING_ENABLED", "false")
    initial = [path.read_bytes() for path in (selected, local, secrets)]
    ps = finished(stdout='{"Service":"victorialogs","State":"running","Health":""}')
    with (
        patch.object(logs, "docker_ready", return_value=True),
        patch.object(
            service_runtime.subprocess,
            "run",
            side_effect=[finished(), finished(), ps] * 2,
        ) as docker,
        patch.object(logs, "check_connection", return_value=ConnectionResult("ok")),
        patch.object(services, "supervise_component", side_effect=AssertionError),
    ):
        assert services.main(["--start", "--config", str(selected)]) == 0
        assert logs.main(["--start"]) == logs.main(["--start"]) == 0
    assert [call.args[0][8:] for call in docker.call_args_list] == [
        ["config", "--quiet"],
        ["up", "-d"],
        ["ps", "--all", "--format", "json"],
    ] * 2
    assert all(
        call.args[0][5] == service_runtime.LOGGING_PROJECT
        for call in docker.call_args_list
    )
    assert initial == [path.read_bytes() for path in (selected, local, secrets)]


@pytest.mark.parametrize(
    ("failure", "code"),
    [
        ("engine", 1),
        ("config", 2),
        ("occupied", 1),
        ("unhealthy", 1),
        ("health timeout", 1),
    ],
)
def test_logging_failures_are_sanitized_and_never_roll_back(
    failure: str, code: int, capsys: pytest.CaptureFixture[str]
) -> None:
    results = {
        "engine": [finished(1, stderr="synthetic-secret-marker")],
        "config": [
            finished(),
            finished(),
            finished(1, stderr="synthetic-secret-marker"),
        ],
        "occupied": [
            finished(),
            finished(),
            finished(),
            finished(1, stderr="synthetic-secret-marker"),
        ],
        "unhealthy": [finished()] * 4
        + [
            finished(
                stdout='{"Service":"victorialogs","State":"running","Health":"unhealthy"}'
            )
        ],
        "health timeout": [finished()] * 4
        + [finished(stdout='{"Service":"victorialogs","State":"running"}')],
    }
    with (
        patch.object(
            service_runtime.subprocess, "run", side_effect=results[failure]
        ) as docker,
        patch.object(
            logs, "check_connection", side_effect=subprocess.TimeoutExpired("GET", 5)
        ),
    ):
        assert logs.main(["--start"]) == code
    assert all("down" not in call.args[0] for call in docker.call_args_list)
    output = capsys.readouterr()
    assert "synthetic-secret-marker" not in output.out + output.err


@pytest.mark.parametrize(
    "kind",
    [
        *sorted(langfuse.SERVICES),
        *sorted(langfuse.VOLUMES),
        "suffix-only",
        "ps-error",
        "volume-error",
    ],
)
def test_missing_settings_blocks_mutation_for_every_asset(
    tmp_path: Path, kind: str, capsys: pytest.CaptureFixture[str]
) -> None:
    settings = tmp_path / "missing.env"
    ps = (
        finished(stdout=f"old-project|{kind}\n")
        if kind in langfuse.SERVICES
        else finished()
    )
    volume = (
        finished(stdout=f"old-project_{kind}|old-project|{kind}\n")
        if kind in langfuse.VOLUMES
        else finished()
    )
    if kind == "suffix-only":
        volume = finished(stdout="old-project_clickhouse_logs||\n")
    if kind == "ps-error":
        ps = finished(1, stderr="synthetic-secret-marker")
    if kind == "volume-error":
        volume = finished(1, stderr="synthetic-secret-marker")
    with (
        patch.object(langfuse, "_docker_ready", return_value=True),
        patch.object(
            service_runtime.subprocess, "run", side_effect=[ps, volume] * 3
        ) as docker,
        patch.object(langfuse, "initialize", side_effect=AssertionError),
    ):
        for action in ("start", "status", "stop"):
            assert langfuse.main([f"--{action}", "--env-file", str(settings)]) == 2
    assert not settings.exists()
    assert [call.args[0][1] for call in docker.call_args_list] == ["ps", "volume"] * 3
    text = capsys.readouterr().err
    assert "restore the original" in text
    assert "synthetic-secret-marker" not in text
    if kind not in ("ps-error", "volume-error"):
        assert "old-project" in text and "readiness unknown" in text


@pytest.mark.parametrize("shell", ["", "shell-project"])
def test_langfuse_config_identity_controls_every_subsequent_operation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    shell: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    settings = tmp_path / "selected.env"
    initial = b"COMPOSE_PROJECT_NAME=file-project\nPOSTGRES_PASSWORD=synthetic-secret-marker\n"
    settings.write_bytes(initial)
    monkeypatch.setenv("COMPOSE_PROJECT_NAME", shell)
    project = shell or "file-project"
    lookup = finished(
        stdout=json.dumps({"name": project, "password": "synthetic-secret-marker"})
    )
    running = finished(
        stdout=json.dumps(
            [
                {"Service": service, "State": "running", "Health": ""}
                for service in langfuse.SERVICES
            ]
        )
    )
    with (
        patch.object(langfuse, "_docker_ready", return_value=True),
        patch.object(langfuse, "_health", return_value=True),
        patch.object(
            service_runtime.subprocess,
            "run",
            side_effect=[
                lookup,
                finished(),
                finished(),
                finished(),
                finished(),
                running,
                lookup,
                running,
                lookup,
                finished(),
            ],
        ) as docker,
        patch.object(langfuse, "initialize", side_effect=AssertionError),
    ):
        for action in ("start", "status", "stop"):
            assert langfuse.main([f"--{action}", "--env-file", str(settings)]) == 0
    commands = [call.args[0] for call in docker.call_args_list]
    exact_lookup = [
        "docker",
        "compose",
        "--project-directory",
        str(langfuse.DEPLOY),
        "--env-file",
        str(settings),
        "-f",
        str(langfuse.COMPOSE),
        "config",
        "--format",
        "json",
    ]
    assert commands[0] == commands[6] == commands[8] == exact_lookup
    assert f"label=com.docker.compose.project={project}" in commands[1]
    expected_names = "|".join(
        sorted(f"{project}_{volume}" for volume in langfuse.VOLUMES)
    )
    assert f"name=^({expected_names})$" in commands[2]
    for index in (3, 4, 5, 7, 9):
        assert commands[index][6:10] == ["-p", project, "-f", str(langfuse.COMPOSE)]
    assert commands[-1][-1:] == ["down"]
    assert langfuse.VOLUMES == frozenset(
        {
            "postgres_data",
            "clickhouse_data",
            "clickhouse_logs",
            "redis_data",
            "minio_data",
        }
    )
    compose: dict[str, object] = yaml.safe_load(langfuse.COMPOSE.read_text())
    volumes = compose["volumes"]
    assert isinstance(volumes, dict) and volumes.keys() == langfuse.VOLUMES
    assert settings.read_bytes() == initial
    assert "synthetic-secret-marker" not in capsys.readouterr().out


@pytest.mark.parametrize("present", [False, True])
def test_reserved_project_rejected_before_creation_or_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    present: bool,
) -> None:
    settings = tmp_path / "selected.env"
    if present:
        settings.write_text("COMPOSE_PROJECT_NAME=unrelated\n")
    name = service_runtime.LOGGING_PROJECT
    monkeypatch.setenv("COMPOSE_PROJECT_NAME", name)
    with (
        patch.object(langfuse, "_docker_ready", return_value=True),
        patch.object(langfuse, "initialize", side_effect=AssertionError),
        patch.object(
            service_runtime.subprocess,
            "run",
            side_effect=[
                finished(
                    stdout=json.dumps(
                        {"name": name, "secret": "synthetic-secret-marker"}
                    )
                ),
            ]
            if present
            else [finished(), finished()],
        ) as docker,
    ):
        assert langfuse.main(["--start", "--env-file", str(settings)]) == 2
    assert settings.exists() == present
    assert not any("up" in call.args[0] for call in docker.call_args_list)
    output = capsys.readouterr()
    assert (
        "reserved" in output.err
        and "synthetic-secret-marker" not in output.out + output.err
    )


def test_failed_identity_lookup_hides_both_streams(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    settings = tmp_path / "selected.env"
    settings.write_text("")
    with (
        patch.object(langfuse, "_docker_ready", return_value=True),
        patch.object(
            service_runtime.subprocess,
            "run",
            return_value=finished(1, "stdout-marker", "stderr-marker"),
        ) as docker,
    ):
        assert langfuse.main(["--stop", "--env-file", str(settings)]) == 2
    assert docker.call_count == 1
    output = capsys.readouterr()
    assert "stdout-marker" not in output.out + output.err
    assert "stderr-marker" not in output.out + output.err


def test_raw_manager_help_needs_no_bootstrapped_package(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-S", str(langfuse.DEPLOY / "manage.py"), "--help"],
        cwd=tmp_path,
        env={"PATH": os.defpath},
        capture_output=True,
        text=True,
        timeout=5,
    )
    assert result.returncode == 0, result.stderr
    assert "--env-file" in result.stdout


def test_logging_work_budget_bounds_each_docker_probe_http_and_sleep(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(service_runtime.time, "monotonic", lambda: clock[0])
    monkeypatch.setenv("_AGENT_PLAYBOOK_SERVICE_WORK_DEADLINE", "105.5")
    commands: list[tuple[list[str], float]] = []

    def docker(
        argv: list[str], *, timeout: float, **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        commands.append((argv, timeout))
        clock[0] += 1
        if "ps" in argv:
            return finished(stdout='{"Service":"victorialogs","State":"running"}')
        return finished()

    sleeps: list[float] = []

    def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        clock[0] += seconds

    with (
        patch.object(service_runtime.subprocess, "run", side_effect=docker),
        patch.object(service_runtime.time, "sleep", side_effect=sleep),
        patch.object(
            logs, "check_connection", return_value=ConnectionResult("unreachable")
        ) as health,
    ):
        assert logs.main(["--start"]) == 1
    assert [
        argv[1] if argv[1] == "info" else argv[2] if len(argv) == 3 else argv[8]
        for argv, _ in commands
    ] == ["version", "info", "config", "up", "ps"]
    assert [timeout for _, timeout in commands] == [5.5, 4.5, 3.5, 2.5, 1.5]
    assert health.call_args.kwargs["timeout_seconds"] == 0.5
    assert sleeps == [0.5]


def test_langfuse_work_budget_bounds_lookup_inventory_compose_and_http(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = tmp_path / "settings.env"
    settings.write_text("")
    clock = [100.0]
    monkeypatch.setattr(service_runtime.time, "monotonic", lambda: clock[0])
    monkeypatch.setenv("_AGENT_PLAYBOOK_SERVICE_WORK_DEADLINE", "108.5")
    timeouts: list[float] = []
    responses = iter(
        [
            finished(),
            finished(),
            finished(stdout='{"name":"observability"}'),
            finished(),
            finished(),
            finished(),
            finished(),
            finished(
                stdout=json.dumps(
                    [
                        {"Service": name, "State": "running"}
                        for name in langfuse.SERVICES
                    ]
                )
            ),
        ]
    )

    def docker(
        _argv: list[str], *, timeout: float, **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        timeouts.append(timeout)
        clock[0] += 1
        return next(responses)

    def advance(seconds: float) -> None:
        clock[0] += seconds

    with (
        patch.object(service_runtime.subprocess, "run", side_effect=docker),
        patch.object(
            langfuse.urllib.request, "urlopen", side_effect=TimeoutError
        ) as health,
        patch.object(
            service_runtime.time,
            "sleep",
            side_effect=advance,
        ) as sleep,
    ):
        assert langfuse.main(["--start", "--env-file", str(settings)]) == 1
    assert timeouts == [8.5, 7.5, 6.5, 5.5, 4.5, 3.5, 2.5, 1.5]
    assert health.call_args.kwargs["timeout"] == 0.5
    sleep.assert_called_once_with(0.5)


def test_present_file_blocks_contested_expected_volume(tmp_path: Path) -> None:
    settings = tmp_path / "selected.env"
    settings.write_text("")
    with (
        patch.object(langfuse, "_docker_ready", return_value=True),
        patch.object(langfuse, "initialize", side_effect=AssertionError),
        patch.object(
            service_runtime.subprocess,
            "run",
            side_effect=[
                finished(stdout='{"name":"selected"}'),
                finished(),
                finished(stdout="selected_postgres_data|foreign|postgres_data\n"),
            ],
        ) as docker,
    ):
        assert langfuse.main(["--start", "--env-file", str(settings)]) == 2
    assert docker.call_count == 3
    assert settings.read_text() == ""


def test_fresh_inventory_initializes_once_then_reuses_selected_settings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = tmp_path / "selected.env"
    monkeypatch.delenv("COMPOSE_PROJECT_NAME", raising=False)
    look_up = finished(stdout='{"name":"observability"}')
    state = finished(
        stdout=json.dumps(
            [{"Service": service, "State": "running"} for service in langfuse.SERVICES]
        )
    )
    stored = b"POSTGRES_PASSWORD=synthetic-fresh-settings\n"

    def initialize(path: Path) -> bool:
        assert not path.exists()
        path.write_bytes(stored)
        return True

    with (
        patch.object(langfuse, "_docker_ready", return_value=True),
        patch.object(langfuse, "_health", return_value=True),
        patch.object(langfuse, "initialize", side_effect=initialize) as create,
        patch.object(
            service_runtime.subprocess,
            "run",
            side_effect=[
                finished(),
                finished(),
                look_up,
                finished(),
                finished(),
                state,
                look_up,
                finished(),
                finished(),
                finished(),
                finished(),
                state,
            ],
        ) as docker,
    ):
        for _ in range(2):
            assert langfuse.main(["--start", "--env-file", str(settings)]) == 0
    create.assert_called_once_with(settings)
    assert settings.read_bytes() == stored
    assert [call.args[0][1] for call in docker.call_args_list[:3]] == [
        "ps",
        "volume",
        "compose",
    ]
