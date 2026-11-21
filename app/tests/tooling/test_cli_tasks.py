"""Selective checks and version bumps preserve their distinct responsibilities."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agent_playbook.cli import commands, development
from tooling.checks import select_commands
from tooling.version import next_patch


@pytest.mark.parametrize(
    ("arguments", "task", "forwarded"),
    [
        (["check"], "check", []),
        (["check", "--lint", "--types"], "check", ["--types", "--lint"]),
        (["check", "--format"], "check", ["--format"]),
        (["format"], "format", []),
        (["test"], "test", []),
        (["version", "patch"], "version", ["patch"]),
        (["version", "minor"], "version", ["minor"]),
        (["version", "major"], "version", ["major"]),
        (["release"], "release", []),
    ],
)
def test_dispatch(arguments: list[str], task: str, forwarded: list[str]) -> None:
    with (
        patch("sys.argv", ["agent-playbook", *arguments]),
        patch.object(commands, "run_development", return_value=17) as run,
    ):
        assert commands.main() == 17
        assert run.call_args.args[0] == task
        assert (
            run.call_args.args[1] if len(run.call_args.args) > 1 else []
        ) == forwarded


def test_selectors_exclude_tests_and_keep_gate_order() -> None:
    assert [x[0] for x in select_commands("check", [])] == [
        "pyright",
        "ruff",
        "ruff",
        "pytest",
    ]
    assert [x[0] for x in select_commands("check", ["lint", "types"])] == [
        "pyright",
        "ruff",
    ]
    assert "--check" in select_commands("check", ["format"])[0]
    assert "--check" not in select_commands("format", [])[0]
    assert select_commands("test", []) == [["pytest", "-q", "tests"]]
    commands = (
        select_commands("check", [])
        + select_commands("test", [])
        + select_commands("format", [])
    )
    for command in commands:
        assert all("examples" not in argument for argument in command)


@pytest.mark.parametrize(
    ("current", "expected"), [("0.0.8", "0.0.9"), ("1.2.99", "1.2.100")]
)
def test_patch_arithmetic(current: str, expected: str) -> None:
    assert next_patch(current) == expected


@pytest.mark.parametrize("current", ["1.2", "1.2.3rc1", "bad"])
def test_patch_rejects_nonstandard_version(current: str) -> None:
    with pytest.raises(ValueError):
        next_patch(current)


@pytest.mark.parametrize(
    "task",
    ["check", "test", "format", "release", "version", "services", "logs", "langfuse"],
)
def test_installed_release_cannot_mutate_checkout(task: str) -> None:
    with (
        patch.object(development, "SOURCE_COMMIT", "release-commit"),
        patch.object(development.subprocess, "run") as run,
    ):
        assert development.run_development(task) == 2
        run.assert_not_called()


def test_release_output_is_resolved_at_cli_boundary(tmp_path: Path) -> None:
    with (
        patch.object(commands, "run_development", return_value=0) as forward,
        patch("os.getcwd", return_value=str(tmp_path)),
    ):
        assert commands.main(["release", "--output", "new folder"]) == 0
    assert forward.call_args.args == (
        "release",
        ["--output", str(tmp_path / "new folder")],
    )


@pytest.mark.parametrize("command", ["logs", "services"])
@pytest.mark.parametrize(
    ("flags", "code"), [(["--help"], 0), ([], 2), (["--start", "--stop"], 2)]
)
def test_service_parser_early_exit(command: str, flags: list[str], code: int) -> None:
    with patch.object(commands, "run_development", side_effect=AssertionError):
        with pytest.raises(SystemExit) as result:
            commands.main([command, *flags])
    assert result.value.code == code


@pytest.mark.parametrize("entry", ["run", "dev-run"])
def test_workflow_entry_points_do_not_delegate_service_management(entry: str) -> None:
    with (
        patch.object(commands, "SOURCE_COMMIT", "development"),
        patch.object(commands, "present_workflow", return_value=0) as workflow,
        patch.object(commands, "present_release", return_value=0) as release,
        patch.object(commands, "run_development", side_effect=AssertionError),
    ):
        assert commands.main([entry, "--workflow", "wf-01"]) == 0
    if entry == "run":
        release.assert_called_once_with(None, ["--workflow", "wf-01"])
        workflow.assert_not_called()
    else:
        workflow.assert_called_once_with("wf-01", None, None)
        release.assert_not_called()
