"""Read project logs only after verifying the startup credentials of their source."""

import json
import os
import re
import selectors
import signal
import subprocess
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from types import FrameType
from typing import IO, TextIO, cast
from urllib.parse import quote

from tooling.service_runtime import captured

_POLL_SECONDS = 1.0
_CONTAINER_ID = re.compile(r"[0-9a-f]{64}\Z")
_AUTH_HEADER = re.compile(r"(?i)(authorization\s*[:=]\s*)[^\r\n,}]+")
DEPLOYMENT_SECRET_FIELDS = {
    "postgres": ("POSTGRES_PASSWORD",),
    "clickhouse": ("CLICKHOUSE_PASSWORD",),
    "redis": ("REDIS_AUTH",),
    "minio": ("MINIO_ROOT_PASSWORD",),
    "langfuse-web": ("NEXTAUTH_SECRET", "SALT", "ENCRYPTION_KEY"),
}
_WEB_SECRET_FIELDS = (
    *DEPLOYMENT_SECRET_FIELDS["langfuse-web"],
    "CLICKHOUSE_PASSWORD",
    "REDIS_AUTH",
    "LANGFUSE_S3_EVENT_UPLOAD_SECRET_ACCESS_KEY",
    "LANGFUSE_S3_MEDIA_UPLOAD_SECRET_ACCESS_KEY",
    "DATABASE_URL",
)
_STARTUP_SECRET_FIELDS = DEPLOYMENT_SECRET_FIELDS | {
    "langfuse-web": _WEB_SECRET_FIELDS,
    "langfuse-worker": _WEB_SECRET_FIELDS,
}
_DB_PREFIX = "postgresql://postgres:"
_DB_SUFFIX = "@postgres:5432/postgres"


@dataclass(frozen=True)
class Container:
    identity: str
    service: str


class LogLookupError(Exception):
    """A Docker result could not safely identify the logs or their credentials."""


