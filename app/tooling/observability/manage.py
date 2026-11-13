"""Manage the optional local Langfuse Compose stack from a source checkout."""

import argparse
import json
import os
import platform
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

DEPLOY = Path(__file__).resolve().parent
APP = DEPLOY.parent.parent
COMPOSE = DEPLOY / "compose.yaml"
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


def _compose_argv(env_file: Path, *arguments: str) -> list[str]:
    return [
        "docker",
        "compose",
        "--project-directory",
        str(DEPLOY),
        "--env-file",
        str(env_file),
        "-f",
        str(COMPOSE),
        *arguments,
    ]


def _compose(
    env_file: Path, *arguments: str, capture: bool = True
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        _compose_argv(env_file, *arguments),
        cwd=DEPLOY,
        text=True,
        capture_output=capture,
        check=False,
        timeout=None if "--follow" in arguments else 300,
    )


def _redact(line: str, env_file: Path) -> str:
    for entry in env_file.read_text(encoding="utf-8").splitlines():
        if "=" not in entry or entry.lstrip().startswith("#"):
            continue
        key, value = entry.split("=", 1)
        if key.strip() not in ("LANGFUSE_PORT", "MINIO_PORT") and len(value) >= 8:
            line = line.replace(value.strip().strip("\"'"), "[REDACTED]")
    for key in (
        "POSTGRES_PASSWORD",
        "CLICKHOUSE_PASSWORD",
        "REDIS_AUTH",
        "MINIO_ROOT_PASSWORD",
        "NEXTAUTH_SECRET",
        "SALT",
        "ENCRYPTION_KEY",
    ):
        value = os.environ.get(key, "")
        if len(value) >= 8:
            line = line.replace(value, "[REDACTED]")
    return re.sub(r"(?i)(authorization\s*[:=]\s*)[^\r\n,}]+", r"\1[REDACTED]", line)


