"""Temporary S03.M1 checks, retained for Sharon; excluded from application gates."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["CREWAI_TRACING_ENABLED"] = "false"

from flow import RecipeFlow  # noqa: E402

HERE = Path(__file__).resolve().parent
DEFAULT = json.loads((HERE / "input.json").read_text())


def run_flow(changes=None, failure=False):
    flow = RecipeFlow(suppress_flow_events=True)
    data = DEFAULT | (changes or {})
    try:
        result = flow.kickoff(inputs=data)
    except ValueError as error:
        assert failure, f"unexpected failure: {error}"
        assert ERROR in str(error), str(error)
    else:
        assert not failure, "expected exception was swallowed"
        assert result == flow.state.result
    return flow.state


def joined(state, branches):
    events = state.events
    assert events.count("join") == 1
    for branch in branches:
        assert events.count(branch + ":start") == 1
        assert events.count(branch + ":done") == 1
        assert events.index(branch + ":done") < events.index("join")
    assert max(events.index(b + ":start") for b in branches) < min(
        events.index(b + ":done") for b in branches
    )


def terminal(state):
    assert state.events.count("report") == 1
    assert state.events[-1] == "report"


def entry(folder, failure=False):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    with tempfile.TemporaryDirectory() as cwd:
        completed = subprocess.run(
            [sys.executable, str(folder / "run.py")],
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            timeout=60,
        )
    assert completed.returncode == (1 if failure else 0), (
        completed.stdout + completed.stderr
    )
    if failure:
        assert ERROR in completed.stderr
        assert "RESULT_JSON=" not in completed.stdout
    state_line = next(
        line for line in completed.stdout.splitlines() if line.startswith("STATE_JSON=")
    )
    state = json.loads(state_line.split("=", 1)[1])
    if not failure:
        result_line = next(
            line
            for line in completed.stdout.splitlines()
            if line.startswith("RESULT_JSON=")
        )
        assert json.loads(result_line.split("=", 1)[1]) == state["result"]
    return state


def common(expected, failure=False):
    before = (HERE / "input.json").read_bytes()
    state = entry(HERE, failure)
    assert state["result"] == expected, state
    with tempfile.TemporaryDirectory() as tmp:
        copied = Path(tmp) / HERE.name
        shutil.copytree(HERE, copied, ignore=shutil.ignore_patterns("__pycache__"))
        copied_state = entry(copied, failure)
        assert copied_state["result"] == expected
        for name in ("diagram.svg", "diagram-static.svg"):
            ET.parse(copied / name)
    assert (HERE / "input.json").read_bytes() == before
    guide = (HERE / "README.md").read_text().splitlines()
    assert guide[0].startswith("# ") and guide[2].startswith("![")
    assert "https://github.com/crewAIInc/" in "\n".join(guide[-10:])
    assert os.environ["CREWAI_DISABLE_TELEMETRY"] == "true"
    assert os.environ["CREWAI_TRACING_ENABLED"] == "false"
    print("V01/V02/V04/V05/V06: direct/copy/assets/input-preservation PASS")


ERROR = "recipe05: deliberate A failure"


def verify():
    for delays in ({"delay_a": 0.01, "delay_b": 0.04}, {"delay_a": 0.04, "delay_b": 0}):
        state = run_flow(delays, failure=True)
        assert state.events.count("A:error") == 1
        assert state.events.count("A:start") == state.events.count("B:start") == 1
        assert "join" not in state.events and "report" not in state.events
        assert state.result == {}
        print("C05 sibling observation:", state.events)
        if delays["delay_b"] == 0:
            assert state.events.index("B:done") < state.events.index("A:error")
        else:
            assert "B:done" not in state.events
    good = run_flow({"fail_a": False})
    assert good.result == {"A": "A complete", "B": "B complete"}
    joined(good, ["A", "B"])
    terminal(good)
    assert state.value_a is None and state.events is not good.events
    common({}, failure=True)
    # Direct success entry without changing checked-in input.
    with tempfile.TemporaryDirectory() as tmp:
        copied = Path(tmp) / "success"
        shutil.copytree(HERE, copied)
        (copied / "input.json").write_text(json.dumps(DEFAULT | {"fail_a": False}))
        assert entry(copied)["result"] == good.result


if __name__ == "__main__":
    verify()
    print("V03.C05 and recipe C05 cases PASS (CrewAI 1.15.40)")
