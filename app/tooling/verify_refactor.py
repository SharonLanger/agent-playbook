"""Review the refactor with the quality gate, CLI smoke checks and optional release.

Run with app/.venv/bin/python. Uses the offline test fixture and never edits source,
local configuration or existing releases. --build-release creates a new installation
from a clean commit. This review helper may be removed after refactor acceptance.
"""

import argparse
import hashlib
import os
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

from pydantic import TypeAdapter

APP = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-I", "-m", "agent_playbook.cli"]


def review_environment() -> dict[str, str]:
    env = os.environ.copy()
    for name in list(env):
        if name.startswith("AGENT_PLAYBOOK_") or name in ("PYTHONPATH", "PYTHONHOME"):
            env.pop(name, None)
    env["AGENT_PLAYBOOK_CONFIG"] = str(APP / "tests/fixtures/offline.yaml")
    return env


def check(
    label: str,
    command: list[str],
    env: dict[str, str],
    cwd: Path,
    *,
    expected: int = 0,
    contains: str | None = None,
    timeout: int = 180,
) -> str:
    print(f"\nChecking: {label}", flush=True)
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        capture_output=contains is not None,
        text=True,
        timeout=timeout,
    )
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != expected or (
        contains is not None and contains not in output
    ):
        print(output, end="" if output.endswith("\n") else "\n")
        raise RuntimeError(
            f"{label}: expected exit {expected}, received {result.returncode}; "
            f"required output: {contains!r}"
        )
    if output:
        print(output, end="" if output.endswith("\n") else "\n")
    print(f"PASS {label}", flush=True)
    return output


