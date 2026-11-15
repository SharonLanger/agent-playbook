"""Prepare current integration before any workflow or framework imports."""

from __future__ import annotations

from agent_playbook.config.models import ApplicationSettings


def assemble_runtime(config_path: str | None = None) -> ApplicationSettings:
    from agent_playbook.config.crewai import configure_crewai
    from agent_playbook.config.loader import load_configuration

    application = load_configuration(config_path)
    configure_crewai(application.integrations.crewai)
    from agent_playbook.observability.adapters.langfuse.runtime import (
        initialize_tracing,
    )

    initialize_tracing(application.integrations.langfuse)
    return application
