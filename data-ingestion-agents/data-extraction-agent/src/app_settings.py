import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env', f'.env.{os.environ.get("ENV")}'),
        env_file_encoding="utf-8"
    )

    cosmos_account_endpoint: str = Field(
        default="",
        validation_alias='COSMOS_ACCOUNT_ENDPOINT'
    )
    cosmos_database_name: str = Field(
        default="",
        validation_alias='COSMOS_DATABASE_NAME'
    )
    cosmos_connection_string: str = Field(
        default="",
        validation_alias='COSMOS_CONNECTION_STRING'
    )
    cosmos_container_name: str = Field(
        default="",
        validation_alias='COSMOS_CONTAINER_NAME'
    )

settings = AppSettings()

# Validate required configuration
if not settings.cosmos_account_endpoint and not settings.cosmos_connection_string:
    raise ValueError("COSMOS_ACCOUNT_ENDPOINT or COSMOS_CONNECTION_STRING environment variable is required")
if not settings.cosmos_database_name:
    raise ValueError("COSMOS_DATABASE_NAME environment variable is required")
if not settings.cosmos_container_name:
    raise ValueError("COSMOS_CONTAINER_NAME environment variable is required")

def is_local_environment() -> bool:
    return os.environ.get("ENV") == "local"

print("App settings loaded successfully.")