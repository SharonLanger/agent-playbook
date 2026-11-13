"""Validated integration settings; workflow policies stay with their workflow."""

from pydantic import BaseModel, ConfigDict, Field


class CrewAISettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    usage_telemetry_enabled: bool
    tracing_enabled: bool
    show_framework_events: bool


class IntegrationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    crewai: CrewAISettings


class ApplicationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    integrations: IntegrationSettings
    workflows: dict[str, object] = Field()
