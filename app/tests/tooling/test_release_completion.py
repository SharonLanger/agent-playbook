"""A failed installed-release verification must leave the build incomplete."""

from pathlib import Path
from unittest.mock import patch

import pytest

from tooling import release


def test_verification_failure_keeps_manifest_incomplete(tmp_path: Path) -> None:
    wheel = tmp_path / "example.whl"
    wheel.write_bytes(b"wheel")
    (tmp_path / "requirements.txt").write_text("dependency==1\n")
    (tmp_path / "uv.lock").write_text("version = 1\n")
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
        patch.object(release, "verify_wheel_contents"),
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


def test_release_verifier_cases_cover_registered_implementations() -> None:
    from agent_playbook.application.workflow_registry import workflow_registry
    from tooling.verify_runtime import IMPLEMENTATION_CASES

    assert set(IMPLEMENTATION_CASES) == set(workflow_registry())


def test_broken_deferred_import_fails_runtime_verification() -> None:
    import subprocess
    import sys

    script = """
import builtins, runpy, sys
original = builtins.__import__
def guard(name, *args, **kwargs):
    if name == 'agent_playbook.workflows.wf_03_conditional_route.flow':
        raise ModuleNotFoundError('broken built-in')
    return original(name, *args, **kwargs)
builtins.__import__ = guard
path = sys.argv[1]
sys.argv = ['verify_runtime.py', 'dev-run']
runpy.run_path(path, run_name='__main__')
"""
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            script,
            str(Path(__file__).resolve().parents[2] / "tooling/verify_runtime.py"),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode != 0
    assert "Installed workflow contract failed: wf-03" in result.stderr
    assert "PASS wf-03" not in result.stdout
