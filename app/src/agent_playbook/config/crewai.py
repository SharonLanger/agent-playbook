"""Apply validated CrewAI startup settings before any framework import."""

import os
import sys

from agent_playbook.config.errors import ConfigurationError
from agent_playbook.config.models import CrewAISettings

_initialized: tuple[bool, bool] | None = None


def configure_crewai(settings: CrewAISettings) -> None:
    """Import-time settings cannot safely change after CrewAI initializes."""
    global _initialized
    selected = (settings.usage_telemetry_enabled, settings.tracing_enabled)
    framework_loaded = "crewai" in sys.modules or "crewai_core" in sys.modules
    if framework_loaded and _initialized != selected:
        raise ConfigurationError(
            "CrewAI is already imported with different or unknown startup settings; "
            "start a fresh process to apply this configuration."
        )
    os.environ["CREWAI_DISABLE_TELEMETRY"] = str(not selected[0]).lower()
    os.environ["CREWAI_TRACING_ENABLED"] = str(selected[1]).lower()
    _initialized = selected
