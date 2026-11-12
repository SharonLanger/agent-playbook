"""Launch a selected installation, preserving isolation and argument boundaries."""

import os
import subprocess
from pathlib import Path

from agent_playbook.config.paths import configuration_path


def launch_release(executable: Path, arguments: list[str] | None = None) -> int:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    # Keep external configuration shared, including with older release CLIs.
    if "--config" not in (arguments or []) and "AGENT_PLAYBOOK_CONFIG" not in env:
        env["AGENT_PLAYBOOK_CONFIG"] = str(configuration_path())
    return subprocess.run(
        [str(executable), "-I", "-m", "agent_playbook.cli", "run", *(arguments or [])],
        env=env,
        check=False,
    ).returncode
