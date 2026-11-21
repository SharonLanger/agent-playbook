"""Local management behavior without Docker or private settings."""

import json
import os
import selectors
import signal
import subprocess
import sys
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tooling.observability import logs, manage


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


def rendered_secret_settings(postgres: str) -> str:
    return json.dumps(
        {
            "services": {
                name: {
                    "environment": {
                        key: postgres
                        if key == "POSTGRES_PASSWORD"
                        else "other-synthetic-secret"
                        for key in fields
                    }
                }
                for name, fields in manage.DEPLOYMENT_SECRET_FIELDS.items()
            }
        }
    )


PROJECT = "observability"
OLD = "1" * 64
OTHER = "2" * 64
NEW = "3" * 64


def result(
    stdout: str = "", stderr: str = "", code: int = 0
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess([], code, stdout, stderr)


def discovery(*entries: tuple[str, str]) -> subprocess.CompletedProcess[str]:
    return result(
        json.dumps(
            [
                {"ID": identity, "Project": PROJECT, "Service": service}
                for identity, service in entries
            ]
        ),
        "synthetic-discovery-stderr",
    )


def inspection(
    identity: str, service: str, *env: str, project: str = PROJECT
) -> subprocess.CompletedProcess[str]:
    return result(
        json.dumps(
            {
                "id": identity,
                "labels": {
                    "com.docker.compose.project": project,
                    "com.docker.compose.service": service,
                },
                "env": list(env),
            }
        ),
        "synthetic-inspect-stderr",
    )


def test_snapshot_masks_current_and_historical_credentials_in_both_streams(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    settings = tmp_path / "selected.env"
    settings.write_text("POSTGRES_PASSWORD=${SYNTHETIC_CURRENT}\n")
    rendered = result(
        rendered_secret_settings("synthetic-current"), "synthetic-render-stderr"
    )
    installed = inspection(
        OLD,
        "langfuse-web",
        "DATABASE_URL=postgresql://postgres:synthetic-old-db@postgres:5432/postgres",
        "NEXTAUTH_SECRET=synthetic-old-auth",
        "SALT=synthetic-old-salt",
        "ENCRYPTION_KEY=synthetic-old-encryption",
        "CLICKHOUSE_PASSWORD=synthetic-old-click",
        "REDIS_AUTH=synthetic-old-redis",
        "LANGFUSE_S3_EVENT_UPLOAD_SECRET_ACCESS_KEY=synthetic-old-event",
        "LANGFUSE_S3_MEDIA_UPLOAD_SECRET_ACCESS_KEY=synthetic-old-media",
    )
    output = result(
        "application stdout synthetic-old-db synthetic-current Authorization: Basic abc123\n",
        "application stderr synthetic-old-db synthetic-old-auth synthetic-old-event synthetic-current\n",
    )
    with (
        patch.object(manage, "_docker_ready", return_value=True),
        patch.object(
            manage, "_compose", side_effect=[rendered, discovery((OLD, "langfuse-web"))]
        ) as compose,
        patch.object(logs, "captured", side_effect=[installed, output]) as docker,
    ):
        assert manage.main(["--logs", "--env-file", str(settings)]) == 0
    assert compose.call_args_list[0].args[-3:] == ("config", "--format", "json")
    assert compose.call_args_list[1].args[-5:] == (
        "ps",
        "--all",
        "--no-trunc",
        "--format",
        "json",
    )
    assert all(call.kwargs["project"] == PROJECT for call in compose.call_args_list)
    commands = [call.args[0] for call in docker.call_args_list]
    assert (
        commands[0][:4] == ["docker", "inspect", "--type", "container"]
        and commands[0][-1] == OLD
    )
    assert commands[1] == ["docker", "logs", "--tail", "80", OLD]
    text = capsys.readouterr()
    assert "langfuse-web | application stdout [REDACTED]" in text.out
    assert "langfuse-web | application stderr [REDACTED]" in text.err
    assert all(
        marker not in text.out + text.err
        for marker in (
            "synthetic-old",
            "synthetic-current",
            "synthetic-render-stderr",
            "synthetic-inspect-stderr",
            "synthetic-discovery-stderr",
            "abc123",
        )
    )


@pytest.mark.parametrize(
    "failure",
    [
        "discovery",
        "inspect",
        "identity",
        "project",
        "service",
        "missing",
        "duplicate",
        "multiline",
    ],
)
def test_snapshot_withholds_only_unverified_container(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    failure: str,
) -> None:
    settings = tmp_path / "selected.env"
    settings.write_text("")
    discovered = discovery(
        (OLD if failure != "discovery" else OLD[:12], "postgres"), (OTHER, "redis")
    )
    unsafe = {
        "inspect": result("synthetic-lookup-stdout", "synthetic-lookup-stderr", 1),
        "identity": inspection(NEW, "postgres", "POSTGRES_PASSWORD=synthetic-bad-id"),
        "project": inspection(
            OLD,
            "postgres",
            "POSTGRES_PASSWORD=synthetic-wrong-project",
            project="another",
        ),
        "service": inspection(
            OLD, "redis", "POSTGRES_PASSWORD=synthetic-wrong-service"
        ),
        "missing": inspection(OLD, "postgres"),
        "duplicate": inspection(
            OLD,
            "postgres",
            "POSTGRES_PASSWORD=synthetic-one",
            "POSTGRES_PASSWORD=synthetic-two",
        ),
        "multiline": inspection(
            OLD,
            "postgres",
            "POSTGRES_PASSWORD=synthetic-old-first\ncontinuation=synthetic-old-second",
        ),
    }
    verified = inspection(OTHER, "redis", "REDIS_AUTH=synthetic-verified-old")
    readable = result("independent diagnostic synthetic-verified-old\n")
    docker_results = (
        [verified, readable]
        if failure == "discovery"
        else [unsafe[failure], verified, readable]
    )
    with (
        patch.object(manage, "_docker_ready", return_value=True),
        patch.object(
            manage,
            "_compose",
            side_effect=[
                result(rendered_secret_settings("synthetic-current")),
                discovered,
            ],
        ),
        patch.object(logs, "captured", side_effect=docker_results) as docker,
    ):
        assert manage.main(["--logs", "--env-file", str(settings)]) == 2
    assert [
        call.args[0][-1] for call in docker.call_args_list if call.args[0][1] == "logs"
    ] == [OTHER]
    text = capsys.readouterr()
    assert "redis | independent diagnostic [REDACTED]" in text.out
    assert "logs withheld" in text.err
    assert "synthetic-" not in text.out + text.err


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


@pytest.mark.parametrize("follow", [False, True])
def test_logs_fail_closed_when_redaction_cannot_be_established(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    follow: bool,
) -> None:
    settings = tmp_path / "selected.env"
    settings.write_text("")
    resolved = subprocess.CompletedProcess([], 1, "hidden-stdout", "hidden-stderr")
    with (
        patch.object(manage, "_docker_ready", return_value=True),
        patch.object(manage, "_compose", return_value=resolved) as compose,
        patch.object(manage.subprocess, "Popen", side_effect=AssertionError),
    ):
        args = ["--logs", "--env-file", str(settings)]
        if follow:
            args.append("--follow")
        assert manage.main(args) == 2
    assert compose.call_count == 1
    output = capsys.readouterr()
    assert "Could not verify log redaction" in output.err
    assert "hidden-" not in output.out + output.err


@pytest.mark.parametrize("follow", [False, True])
def test_multiline_interpolated_secret_with_assignment_withholds_both_log_modes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    follow: bool,
) -> None:
    settings = tmp_path / "selected.env"
    settings.write_text("POSTGRES_PASSWORD=${SYNTHETIC_MULTILINE}\n")
    secret = "synthetic-first-line\ncontinuation=synthetic-continuation"
    monkeypatch.setenv("POSTGRES_PASSWORD", secret)
    structured_result = subprocess.CompletedProcess(
        [],
        0,
        rendered_secret_settings(secret),
        "synthetic-render-stderr",
    )
    with (
        patch.object(manage, "_docker_ready", return_value=True),
        patch.object(manage, "_compose", side_effect=[structured_result]) as compose,
        patch.object(manage.subprocess, "Popen", side_effect=AssertionError) as popen,
    ):
        args = ["--logs", "--env-file", str(settings)]
        if follow:
            args.append("--follow")
        assert manage.main(args) == 2
    assert compose.call_args.args[-3:] == ("config", "--format", "json")
    assert compose.call_count == 1
    popen.assert_not_called()
    output = capsys.readouterr()
    assert "multiline private setting" in output.err
    for marker in (
        "synthetic-first-line",
        "synthetic-continuation",
        "synthetic-render-stderr",
    ):
        assert marker not in output.out + output.err


@pytest.mark.skipif(
    os.name != "posix", reason="Follow uses selectable Docker pipes and POSIX signals"
)
def test_follow_reverifies_replacements_and_masks_both_docker_streams(
    tmp_path: Path,
) -> None:
    settings = tmp_path / "selected.env"
    settings.write_text("POSTGRES_PASSWORD=fixture-file-current\n")
    config = tmp_path / "config.json"
    for suffix, password in (
        ("first", "synthetic-config-first"),
        ("second", "synthetic-config-second"),
    ):
        (tmp_path / f"{suffix}.json").write_text(rendered_secret_settings(password))
    config.write_bytes((tmp_path / "first.json").read_bytes())
    live = tmp_path / "active"
    live.write_text(OLD)
    calls = tmp_path / "calls.jsonl"
    docker = tmp_path / "docker"
    docker.write_text(
        f"#!{sys.executable}\n"
        + r"""
import json
import os
import sys
import time
from pathlib import Path
root = Path(os.environ["SYNTHETIC_DOCKER_ROOT"])
args = sys.argv[1:]
with (root / "calls.jsonl").open("a") as out:
    out.write(json.dumps(args) + "\n")
if args in (["info"], ["compose", "version"]):
    sys.exit(0)
project = "observability"
old_id, new_id, unsafe_id = "1" * 64, "3" * 64, "2" * 64
if args[0] == "compose":
    if "config" in args:
        if "-p" in args:
            print((root / "config.json").read_text())
            print("synthetic-config-stderr", file=sys.stderr)
        else:
            print(json.dumps({"name": project}))
    else:
        active = (root / "active").read_text()
        print(json.dumps([
            {"ID": identity, "Project": project, "Service": "postgres"}
            for identity in active.split()
        ]))
        print("synthetic-ps-stderr", file=sys.stderr)
elif args[0] == "inspect":
    assert args[1:4] == ["--type", "container", "--format"]
    identity = args[-1]
    if identity == unsafe_id:
        print("synthetic-unverified-inspect-stdout")
        print("synthetic-unverified-inspect-stderr", file=sys.stderr)
        sys.exit(1)
    credential = "synthetic-startup-old" if identity == old_id else "synthetic-startup-new"
    print(json.dumps({
        "id": identity,
        "labels": {"com.docker.compose.project": project, "com.docker.compose.service": "postgres"},
        "env": [f"POSTGRES_PASSWORD={credential}"],
    }))
    print("synthetic-inspect-stderr", file=sys.stderr)
elif args[0] == "logs":
    assert args[1:-1] == ["--tail", "80", "--follow"]
    identity = args[-1]
    assert identity in (old_id, new_id)
    phase = "first" if identity == old_id else "second"
    credential = "synthetic-startup-old" if identity == old_id else "synthetic-startup-new"
    sys.stdout.write(f"{phase} stdout {credential[:12]}")
    sys.stdout.flush()
    # A complete stderr line appears between two writes carrying one stdout secret.
    print(f"{phase} stderr {credential} synthetic-config-{phase}", file=sys.stderr, flush=True)
    time.sleep(.06)
    print(f"{credential[12:]} synthetic-config-{phase}", flush=True)
    (root / f"{phase}.pid").write_text(str(os.getpid()))
    time.sleep(30)
else:
    sys.exit(92)
"""
    )
    docker.chmod(0o755)
    env = {
        "PATH": str(tmp_path) + os.pathsep + os.defpath,
        "SYNTHETIC_DOCKER_ROOT": str(tmp_path),
    }
    process: subprocess.Popen[bytes] = subprocess.Popen(
        [
            sys.executable,
            str(manage.DEPLOY / "manage.py"),
            "--logs",
            "--follow",
            "--env-file",
            str(settings),
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    chunks = bytearray()
    try:
        assert process.stdout is not None and process.stderr is not None
        with selectors.DefaultSelector() as reader:
            reader.register(process.stdout, selectors.EVENT_READ)
            reader.register(process.stderr, selectors.EVENT_READ)
            for phase in (b"first", b"second"):
                expected = (
                    phase + b" stdout [REDACTED]",
                    phase + b" stderr [REDACTED]",
                )
                deadline = time.monotonic() + 8.0
                while (
                    not all(message in chunks for message in expected)
                    and time.monotonic() < deadline
                ):
                    for key, _ in reader.select(0.1):
                        chunk = os.read(key.fd, 65536)
                        if not chunk:
                            reader.unregister(key.fd)
                        chunks.extend(chunk)
                assert all(message in chunks for message in expected), bytes(chunks)
                if phase == b"first":
                    next_config = tmp_path / "second.json"
                    next_config.replace(config)
                    staged = tmp_path / "next-active"
                    staged.write_text(f"{OTHER}\n{NEW}")
                    staged.replace(live)
        process.send_signal(signal.SIGINT)
        out, err = process.communicate(timeout=5)
    finally:
        if process.poll() is None:
            process.send_signal(signal.SIGINT)
            try:
                process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate(timeout=5)

    text = (bytes(chunks) + out + err).decode()
    assert (
        process.returncode == 2
    )  # A failed lookup was reported while its sibling kept streaming.
    for phase in ("first", "second"):
        assert f"postgres | {phase} stdout [REDACTED] [REDACTED]" in text
        assert f"postgres | {phase} stderr [REDACTED] [REDACTED]" in text
        pid = int((tmp_path / f"{phase}.pid").read_text())
        with pytest.raises(ProcessLookupError):
            os.kill(pid, 0)
    assert "logs withheld" in text
    assert "Stopped following logs; containers remain running." in text
    assert "synthetic-" not in text
    commands: list[list[str]] = [
        json.loads(line) for line in calls.read_text().splitlines()
    ]
    assert [cmd[-1] for cmd in commands if cmd[0] == "logs"] == [OLD, NEW]
    for identity in (OLD, NEW):
        assert commands.index(
            next(cmd for cmd in commands if cmd[0] == "inspect" and cmd[-1] == identity)
        ) < commands.index(["logs", "--tail", "80", "--follow", identity])
    assert not any("down" in cmd for cmd in commands)
