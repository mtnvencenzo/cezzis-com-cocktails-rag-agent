import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class OTelSettings(BaseSettings):
    """Opentelemetry settings loaded from environment variables and .env files.

    Attributes:
        otel_exporter_otlp_endpoint (str): OpenTelemetry OTLP exporter endpoint.
        otel_service_name (str): OpenTelemetry service name.
        otel_service_namespace (str): OpenTelemetry service namespace.
        otel_otlp_exporter_auth_header (str): OpenTelemetry OTLP exporter authorization header
    """

    model_config = SettingsConfigDict(
        extra='allow',
        env_file=(".env", f".env.{os.environ.get('ENV')}"),
        env_file_encoding="utf-8")

    otel_exporter_otlp_endpoint: str = Field(default="", validation_alias="OTEL_EXPORTER_OTLP_ENDPOINT")
    otel_service_name: str = Field(default="", validation_alias="OTEL_SERVICE_NAME")
    otel_service_namespace: str = Field(default="", validation_alias="OTEL_SERVICE_NAMESPACE")
    otel_otlp_exporter_auth_header: str = Field(default="", validation_alias="OTEL_OTLP_AUTH_HEADER")


_otel_settings: OTelSettings | None = None


def get_otel_settings() -> OTelSettings:
    """Get the singleton instance of OTelSettings.

    Returns:
        OTelSettings: The OpenTelemetry settings instance.
    """
    global _otel_settings
    if _otel_settings is None:
        _otel_settings = OTelSettings()

        # Validate required configuration
        if not _otel_settings.otel_exporter_otlp_endpoint:
            raise ValueError("OTEL_EXPORTER_OTLP_ENDPOINT environment variable is required")
        if not _otel_settings.otel_service_name:
            raise ValueError("OTEL_SERVICE_NAME environment variable is required")
        if not _otel_settings.otel_service_namespace:
            raise ValueError("OTEL_SERVICE_NAMESPACE environment variable is required")
        if not _otel_settings.otel_otlp_exporter_auth_header:
            raise ValueError("OTEL_OTLP_AUTH_HEADER environment variable is required")

        print("OpenTelemetry settings loaded successfully.")

    return _otel_settings


def clear_otel_settings_cache() -> None:
    """Clear the cached settings instance. Useful for testing."""
    global _otel_settings
    _otel_settings = None
