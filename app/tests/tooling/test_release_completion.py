"""A failed installed-release verification must leave the build incomplete."""

from pathlib import Path
from unittest.mock import patch

import pytest

from tooling import release


def test_verification_failure_keeps_manifest_incomplete(tmp_path: Path) -> None:
    wheel = tmp_path / "example.whl"
    wheel.write_bytes(b"wheel")
    with (
        patch.object(
            release, "validate_release_source", return_value=(tmp_path, "abc", "0.0.1")
        ),
        patch.object(release, "release_destination", return_value=tmp_path),
        patch.object(release, "pinned_uv", return_value="uv"),
        patch.object(release, "run"),
        patch.object(release, "assert_source_unchanged"),
        patch.object(release, "build_wheel", return_value=wheel),
        patch.object(release, "verify_wheel"),
        patch.object(
            release, "install_release", return_value=tmp_path / "venv/bin/python"
        ),
        patch.object(
            release,
            "verify_installed_release",
            side_effect=RuntimeError("installed verification failed"),
        ),
        pytest.raises(RuntimeError, match="installed verification failed"),
    ):
        release.build_release(None)

    assert '"verified": false' in (tmp_path / "release.json").read_text()
