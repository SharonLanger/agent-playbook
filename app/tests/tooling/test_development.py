"""The combined gate must fail visibly and stop after a failing tool."""

import subprocess
from unittest.mock import patch

import pytest

from tooling.checks import run_tools

COMMANDS = [
    ["pyright"],
    ["ruff", "check", "src", "tooling", "examples", "tests"],
    ["ruff", "format", "--check", "src", "tooling", "examples", "tests"],
    ["pytest", "-q", "tests"],
]
LABELS = ["Pyright (types)", "Ruff (lint)", "Ruff (formatting)", "pytest (tests)"]


@pytest.mark.parametrize("failed_index", range(4))
def test_gate_propagates_failure_and_stops(
    failed_index: int, capsys: pytest.CaptureFixture[str]
) -> None:
    with (
        patch("tooling.checks.importlib.util.find_spec"),
        patch(
            "tooling.checks.subprocess.run",
            side_effect=[subprocess.CompletedProcess([], 0)] * failed_index
            + [subprocess.CompletedProcess([], 23)],
        ) as runner,
    ):
        assert run_tools(COMMANDS) == 23
        assert runner.call_count == failed_index + 1
    output = capsys.readouterr().out
    summary = output.split("Check summary\n")[1]
    assert f"FAIL     {LABELS[failed_index]} (exit 23)" in summary
    for label in LABELS[:failed_index]:
        assert f"PASS     {label}" in summary
    for label in LABELS[failed_index + 1 :]:
        assert f"NOT RUN  {label}" in summary
    assert "Result: PASS" not in output


def test_gate_runs_all_checks_in_order(capsys: pytest.CaptureFixture[str]) -> None:
    with (
        patch("tooling.checks.importlib.util.find_spec"),
        patch(
            "tooling.checks.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0),
        ) as runner,
    ):
        assert run_tools(COMMANDS) == 0
        assert [call.args[0][2:] for call in runner.call_args_list] == COMMANDS
    output = capsys.readouterr().out
    assert "Result: PASS (4 passed, 0 failed, 0 not run)" in output
    for index, label in enumerate(LABELS, start=1):
        assert f"[{index}/4] {label}" in output


def test_missing_tool_is_an_error(capsys: pytest.CaptureFixture[str]) -> None:
    with (
        patch(
            "tooling.checks.importlib.util.find_spec",
            side_effect=[object(), None],
        ),
        patch("tooling.checks.subprocess.run") as runner,
    ):
        assert run_tools(COMMANDS) == 2
        runner.assert_not_called()
    output = capsys.readouterr().out
    assert "Missing development tool ruff; rerun bootstrap." in output
    assert "No checks were started" in output
    assert "NOT RUN  Pyright (types)" in output
    assert "FAIL     Ruff (lint) (exit 2)" in output


def test_tool_launch_failure_has_a_summary(capsys: pytest.CaptureFixture[str]) -> None:
    with (
        patch("tooling.checks.importlib.util.find_spec"),
        patch(
            "tooling.checks.subprocess.run",
            side_effect=OSError("Unable to launch interpreter"),
        ) as runner,
    ):
        assert run_tools(COMMANDS) == 2
        assert runner.call_count == 1
    output = capsys.readouterr().out
    assert "Could not start Pyright (types): Unable to launch interpreter" in output
    assert "Result: FAIL (0 passed, 1 failed, 3 not run)" in output
