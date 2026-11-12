"""Bridge development commands to checkout-only tooling."""

import subprocess
import sys
from pathlib import Path

from agent_playbook._build_info import SOURCE_COMMIT


def run_development(command: str, arguments: list[str] | None = None) -> int:
    app = Path(__file__).resolve().parents[3]
    arguments = list(arguments or [])
    if command == "release" and arguments:
        arguments[1] = str(Path(arguments[1]).resolve())
    script_name = {"release": "release.py", "version": "version.py"}.get(
        command, "checks.py"
    )
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
        return subprocess.run(
            [sys.executable, str(script), *arguments], cwd=app
        ).returncode
    except OSError as error:
        print(f"Could not start {command}: {error}", file=sys.stderr)
        return 2
