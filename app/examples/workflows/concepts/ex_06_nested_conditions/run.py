"""Click Run on this file in PyCharm with the project's interpreter."""

import json
from pathlib import Path

from settings import configure


def main() -> None:
    suppress = configure()  # Must precede importing flow.py / CrewAI.
    from flow import ExampleFlow

    data = json.loads(Path(__file__).with_name("input.json").read_text())
    if not isinstance(data, dict):
        raise ValueError("input.json must contain an object")
    flow = ExampleFlow(suppress_flow_events=suppress)
    result = flow.kickoff(inputs=data)
    print("Result:", json.dumps(result))
    print("State:", flow.state.model_dump_json(exclude={"id"}))


if __name__ == "__main__":
    main()
