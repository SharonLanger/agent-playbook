"""Gate, archive a clean Git revision, build, hash, and verify an isolated release."""

import argparse
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import tomllib
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tooling.toolchain import pinned_uv
from tooling.verify_wheel import verify_wheel

APP = Path(__file__).resolve().parents[1]


def capture(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> str:
    return subprocess.check_output(command, cwd=cwd, env=env, text=True).strip()


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> None:
    print("+ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, env=env, check=True)


def release_destination(output: Path | None, version: str, commit: str) -> Path:
    if output is not None:
        destination = output.resolve()
        if destination.exists():
            raise RuntimeError(
                "Output already exists; choose an unused --output directory."
            )
        return destination

    base = APP / "dist" / f"{version}-{commit[:12]}"
    destination = base
    attempt = 2
    while destination.exists():
        destination = base.with_name(f"{base.name}-{attempt}")
        attempt += 1
    return destination.resolve()


def validate_release_source() -> tuple[Path, str, str]:
    repo = Path(capture(["git", "rev-parse", "--show-toplevel"], APP))
    changes = capture(["git", "status", "--short", "--untracked-files=all"], repo)
    if changes:
        raise RuntimeError(
            "Release requires a clean committed checkout. Git still sees:\n"
            f"{changes}\nCommit these changes or restore only the edits you intended "
            "to discard. Pushing is not required."
        )
    commit = capture(["git", "rev-parse", "HEAD"], repo)
    project = tomllib.loads((APP / "pyproject.toml").read_text())
    version = str(project["project"]["version"])
    lock = tomllib.loads((APP / "uv.lock").read_text())
    locked_versions = [
        package["version"]
        for package in lock["package"]
        if package["name"] == project["project"]["name"]
    ]
    if locked_versions != [version]:
        raise RuntimeError(
            f"Version mismatch: pyproject.toml has {version}, uv.lock has "
            f"{', '.join(locked_versions) or 'no project version'}. "
            "Run python app/tooling/version.py <version>, then commit both files."
        )
    return repo, commit, version


def assert_source_unchanged(repo: Path, commit: str) -> None:
    if (
        capture(["git", "status", "--porcelain"], repo)
        or capture(["git", "rev-parse", "HEAD"], repo) != commit
    ):
        raise RuntimeError("Checkout changed during checks; release aborted.")


def build_wheel(repo: Path, commit: str, destination: Path, uv: str) -> Path:
    """Build the exact committed app tree, with embedded source metadata."""
    archive = subprocess.check_output(
        ["git", "archive", "--format=tar", f"{commit}:app"], cwd=repo
    )
    with tempfile.TemporaryDirectory(prefix="agent-playbook-release-") as temporary:
        source = Path(temporary) / "source"
        source.mkdir()
        with tarfile.open(fileobj=io.BytesIO(archive)) as files:
            files.extractall(source, filter="data")
        (source / "src/agent_playbook/_build_info.py").write_text(
            f'SOURCE_COMMIT = "{commit}"\n'
        )
        destination.mkdir(parents=True)
        run(
            [uv, "build", "--wheel", "--no-sources", "--out-dir", str(destination)],
            source,
        )
    wheels = list(destination.glob("*.whl"))
    if len(wheels) != 1:
        raise RuntimeError("Expected exactly one Wheel.")
    return wheels[0]


def write_release_manifest(destination: Path, evidence: dict[str, str | bool]) -> None:
    (destination / "release.json").write_text(json.dumps(evidence, indent=2) + "\n")


def install_release(destination: Path, wheel: Path, uv: str) -> Path:
    environment = destination / "venv"
    run([uv, "venv", "--python", sys.executable, str(environment)], destination)
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    run(
        [uv, "pip", "install", "--python", str(python), "--no-deps", str(wheel)],
        destination,
    )
    return python


def verify_installed_release(
    destination: Path, python: Path, version: str, commit: str
) -> tuple[str, Path]:
    """Verify application behavior, identity, isolation and checkout-only guards."""
    environment = destination / "venv"
    clean_env = os.environ.copy()
    for key in ("PYTHONPATH", "PYTHONHOME"):
        clean_env.pop(key, None)
    clean_env["PYTHONNOUSERSITE"] = "1"
    run([str(python), "-I", "-m", "agent_playbook.cli", "run"], destination, clean_env)
    reported = capture(
        [str(python), "-I", "-m", "agent_playbook.cli", "version"],
        destination,
        clean_env,
    )
    if reported != f"agent-playbook {version} (source: {commit})":
        raise RuntimeError("Installed metadata differs from release evidence.")
    location = Path(
        capture(
            [
                str(python),
                "-I",
                "-c",
                "import agent_playbook; print(agent_playbook.__file__)",
            ],
            destination,
            clean_env,
        )
    )
    if not location.is_relative_to(environment):
        raise RuntimeError("Release imported code outside its isolated environment.")
    for arguments in (
        ["test"],
        ["check"],
        ["format"],
        ["release"],
        ["version", "patch"],
    ):
        result = subprocess.run(
            [str(python), "-I", "-m", "agent_playbook.cli", *arguments],
            cwd=destination,
            env=clean_env,
            capture_output=True,
            text=True,
        )
        if (
            result.returncode != 2
            or "Development command requires" not in result.stderr
        ):
            raise RuntimeError(
                f"Release unexpectedly accepted development command {arguments}."
            )
    return reported, location


def build_release(output: Path | None) -> None:
    repo, commit, version = validate_release_source()
    destination = release_destination(output, version, commit)
    uv = pinned_uv(APP)
    if uv is None:
        raise RuntimeError(
            "Pinned uv was not found; run app/tooling/bootstrap.py first."
        )
    run([sys.executable, "-m", "agent_playbook.cli", "check"], APP)
    assert_source_unchanged(repo, commit)
    wheel = build_wheel(repo, commit, destination, uv)
    digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
    evidence = {
        "version": version,
        "source_commit": commit,
        "wheel": wheel.name,
        "sha256": digest,
        "verified": False,
    }
    write_release_manifest(destination, evidence)
    (destination / "SHA256SUMS").write_text(f"{digest}  {wheel.name}\n")
    verify_wheel(wheel, digest)

    python = install_release(destination, wheel, uv)
    reported, location = verify_installed_release(destination, python, version, commit)
    evidence["verified"] = True
    write_release_manifest(destination, evidence)
    print(reported)
    print(
        f"Verified release: {destination}\nSHA-256: {digest}\nInstalled source: {location}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        help="New directory for the Wheel, evidence and isolated environment.",
    )
    args = parser.parse_args()
    try:
        build_release(args.output)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Release failed: {error}\n")


if __name__ == "__main__":
    main()
