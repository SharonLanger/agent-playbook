"""Configure the test process before pytest imports any workflow modules."""

import os
from pathlib import Path

from agent_playbook.config.crewai import configure_crewai
from agent_playbook.config.loader import load_configuration

# Tests always use a dedicated fixture, independent of user files/preferences.
os.environ["AGENT_PLAYBOOK_CONFIG"] = str(
    Path(__file__).with_name("fixtures") / "offline.yaml"
)
for name in (
    "AGENT_PLAYBOOK_CREWAI_USAGE_TELEMETRY_ENABLED",
    "AGENT_PLAYBOOK_CREWAI_TRACING_ENABLED",
    "AGENT_PLAYBOOK_CREWAI_SHOW_FRAMEWORK_EVENTS",
):
    os.environ.pop(name, None)
configure_crewai(load_configuration().integrations.crewai)
