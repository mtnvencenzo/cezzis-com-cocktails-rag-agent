from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env', '.env.local'),
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