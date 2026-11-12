"""Release errors identify the files and metadata blocking a build."""

from pathlib import Path
from unittest.mock import patch

import pytest

from tooling import release


def test_dirty_checkout_lists_the_paths(tmp_path: Path) -> None:
    with (
        patch.object(release, "APP", tmp_path),
        patch.object(
            release,
            "capture",
            side_effect=[str(tmp_path), " M app/pyproject.toml\n?? notes.txt"],
        ),
        pytest.raises(
            RuntimeError, match=r"(?s)app/pyproject.toml.*notes.txt"
        ) as error,
    ):
        release.build_release(None)
    assert "Pushing is not required" in str(error.value)


def test_committed_version_mismatch_is_actionable(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname="agent-playbook"\nversion="0.0.2"\n'
    )
    (tmp_path / "uv.lock").write_text(
        '[[package]]\nname="agent-playbook"\nversion="0.0.1"\n'
    )
    with (
        patch.object(release, "APP", tmp_path),
        patch.object(release, "capture", side_effect=[str(tmp_path), "", "abc123"]),
        pytest.raises(
            RuntimeError, match="pyproject.toml has 0.0.2, uv.lock has 0.0.1"
        ),
    ):
        release.build_release(None)
