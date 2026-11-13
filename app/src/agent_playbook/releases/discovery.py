"""Discover completed local release installations without launching them."""

import json
from pathlib import Path


def find_release(
    requested_version: str | None, releases_dir: Path | None = None
) -> tuple[Path, str] | None:
    if releases_dir is None:
        releases_dir = Path(__file__).resolve().parents[3] / "dist"
    candidates: list[tuple[int, str, Path, str]] = []
    for manifest in releases_dir.glob("*/release.json"):
        try:
            data = json.loads(manifest.read_text())
            release_version = data["version"]
            executable = manifest.parent / "venv" / "bin" / "python"
            installed_cli = manifest.parent / "venv" / "bin" / "agent-playbook"
            if (
                isinstance(release_version, str)
                and (requested_version is None or release_version == requested_version)
                and executable.is_file()
                and installed_cli.is_file()
                and data.get("verified", True) is True
            ):
                candidates.append(
                    (
                        manifest.stat().st_mtime_ns,
                        manifest.parent.name,
                        executable,
                        release_version,
                    )
                )
        except (OSError, ValueError, KeyError, TypeError):
            continue
    if not candidates:
        return None
    _, _, executable, release_version = max(candidates)
    return executable, release_version
