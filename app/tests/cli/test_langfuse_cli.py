"""The public Langfuse command validates before entering tooling."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agent_playbook.cli import commands


@pytest.mark.parametrize("action", ("start", "stop", "status", "logs", "open", "check"))
def test_dispatch(action: str) -> None:
    with patch.object(commands, "run_development", return_value=0) as bridge:
        assert commands.main(["langfuse", f"--{action}"]) == 0
    bridge.assert_called_once_with("langfuse", [f"--{action}"])


def test_relative_config_and_env_file_across_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    with patch.object(commands, "run_development", return_value=0) as bridge:
        assert commands.main(["langfuse", "--check", "--config", "my config.yaml"]) == 0
        assert bridge.call_args.args[1][-1] == str(tmp_path / "my config.yaml")
        assert (
            commands.main(["langfuse", "--start", "--env-file", "my secrets.env"]) == 0
        )
        assert bridge.call_args.args[1][-1] == str(tmp_path / "my secrets.env")


def test_invalid_and_help_never_dispatch(capsys: pytest.CaptureFixture[str]) -> None:
    with patch.object(commands, "run_development", side_effect=AssertionError):
        for args in (
            [],
            ["--start", "--stop"],
            ["--follow"],
            ["--open", "--config", "x"],
        ):
            with pytest.raises(SystemExit) as error:
                commands.main(["langfuse", *args])
            assert error.value.code == 2
        with pytest.raises(SystemExit) as error:
            commands.main(["langfuse", "--help"])
        assert error.value.code == 0
    assert "--check" in capsys.readouterr().out


def test_installed_release_rejects_management(
    capsys: pytest.CaptureFixture[str],
) -> None:
    from agent_playbook.cli import development

    with (
        patch.object(development, "SOURCE_COMMIT", "installed-release"),
        patch.object(development.subprocess, "run", side_effect=AssertionError),
    ):
        assert commands.main(["langfuse", "--status"]) == 2
    assert "source checkout" in capsys.readouterr().err
