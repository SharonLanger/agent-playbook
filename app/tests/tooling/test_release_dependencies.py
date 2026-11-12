"""A release installs locked hashes, then its wheel, and checks dependency consistency."""

from pathlib import Path
from unittest.mock import patch

import pytest

from tooling import release


def test_dependency_install_uses_hashes_without_resolving_new_versions(
    tmp_path: Path,
) -> None:
    wheel = tmp_path / "app.whl"
    with patch.object(release, "run") as run:
        release.install_release(tmp_path, wheel, "uv")
    calls = [call.args[0] for call in run.call_args_list]
    dependency_install = next(
        command for command in calls if "--requirements" in command
    )
    assert (
        "--require-hashes" in dependency_install and "--no-deps" in dependency_install
    )
    assert dependency_install[-1] == str(tmp_path / "requirements.txt")
    assert calls.index(dependency_install) < next(
        i for i, command in enumerate(calls) if str(wheel) in command
    )
    assert calls[-1][1:3] == ["pip", "check"]


def test_failed_dependency_install_stops_before_wheel(tmp_path: Path) -> None:
    with patch.object(
        release, "run", side_effect=[None, RuntimeError("hash mismatch")]
    ) as run:
        with pytest.raises(RuntimeError, match="hash mismatch"):
            release.install_release(tmp_path, tmp_path / "app.whl", "uv")
    assert run.call_count == 2
