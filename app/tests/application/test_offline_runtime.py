"""Probe import and execution with network attempts denied before the first import."""

import os
import subprocess
import sys
from pathlib import Path


def test_fresh_process_offline_runtime(tmp_path: Path) -> None:
    script = Path(__file__).resolve().parents[2] / "tooling/verify_runtime.py"
    env = {
        k: v
        for k, v in os.environ.items()
        if not k.endswith("_API_KEY")
        and k
        not in (
            "AGENT_PLAYBOOK_SECRETS_FILE",
            "CREWAI_TOKEN",
            "PYTHONPATH",
            "PYTHONHOME",
        )
    }
    # Verification selects its own explicit offline fixture; user settings are separate.
    env["AGENT_PLAYBOOK_SECRETS_FILE"] = str(tmp_path / "must-not-be-read.env")
    env["AGENT_PLAYBOOK_CREWAI_TRACING_ENABLED"] = "true"
    env["AGENT_PLAYBOOK_CONFIG"] = str(tmp_path / "missing-user-config.yaml")
    env["CREWAI_DISABLE_TELEMETRY"] = "false"
    env["CREWAI_TRACING_ENABLED"] = "true"
    result = subprocess.run(
        [sys.executable, "-I", str(script), "dev-run"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "zero Python socket/DNS attempts" in result.stdout
