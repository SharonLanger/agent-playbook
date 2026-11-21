"""Opt-in daemon-free Compose syntax and project-selection check."""

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import cast
from unittest.mock import patch

from tooling.observability import manage

APP = Path(__file__).resolve().parents[2]
MARKER = "synthetic-compose-smoke-marker"
INFRASTRUCTURE_NAMES = (
    "POSTGRES_PASSWORD",
    "CLICKHOUSE_PASSWORD",
    "REDIS_AUTH",
    "MINIO_ROOT_PASSWORD",
    "NEXTAUTH_SECRET",
    "SALT",
    "ENCRYPTION_KEY",
)


def run(
    argv: list[str], environment: dict[str, str]
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        check=False,
        text=True,
        capture_output=True,
        env=environment,
        timeout=15,
    )


def main() -> int:
    environment = {
        "PATH": os.environ.get("PATH", os.defpath),
        "COMPOSE_DISABLE_ENV_FILE": "1",
    }
    version = run(["docker", "compose", "version"], environment)
    if version.returncode:
        print("FAIL: Docker Compose version unavailable.")
        return 1
    print(version.stdout.strip())
    revision = run(["git", "-C", str(APP), "rev-parse", "HEAD"], environment)
    if revision.returncode == 0:
        print(f"Checkout HEAD: {revision.stdout.strip()}")
    logging = run(
        [
            "docker",
            "compose",
            "-f",
            str(APP / "tooling" / "logging" / "compose.yaml"),
            "config",
            "--quiet",
        ],
        environment,
    )
    print(
        f"VictoriaLogs config --quiet: {'PASS' if logging.returncode == 0 else 'FAIL'}"
    )
    failed = logging.returncode != 0
    with tempfile.TemporaryDirectory() as directory:
        settings = Path(directory) / "synthetic.env"
        values = "".join(f"{name}={MARKER}\n" for name in INFRASTRUCTURE_NAMES)
        settings.write_text(values)
        compose = manage._compose_argv  # pyright: ignore[reportPrivateUsage]
        langfuse = run(compose(settings, "config", "--quiet"), environment)
        print(
            f"Langfuse config --quiet: {'PASS' if langfuse.returncode == 0 else 'FAIL'}"
        )
        failed = failed or langfuse.returncode != 0

        for label, file_project, shell_project, expected in (
            ("default", "", "", "observability"),
            ("file", "file-project", "", "file-project"),
            ("shell", "file-project", "shell-project", "shell-project"),
        ):
            settings.write_text(
                values
                + (f"COMPOSE_PROJECT_NAME={file_project}\n" if file_project else "")
            )
            selected_env = environment | (
                {"COMPOSE_PROJECT_NAME": shell_project} if shell_project else {}
            )
            result = run(compose(settings, "config", "--format", "json"), selected_env)
            observed = "(unavailable)"
            if result.returncode == 0:
                try:
                    model: object = json.loads(result.stdout)
                    if isinstance(model, dict):
                        name = cast(dict[str, object], model).get("name")
                        if name in ("observability", "file-project", "shell-project"):
                            observed = str(name)
                except ValueError:
                    pass
            passed = observed == expected
            print(
                f"Langfuse {label}: expected {expected}, observed {observed}, {'PASS' if passed else 'FAIL'}"
            )
            failed = failed or not passed
        settings.write_text(values)
        with patch.dict(os.environ, environment, clear=True):
            redact = manage._log_redactor(settings, "observability")  # pyright: ignore[reportPrivateUsage]
            passed = MARKER not in redact(f"synthetic logs: {MARKER}")
            print(
                f"Langfuse structured single-line redaction: {'PASS' if passed else 'FAIL'}"
            )
            failed = failed or not passed

            os.environ["POSTGRES_PASSWORD"] = (
                "synthetic-first-line\ncontinuation=synthetic-continuation"
            )
            passed = False
            try:
                manage._log_redactor(settings, "observability")  # pyright: ignore[reportPrivateUsage]
            except manage.SettingsConflict as error:
                passed = "multiline private setting" in str(error)
            print(
                f"Langfuse structured multiline rejection: {'PASS' if passed else 'FAIL'}"
            )
            failed = failed or not passed
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
