"""Start, inspect or stop the checkout's VictoriaLogs project."""

import argparse
import subprocess
import sys
import time
from pathlib import Path

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from agent_playbook.config.models import LoggingSettings
from agent_playbook.observability.adapters.otel_logging.connection import (
    check_connection,
)
from tooling.service_runtime import (
    LOGGING_PROJECT,
    captured,
    container_state,
    docker_ready,
    remaining,
    sleep,
)

DEPLOY = Path(__file__).resolve().parent
URL = "http://127.0.0.1:9428"
PREFIX = f"VictoriaLogs ({LOGGING_PROJECT})"
SERVICES = frozenset({"victorialogs"})


def _compose(
    *arguments: str, deadline: float = float("inf")
) -> subprocess.CompletedProcess[str]:
    return captured(
        [
            "docker",
            "compose",
            "--project-directory",
            str(DEPLOY),
            "-p",
            LOGGING_PROJECT,
            "-f",
            str(DEPLOY / "compose.yaml"),
            *arguments,
        ],
        cwd=DEPLOY,
        timeout=300,
        deadline=deadline,
    )


def _state(deadline: float = float("inf")) -> tuple[str, str]:
    state, detail = container_state(
        _compose("ps", "--all", "--format", "json", deadline=deadline), SERVICES
    )
    if state != "running":
        return state, detail
    health = check_connection(
        LoggingSettings(enabled=True), timeout_seconds=remaining(5, deadline)
    )
    if health.status == "ok":
        return "ready", "The read-only health endpoint responded."
    return "starting", "The read-only health endpoint did not respond successfully."


def _manage(action: str) -> int:
    if not docker_ready(launch=action == "start"):
        print(f"{PREFIX} unavailable. Local URL: {URL}")
        return 1
    if action == "stop":
        if _compose("down").returncode:
            print(f"{PREFIX} failed to stop. Local URL: {URL}")
            return 1
        print(f"{PREFIX} stopped; named volume retained. Local URL: {URL}")
        return 0
    if action == "status":
        state, detail = _state()
        display_state = "unhealthy" if state == "starting" else state
        print(f"{PREFIX} {display_state}: {detail} Local URL: {URL}")
        return 0 if state == "ready" else 1
    if _compose("config", "--quiet").returncode:
        print(f"{PREFIX} failed: invalid Compose settings. Local URL: {URL}")
        return 2
    if _compose("up", "-d").returncode:
        print(
            f"{PREFIX} failed to start. Check Docker disk space and ports. Local URL: {URL}"
        )
        return 1
    deadline = time.monotonic() + 300
    while time.monotonic() < deadline:
        state, detail = _state(deadline)
        if state == "ready":
            print(f"{PREFIX} ready. Local URL: {URL}")
            return 0
        if state in ("unavailable", "unhealthy"):
            print(f"{PREFIX} {state}: {detail} Local URL: {URL}")
            return 1
        sleep(2, deadline)
    print(
        f"{PREFIX} failed: startup timed out. Inspect --status before retrying. Local URL: {URL}"
    )
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    for action in ("start", "status", "stop"):
        actions.add_argument(
            f"--{action}", dest="action", action="store_const", const=action
        )
    args = parser.parse_args(argv)
    try:
        return _manage(args.action)
    except (OSError, subprocess.TimeoutExpired, KeyboardInterrupt):
        print(
            f"{PREFIX} failed or timed out. Inspect --status before retrying. Local URL: {URL}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
