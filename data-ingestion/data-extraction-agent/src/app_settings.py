import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env', f'.env.{os.environ.get("ENV")}'),
        env_file_encoding="utf-8"
    )

    bootstrap_servers: str = Field(
        default="",
        validation_alias='KAFKA_BOOTSTRAP_SERVERS'
    )
    consumer_group: str = Field(
        default="",
        validation_alias='KAFKA_CONSUMER_GROUP'
    )
    topic_name: str = Field(
        default="",
        validation_alias='KAFKA_TOPIC_NAME'
    )

settings = AppSettings()

# Validate required configuration
if not settings.bootstrap_servers:
    raise ValueError("KAFKA_BOOTSTRAP_SERVERS environment variable is required")
if not settings.consumer_group:
    raise ValueError("KAFKA_CONSUMER_GROUP environment variable is required")
if not settings.topic_name:
    raise ValueError("KAFKA_TOPIC_NAME environment variable is required")

print("App settings loaded successfully.")