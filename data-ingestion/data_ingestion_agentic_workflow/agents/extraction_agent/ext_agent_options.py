import logging
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ExtractionAgentOptions(BaseSettings):
    """Application settings loaded from environment variables and .env files.

    Attributes:
        enabled (bool): Flag to enable or disable the extraction agent.
        consumer_topic_name (str): Kafka extraction topic name.
        results_topic_name (str): Kafka results topic name.
        num_consumers (int): Number of Kafka consumer processes to start.
        model (str): LLM model to use for extraction.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", f".env.{os.environ.get('ENV')}"), env_file_encoding="utf-8", extra="allow"
    )

    enabled: bool = Field(default=True, validation_alias="EXTRACTION_AGENT_ENABLED")
    consumer_topic_name: str = Field(default="", validation_alias="EXTRACTION_AGENT_KAFKA_TOPIC_NAME")
    num_consumers: int = Field(default=1, validation_alias="EXTRACTION_AGENT_KAFKA_NUM_CONSUMERS")
    results_topic_name: str = Field(default="", validation_alias="EXTRACTION_AGENT_KAFKA_RESULTS_TOPIC_NAME")
    model: str = Field(default="", validation_alias="EXTRACTION_AGENT_MODEL")


_logger: logging.Logger = logging.getLogger("ext_agent_options")

_ext_agent_options: ExtractionAgentOptions | None = None


def get_ext_agent_options() -> ExtractionAgentOptions:
    """Get the singleton instance of ExtractionAgentOptions.

    Returns:
        ExtractionAgentOptions: The application options instance.
    """
    global _ext_agent_options
    if _ext_agent_options is None:
        _ext_agent_options = ExtractionAgentOptions()

        # Validate required configuration
        if not _ext_agent_options.consumer_topic_name:
            raise ValueError("EXTRACTION_AGENT_KAFKA_TOPIC_NAME environment variable is required")
        if not _ext_agent_options.results_topic_name:
            raise ValueError("EXTRACTION_AGENT_KAFKA_RESULTS_TOPIC_NAME environment variable is required")
        if not _ext_agent_options.num_consumers or _ext_agent_options.num_consumers < 1:
            raise ValueError("EXTRACTION_AGENT_KAFKA_NUM_CONSUMERS environment variable must be a positive integer")
        if not _ext_agent_options.model:
            raise ValueError("EXTRACTION_AGENT_MODEL environment variable is required")

        _logger.info("Extraction agent options loaded successfully.")

    return _ext_agent_options


def clear_ext_agent_options_cache() -> None:
    """Clear the cached options instance. Useful for testing."""
    global _ext_agent_options
    _ext_agent_options = None
