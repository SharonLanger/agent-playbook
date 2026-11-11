"""Reject corruption before installing a release artifact."""

import hashlib
from pathlib import Path

import pytest

from scripts.verify_wheel import verify_wheel


def test_wheel_corruption_is_detected(tmp_path: Path) -> None:
    wheel = tmp_path / "example.whl"
    wheel.write_bytes(b"original artifact")
    digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
    verify_wheel(wheel, digest)
    wheel.write_bytes(b"changed artifact")
    with pytest.raises(ValueError, match="mismatch"):
        verify_wheel(wheel, digest)


def test_invalid_digest_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="64 lowercase"):
        verify_wheel(tmp_path / "unused.whl", "invalid")
