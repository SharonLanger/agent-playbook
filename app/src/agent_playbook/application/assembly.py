"""Prepare the current integration before any workflow or framework imports."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agent_playbook.config.models import CrewAISettings


def assemble_runtime(config_path: str | None = None) -> CrewAISettings:
    from agent_playbook.config.crewai import configure_crewai
    from agent_playbook.config.loader import load_configuration

    settings = load_configuration(config_path).integrations.crewai
    configure_crewai(settings)
    return settings
