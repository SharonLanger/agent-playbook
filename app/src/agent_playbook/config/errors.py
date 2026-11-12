"""Configuration failures safe to show without printing configuration values."""


class ConfigurationError(ValueError):
    """Invalid configuration or an unsafe attempt to reconfigure initialized code."""
