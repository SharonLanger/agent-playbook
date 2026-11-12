"""Run a copied example with no repository imports or working-directory dependency."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def test_case_0(tmp_path: Path) -> None:
    example = tmp_path / "example"
    shutil.copytree(
        Path(__file__).parent,
        example,
        ignore=shutil.ignore_patterns(".runtime", "__pycache__", ".pytest_cache"),
    )
    data = json.loads((example / "input.json").read_text())
    data.update({"target_reviews": 3})
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
    assert (
        json.loads(
            next(
                line.removeprefix("Result: ")
                for line in lines
                if line.startswith("Result: ")
            )
        )
        == "published"
    )
    assert state["reviews"] == 3
    assert state["calls"] == [
        "write_draft",
        "review_1",
        "review_2",
        "review_3",
        "publish",
    ]


def test_case_1(tmp_path: Path) -> None:
    example = tmp_path / "example"
    shutil.copytree(
        Path(__file__).parent,
        example,
        ignore=shutil.ignore_patterns(".runtime", "__pycache__", ".pytest_cache"),
    )
    data = json.loads((example / "input.json").read_text())
    data.update({"target_reviews": 1})
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
    assert (
        json.loads(
            next(
                line.removeprefix("Result: ")
                for line in lines
                if line.startswith("Result: ")
            )
        )
        == "published"
    )
    assert state["reviews"] == 1