def verify_release(destination: Path, env: dict[str, str], cwd: Path) -> None:
    manifest = TypeAdapter(dict[str, object]).validate_json(
        (destination / "release.json").read_text(), strict=True
    )
    version: object = manifest.get("version")
    commit: object = manifest.get("source_commit")
    wheel_name: object = manifest.get("wheel")
    if (
        manifest.get("verified") is not True
        or not isinstance(version, str)
        or not isinstance(commit, str)
        or not isinstance(wheel_name, str)
        or Path(wheel_name).name != wheel_name
    ):
        raise RuntimeError(
            "Select a verified release with version, commit and wheel evidence."
        )
    for filename, key in (
        (wheel_name, "sha256"),
        ("requirements.txt", "requirements_sha256"),
        ("uv.lock", "lock_sha256"),
    ):
        if hashlib.sha256(
            (destination / filename).read_bytes()
        ).hexdigest() != manifest.get(key):
            raise RuntimeError(f"Release evidence hash mismatch: {filename}")
    print("PASS release evidence hashes", flush=True)
    python = (
        destination
        / "venv"
        / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    )
    installed = [str(python), "-I", "-m", "agent_playbook.cli"]
    check(
        "installed identity",
        [*installed, "version"],
        env,
        cwd,
        contains=f"agent-playbook {version} (source: {commit})",
    )
    check(
        "installed workflows and offline probe",
        [str(python), "-I", str(APP / "tooling/verify_runtime.py"), "run"],
        env,
        cwd,
        contains="zero Python socket/DNS attempts",
    )
    check(
        "installed import isolation",
        [
            str(python),
            "-I",
            "-c",
            "import agent_playbook,sys; from pathlib import Path; "
            "assert Path(agent_playbook.__file__).resolve().is_relative_to(Path(sys.argv[1])); "
            "print('isolated import confirmed')",
            str(destination / "venv"),
        ],
        env,
        cwd,
        contains="isolated import confirmed",
    )
    for command in ("test", "check", "format", "release"):
        check(
            f"installed {command} guard",
            [*installed, command],
            env,
            cwd,
            expected=2,
            contains="Development command requires",
        )
    check(
        "installed dev-run guard",
        [*installed, "dev-run"],
        env,
        cwd,
        expected=2,
        contains="dev-run requires",
    )
    check(
        "installed version mutation guard",
        [*installed, "version", "patch"],
        env,
        cwd,
        expected=2,
        contains="Development command requires",
    )
    with zipfile.ZipFile(destination / wheel_name) as wheel:
        names = wheel.namelist()
    forbidden = ("tooling/", "tests/", "examples/", "configs/")
    if any(
        name.startswith(forbidden)
        or name.endswith(("application.yaml", "application.local.yaml"))
        for name in names
    ):
        raise RuntimeError("Wheel contains checkout-only code or active configuration.")
    if any(
        name.endswith(("application/runner.py", "releases/selection.py"))
        for name in names
    ):
        raise RuntimeError("Wheel still contains pre-refactor runtime modules.")
    required = (
        "application/assembly.py",
        "application/workflow_factory.py",
        "application/workflow_runner.py",
        "releases/discovery.py",
        "releases/launcher.py",
    )
    if not all("agent_playbook/" + name in names for name in required):
        raise RuntimeError("Wheel is missing a refactored runtime component.")
    print("PASS wheel contents", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    release = parser.add_mutually_exclusive_group()
    release.add_argument(
        "--build-release",
        action="store_true",
        help="Build and verify a new release; requires a clean committed checkout.",
    )
    release.add_argument(
        "--release",
        type=Path,
        help="Also verify an existing refactored release directory.",
    )
    args = parser.parse_args()
    env = review_environment()
    destination = Path(args.release).resolve() if args.release else None
    try:
        with tempfile.TemporaryDirectory(prefix="agent-playbook-review-") as temporary:
            cwd = Path(temporary)
            if args.build_release:
                destination = APP / "dist" / f"refactor-review-{time.time_ns()}"
                check(
                    "release build (includes full quality gate)",
                    [*CLI, "release", "--output", str(destination)],
                    env,
                    cwd,
                    timeout=1800,
                )
            else:
                check("full quality gate", [*CLI, "check"], env, cwd, timeout=600)
            check("CLI help", [*CLI, "--help"], env, cwd, contains="dev-run")
            check(
                "version", [*CLI, "version"], env, cwd, contains="source: development"
            )
            console = Path(sys.executable).parent / (
                "agent-playbook.exe" if os.name == "nt" else "agent-playbook"
            )
            check(
                "console entry point",
                [str(console), "--help"],
                env,
                cwd,
                contains="dev-run",
            )
            check(
                "direct package entry point",
                [sys.executable, "-I", "-m", "agent_playbook"],
                env,
                cwd,
                contains="[WF-01] result: [Hello, workflow!]",
            )
            check(
                "workflow arguments",
                [
                    *CLI,
                    "dev-run",
                    "--workflow",
                    "wf-02",
                    "--input",
                    '{"initial":10,"increment":-2,"multiplier":3}',
                ],
                env,
                cwd,
                contains="[WF-02] result: 24",
            )
            check(
                "invalid command",
                [*CLI, "unknown"],
                env,
                cwd,
                expected=2,
                contains="invalid choice",
            )
            check(
                "invalid workflow input",
                [*CLI, "dev-run", "--workflow", "wf-03", "--input", '{"score":101}'],
                env,
                cwd,
                expected=2,
                contains="Input error",
            )
            check(
                "source workflows and offline probe",
                [
                    sys.executable,
                    "-I",
                    str(APP / "tooling/verify_runtime.py"),
                    "dev-run",
                ],
                env,
                cwd,
                contains="zero Python socket/DNS attempts",
            )
            if destination is not None:
                verify_release(destination, env, cwd)
                if args.build_release:
                    check(
                        "source launcher selects the new release",
                        [*CLI, "run"],
                        env,
                        cwd,
                        contains=f"from {destination}",
                    )
        print("\nPASS all requested refactor checks.")
        if destination is None:
            print("Release checks NOT RUN. Use --build-release or --release PATH.")
        else:
            print(f"Verified release: {destination}")
        return 0
    except (
        OSError,
        ValueError,
        RuntimeError,
        subprocess.TimeoutExpired,
        zipfile.BadZipFile,
    ) as error:
        print(f"\nFAIL refactor review: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
