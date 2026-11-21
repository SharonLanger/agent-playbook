"""Run the real checkout CLI and helpers against disposable service fixtures."""

import json
import os
import signal
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import pytest

LOGS = "agent-playbook-logging-smoke"
LANGFUSE = "synthetic-custom-project"
STORES = (
    "postgres_data",
    "clickhouse_data",
    "clickhouse_logs",
    "redis_data",
    "minio_data",
)
DOCKER = r"""
import json
import os
import re
import sys
from pathlib import Path

root = Path(os.environ["SERVICE_FIXTURE_DIRECTORY"])
args = sys.argv[1:]
with (root / "docker.jsonl").open("a") as output:
    output.write(json.dumps(args) + "\n")
data_file = root / "docker-state.json"
state = json.loads(data_file.read_text())
running, volumes = state["running"], state["volumes"]
if args in (["compose", "version"], ["info"]):
    sys.exit(0)
if args[0] == "ps":
    project = args[args.index("--filter") + 1].partition("=")[2].partition("=")[2] if "--filter" in args else None
    for label, names in running.items():
        if not project or label == project:
            for service in names:
                print(f"{label}|{service}")
    sys.exit(0)
if args[:2] == ["volume", "ls"]:
    pattern = args[args.index("--filter") + 1].split("=", 1)[1] if "--filter" in args else ""
    for name, labels in volumes.items():
        if not pattern or re.search(pattern, name):
            print(f'{name}|{labels["project"]}|{labels["target"]}')
    sys.exit(0)
assert args[0] == "compose"
file_position = args.index("-f")
action, *options = args[file_position + 2:]
if "-p" in args:
    project = args[args.index("-p") + 1]
else:
    env_file = Path(args[args.index("--env-file") + 1])
    assert env_file == root / "private settings.env"
    project = next(line.split("=", 1)[1] for line in env_file.read_text().splitlines() if line.startswith("COMPOSE_PROJECT_NAME="))
if action == "config":
    if options == ["--format", "json"]:
        import sys
        sys.stderr.write("synthetic-render-stderr\n")
        print(json.dumps({"name": project, "hidden": "synthetic-render-stdout"}))
    else:
        assert options == ["--quiet"]
elif action == "up":
    assert options == ["-d"]
    if project == "agent-playbook-logging-smoke":
        running[project] = ["victorialogs"]
        targets = ["logs-data"]
    else:
        assert Path(args[args.index("--env-file") + 1]) == root / "private settings.env"
        running[project] = ["langfuse-web","langfuse-worker","postgres","clickhouse","redis","minio"]
        targets = ["postgres_data","clickhouse_data","clickhouse_logs","redis_data","minio_data"]
    for target in targets:
        volumes.setdefault(f"{project}_{target}", {"project":project,"target":target,"id":f"volume-{len(volumes)+1}"})
elif action == "down":
    assert not options
    running.pop(project, None)
elif action == "ps":
    assert options == ["--all", "--format", "json"]
    print(json.dumps([{"Service":name,"State":"running","Health":"healthy"} for name in running.get(project, [])]))
else:
    raise AssertionError(args)
data_file.write_text(json.dumps(state))
"""
HEALTH = """
import sys
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

if Path(sys.argv[0]).name == "manage.py":
    import requests
    import urllib.request

    def requests_get(self, url, **options):
        assert url == "http://127.0.0.1:9428/health"
        return SimpleNamespace(status_code=200)

    def urlopen(url, **options):
        assert url == "http://127.0.0.1:34000/api/public/health"
        return nullcontext(SimpleNamespace(status=200))

    requests.Session.get = requests_get
    urllib.request.urlopen = urlopen
"""


