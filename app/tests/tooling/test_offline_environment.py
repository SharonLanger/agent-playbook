"""Release probes ignore ambient opt-ins while normal configuration honors them."""

import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from agent_playbook.config.loader import load_configuration
from tooling import release
from tooling.verify_runtime import offline_environment

OVERRIDES = {
    "AGENT_PLAYBOOK_LOGGING_ENABLED": "true",
    "AGENT_PLAYBOOK_LOGGING_ENDPOINT": "http://127.0.0.1:19999/insert/opentelemetry/v1/logs",
    "AGENT_PLAYBOOK_LANGFUSE_ENABLED": "true",
    "AGENT_PLAYBOOK_LANGFUSE_BASE_URL": "http://127.0.0.1:19998",
    "LANGFUSE_PUBLIC_KEY": "synthetic-public",
    "LANGFUSE_SECRET_KEY": "synthetic-secret",
    "AGENT_PLAYBOOK_CREWAI_USAGE_TELEMETRY_ENABLED": "true",
    "AGENT_PLAYBOOK_CREWAI_TRACING_ENABLED": "true",
    "AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS": "true",
    "CREWAI_USAGE_TELEMETRY_ENABLED": "true",
    "CREWAI_TRACING_ENABLED": "true",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://127.0.0.1:19997",
    "OPENAI_API_KEY": "synthetic-provider-key",
}
FIXTURE = Path(__file__).resolve().parents[1] / "fixtures/offline.yaml"


def assert_offline(env: dict[str, str]) -> None:
    with patch.dict(os.environ, env, clear=True):
        settings = load_configuration(str(FIXTURE)).integrations
    assert not settings.logging.enabled
    assert not settings.langfuse.enabled
    assert not settings.crewai.usage_telemetry_enabled
    assert not settings.crewai.tracing_enabled
    assert not settings.crewai.show_framework_events
    assert env["CREWAI_USAGE_TELEMETRY_ENABLED"] == "false"
    assert env["CREWAI_DISABLE_TELEMETRY"] == "true"
    assert env["CREWAI_TRACING_ENABLED"] == "false"
    assert env["OTEL_SDK_DISABLED"] == "true"
    assert "OPENAI_API_KEY" not in env
    assert not any(key.startswith("AGENT_PLAYBOOK_") for key in env)


def test_policy_is_verification_only() -> None:
    with patch.dict(
        os.environ, {**OVERRIDES, "AGENT_PLAYBOOK_LANGFUSE_ENABLED": "false"}
    ):
        normal = load_configuration(str(FIXTURE)).integrations
        assert normal.logging.enabled
        assert normal.crewai.usage_telemetry_enabled
        assert_offline(offline_environment(os.environ))
        assert os.environ["AGENT_PLAYBOOK_LOGGING_ENABLED"] == "true"


def test_every_installed_probe_receives_same_offline_policy(tmp_path: Path) -> None:
    python = tmp_path / "venv/bin/python"
    identity = "agent-playbook 0.2.0 (source: abc)"
    with (
        patch.dict(os.environ, OVERRIDES),
        patch.object(release, "run") as run,
        patch.object(
            release,
            "capture",
            side_effect=[
                identity,
                str(python.parent / "agent_playbook/__init__.py"),
                identity,
                "[WF-03] result: pass",
            ],
        ) as capture,
        patch.object(
            release.subprocess,
            "run",
            return_value=subprocess.CompletedProcess(
                [], 2, "", "Development command requires"
            ),
        ) as guard,
    ):
        release.verify_installed_release(tmp_path, python, "0.2.0", "abc")
    environments = [
        call.args[2] for call in [*run.call_args_list, *capture.call_args_list]
    ]
    environments += [call.kwargs["env"] for call in guard.call_args_list]
    assert len(environments) == 12
    for env in environments:
        assert_offline(env)


def test_fresh_runtime_probe_ignores_synthetic_opt_ins() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            str(Path(__file__).resolve().parents[2] / "tooling/verify_runtime.py"),
            "dev-run",
        ],
        env={**os.environ, **OVERRIDES},
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert (
        "PASS runtime network probe: zero Python socket/DNS attempts" in result.stdout
    )
    assert "PASS wf-03" in result.stdout
