"""Bound one checkout service helper and the local processes it spawns."""

import os
import signal
import subprocess
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from types import FrameType
from typing import IO

WORK_DEADLINE_ENV = "_AGENT_PLAYBOOK_SERVICE_WORK_DEADLINE"
COMPONENT_SECONDS = {"start": 720.0, "status": 60.0, "stop": 60.0}
CLEANUP_SECONDS = 5.0
TERM_SECONDS = 3.0
WAIT_SLICE = 0.25
LANGFUSE_INFRASTRUCTURE = frozenset(
    {
        "POSTGRES_PASSWORD",
        "CLICKHOUSE_PASSWORD",
        "REDIS_AUTH",
        "MINIO_ROOT_PASSWORD",
        "NEXTAUTH_SECRET",
        "SALT",
        "ENCRYPTION_KEY",
    }
)
LANGFUSE_PROJECT_KEYS = frozenset({"LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"})


@dataclass
class Cancellation:
    signum: int | None = None

    def receive(self, signum: int, _frame: FrameType | None) -> None:
        self.signum = signum

    def check(self) -> None:
        if self.signum is not None:
            raise OperationCancelled("Service operation interrupted.")


class OperationCancelled(Exception):
    """The owning operation must stop after the active helper is reaped."""


@contextmanager
def cancellation_signals() -> Iterator[Cancellation]:
    pending = Cancellation()
    previous = {
        sig: signal.signal(sig, pending.receive)
        for sig in (signal.SIGINT, signal.SIGTERM)
    }
    try:
        yield pending
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)


def _group_signal(pgid: int, signum: int) -> bool:
    try:
        os.killpg(pgid, signum)
    except ProcessLookupError:
        return False
    except PermissionError:
        if signum == 0:
            return True
        raise
    return True


def _cleanup(process: subprocess.Popen[bytes], pgid: int, deadline: float) -> None:
    started = time.monotonic()
    if _group_signal(pgid, signal.SIGTERM):
        term_deadline = min(
            started + TERM_SECONDS, deadline - (CLEANUP_SECONDS - TERM_SECONDS)
        )
        while time.monotonic() < term_deadline:
            process.poll()  # Reap the leader while checking for remaining descendants.
            if not _group_signal(pgid, 0):
                break
            time.sleep(max(0, min(WAIT_SLICE, term_deadline - time.monotonic())))
        _group_signal(pgid, signal.SIGKILL)
    try:
        process.wait(
            timeout=max(0, min(deadline, started + CLEANUP_SECONDS) - time.monotonic())
        )
    except subprocess.TimeoutExpired:
        raise OperationCancelled(
            "Service helper could not be reaped before the deadline."
        ) from None


def ensure_active(cancellation: Cancellation, aggregate_deadline: float) -> None:
    cancellation.check()
    if time.monotonic() >= aggregate_deadline - CLEANUP_SECONDS:
        raise OperationCancelled("Aggregate service operation timed out.")


def _local_service_environment(name: str, work_deadline: float) -> dict[str, str]:
    excluded = LANGFUSE_PROJECT_KEYS
    env = {WORK_DEADLINE_ENV: str(work_deadline)}
    if name == "logs":
        excluded = excluded | LANGFUSE_INFRASTRUCTURE | {"COMPOSE_ENV_FILES"}
        env["COMPOSE_DISABLE_ENV_FILE"] = "1"
    return {
        key: value for key, value in os.environ.items() if key not in excluded
    } | env


def supervise_component(
    argv: list[str],
    cwd: Path,
    name: str,
    action: str,
    cancellation: Cancellation,
    *,
    aggregate_deadline: float = float("inf"),
) -> int:
    return supervise_helper(
        argv,
        cwd,
        name,
        cancellation,
        aggregate_deadline=aggregate_deadline,
        component_seconds=COMPONENT_SECONDS[action],
    )


def supervise_helper(
    argv: list[str],
    cwd: Path,
    name: str,
    cancellation: Cancellation,
    *,
    aggregate_deadline: float,
    component_seconds: float = float("inf"),
    stdout: IO[bytes] | None = None,
) -> int:
    ensure_active(cancellation, aggregate_deadline)
    deadline = min(time.monotonic() + component_seconds, aggregate_deadline)
    work_deadline = deadline - CLEANUP_SECONDS
    process: subprocess.Popen[bytes] | None = None
    pgid: int | None = None
    try:
        if time.monotonic() >= work_deadline:
            return 1
        process = subprocess.Popen(
            argv,
            cwd=cwd,
            env=_local_service_environment(name, work_deadline),
            start_new_session=True,
            stdout=stdout,
        )
        pgid = process.pid
        while True:
            ensure_active(cancellation, aggregate_deadline)
            remaining = work_deadline - time.monotonic()
            if remaining <= 0:
                print(
                    f"{name} failed: operation timed out. Inspect --status before retrying."
                )
                return 1
            try:
                result = process.wait(timeout=min(WAIT_SLICE, remaining))
            except subprocess.TimeoutExpired:
                continue
            ensure_active(cancellation, aggregate_deadline)
            if time.monotonic() >= work_deadline:
                print(
                    f"{name} failed: operation timed out. Inspect --status before retrying."
                )
                return 1
            return result if result >= 0 else 1
    except OSError:
        print(f"{name} unavailable: could not launch its local manager.")
        return 1
    finally:
        if process is not None and pgid is not None:
            _cleanup(process, pgid, deadline)


def wait_for_coordinator(argv: list[str], cwd: Path) -> int:
    """The coordinator owns cleanup, including for a signal received by the bridge."""
    with cancellation_signals() as cancellation:
        process: subprocess.Popen[bytes] = subprocess.Popen(argv, cwd=cwd)
        forwarded = False
        while True:
            if cancellation.signum is not None and not forwarded:
                try:
                    process.send_signal(cancellation.signum)
                except ProcessLookupError:
                    pass
                forwarded = True
            try:
                result = process.wait(timeout=WAIT_SLICE)
            except subprocess.TimeoutExpired:
                continue
            if result < 0:
                print(
                    "Service operation interrupted. Inspect --status before retrying."
                )
                return 1
            return result
