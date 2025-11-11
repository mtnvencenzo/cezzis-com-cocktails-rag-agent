import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ExtractionAgentAppSettings(BaseSettings):
    """Application settings loaded from environment variables and .env files.

    Attributes:
        bootstrap_servers (str): Kafka bootstrap servers.
        consumer_group (str): Kafka consumer group ID.
        extraction_topic_name (str): Kafka extraction topic name.
        num_consumers (int): Number of Kafka consumer processes to start.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", f".env.{os.environ.get('ENV')}"), env_file_encoding="utf-8", extra="allow"
    )

    bootstrap_servers: str = Field(default="", validation_alias="KAFKA_BOOTSTRAP_SERVERS")
    consumer_group: str = Field(default="", validation_alias="KAFKA_CONSUMER_GROUP")
    extraction_topic_name: str = Field(default="", validation_alias="KAFKA_EXTRACTION_TOPIC_NAME")
    num_consumers: int = Field(default=1, validation_alias="KAFKA_NUM_CONSUMERS")


_ext_agent_settings: ExtractionAgentAppSettings | None = None


def get_ext_agent_settings() -> ExtractionAgentAppSettings:
    """Get the singleton instance of ExtractionAgentAppSettings.

    Returns:
        ExtractionAgentAppSettings: The application settings instance.
    """
    global _ext_agent_settings
    if _ext_agent_settings is None:
        _ext_agent_settings = ExtractionAgentAppSettings()

        # Validate required configuration
        if not _ext_agent_settings.bootstrap_servers:
            raise ValueError("KAFKA_BOOTSTRAP_SERVERS environment variable is required")
        if not _ext_agent_settings.consumer_group:
            raise ValueError("KAFKA_CONSUMER_GROUP environment variable is required")
        if not _ext_agent_settings.extraction_topic_name:
            raise ValueError("KAFKA_EXTRACTION_TOPIC_NAME environment variable is required")
        if not _ext_agent_settings.num_consumers or _ext_agent_settings.num_consumers < 1:
            raise ValueError("KAFKA_NUM_CONSUMERS environment variable must be a positive integer")

        print("App settings loaded successfully.")

    return _ext_agent_settings


def clear_ext_agent_settings_cache() -> None:
    """Clear the cached settings instance. Useful for testing."""
    global _ext_agent_settings
    _ext_agent_settings = None
