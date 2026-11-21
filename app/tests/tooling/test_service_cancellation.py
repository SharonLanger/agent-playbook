"""Exercise real POSIX helper groups without Docker or private settings."""

import os
import signal
import subprocess
import sys
import time
import traceback
from collections.abc import Callable
from pathlib import Path
from typing import IO
from unittest.mock import MagicMock, patch

import pytest

from agent_playbook.cli import development, service_process
from tooling import services

pytestmark = pytest.mark.skipif(os.name != "posix", reason="POSIX process groups")

HELPER = r"""
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

root = Path.cwd()
name = Path(__file__).parent.name
with (root / 'calls').open('a') as calls:
    calls.write(f"{name} {sys.argv[1]}\n")
if name != (root / 'active').read_text():
    raise SystemExit(0)
subprocess.run(["docker", "info"], check=True)
subprocess.run(["docker", "compose", "ps"], check=True)
child = subprocess.Popen([sys.executable, '-c',
    "import os, signal, time; from pathlib import Path; "
    "signal.signal(signal.SIGTERM, lambda *_: Path('received-term').write_text('TERM')); "
    "Path('grandchild').write_text(str(os.getpid())); time.sleep(30)"
])
(root / 'helper').write_text(str(os.getpid()))
while not (root / 'grandchild').exists():
    time.sleep(.01)
if (root / 'stray').exists():
    raise SystemExit(0)
time.sleep(30)
"""


@pytest.fixture
def checkout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    for component in ("logging", "observability"):
        path = tmp_path / "tooling" / component / "manage.py"
        path.parent.mkdir(parents=True)
        path.write_text(HELPER)
    docker = tmp_path / "docker"
    invocation_log = tmp_path / "docker-calls"
    docker.write_text(
        f"#!{sys.executable}\n"
        + r"""
import sys
from pathlib import Path
with Path(sys.argv[0]).with_name("docker-calls").open("a") as handle:
    handle.write(" ".join(sys.argv[1:]) + "\n")
"""
    )
    docker.chmod(0o755)
    monkeypatch.setenv("PATH", str(tmp_path) + os.pathsep + os.defpath)
    assert not invocation_log.exists()
    monkeypatch.setattr(services, "APP", tmp_path)
    monkeypatch.setattr(
        development,
        "__file__",
        str(tmp_path / "src" / "agent_playbook" / "cli" / "development.py"),
    )
    monkeypatch.setattr(service_process, "CLEANUP_SECONDS", 0.6)
    monkeypatch.setattr(service_process, "TERM_SECONDS", 0.25)
    monkeypatch.setattr(service_process, "WAIT_SLICE", 0.025)
    return tmp_path


def assert_reaped(root: Path) -> None:
    assert (root / "docker-calls").read_text().splitlines() == ["info", "compose ps"]
    assert (root / "received-term").read_text() == "TERM"
    helper = int((root / "helper").read_text())
    grandchild = int((root / "grandchild").read_text())
    with pytest.raises(ChildProcessError):
        os.waitpid(helper, os.WNOHANG)
    for pid in (helper, grandchild):
        for _ in range(25):
            status = subprocess.run(
                ["ps", "-o", "stat=", "-p", str(pid)],
                capture_output=True,
                text=True,
                timeout=2,
                check=False,
            ).stdout.strip()
            if not status or status.startswith("Z"):
                break
            time.sleep(0.02)
        else:
            os.kill(pid, signal.SIGKILL)
            pytest.fail(f"Helper process {pid} was still live")


