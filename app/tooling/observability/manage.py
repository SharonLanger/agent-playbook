"""Manage the optional local Langfuse Compose stack from a source checkout."""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path
from typing import cast

if __package__:
    from .setup import initialize
else:
    from setup import initialize

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tooling.observability.logs import DEPLOYMENT_SECRET_FIELDS, show_logs
from tooling.service_runtime import (
    LOGGING_PROJECT,
    captured,
    container_state,
    remaining,
    sleep,
)
from tooling.service_runtime import (
    docker_ready as _docker_ready,
)

DEPLOY = Path(__file__).resolve().parent
APP = DEPLOY.parent.parent
COMPOSE = DEPLOY / "compose.yaml"
DEFAULT_PROJECT = "observability"
PROJECT = re.compile(r"[a-z0-9][a-z0-9_-]*\Z")
VOLUMES = frozenset(
    {"postgres_data", "clickhouse_data", "clickhouse_logs", "redis_data", "minio_data"}
)
SERVICES = frozenset(
    {"langfuse-web", "langfuse-worker", "postgres", "clickhouse", "redis", "minio"}
)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    actions = result.add_mutually_exclusive_group(required=True)
    for name, description in (
        ("start", "Start and wait for the local stack."),
        ("stop", "Stop containers while retaining settings and data."),
        ("status", "Show service and UI readiness."),
        ("logs", "Show recent service logs."),
        ("open", "Open the local UI in a browser."),
        ("check", "Check configured project authentication (app environment needed)."),
    ):
        actions.add_argument(f"--{name}", action="store_true", help=description)
    result.add_argument(
        "--follow", action="store_true", help="Follow --logs until Ctrl-C."
    )
    result.add_argument(
        "--env-file",
        type=Path,
        help="Private Compose settings file (default: adjacent .env).",
    )
    result.add_argument(
        "--config", type=Path, help="Application YAML selection for --check."
    )
    return result


def _ports(env_file: Path) -> tuple[int, int]:
    values: dict[str, str] = {}
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip().strip("\"'")
    ports: list[int] = []
    for key, default in (("LANGFUSE_PORT", "3000"), ("MINIO_PORT", "9090")):
        value = os.environ.get(key, values.get(key, default))
        try:
            port = int(value)
            if not 1 <= port <= 65535:
                raise ValueError
        except ValueError as error:
            raise ValueError(
                f"Invalid {key}; choose a port from 1 to 65535."
            ) from error
        ports.append(port)
    return ports[0], ports[1]


def _compose_argv(
    env_file: Path, *arguments: str, project: str | None = None
) -> list[str]:
    return [
        "docker",
        "compose",
        "--project-directory",
        str(DEPLOY),
        "--env-file",
        str(env_file),
        *(["-p", project] if project is not None else []),
        "-f",
        str(COMPOSE),
        *arguments,
    ]


def _compose(
    env_file: Path,
    *arguments: str,
    project: str | None = None,
    deadline: float = float("inf"),
) -> subprocess.CompletedProcess[str]:
    return captured(
        _compose_argv(env_file, *arguments, project=project),
        cwd=DEPLOY,
        timeout=300,
        deadline=deadline,
    )


class SettingsConflict(Exception):
    """Compose identity or settings could not be safely established."""


def _validate_project(name: str) -> str:
    if not PROJECT.fullmatch(name):
        raise SettingsConflict("Invalid Langfuse Compose project setting.")
    if name == LOGGING_PROJECT:
        raise SettingsConflict(
            "Langfuse cannot use the reserved VictoriaLogs project name."
        )
    return name


def _resolve_project(env_file: Path) -> str:
    result = _compose(env_file, "config", "--format", "json")
    if result.returncode == 0:
        try:
            document: object = json.loads(result.stdout)
            if isinstance(document, dict):
                name = cast(dict[str, object], document).get("name")
                if isinstance(name, str):
                    return _validate_project(name)
        except ValueError:
            pass
    raise SettingsConflict(
        "Could not resolve the Langfuse Compose project; check private settings."
    )