def _follow_logs(env_file: Path) -> int:
    process = subprocess.Popen(
        _compose_argv(env_file, "logs", "--tail", "80", "--follow"),
        cwd=DEPLOY,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    try:
        assert process.stdout is not None
        for line in process.stdout:
            print(_redact(line, env_file), end="", flush=True)
        return 0 if process.wait() == 0 else 1
    except KeyboardInterrupt:
        process.terminate()
        process.wait(timeout=5)
        print("\nStopped following logs; containers remain running.")
        return 0
    finally:
        if process.stdout is not None:
            process.stdout.close()


def _docker_ready(*, launch: bool) -> bool:
    try:
        if subprocess.run(
            ["docker", "compose", "version"], capture_output=True, timeout=10
        ).returncode:
            print(
                "Docker Compose plugin is unavailable; install/start Docker Desktop.",
                file=sys.stderr,
            )
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print(
            "Docker is missing or timed out. Install Docker Desktop and finish its first launch.",
            file=sys.stderr,
        )
        return False

    def engine() -> bool:
        try:
            return (
                subprocess.run(
                    ["docker", "info"], capture_output=True, timeout=10
                ).returncode
                == 0
            )
        except (OSError, subprocess.TimeoutExpired):
            return False

    if engine():
        return True
    if launch and platform.system() == "Darwin":
        try:
            subprocess.run(
                ["open", "-a", "Docker"], capture_output=True, timeout=10, check=False
            )
        except (OSError, subprocess.TimeoutExpired):
            pass
        print("Waiting for Docker Desktop engine...", flush=True)
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            if engine():
                return True
            time.sleep(2)
    print(
        "Docker engine is unavailable. Open Docker Desktop, finish permissions, then retry.",
        file=sys.stderr,
    )
    return False


def _state(env_file: Path) -> tuple[str, str]:
    result = _compose(env_file, "ps", "--all", "--format", "json")
    if result.returncode:
        return "unavailable", "Could not inspect this Compose stack."
    try:
        parsed: object = (
            json.loads(result.stdout)
            if result.stdout.strip().startswith("[")
            else [
                json.loads(line) for line in result.stdout.splitlines() if line.strip()
            ]
        )
        records = cast(list[object], parsed) if isinstance(parsed, list) else [parsed]
        entries: list[dict[str, str]] = []
        for record in records:
            if not isinstance(record, dict):
                raise ValueError("invalid service record")
            fields = cast(dict[str, object], record)
            entries.append({key: str(value or "") for key, value in fields.items()})
        by_service = {entry["Service"]: entry for entry in entries}
    except (ValueError, KeyError, TypeError):
        return "unavailable", "Docker returned an unreadable service state."
    if not entries:
        return "stopped", "No containers for this stack."
    if any(entry.get("Health") == "unhealthy" for entry in entries):
        return "unhealthy", "One or more services are unhealthy."
    if any(entry.get("State") != "running" for entry in entries):
        return "stopped", "One or more services are stopped."
    if SERVICES - by_service.keys():
        return "starting", "Some services have not started."
    if any(entry.get("Health") not in ("healthy", "") for entry in entries):
        return "starting", "Services are still becoming healthy."
    return "running", "All six services are running."


def _health(port: int) -> bool:
    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/api/public/health", timeout=3
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
    except KeyboardInterrupt:
        print(
            "\nOperation interrupted; use --status or --stop to inspect this stack.",
            file=sys.stderr,
        )
        return 1
    except (OSError, subprocess.TimeoutExpired):
        print(
            "Docker operation failed or timed out; check the engine, ports and disk space.",
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
    if not args.start and not env_file.is_file() and (args.env_file or args.logs):
        print(
            f"Private settings missing at {env_file}; run --start first.",
            file=sys.stderr,
        )
        return 2
    try:
        port, _ = _ports(env_file)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 2
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
        return 1
    if not args.start and not env_file.is_file():
        project = os.environ.get("COMPOSE_PROJECT_NAME", DEPLOY.name)
        containers = subprocess.run(
            [
                "docker",
                "ps",
                "-a",
                "--filter",
                f"label=com.docker.compose.project={project}",
                "--format",
                "{{.ID}}",
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if containers.returncode:
            print("Could not inspect this Docker project.", file=sys.stderr)
            return 1
        if containers.stdout.strip():
            print(
                "Containers exist but private settings are missing; restore the original .env.",
                file=sys.stderr,
            )
            return 2
        if args.stop:
            print("Langfuse already stopped; no containers or settings found.")
            return 0
        print(f"Langfuse stopped: no containers or settings found. UI: {url}")
        return 1
    if args.start:
        try:
            if initialize(env_file):
                print(
                    f"Created private settings at {env_file}; keep them for future starts."
                )
        except OSError:
            print(
                "Could not create private settings; check the selected path and permissions.",
                file=sys.stderr,
            )
            return 2
        result = _compose(env_file, "config", "--quiet")
        if result.returncode:
            print(
                "Compose configuration invalid; check the private settings file.",
                file=sys.stderr,
            )
            return 2
        print(
            "Starting local Langfuse; first image download may take several minutes...",
            flush=True,
        )
        result = _compose(env_file, "up", "-d")
        if result.returncode:
            print(
                "Compose start failed. Check Docker disk space, ports, and --logs.",
                file=sys.stderr,
            )
            return 1
        deadline = time.monotonic() + 300
        while time.monotonic() < deadline:
            state, detail = _state(env_file)
            if state in ("unhealthy", "unavailable"):
                print(
                    f"Langfuse {state}: {detail} Use --logs for details.",
                    file=sys.stderr,
                )
                return 1
            if state == "running" and _health(port):
                print(f"Langfuse ready. UI: {url}")
                return 0
            time.sleep(3)
        print("Langfuse startup timed out; use --status and --logs.", file=sys.stderr)
        return 1
    if args.stop:
        result = _compose(env_file, "down")
        if result.returncode:
            print(
                "Could not stop this stack; check Docker engine and --logs.",
                file=sys.stderr,
            )
            return 1
        print("Langfuse stopped; private settings and named volumes retained.")
        return 0
    if args.logs:
        if args.follow:
            return _follow_logs(env_file)
        result = _compose(env_file, "logs", "--tail", "80")
        print(_redact(result.stdout, env_file), end="")
        return 0 if result.returncode == 0 else 1
    state, detail = _state(env_file)
    ready = state == "running" and _health(port)
    print(
        f"Langfuse {('ready' if ready else 'starting' if state == 'running' else state)}: {detail} UI: {url}"
    )
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
