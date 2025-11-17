from typing import Dict, Generator

import pytest


@pytest.fixture
def mock_env_vars() -> Dict[str, str]:
    """Fixture to provide mock environment variables.

    Returns:
        Dict[str, str]: A dictionary of mock environment variables.
    """
    return {
        "EMBEDDING_AGENT_KAFKA_TOPIC_NAME": "test-topic-emb",
        "EMBEDDING_AGENT_KAFKA_NUM_CONSUMERS": "1",
    }


@pytest.fixture
def clear_settings_cache() -> Generator[None, None, None]:
    """Clear the settings module cache before each test."""
    from data_ingestion_agentic_workflow.agents.embedding_agent.emb_agent_options import clear_emb_agent_options_cache

    # Clear the cached settings before test
    clear_emb_agent_options_cache()

    yield

    # Clear the cached settings after test
    clear_emb_agent_options_cache()
