import logging
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ExtractionAgentAppOptions(BaseSettings):
    """Application settings loaded from environment variables and .env files.

    Attributes:
        bootstrap_servers (str): Kafka bootstrap servers.
        consumer_group (str): Kafka consumer group ID.
        extraction_topic_name (str): Kafka extraction topic name.
        embedding_topic_name (str): Kafka embedding topic name.
        num_consumers (int): Number of Kafka consumer processes to start.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", f".env.{os.environ.get('ENV')}"), env_file_encoding="utf-8", extra="allow"
    )

    bootstrap_servers: str = Field(default="", validation_alias="KAFKA_BOOTSTRAP_SERVERS")
    consumer_group: str = Field(default="", validation_alias="KAFKA_CONSUMER_GROUP")
    extraction_topic_name: str = Field(default="", validation_alias="KAFKA_EXTRACTION_TOPIC_NAME")
    embedding_topic_name: str = Field(default="", validation_alias="KAFKA_EMBEDDING_TOPIC_NAME")
    num_consumers: int = Field(default=1, validation_alias="KAFKA_NUM_CONSUMERS")


_logger: logging.Logger = logging.getLogger("ext_agent_app_options")

_ext_agent_options: ExtractionAgentAppOptions | None = None


def get_ext_agent_options() -> ExtractionAgentAppOptions:
    """Get the singleton instance of ExtractionAgentAppOptions.

    Returns:
        ExtractionAgentAppOptions: The application options instance.
    """
    global _ext_agent_options
    if _ext_agent_options is None:
        _ext_agent_options = ExtractionAgentAppOptions()

        # Validate required configuration
        if not _ext_agent_options.bootstrap_servers:
            raise ValueError("KAFKA_BOOTSTRAP_SERVERS environment variable is required")
        if not _ext_agent_options.consumer_group:
            raise ValueError("KAFKA_CONSUMER_GROUP environment variable is required")
        if not _ext_agent_options.extraction_topic_name:
            raise ValueError("KAFKA_EXTRACTION_TOPIC_NAME environment variable is required")
        if not _ext_agent_options.embedding_topic_name:
            raise ValueError("KAFKA_EMBEDDING_TOPIC_NAME environment variable is required")
        if not _ext_agent_options.num_consumers or _ext_agent_options.num_consumers < 1:
            raise ValueError("KAFKA_NUM_CONSUMERS environment variable must be a positive integer")

        _logger.info("Extraction agent app settings loaded successfully.")

    return _ext_agent_options


def clear_ext_agent_options_cache() -> None:
    """Clear the cached options instance. Useful for testing."""
    global _ext_agent_options
    _ext_agent_options = None
