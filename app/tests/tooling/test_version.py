"""Version arithmetic and transaction failures preserve checkout consistency."""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from tooling import version


@pytest.mark.parametrize(
    ("part", "expected"), [("patch", "0.2.8"), ("minor", "0.3.0"), ("major", "1.0.0")]
)
def test_bump_arithmetic(part: str, expected: str) -> None:
    assert version.next_version("0.2.7", part) == expected


@pytest.mark.parametrize("failure", [True, False])
def test_failed_update_restores_both_inputs(tmp_path: Path, failure: bool) -> None:
    project = tmp_path / "pyproject.toml"
    lock = tmp_path / "uv.lock"
    project.write_text('[project]\nname = "sample"\nversion = "0.2.7"\n')
    lock.write_text('[[package]]\nname = "sample"\nversion = "0.2.7"\n')
    originals = (project.read_bytes(), lock.read_bytes())

    def update(_command: list[str], *, check: bool) -> None:
        assert check
        project.write_text('[project]\nname = "sample"\nversion = "0.2.8"\n')
        if failure:
            lock.write_text("partially written")
            raise subprocess.CalledProcessError(1, "uv")

    with patch.object(version.subprocess, "run", side_effect=update):
        with pytest.raises((subprocess.CalledProcessError, ValueError)):
            version.update_version(tmp_path, "uv", "0.2.8")
    assert (project.read_bytes(), lock.read_bytes()) == originals


def test_explicit_version_retained_and_no_git_commands(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "sample"\nversion = "0.2.7"\n'
    )
    (tmp_path / "uv.lock").write_text(
        '[[package]]\nname = "sample"\nversion = "0.2.7"\n'
    )
    with (
        patch.object(version, "APP", tmp_path),
        patch.object(version, "pinned_uv", return_value="uv"),
        patch.object(version, "update_version") as update,
        patch("sys.argv", ["version.py", "2.3.4"]),
    ):
        version.main()
    update.assert_called_once_with(tmp_path, "uv", "2.3.4")


@pytest.mark.parametrize("argument", ["invalid", "1.2", "1.2.3rc1"])
def test_invalid_input_does_not_invoke_uv(argument: str) -> None:
    with (
        patch("sys.argv", ["version.py", argument]),
        patch.object(version, "pinned_uv") as uv,
        pytest.raises(SystemExit) as error,
    ):
        version.main()
    assert error.value.code == 2
    uv.assert_not_called()


def test_bare_cli_version_is_read_only(capsys: pytest.CaptureFixture[str]) -> None:
    from agent_playbook.cli import commands

    with patch.object(commands, "run_development") as update:
        assert commands.main(["version"]) == 0
    assert "agent-playbook " in capsys.readouterr().out
    update.assert_not_called()