def _inventory(project: str | None = None) -> set[str]:
    """Return labels for possible Langfuse assets, including custom projects."""
    container_scope = (
        ["--filter", f"label=com.docker.compose.project={project}"]
        if project is not None
        else []
    )
    expected_volumes = (
        {f"{project}_{volume}": volume for volume in VOLUMES} if project else {}
    )
    volume_scope = (
        ["--filter", "name=^(" + "|".join(sorted(expected_volumes)) + ")$"]
        if expected_volumes
        else []
    )
    try:
        containers = captured(
            [
                "docker",
                "ps",
                "-a",
                *container_scope,
                "--format",
                '{{.Label "com.docker.compose.project"}}|{{.Label "com.docker.compose.service"}}',
            ],
            timeout=10,
        )
        volumes = captured(
            [
                "docker",
                "volume",
                "ls",
                *volume_scope,
                "--format",
                '{{.Name}}|{{.Label "com.docker.compose.project"}}|{{.Label "com.docker.compose.volume"}}',
            ],
            timeout=10,
        )
        if containers.returncode or volumes.returncode:
            raise ValueError
        found: set[str] = set()
        for line in containers.stdout.splitlines():
            label, service = line.split("|")
            if label and service in SERVICES:
                if project is not None and label != project:
                    raise SettingsConflict(
                        "Langfuse container project labels conflict with the selected project."
                    )
                found.add(label)
        for line in volumes.stdout.splitlines():
            name, label, volume = line.split("|")
            if project is not None:
                expected = expected_volumes.get(name)
                if expected is not None:
                    if label not in ("", project) or volume not in ("", expected):
                        raise SettingsConflict(
                            "A named Langfuse volume has conflicting Compose identity labels."
                        )
                    found.add(project)
                continue
            suffix = next(
                (entry for entry in VOLUMES if name.endswith(f"_{entry}")), ""
            )
            if volume in VOLUMES or suffix:
                inferred = name.removesuffix(f"_{suffix}") if suffix else ""
                found.add(label or inferred or "(unlabeled)")
        return found
    except (OSError, ValueError, subprocess.TimeoutExpired):
        raise SettingsConflict(
            "Could not inspect Langfuse assets; verify Docker access and restore the original private settings if they exist."
        ) from None


def _json_mapping(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError
    return cast(dict[str, object], value)


def _resolved_log_secrets(env_file: Path, project: str) -> set[str]:
    # This project-scoped redaction lookup is separate from identity resolution.
    # JSON preserves newlines within interpolated environment values.
    rendered = _compose(env_file, "config", "--format", "json", project=project)
    if rendered.returncode:
        raise SettingsConflict("Could not verify log redaction from private settings.")
    try:
        model = _json_mapping(json.loads(rendered.stdout))
        services = _json_mapping(model["services"])
        secrets: set[str] = set()
        for service, keys in DEPLOYMENT_SECRET_FIELDS.items():
            environment = _json_mapping(_json_mapping(services[service])["environment"])
            for key in keys:
                value = environment[key]
                if not isinstance(value, str) or not value:
                    raise ValueError
                if value.splitlines() != [value]:
                    raise SettingsConflict(
                        "Could not verify log redaction for a multiline private setting."
                    )
                secrets.add(value)
        return secrets
    except (KeyError, ValueError, RecursionError):
        raise SettingsConflict(
            "Could not verify log redaction from private settings."
        ) from None


def _current_log_secrets(env_file: Path, project: str) -> set[str]:
    secrets = _resolved_log_secrets(env_file, project)
    for entry in env_file.read_text(encoding="utf-8").splitlines():
        if "=" not in entry or entry.lstrip().startswith("#"):
            continue
        key, value = entry.split("=", 1)
        secret = value.strip().strip("\"'")
        if key.strip() not in ("LANGFUSE_PORT", "MINIO_PORT") and secret:
            secrets.add(secret)
    return secrets


def _state(
    env_file: Path, project: str, deadline: float = float("inf")
) -> tuple[str, str]:
    return container_state(
        _compose(
            env_file,
            "ps",
            "--all",
            "--format",
            "json",
            project=project,
            deadline=deadline,
        ),
        SERVICES,
    )


def _health(port: int, deadline: float = float("inf")) -> bool:
    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/api/public/health", timeout=remaining(3, deadline)
        ) as response:
            return response.status == 200
    except (OSError, urllib.error.URLError, ValueError):
        return False


def _check(config: Path | None) -> int:
    python = APP / ".venv" / "bin" / "python"
    if not python.is_file():
        print(
            "Application environment missing; run python3 app/tooling/bootstrap.py first.",
            file=sys.stderr,
        )
        return 2
    command = [str(python), str(DEPLOY / "check_connection.py")]
    if config is not None:
        command += ["--config", str(config)]
    return subprocess.run(command, cwd=APP, check=False).returncode


def main(argv: list[str] | None = None) -> int:
    try:
        return _main(argv)
    except SettingsConflict as error:
        print(f"Langfuse failed: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print(
            "\nOperation interrupted; use --status or --stop to inspect this stack.",
            file=sys.stderr,
        )
        return 1
    except (OSError, subprocess.TimeoutExpired):
        print(
            "Langfuse failed or timed out. Inspect --status before retrying.",
            file=sys.stderr,
        )
        return 1


