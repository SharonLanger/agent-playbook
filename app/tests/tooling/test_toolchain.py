"""Keep the uv selection policy consistent across development commands."""

import subprocess
from pathlib import Path
from unittest.mock import patch

from tooling import toolchain


def test_wrong_path_version_uses_private_pinned_copy(tmp_path: Path) -> None:
    private = str(toolchain.private_uv_path(tmp_path))
    with (
        patch.object(toolchain.shutil, "which", return_value="/foreign/uv"),
        patch.object(
            toolchain.subprocess,
            "check_output",
            side_effect=["uv 0.12.0", "uv 0.13.6"],
        ) as probe,
    ):
        assert toolchain.pinned_uv(tmp_path) == private
        assert [call.args[0][0] for call in probe.call_args_list] == [
            "/foreign/uv",
            private,
        ]


def test_malformed_or_broken_candidates_fail_cleanly(tmp_path: Path) -> None:
    with (
        patch.object(toolchain.shutil, "which", return_value="/foreign/uv"),
        patch.object(
            toolchain.subprocess,
            "check_output",
            side_effect=["unexpected", subprocess.CalledProcessError(1, "uv")],
        ),
    ):
        assert toolchain.pinned_uv(tmp_path) is None
