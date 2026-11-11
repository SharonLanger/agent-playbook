"""The combined gate must fail visibly and stop after a failing tool."""

import subprocess
from unittest.mock import patch

from agent_playbook.development import run_tools


def test_gate_propagates_failure_and_stops() -> None:
    with (
        patch("agent_playbook.development.importlib.util.find_spec"),
        patch(
            "agent_playbook.development.subprocess.run",
            side_effect=[subprocess.CompletedProcess([], 23)],
        ) as runner,
    ):
        assert run_tools([["pyright"], ["pytest", "-q"]]) == 23
        assert runner.call_count == 1


def test_missing_tool_is_an_error() -> None:
    with patch(
        "agent_playbook.development.importlib.util.find_spec", return_value=None
    ):
        assert run_tools([["pytest", "-q"]]) == 2
