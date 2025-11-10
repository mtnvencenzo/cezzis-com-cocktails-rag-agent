import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application settings loaded from environment variables and .env files.

    Attributes:
        bootstrap_servers (str): Kafka bootstrap servers.
        consumer_group (str): Kafka consumer group ID.
        extraction_topic_name (str): Kafka extraction topic name.
        embedding_topic_name (str): Kafka embedding topic name.
        num_consumers (int): Number of Kafka consumer processes to start.
        otel_exporter_otlp_endpoint (str): OpenTelemetry OTLP exporter endpoint.
        otel_service_name (str): OpenTelemetry service name.
        otel_service_namespace (str): OpenTelemetry service namespace.
        otel_otlp_exporter_auth_header (str): OpenTelemetry OTLP exporter authorization header
    """

    model_config = SettingsConfigDict(env_file=(".env", f".env.{os.environ.get('ENV')}"), env_file_encoding="utf-8")

    bootstrap_servers: str = Field(default="", validation_alias="KAFKA_BOOTSTRAP_SERVERS")
    consumer_group: str = Field(default="", validation_alias="KAFKA_CONSUMER_GROUP")
    extraction_topic_name: str = Field(default="", validation_alias="KAFKA_EXTRACTION_TOPIC_NAME")
    embedding_topic_name: str = Field(default="", validation_alias="KAFKA_EMBEDDING_TOPIC_NAME")
    num_consumers: int = Field(default=1, validation_alias="KAFKA_NUM_CONSUMERS")
    otel_exporter_otlp_endpoint: str = Field(default="", validation_alias="OTEL_EXPORTER_OTLP_ENDPOINT")
    otel_service_name: str = Field(default="", validation_alias="OTEL_SERVICE_NAME")
    otel_service_namespace: str = Field(default="", validation_alias="OTEL_SERVICE_NAMESPACE")
    otel_otlp_exporter_auth_header: str = Field(default="", validation_alias="OTEL_OTLP_AUTH_HEADER")


settings = AppSettings()

# Validate required configuration
if not settings.bootstrap_servers:
    raise ValueError("KAFKA_BOOTSTRAP_SERVERS environment variable is required")
if not settings.consumer_group:
    raise ValueError("KAFKA_CONSUMER_GROUP environment variable is required")
if not settings.extraction_topic_name:
    raise ValueError("KAFKA_EXTRACTION_TOPIC_NAME environment variable is required")
if not settings.embedding_topic_name:
    raise ValueError("KAFKA_EMBEDDING_TOPIC_NAME environment variable is required")
if not settings.otel_exporter_otlp_endpoint:
    raise ValueError("OTEL_EXPORTER_OTLP_ENDPOINT environment variable is required")
if not settings.otel_service_name:
    raise ValueError("OTEL_SERVICE_NAME environment variable is required")
if not settings.otel_service_namespace:
    raise ValueError("OTEL_SERVICE_NAMESPACE environment variable is required")
if not settings.otel_otlp_exporter_auth_header:
    raise ValueError("OTEL_OTLP_AUTH_HEADER environment variable is required")
if not settings.num_consumers or settings.num_consumers < 1:
    raise ValueError("KAFKA_NUM_CONSUMERS environment variable must be a positive integer")

print("App settings loaded successfully.")