def _mapping(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError
    return cast(dict[str, object], value)


def _containers(
    result: subprocess.CompletedProcess[str], project: str
) -> tuple[list[Container], bool]:
    if result.returncode:
        raise LogLookupError
    try:
        output = result.stdout.strip()
        records: object = (
            json.loads(output)
            if output.startswith("[")
            else [json.loads(line) for line in output.splitlines()]
        )
        if not isinstance(records, list):
            raise ValueError
        containers: dict[str, Container] = {}
        ambiguous: set[str] = set()
        invalid = False
        for row in cast(list[object], records):
            if not isinstance(row, dict):
                invalid = True
                continue
            fields = cast(dict[str, object], row)
            identity = fields.get("ID")
            if not isinstance(identity, str) or not _CONTAINER_ID.fullmatch(identity):
                invalid = True
                continue
            service = fields.get("Service")
            if (
                fields.get("Project") != project
                or not isinstance(service, str)
                or service not in _STARTUP_SECRET_FIELDS
                or identity in containers
            ):
                invalid = True
                ambiguous.add(identity)
                continue
            containers[identity] = Container(identity, service)
        return [
            container
            for identity, container in containers.items()
            if identity not in ambiguous
        ], invalid
    except (ValueError, RecursionError):
        raise LogLookupError from None


def _startup_secrets(container: Container, project: str) -> set[str]:
    try:
        metadata = captured(
            [
                "docker",
                "inspect",
                "--type",
                "container",
                "--format",
                '{"id":{{json .Id}},"labels":{{json .Config.Labels}},"env":{{json .Config.Env}}}',
                container.identity,
            ],
            timeout=10,
        )
        if metadata.returncode:
            raise ValueError
        record = _mapping(json.loads(metadata.stdout))
        labels = _mapping(record["labels"])
        if (
            record["id"] != container.identity
            or labels.get("com.docker.compose.project") != project
            or labels.get("com.docker.compose.service") != container.service
        ):
            raise ValueError
        fields = _STARTUP_SECRET_FIELDS[container.service]
        entries = record["env"]
        if not isinstance(entries, list):
            raise ValueError
        secrets: dict[str, str] = {}
        for entry in cast(list[object], entries):
            if not isinstance(entry, str):
                raise ValueError
            key, separator, value = entry.partition("=")
            if key in fields:
                if (
                    not separator
                    or key in secrets
                    or not value
                    or value.splitlines() != [value]
                ):
                    raise ValueError
                secrets[key] = value
        if secrets.keys() != set(fields):
            raise ValueError
        values = set(secrets.values())
        if database := secrets.get("DATABASE_URL"):
            if not database.startswith(_DB_PREFIX) or not database.endswith(_DB_SUFFIX):
                raise ValueError
            password = database.removeprefix(_DB_PREFIX).removesuffix(_DB_SUFFIX)
            if not password:
                raise ValueError
            values.add(password)
        return values
    except (KeyError, ValueError, OSError, RecursionError, subprocess.TimeoutExpired):
        raise LogLookupError from None


def redactor(secrets: set[str]) -> Callable[[str], str]:
    variants = (
        secrets
        | {quote(value, safe="") for value in secrets}
        | {json.dumps(value, ensure_ascii=False)[1:-1] for value in secrets}
    )
    pattern = re.compile(
        "|".join(re.escape(value) for value in sorted(variants, key=len, reverse=True))
    )

    def redact(line: str) -> str:
        return _AUTH_HEADER.sub(r"\1[REDACTED]", pattern.sub("[REDACTED]", line))

    return redact


def _emit(
    container: Container, text: str, redact: Callable[[str], str], target: TextIO
) -> None:
    for line in redact(text).splitlines():
        print(f"{container.service} | {line}", file=target, flush=True)


def _withheld(container: Container) -> None:
    print(
        f"Langfuse {container.service} logs withheld. Could not verify container identity or startup credentials.",
        file=sys.stderr,
    )


def _log_command(container: Container, *, follow: bool = False) -> list[str]:
    return [
        "docker",
        "logs",
        "--tail",
        "80",
        *(["--follow"] if follow else []),
        container.identity,
    ]


def _snapshot(
    project: str, containers: list[Container], current: set[str], result: int
) -> int:
    for container in containers:
        try:
            redact = redactor(current | _startup_secrets(container, project))
        except LogLookupError:
            _withheld(container)
            result = 2
            continue
        try:
            output = captured(_log_command(container), timeout=300)
        except (OSError, subprocess.TimeoutExpired):
            print(f"Langfuse {container.service} logs unavailable.", file=sys.stderr)
            result = max(result, 1)
            continue
        if output.returncode:
            print(f"Langfuse {container.service} logs unavailable.", file=sys.stderr)
            result = max(result, 1)
            continue
        _emit(container, output.stdout, redact, sys.stdout)
        _emit(container, output.stderr, redact, sys.stderr)
    return result


@dataclass
class Stream:
    container: Container
    process: subprocess.Popen[bytes]
    redact: Callable[[str], str]
    startup: set[str]
    pending: dict[IO[bytes], bytes] = field(default_factory=dict[IO[bytes], bytes])

    def read(self, pipe: IO[bytes], target: TextIO) -> bool:
        """Buffer complete lines so read boundaries cannot split a secret."""
        chunk = os.read(pipe.fileno(), 65536)
        prior = self.pending[pipe]
        if chunk:
            ready, separator, self.pending[pipe] = (prior + chunk).rpartition(b"\n")
            if separator:
                _emit(
                    self.container, ready.decode(errors="replace"), self.redact, target
                )
        elif prior:
            _emit(self.container, prior.decode(errors="replace"), self.redact, target)
        return bool(chunk)

    def close(self, *, drained: bool = False) -> int:
        if not drained and self.process.poll() is None:
            try:
                self.process.terminate()
            except ProcessLookupError:
                pass
        try:
            try:
                return self.process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.process.kill()
                return self.process.wait(timeout=1)
        finally:
            if self.process.stdout is not None:
                self.process.stdout.close()
            if self.process.stderr is not None:
                self.process.stderr.close()


def _attach(
    container: Container,
    startup: set[str],
    current: set[str],
    selector: selectors.BaseSelector,
    active: dict[str, Stream],
) -> None:
    # Defer Ctrl-C only long enough to make a newly spawned stream owned.
    interrupted = False

    def interrupt(_signum: int, _frame: FrameType | None) -> None:
        nonlocal interrupted
        interrupted = True

    redact = redactor(current | startup)
    previous = signal.signal(signal.SIGINT, interrupt)
    try:
        process: subprocess.Popen[bytes] = subprocess.Popen(
            _log_command(container, follow=True),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stream = Stream(container, process, redact, startup)
        assert process.stdout is not None and process.stderr is not None
        try:
            for pipe, target in (
                (process.stdout, sys.stdout),
                (process.stderr, sys.stderr),
            ):
                selector.register(pipe, selectors.EVENT_READ, (stream, pipe, target))
                stream.pending[pipe] = b""
        except (KeyError, OSError, ValueError):
            for pipe in stream.pending:
                selector.unregister(pipe)
            stream.close()
            raise
        active[container.identity] = stream
    finally:
        signal.signal(signal.SIGINT, previous)
        if interrupted:
            raise KeyboardInterrupt


def _follow(
    project: str,
    discover: Callable[[], subprocess.CompletedProcess[str]],
    current_settings: Callable[[], set[str]],
    current: set[str],
) -> int:
    active: dict[str, Stream] = {}
    seen: set[str] = set()
    next_discovery = 0.0
    first_discovery = True
    reported_invalid = False
    failure = 0
    with selectors.DefaultSelector() as selector:

        def close(identity: str, *, drained: bool = False) -> int:
            stream = active.pop(identity)
            for pipe in stream.pending:
                selector.unregister(pipe)
            return stream.close(drained=drained)

        try:
            while True:
                if time.monotonic() >= next_discovery:
                    containers, invalid = _containers(discover(), project)
                    if invalid and not reported_invalid:
                        _unidentified()
                        reported_invalid = True
                        failure = 2
                    present = {container.identity for container in containers}
                    seen.intersection_update(present)
                    for identity in active.keys() - present:
                        close(identity)
                    new = [
                        container
                        for container in containers
                        if container.identity not in seen
                    ]
                    if not first_discovery and new:
                        current.update(current_settings())
                        for stream in active.values():
                            stream.redact = redactor(current | stream.startup)
                    first_discovery = False
                    for container in new:
                        seen.add(container.identity)
                        try:
                            startup = _startup_secrets(container, project)
                        except LogLookupError:
                            _withheld(container)
                            failure = 2
                            continue
                        try:
                            _attach(container, startup, current, selector, active)
                        except OSError:
                            print(
                                f"Langfuse {container.service} logs unavailable.",
                                file=sys.stderr,
                            )
                            failure = max(failure, 1)
                    next_discovery = time.monotonic() + _POLL_SECONDS
                delay = max(0, next_discovery - time.monotonic())
                if not active:
                    time.sleep(delay)
                    continue
                for key, _ in selector.select(delay):
                    stream, pipe, target = cast(
                        tuple[Stream, IO[bytes], TextIO], key.data
                    )
                    if not stream.read(pipe, target):
                        selector.unregister(pipe)
                        del stream.pending[pipe]
                        pipe.close()
                        if not stream.pending and close(
                            stream.container.identity, drained=True
                        ):
                            print(
                                f"Langfuse {stream.container.service} logs unavailable.",
                                file=sys.stderr,
                            )
                            failure = max(failure, 1)
        except KeyboardInterrupt:
            print("\nStopped following logs; containers remain running.")
            return failure
        finally:
            for identity in list(active):
                close(identity)


def _unidentified() -> None:
    print(
        "Langfuse logs withheld for an unverified project container.",
        file=sys.stderr,
    )


def show_logs(
    project: str,
    discover: Callable[[], subprocess.CompletedProcess[str]],
    current_settings: Callable[[], set[str]],
    *,
    follow: bool,
) -> int:
    try:
        current = current_settings()
        if follow:
            return _follow(project, discover, current_settings, current)
        containers, invalid = _containers(discover(), project)
        if invalid:
            _unidentified()
        return _snapshot(project, containers, current, 2 if invalid else 0)
    except LogLookupError:
        print(
            "Langfuse logs withheld. Could not verify the project containers.",
            file=sys.stderr,
        )
        return 2
