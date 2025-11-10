from typing import Dict, Generator

import pytest


@pytest.fixture
def mock_env_vars() -> Dict[str, str]:
    """Fixture to provide mock environment variables.

    Returns:
        Dict[str, str]: A dictionary of mock environment variables.
    """
    return {
        "KAFKA_BOOTSTRAP_SERVERS": "localhost:9092",
        "KAFKA_CONSUMER_GROUP": "test-consumer-group",
        "KAFKA_EXTRACTION_TOPIC_NAME": "test-topic-ext",
        "KAFKA_EMBEDDING_TOPIC_NAME": "test-topic-emb",
        "KAFKA_NUM_CONSUMERS": "1",
        "OTEL_EXPORTER_OTLP_ENDPOINT": "http://localhost:4316",
        "OTEL_SERVICE_NAME": "test-service",
        "OTEL_SERVICE_NAMESPACE": "test-namespace",
        "OTEL_OTLP_AUTH_HEADER": "Bearer test-token",
    }


@pytest.fixture
def clear_settings_cache() -> Generator[None, None, None]:
    """Clear the settings module cache before each test."""
    import sys

    # Remove the module from sys.modules to force a fresh import
    modules_to_remove = [key for key in sys.modules.keys() if key.startswith(("app_settings", "config"))]
    for module in modules_to_remove:
        del sys.modules[module]

    yield

    # Clean up after test
    modules_to_remove = [key for key in sys.modules.keys() if key.startswith(("app_settings", "config"))]
    for module in modules_to_remove:
        del sys.modules[module]
