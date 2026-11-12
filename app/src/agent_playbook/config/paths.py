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
        app = Path(__file__).resolve().parents[3]
        legacy_local = app / "configs/application.local.yaml"
        if legacy_local.exists():
            raise ConfigurationError(
                f"Legacy local override found at {legacy_local}. Move or merge it "
                f"into {app / 'application.local.yaml'}, then remove the old file. "
                "No files were changed. An explicit configuration selector still "
                "takes precedence."
            )
        return app / "application.yaml"
    raise ConfigurationError(
        "Select an external configuration with --config PATH or AGENT_PLAYBOOK_CONFIG."
    )
