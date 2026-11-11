"""Repeated releases preserve earlier output and choose a new destination."""

import sys
from pathlib import Path

import pytest


def test_repeated_release_picks_next_unused_folder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    try:
        from scripts import release
    finally:
        sys.path.pop(0)

    monkeypatch.setattr(release, "APP", tmp_path)
    base = tmp_path / "dist" / "0.0.1-abcdef123456"
    base.mkdir(parents=True)
    (base / "release.json").write_text("original")
    second = base.with_name(base.name + "-2")
    second.mkdir()

    assert release.release_destination(
        None, "0.0.1", "abcdef1234567890"
    ) == base.with_name(base.name + "-3")
    assert (base / "release.json").read_text() == "original"


def test_explicit_output_must_be_unused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    try:
        from scripts import release
    finally:
        sys.path.pop(0)

    output = tmp_path / "custom"
    output.mkdir()
    with pytest.raises(RuntimeError, match="already exists"):
        release.release_destination(output, "0.0.1", "abcdef1234567890")
    assert release.release_destination(
        tmp_path / "next", "0.0.1", "abcdef1234567890"
    ) == (tmp_path / "next")
