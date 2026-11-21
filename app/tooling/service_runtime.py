"""Shared, credential-safe primitives for checkout Docker service managers."""

import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import cast

LOGGING_PROJECT = "agent-playbook-logging-smoke"


def work_deadline() -> float:
    # Unset for the original pre-bootstrap Langfuse entry point.
    return float(os.environ.get("_AGENT_PLAYBOOK_SERVICE_WORK_DEADLINE", "inf"))


def remaining(limit: float, deadline: float = float("inf")) -> float:
    seconds = min(
        limit, deadline - time.monotonic(), work_deadline() - time.monotonic()
    )
    if seconds <= 0:
        raise subprocess.TimeoutExpired("local service operation", limit)
    return seconds


def sleep(seconds: float, deadline: float) -> None:
    time.sleep(remaining(seconds, deadline))


def captured(
    argv: list[str],
    *,
    timeout: float,
    cwd: Path | None = None,
    deadline: float = float("inf"),
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        timeout=remaining(timeout, deadline),
        check=False,
        capture_output=True,
        text=True,
        errors="replace",
    )


def docker_ready(*, launch: bool) -> bool:
    try:
        if captured(["docker", "compose", "version"], timeout=10).returncode:
            print(
                "Docker Compose plugin is unavailable; install/start Docker Desktop.",
                file=sys.stderr,
            )
            return False
    except (OSError, subprocess.TimeoutExpired):
        print(
            "Docker is missing or timed out. Install Docker Desktop and finish its first launch.",
            file=sys.stderr,
        )
        return False

    def engine(deadline: float = float("inf")) -> bool:
        try:
            return (
                captured(["docker", "info"], timeout=10, deadline=deadline).returncode
                == 0
            )
        except (OSError, subprocess.TimeoutExpired):
            return False

    if engine():
        return True
    if launch and platform.system() == "Darwin":
        deadline = time.monotonic() + 90
        try:
            captured(["open", "-a", "Docker"], timeout=10, deadline=deadline)
        except OSError:
            pass
        print("Waiting for Docker Desktop engine...", flush=True)
        while time.monotonic() < deadline:
            if engine(deadline):
                return True
            try:
                sleep(2, deadline)
            except subprocess.TimeoutExpired:
                break
    print(
        "Docker engine is unavailable. Open Docker Desktop, finish permissions, then retry.",
        file=sys.stderr,
    )
    return False


def container_state(
    result: subprocess.CompletedProcess[str], services: frozenset[str]
) -> tuple[str, str]:
    if result.returncode:
        return "unavailable", "Could not inspect this Compose stack."
    try:
        output = result.stdout.strip()
        parsed: object = (
            json.loads(output)
            if output.startswith("[")
            else [json.loads(line) for line in output.splitlines()]
        )
        if not isinstance(parsed, list):
            raise ValueError
        entries: dict[str, dict[str, object]] = {}
        for row in cast(list[object], parsed):
            if not isinstance(row, dict):
                raise ValueError
            entry = cast(dict[str, object], row)
            service = entry.get("Service")
            if not isinstance(service, str):
                raise ValueError
            if service in services:
                entries[service] = entry
    except (ValueError, TypeError):
        return "unavailable", "Docker returned an unreadable service state."
    if not entries:
        return "stopped", "No containers for this stack."
    if any(entry.get("Health") == "unhealthy" for entry in entries.values()):
        return "unhealthy", "One or more services are unhealthy."
    if any(entry.get("State") != "running" for entry in entries.values()):
        return "stopped", "One or more services are stopped."
    if entries.keys() != services:
        return "starting", "Some services have not started."
    if any(
        entry.get("Health") not in ("healthy", "", None) for entry in entries.values()
    ):
        return "starting", "Services are still becoming healthy."
    return "running", "All services are running."