def _main(argv: list[str] | None = None) -> int:
    argparser = parser()
    args = argparser.parse_args(argv)
    if args.follow and not args.logs:
        argparser.error("--follow requires --logs")
    if args.config and not args.check:
        argparser.error("--config requires --check")
    if args.env_file and args.check:
        argparser.error("--env-file does not apply to --check")
    if args.check:
        return _check(args.config.resolve() if args.config else None)
    env_file = args.env_file.resolve() if args.env_file else DEPLOY / ".env"
    present = env_file.is_file()
    if not present and (args.logs or (args.open and args.env_file)):
        raise SettingsConflict(
            "Private settings missing; restore the original file or run --start for a fresh project."
        )
    try:
        port, _ = _ports(env_file)
    except (OSError, UnicodeError, ValueError):
        raise SettingsConflict(
            "Could not read private settings; check file access and port values."
        ) from None
    url = f"http://localhost:{port}"
    if args.open:
        print(f"Langfuse UI: {url}", flush=True)
        if not webbrowser.open(url):
            print(
                "Could not open the browser; use the URL above manually.",
                file=sys.stderr,
            )
            return 1
        return 0
    if not _docker_ready(launch=args.start):
        print("Langfuse unavailable: Docker engine or Compose could not be reached.")
        return 1
    if present:
        project = _resolve_project(env_file)
        if args.start:
            _inventory(project)
    else:
        labels = _inventory()
        if labels:
            # Only print validated Docker project labels, never raw command output.
            projects = ", ".join(
                sorted(label for label in labels if PROJECT.fullmatch(label))
            )
            identified = projects or "unknown project"
            raise SettingsConflict(
                f"Assets observed for {identified}; readiness unknown. Settings missing; restore the original file and project selection."
            )
        if not args.start:
            print(f"Langfuse stopped: no containers or settings found. UI: {url}")
            return 0 if args.stop else 1
        expected = _validate_project(
            os.environ.get("COMPOSE_PROJECT_NAME") or DEFAULT_PROJECT
        )
        try:
            remaining(float("inf"))
            if initialize(env_file):
                print(
                    f"Created private settings at {env_file}; keep them for future starts."
                )
        except OSError:
            raise SettingsConflict(
                "Could not create private settings; check the selected path and permissions."
            ) from None
        project = _resolve_project(env_file)
        if project != expected:
            raise SettingsConflict(
                "Generated settings resolve to a different Compose project; check the selected settings and environment."
            )
    prefix = f"Langfuse ({project})"
    if args.start:
        result = _compose(env_file, "config", "--quiet", project=project)
        if result.returncode:
            raise SettingsConflict(
                "Compose configuration invalid; check the private settings file."
            )
        print(
            "Starting local Langfuse; first image download may take several minutes...",
            flush=True,
        )
        result = _compose(env_file, "up", "-d", project=project)
        if result.returncode:
            print(
                f"{prefix} failed to start. Check Docker disk space, ports, and --logs. UI: {url}",
                file=sys.stderr,
            )
            return 1
        deadline = time.monotonic() + 300
        while time.monotonic() < deadline:
            state, detail = _state(env_file, project, deadline)
            if state in ("unhealthy", "unavailable"):
                print(
                    f"{prefix} {state}: {detail} UI: {url}. Use --logs for details.",
                    file=sys.stderr,
                )
                return 1
            if state == "running" and _health(port, deadline):
                print(f"{prefix} ready. UI: {url}")
                return 0
            sleep(3, deadline)
        print(
            f"{prefix} failed: startup timed out. Inspect --status before retrying. UI: {url}",
            file=sys.stderr,
        )
        return 1
    if args.stop:
        result = _compose(env_file, "down", project=project)
        if result.returncode:
            print(
                f"{prefix} failed to stop; check Docker engine and --logs. UI: {url}",
                file=sys.stderr,
            )
            return 1
        print(
            f"{prefix} stopped; private settings and named volumes retained. UI: {url}"
        )
        return 0
    if args.logs:
        return show_logs(
            project,
            lambda: _compose(
                env_file,
                "ps",
                "--all",
                "--no-trunc",
                "--format",
                "json",
                project=project,
            ),
            lambda: _current_log_secrets(env_file, project),
            follow=args.follow,
        )
    state, detail = _state(env_file, project)
    ready = state == "running" and _health(port)
    print(
        f"{prefix} {('ready' if ready else 'unhealthy' if state == 'running' else state)}: {detail} UI: {url}"
    )
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
