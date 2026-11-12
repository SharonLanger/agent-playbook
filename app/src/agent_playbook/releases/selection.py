"""Select and launch completed local releases."""

import json
import os
import subprocess
import sys
from pathlib import Path

from agent_playbook.config.paths import configuration_path


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


def run_release(
    requested_version: str | None, arguments: list[str] | None = None
) -> int:
    selected = find_release(requested_version)
    if selected is None:
        detail = f" version {requested_version}" if requested_version else ""
        print(
            f"No installed release{detail} found in app/dist. Build one with "
            "agent-playbook release, or run editable code with agent-playbook dev-run.",
            file=sys.stderr,
        )
        return 2
    executable, release_version = selected
    print(f"Running release {release_version} from {executable.parents[2]}", flush=True)
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    # Pass the shared external path, never a copy inside a versioned release.
    # Environment forwarding preserves old releases that do not accept --config.
    if "--config" not in (arguments or []) and "AGENT_PLAYBOOK_CONFIG" not in env:
        env["AGENT_PLAYBOOK_CONFIG"] = str(configuration_path())
    return subprocess.run(
        [str(executable), "-I", "-m", "agent_playbook.cli", "run", *(arguments or [])],
        env=env,
        check=False,
    ).returncode
