"""Resolve configuration independently of the caller's working directory."""

import os
from pathlib import Path

from agent_playbook._build_info import SOURCE_COMMIT
from agent_playbook.config.errors import ConfigurationError


def configuration_path(explicit: str | None = None) -> Path:
    selected = (
        explicit if explicit is not None else os.environ.get("AGENT_PLAYBOOK_CONFIG")
    )
    if selected is not None:
        if not selected.strip():
            raise ConfigurationError("Configuration path must not be empty.")
        return Path(selected).expanduser().resolve()
    if SOURCE_COMMIT == "development":
        return Path(__file__).resolve().parents[3] / "configs" / "application.yaml"
    raise ConfigurationError(
        "Select an external configuration with --config PATH or AGENT_PLAYBOOK_CONFIG."
    )
