"""Run a copied example with no repository imports or working-directory dependency."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("change", ["none", "return_value", "method_name"])
def test_name_vs_payload(tmp_path: Path, change: str) -> None:
    example = tmp_path / "example"
    shutil.copytree(
        Path(__file__).parent,
        example,
        ignore=shutil.ignore_patterns(".runtime", "__pycache__", ".pytest_cache"),
    )
    source = example / "flow.py"
    content = source.read_text()
    if change == "return_value":
        content = content.replace(
            'return "needs_work"\n\n    @listen',
            'return "different_payload"\n\n    @listen',
            1,
        )
    elif change == "method_name":
        content = content.replace("def needs_work(self)", "def extra_step(self)")
    source.write_text(content)
    data = json.loads((example / "input.json").read_text())
    data.update({"score": 80})
    (example / "input.json").write_text(json.dumps(data))
    env = {
        **os.environ,
        "PYTHONPATH": "",
        "CREWAI_DISABLE_TELEMETRY": "true",
        "CREWAI_TRACING_ENABLED": "false",
    }
    completed = subprocess.run(
        [sys.executable, str(example / "run.py")],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        timeout=45,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    lines = completed.stdout.splitlines()
    state = json.loads(
        next(
            line.removeprefix("State: ") for line in lines if line.startswith("State: ")
        )
    )
    expected = ["begin", "choose", "needs_work", "accept"]
    if change != "method_name":
        expected.append("revise")
    assert sorted(state["calls"]) == sorted(expected)
