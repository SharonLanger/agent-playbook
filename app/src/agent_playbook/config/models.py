"""Validated integration settings; workflow policies stay with their workflow."""

from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, SecretStr, field_validator, model_validator


class CrewAISettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    usage_telemetry_enabled: bool
    tracing_enabled: bool
    show_framework_events: bool


class LangfuseSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    enabled: bool = False
    base_url: str = "http://localhost:3000"
    environment: str = "local"
    public_key: SecretStr | None = None
    secret_key: SecretStr | None = None

    @field_validator("base_url")
    @classmethod
    def valid_base_url(cls, value: str) -> str:
        try:
            parts = urlsplit(value)
            valid = (
                parts.scheme in {"http", "https"}
                and parts.hostname is not None
                and parts.port != 0
                and parts.username is None
                and parts.password is None
                and parts.path in {"", "/"}
                and not parts.query
                and not parts.fragment
                and not any(char.isspace() for char in value)
            )
        except ValueError:
            valid = False
        if not valid:
            raise ValueError("base_url must be an HTTP(S) origin without credentials")
        return value.rstrip("/")

    @field_validator("environment")
    @classmethod
    def valid_environment(cls, value: str) -> str:
        if (
            not value
            or len(value) > 64
            or not all(char.isalnum() or char in "_-" for char in value)
        ):
            raise ValueError("environment must be a short label")
        return value

    @model_validator(mode="after")
    def required_keys(self) -> "LangfuseSettings":
        if self.enabled and (self.public_key is None or self.secret_key is None):
            raise ValueError("enabled Langfuse requires project keys")
        return self


class IntegrationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    crewai: CrewAISettings
    langfuse: LangfuseSettings = LangfuseSettings()


class ApplicationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    integrations: IntegrationSettings
