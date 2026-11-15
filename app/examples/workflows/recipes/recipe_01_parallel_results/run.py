"""Run directly with the project's Python interpreter, from any directory."""

import json
import os
from pathlib import Path

# Supported switches must be set BEFORE importing CrewAI (also when copied).
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["CREWAI_TRACING_ENABLED"] = "false"

from flow import RecipeFlow  # noqa: E402


def main():
    data = json.loads(Path(__file__).with_name("input.json").read_text())
    if not isinstance(data, dict):
        raise ValueError("input.json must contain an object")
    flow = RecipeFlow(suppress_flow_events=True)
    try:
        result = flow.kickoff(inputs=data)
    finally:
        # Also retain inspection evidence if a branch fails. No exception is swallowed.
        print("STATE_JSON=" + flow.state.model_dump_json(exclude={"id"}), flush=True)
    print("RESULT_JSON=" + json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