@dataclass
class Checkout:
    directory: Path
    env: dict[str, str]
    config: Path
    local: Path
    secrets: Path
    private: Path

    def run(self, *args: str, **extra_env: str) -> subprocess.CompletedProcess[str]:
        argv = [sys.executable, "-m", "agent_playbook.cli", *args]
        with subprocess.Popen(
            argv,
            cwd=self.directory,
            env=self.env | extra_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as process:
            try:
                out, err = process.communicate(timeout=15)
            except subprocess.TimeoutExpired:
                process.send_signal(signal.SIGINT)
                out, err = process.communicate(timeout=10)
                pytest.fail(f"CLI timed out during {args!r}: {out} {err}")
        for marker in (
            "synthetic-render-stdout",
            "synthetic-render-stderr",
            "synthetic-deploy-secret",
        ):
            assert marker not in out + err
        return subprocess.CompletedProcess(argv, process.returncode, out, err)

    def state(self) -> dict[str, dict[str, object]]:
        return cast(
            dict[str, dict[str, object]],
            json.loads((self.directory / "docker-state.json").read_text()),
        )

    def commands(self) -> list[list[str]]:
        return [
            cast(list[str], json.loads(line))
            for line in (self.directory / "docker.jsonl").read_text().splitlines()
        ]


@pytest.fixture
def checkout(tmp_path: Path) -> Checkout:
    docker = tmp_path / "docker"
    docker.write_text(f"#!{sys.executable}\n" + DOCKER)
    docker.chmod(0o755)
    (tmp_path / "sitecustomize.py").write_text(HEALTH)
    (tmp_path / "docker-state.json").write_text('{"running":{},"volumes":{}}')
    config = tmp_path / "selected.yaml"
    config.write_text(
        "secrets: {file: application.env}\n"
        "integrations:\n"
        "  logging: {enabled: false}\n"
        "  langfuse: {enabled: false}\n"
        "  crewai: {usage_telemetry_enabled: false, tracing_enabled: false, show_framework_events: false}\n"
        "workflows: {}\n"
    )
    local = tmp_path / "selected.local.yaml"
    local.write_text("integrations: {logging: {level: DEBUG}}")
    secrets = tmp_path / "application.env"
    secrets.write_text("")
    private = tmp_path / "private settings.env"
    private.write_text(
        f"COMPOSE_PROJECT_NAME={LANGFUSE}\nLANGFUSE_PORT=34000\n"
        "POSTGRES_PASSWORD=synthetic-deploy-secret\n"
    )
    return Checkout(
        tmp_path,
        {
            "PATH": str(tmp_path) + os.pathsep + os.defpath,
            "PYTHONPATH": str(tmp_path),
            "SERVICE_FIXTURE_DIRECTORY": str(tmp_path),
        },
        config,
        local,
        secrets,
        private,
    )


@pytest.mark.skipif(
    os.name != "posix", reason="Checkout service group supervision requires POSIX"
)
def test_aggregate_keeps_custom_settings_and_volumes_and_stops_logs_after_unsafe_langfuse(
    checkout: Checkout,
) -> None:
    option = ["--env-file", checkout.private.name]
    private_bytes = checkout.private.read_bytes()
    selection = ["--config", checkout.config.name]
    enable = {
        "AGENT_PLAYBOOK_LOGGING_ENABLED": "true",
        "AGENT_PLAYBOOK_LANGFUSE_ENABLED": "true",
    }

    started = checkout.run("services", "--start", *option, *selection, **enable)
    assert started.returncode == 0, started
    assert started.stdout.index(f"VictoriaLogs ({LOGS}) ready") < started.stdout.index(
        f"Langfuse ({LANGFUSE}) ready"
    )
    original = checkout.state()
    assert set(original["volumes"]) == {
        f"{LOGS}_logs-data",
        *(f"{LANGFUSE}_{store}" for store in STORES),
    }
    observed = checkout.run("services", "--status", *option, *selection)
    assert observed.returncode == 0
    for label in (
        "logs selection: disabled",
        "langfuse selection: disabled",
        f"VictoriaLogs ({LOGS}) ready",
        f"Langfuse ({LANGFUSE}) ready",
    ):
        assert label in observed.stdout

    stopped = checkout.run("services", "--stop", *option, "--config", "absent.yaml")
    assert stopped.returncode == 0
    assert stopped.stdout.index(
        f"Langfuse ({LANGFUSE}) stopped"
    ) < stopped.stdout.index(f"VictoriaLogs ({LOGS}) stopped")
    assert checkout.state() == {"running": {}, "volumes": original["volumes"]}
    assert (
        checkout.run("services", "--start", *option, *selection, **enable).returncode
        == 0
    )
    assert original == checkout.state()
    assert checkout.private.read_bytes() == private_bytes

    backup = checkout.private.with_suffix(".bak")
    checkout.private.rename(backup)
    guarded = checkout.run("services", "--stop", *option)
    assert guarded.returncode == 2
    assert "restore the original" in guarded.stderr
    assert f"VictoriaLogs ({LOGS}) stopped" in guarded.stdout
    guarded_state = checkout.state()
    assert set(guarded_state["running"]) == {LANGFUSE}
    assert guarded_state["volumes"] == original["volumes"]
    compose_down = [command for command in checkout.commands() if command[-1] == "down"]
    assert [command[command.index("-p") + 1] for command in compose_down] == [
        LANGFUSE,
        LOGS,
        LOGS,
    ]
    assert backup.read_bytes() == private_bytes


@pytest.mark.skipif(
    os.name != "posix", reason="Checkout service group supervision requires POSIX"
)
def test_supported_logs_cli_is_independent_of_export_and_langfuse_keys(
    checkout: Checkout,
) -> None:
    checkout.private.unlink()
    checkout.secrets.write_text("AGENT_PLAYBOOK_LOGGING_ENABLED=true\n")
    files = (checkout.config, checkout.local, checkout.secrets)
    initial = [file.read_bytes() for file in files]
    disabled = {"AGENT_PLAYBOOK_LOGGING_ENABLED": "false"}
    selection = ["--config", checkout.config.name, "--env-file", checkout.private.name]
    skipped = checkout.run("services", "--start", *selection, **disabled)
    assert skipped.returncode == 0 and skipped.stdout.count("skipped") == 2
    assert not (checkout.directory / "docker.jsonl").exists()
    assert checkout.run("logs", "--start", **disabled).returncode == 0
    assert checkout.run("logs", "--status", **disabled).returncode == 0
    assert checkout.run("logs", "--stop", **disabled).returncode == 0
    assert checkout.run("logs", "--status", **disabled).returncode == 1

    aggregate = checkout.run("services", "--start", *selection)
    assert aggregate.returncode == 0 and "langfuse skipped" in aggregate.stdout
    assert checkout.run("services", "--status", *selection).returncode == 0
    assert checkout.run("services", "--stop", *selection).returncode == 0
    assert not checkout.private.exists()
    assert [file.read_bytes() for file in files] == initial
    operations = [cmd for cmd in checkout.commands() if "-f" in cmd]
    assert all(
        "--env-file" not in cmd and cmd[cmd.index("-p") + 1] == LOGS
        for cmd in operations
    )

    exported = subprocess.run(
        [
            sys.executable,
            "-c",
            "from agent_playbook.config.loader import load_configuration; print(load_configuration().integrations.logging.enabled)",
        ],
        cwd=checkout.directory,
        env=checkout.env | disabled | {"AGENT_PLAYBOOK_CONFIG": str(checkout.config)},
        text=True,
        capture_output=True,
        timeout=5,
    )
    assert exported.returncode == 0 and exported.stdout == "False\n"
