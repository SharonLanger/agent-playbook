"""Run all workflows in a fresh process with outbound network attempts denied.

Used with the installed release's Python (-I), so imports cannot fall back to the
checkout. This guard records even attempts that third-party code catches. It is a
regression probe for these Python workflow paths, not an OS network sandbox.
"""

import contextlib
import io
import os
import sys
from collections.abc import Mapping
from pathlib import Path

IMPLEMENTATION_CASES: dict[str, tuple[str, str, str]] = {
    "step_sequence": ("wf-01", "{}", "[Hello, workflow!]"),
    "shared_state": ("wf-02", '{"initial":3,"increment":2,"multiplier":4}', "20"),
    "conditional_route": ("wf-03", '{"score":80}', "pass"),
}


def offline_environment(source: Mapping[str, str]) -> dict[str, str]:
    """Isolate verification from checkout settings and provider opt-ins.

    Only verification subprocesses use this policy; normal application commands
    continue honoring their documented environment overrides.
    """
    clean = {
        key: value
        for key, value in source.items()
        if key not in {"PYTHONPATH", "PYTHONHOME"}
        and not key.startswith(("AGENT_PLAYBOOK_", "CREWAI_", "LANGFUSE_", "OTEL_"))
        and not key.endswith(("_API_KEY", "_TOKEN"))
    }
    clean.update(
        {
            "PYTHONNOUSERSITE": "1",
            "CREWAI_DISABLE_VERSION_CHECK": "true",
            "CREWAI_DISABLE_TELEMETRY": "true",
            "CREWAI_USAGE_TELEMETRY_ENABLED": "false",
            "CREWAI_TRACING_ENABLED": "false",
            "OTEL_SDK_DISABLED": "true",
        }
    )
    return clean


def main() -> None:
    attempts: list[str] = []

    def block_network(event: str, _arguments: tuple[object, ...]) -> None:
        if event in (
            "socket.connect",
            "socket.getaddrinfo",
            "socket.sendto",
            "socket.sendmsg",
        ):
            attempts.append(event)
            raise RuntimeError(f"Unexpected network attempt: {event}")

    # Verification uses committed fixture data, never the user's active settings.
    configuration = Path(__file__).resolve().parents[1] / "tests/fixtures/offline.yaml"
    clean_env = offline_environment(os.environ)
    os.environ.clear()
    os.environ.update(clean_env)
    sys.addaudithook(block_network)
    from agent_playbook.application.workflow_registry import workflow_registry
    from agent_playbook.cli.commands import main as cli_main

    command = sys.argv[1] if len(sys.argv) > 1 else "dev-run"
    if command not in ("run", "dev-run"):
        raise ValueError("Use run (installed) or dev-run (checkout).")
    if set(IMPLEMENTATION_CASES) != set(workflow_registry()):
        raise RuntimeError(
            "Release cases do not cover every registered implementation."
        )
    cases = (
        *IMPLEMENTATION_CASES.values(),
        ("wf-03", '{"score":40}', "needs_work"),
        ("wf-02-custom", "{}", "24"),
        ("wf-02-custom", '{"initial":2}', "0"),
        ("wf-03-custom", "{}", "needs_work"),
        ("wf-03-custom", '{"score":60}', "pass"),
    )
    for workflow, raw, expected in cases:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = cli_main(
                [
                    command,
                    "--config",
                    str(configuration),
                    "--workflow",
                    workflow,
                    "--input",
                    raw,
                ]
            )
        if (
            code != 0
            or f"[{workflow.upper()}] result: {expected}"
            not in output.getvalue().splitlines()
        ):
            raise RuntimeError(f"Installed workflow contract failed: {workflow} {raw}")
        print(f"PASS {workflow} {raw} -> {expected}")
    output = io.StringIO()
    with contextlib.redirect_stderr(output):
        code = cli_main(
            [
                command,
                "--config",
                str(configuration),
                "--workflow",
                "wf-03",
                "--input",
                '{"score":101}',
            ]
        )
    if code != 2 or "Input error" not in output.getvalue():
        raise RuntimeError("Invalid input did not produce exit 2.")
    from unittest.mock import patch

    from agent_playbook.workflows.wf_01_step_sequence import steps

    error_output = io.StringIO()
    with (
        patch.object(steps, "decorate_message", side_effect=ValueError("private step")),
        contextlib.redirect_stderr(error_output),
    ):
        code = cli_main(
            [command, "--config", str(configuration), "--workflow", "wf-01"]
        )
    if (
        code != 1
        or "Workflow failed: wf-01 EXECUTE failed." not in error_output.getvalue()
        or "private step" in error_output.getvalue()
    ):
        raise RuntimeError("Execution failure did not produce safe exit 1.")
    print("PASS execution failure -> exit 1")
    if attempts:
        raise RuntimeError(f"Network attempts were observed: {attempts}")
    print("PASS runtime network probe: zero Python socket/DNS attempts")


if __name__ == "__main__":
    main()
