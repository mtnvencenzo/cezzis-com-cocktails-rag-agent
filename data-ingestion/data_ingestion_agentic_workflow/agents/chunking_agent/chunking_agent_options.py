import logging
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ChunkingAgentOptions(BaseSettings):
    """Application settings loaded from environment variables and .env files.

    Attributes:
        enabled (bool): Flag to enable or disable the chunking agent.
        consumer_topic_name (str): Kafka chunking topic name.
        results_topic_name (str): Kafka results topic name.
        num_consumers (int): Number of Kafka consumer processes to start.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", f".env.{os.environ.get('ENV')}"), env_file_encoding="utf-8", extra="allow"
    )

    enabled: bool = Field(default=True, validation_alias="CHUNKING_AGENT_ENABLED")
    consumer_topic_name: str = Field(default="", validation_alias="CHUNKING_AGENT_KAFKA_TOPIC_NAME")
    num_consumers: int = Field(default=1, validation_alias="CHUNKING_AGENT_KAFKA_NUM_CONSUMERS")
    results_topic_name: str = Field(default="", validation_alias="CHUNKING_AGENT_KAFKA_RESULTS_TOPIC_NAME")


_logger: logging.Logger = logging.getLogger("chunking_agent_options")

_chunking_agent_options: ChunkingAgentOptions | None = None


def get_chunking_agent_options() -> ChunkingAgentOptions:
    """Get the singleton instance of ChunkingAgentOptions.

    Returns:
        ChunkingAgentOptions: The application options instance.
    """
    global _chunking_agent_options
    if _chunking_agent_options is None:
        _chunking_agent_options = ChunkingAgentOptions()

        # Validate required configuration
        if not _chunking_agent_options.consumer_topic_name:
            raise ValueError("CHUNKING_AGENT_KAFKA_TOPIC_NAME environment variable is required")
        if not _chunking_agent_options.results_topic_name:
            raise ValueError("CHUNKING_AGENT_KAFKA_RESULTS_TOPIC_NAME environment variable is required")
        if not _chunking_agent_options.num_consumers or _chunking_agent_options.num_consumers < 1:
            raise ValueError("CHUNKING_AGENT_KAFKA_NUM_CONSUMERS environment variable must be a positive integer")
        _logger.info("Chunking agent options loaded successfully.")

    return _chunking_agent_options


def clear_chunking_agent_options_cache() -> None:
    """Clear the cached options instance. Useful for testing."""
    global _chunking_agent_options
    _chunking_agent_options = None
