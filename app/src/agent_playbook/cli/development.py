"""Bridge development commands to checkout-only tooling."""

import subprocess
import sys
from pathlib import Path

from agent_playbook._build_info import SOURCE_COMMIT


def run_development(command: str) -> int:
    app = Path(__file__).resolve().parents[3]
    script = app / "tooling" / "checks.py"
    if SOURCE_COMMIT != "development" or not script.is_file():
        print(
            "Development command requires a source checkout; run its bootstrap.",
            file=sys.stderr,
        )
        return 2
    return subprocess.run([sys.executable, str(script), command], cwd=app).returncode