@pytest.mark.parametrize("action", ["start", "status", "stop"])
def test_outer_deadline_cleans_group_and_stops_aggregate(
    checkout: Path,
    action: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    active = "observability" if action == "stop" else "logging"
    (checkout / "active").write_text(active)
    monkeypatch.setitem(services.AGGREGATE_SECONDS, action, 1.5)
    monkeypatch.setitem(service_process.COMPONENT_SECONDS, action, 4.0)
    with patch.object(services, "_select", return_value=(True, True)):
        started = time.monotonic()
        assert services.main([f"--{action}"]) == 1
        assert time.monotonic() - started < 1.65
    assert "Aggregate service operation timed out" in capsys.readouterr().err
    assert (checkout / "calls").read_text().splitlines() == [f"{active} --{action}"]
    assert_reaped(checkout)


@pytest.mark.parametrize("stray", [False, True])
def test_inner_timeout_or_stray_cleans_group_before_next_component(
    checkout: Path,
    stray: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (checkout / "active").write_text("logging")
    if stray:
        (checkout / "stray").touch()
    monkeypatch.setitem(services.AGGREGATE_SECONDS, "start", 4.0)
    monkeypatch.setitem(service_process.COMPONENT_SECONDS, "start", 1.5)
    original = services.supervise_component

    def check_before_next(
        argv: list[str],
        cwd: Path,
        name: str,
        action: str,
        cancellation: service_process.Cancellation,
        *,
        aggregate_deadline: float,
    ) -> int:
        if name == "langfuse":
            assert_reaped(checkout)
        return original(
            argv, cwd, name, action, cancellation, aggregate_deadline=aggregate_deadline
        )

    with (
        patch.object(
            services,
            "_select",
            return_value=(True, True),
        ),
        patch.object(services, "supervise_component", side_effect=check_before_next),
    ):
        assert services.main(["--start"]) == (0 if stray else 1)
    assert (checkout / "calls").read_text().splitlines() == [
        "logging --start",
        "observability --start",
    ]


def interrupt_after_spawn(checkout: Path) -> Callable[..., subprocess.Popen[bytes]]:
    """Deliver a signal inside Popen's return window, before the owner can wait."""
    real_popen = subprocess.Popen

    def launch(
        argv: list[str],
        *,
        cwd: Path,
        env: dict[str, str] | None = None,
        start_new_session: bool = False,
        stdout: IO[bytes] | None = None,
    ) -> subprocess.Popen[bytes]:
        process = real_popen(
            argv, cwd=cwd, env=env, start_new_session=start_new_session, stdout=stdout
        )
        until = time.monotonic() + 2
        while not (checkout / "grandchild").exists() and time.monotonic() < until:
            time.sleep(0.01)
        os.kill(os.getpid(), signal.SIGINT)
        return process

    return launch


def test_aggregate_ctrl_c_between_spawn_and_wait(
    checkout: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    (checkout / "active").write_text("logging")
    with (
        patch.object(
            services,
            "_select",
            return_value=(True, True),
        ),
        patch.object(
            service_process.subprocess,
            "Popen",
            side_effect=interrupt_after_spawn(checkout),
        ),
    ):
        assert services.main(["--start"]) == 1
    assert "interrupted" in capsys.readouterr().err
    assert (checkout / "calls").read_text().splitlines() == ["logging --start"]
    assert_reaped(checkout)


@pytest.mark.parametrize(
    ("command", "active"), [("logs", "logging"), ("langfuse", "observability")]
)
@pytest.mark.parametrize("interrupt", [False, True])
def test_direct_component_timeout_or_ctrl_c_cleans_group(
    checkout: Path,
    monkeypatch: pytest.MonkeyPatch,
    command: str,
    active: str,
    interrupt: bool,
) -> None:
    (checkout / "active").write_text(active)
    monkeypatch.setitem(service_process.COMPONENT_SECONDS, "status", 1.5)
    if interrupt:
        with patch.object(
            service_process.subprocess,
            "Popen",
            side_effect=interrupt_after_spawn(checkout),
        ):
            assert development.run_development(command, ["--status"]) == 1
    else:
        assert development.run_development(command, ["--status"]) == 1
    assert (checkout / "calls").read_text().splitlines() == [f"{active} --status"]
    assert_reaped(checkout)


def test_bridge_forwards_a_signal_sent_only_to_it(
    checkout: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (checkout / "tooling" / "services.py").write_text(
        "import signal, time\n"
        "from pathlib import Path\n"
        "def cancel(*_):\n"
        "    Path('forwarded').write_text('yes')\n"
        "    raise SystemExit(1)\n"
        "signal.signal(signal.SIGINT, cancel)\n"
        "Path('coordinator').touch()\n"
        "time.sleep(5)\n"
    )
    real_popen = subprocess.Popen

    def launch(
        argv: list[str],
        *,
        cwd: Path,
        env: dict[str, str] | None = None,
        start_new_session: bool = False,
        stdout: IO[bytes] | None = None,
    ) -> subprocess.Popen[bytes]:
        process = real_popen(
            argv, cwd=cwd, env=env, start_new_session=start_new_session, stdout=stdout
        )
        until = time.monotonic() + 2
        while not (checkout / "coordinator").exists() and time.monotonic() < until:
            time.sleep(0.01)
        os.kill(os.getpid(), signal.SIGINT)
        return process

    monkeypatch.setattr(service_process.subprocess, "Popen", launch)
    assert development.run_development("services", ["--status"]) == 1
    assert (checkout / "forwarded").read_text() == "yes"


@pytest.mark.parametrize(
    ("action", "component_cap", "aggregate_cap"),
    [
        ("start", 720, 1500),
        ("status", 60, 130),
        ("stop", 60, 130),
    ],
)
def test_production_caps_reserve_cleanup_inside_elapsed_limits(
    tmp_path: Path,
    action: str,
    component_cap: int,
    aggregate_cap: int,
) -> None:
    start = 1000.0
    process = MagicMock()
    process.pid = 42
    process.wait.return_value = 0
    with (
        patch.object(service_process.time, "monotonic", return_value=start),
        patch.object(
            service_process.subprocess, "Popen", return_value=process
        ) as popen,
        patch.object(service_process, "_cleanup") as cleanup,
        patch.object(
            services,
            "_select",
            return_value=(True, True),
        ),
        patch.object(
            services, "supervise_component", wraps=service_process.supervise_component
        ) as child,
    ):
        assert (
            service_process.supervise_component(
                ["synthetic"], tmp_path, "logs", action, service_process.Cancellation()
            )
            == 0
        )
        assert services.main([f"--{action}"]) == 0
    for launch in popen.call_args_list:
        assert (
            float(launch.kwargs["env"][service_process.WORK_DEADLINE_ENV])
            == start + component_cap - 5
        )
    for group in cleanup.call_args_list:
        assert group.args == (process, 42, start + component_cap)
    assert all(
        call.kwargs["aggregate_deadline"] == start + aggregate_cap
        for call in child.call_args_list
    )
    assert child.call_count == 2
    assert process.wait.call_args.kwargs["timeout"] == 0.25
    with patch.object(
        service_process.time, "monotonic", return_value=start + aggregate_cap - 5
    ):
        with pytest.raises(
            service_process.OperationCancelled, match="Aggregate.*timed out"
        ):
            service_process.ensure_active(
                service_process.Cancellation(), start + aggregate_cap
            )


def test_production_cleanup_waits_three_seconds_then_leaves_two_to_reap() -> None:
    clock = [1000.0]
    delivered: list[tuple[float, int]] = []
    process = MagicMock()

    def sleep(seconds: float) -> None:
        clock[0] += seconds

    def send(_pgid: int, signum: int) -> None:
        if signum:
            delivered.append((clock[0], signum))

    with (
        patch.object(service_process.time, "monotonic", side_effect=lambda: clock[0]),
        patch.object(service_process.time, "sleep", side_effect=sleep),
        patch.object(service_process.os, "killpg", side_effect=send),
    ):
        service_process._cleanup(process, 42, 1005.0)  # pyright: ignore[reportPrivateUsage]
    assert delivered == [(1000.0, signal.SIGTERM), (1003.0, signal.SIGKILL)]
    process.wait.assert_called_once_with(timeout=2.0)


@pytest.mark.parametrize("interrupt", [False, True], ids=["outer-deadline", "sigint"])
def test_large_regular_selection_cancellation_reaps_without_docker(
    checkout: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    interrupt: bool,
) -> None:
    selected = checkout / "large.yaml"
    selected.write_text(
        "# large synthetic configuration comment\n" * 450_000
        + "integrations: {logging: {enabled: true}}\n"
        + "secrets: {file: synthetic.env}\n"
    )
    (checkout / "synthetic.env").write_text("")
    opened = checkout / "selection-opened"
    (checkout / "sitecustomize.py").write_text(
        "import os\n"
        "from pathlib import Path\n"
        "real_open = os.open\n"
        "def record_open(path, *args, **kwargs):\n"
        f"    if isinstance(path, (str, os.PathLike)) and Path(path) == Path({str(selected)!r}):\n"
        f"        Path({str(opened)!r}).write_text(str(os.getpid()))\n"
        "    return real_open(path, *args, **kwargs)\n"
        "os.open = record_open\n"
    )
    monkeypatch.setenv("PYTHONPATH", str(checkout))
    cleanup_errors: list[str] = []
    original_cleanup = service_process._cleanup  # pyright: ignore[reportPrivateUsage]

    def inspect_cleanup(
        process: subprocess.Popen[bytes], pgid: int, deadline: float
    ) -> None:
        try:
            original_cleanup(process, pgid, deadline)
        except Exception as error:
            cleanup_errors.append("".join(traceback.format_exception(error)))
            raise

    monkeypatch.setattr(service_process, "_cleanup", inspect_cleanup)
    # Let the worker reach the file before cancelling it, regardless of machine speed.
    monkeypatch.setitem(services.AGGREGATE_SECONDS, "start", 12.0)
    original_ensure_active = service_process.ensure_active

    def cancel_after_open(
        cancellation: service_process.Cancellation, aggregate_deadline: float
    ) -> None:
        original_ensure_active(cancellation, aggregate_deadline)
        if not interrupt and opened.exists():
            raise service_process.OperationCancelled(
                "Aggregate service operation timed out."
            )

    if not interrupt:
        monkeypatch.setattr(service_process, "ensure_active", cancel_after_open)
    real_popen = subprocess.Popen
    workers: list[subprocess.Popen[bytes]] = []

    def launch(
        argv: list[str],
        *,
        cwd: Path,
        env: dict[str, str],
        start_new_session: bool,
        stdout: IO[bytes] | None = None,
    ) -> subprocess.Popen[bytes]:
        worker = real_popen(
            argv,
            cwd=cwd,
            env=env,
            start_new_session=start_new_session,
            stdout=stdout,
        )
        workers.append(worker)
        if interrupt:
            deadline = time.monotonic() + 10.0
            while not opened.exists() and time.monotonic() < deadline:
                time.sleep(0.01)
            assert opened.exists(), (
                "The selection worker never opened the configuration"
            )
            os.kill(os.getpid(), signal.SIGINT)
        return worker

    with patch.object(service_process.subprocess, "Popen", side_effect=launch) as popen:
        assert services.main(["--start", "--config", str(selected)]) == 1
    assert not cleanup_errors, cleanup_errors
    assert opened.is_file(), "The worker must begin reading the real regular file"
    assert len(workers) == 1 and popen.call_args.args[0][-2:] == [
        "--select",
        str(selected),
    ]
    assert workers[0].pid == int(opened.read_text())
    assert workers[0].returncode == -signal.SIGTERM
    with pytest.raises(ChildProcessError):
        os.waitpid(workers[0].pid, os.WNOHANG)
    assert not (checkout / "docker-calls").exists()
    assert not (checkout / "calls").exists()
    assert ("interrupted" if interrupt else "timed out") in capsys.readouterr().err
