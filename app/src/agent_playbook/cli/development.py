"""Bridge development commands to checkout-only tooling."""

import subprocess
import sys
from pathlib import Path

from agent_playbook._build_info import SOURCE_COMMIT
from agent_playbook.cli.service_process import (
    OperationCancelled,
    cancellation_signals,
    supervise_component,
    wait_for_coordinator,
)


def run_development(command: str, arguments: list[str] | None = None) -> int:
    app = Path(__file__).resolve().parents[3]
    arguments = list(arguments or [])
    script_name = {
        "release": "release.py",
        "version": "version.py",
        "langfuse": "observability/manage.py",
        "logs": "logging/manage.py",
        "services": "services.py",
    }.get(command, "checks.py")
    script = app / "tooling" / script_name
    if script_name == "checks.py":
        arguments.insert(0, command)
    if SOURCE_COMMIT != "development" or not script.is_file():
        print(
            "Development command requires a source checkout; run its bootstrap.",
            file=sys.stderr,
        )
        return 2
    try:
        argv = [sys.executable, str(script), *arguments]
        if command == "services":
            return wait_for_coordinator(argv, app)
        if command in ("logs", "langfuse") and arguments:
            action = arguments[0].removeprefix("--")
            if action in ("start", "status", "stop"):
                with cancellation_signals() as cancellation:
                    result = supervise_component(
                        argv, app, command, action, cancellation
                    )
                    cancellation.check()
                    return result
        return subprocess.run(argv, cwd=app).returncode
    except (OperationCancelled, KeyboardInterrupt):
        print(
            "Service operation interrupted or timed out. Inspect --status before retrying.",
            file=sys.stderr,
        )
        return 1
    except OSError as error:
        print(f"Could not start {command}: {error}", file=sys.stderr)
        return 2
