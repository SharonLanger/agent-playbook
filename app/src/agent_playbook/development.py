"""Development-only commands; installed releases have no checkout or dev tools."""

import importlib.util
import subprocess
import sys
from pathlib import Path


def run_tools(commands: list[list[str]]) -> int:
    app = Path(__file__).resolve().parents[2]
    if not (app / "pyproject.toml").is_file() or not (app / "tests").is_dir():
        print(
            "Development command requires a source checkout; run its bootstrap.",
            file=sys.stderr,
        )
        return 2
    for command in commands:
        if importlib.util.find_spec(command[0]) is None:
            print(
                f"Missing development tool {command[0]}; rerun bootstrap.",
                file=sys.stderr,
            )
            return 2
    for command in commands:
        result = subprocess.run([sys.executable, "-m", *command], cwd=app)
        if result.returncode:
            return result.returncode
    return 0
