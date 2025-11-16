from typing import Dict, Generator

import pytest


@pytest.fixture
def mock_env_vars() -> Dict[str, str]:
    """Fixture to provide mock environment variables.

    Returns:
        Dict[str, str]: A dictionary of mock environment variables.
    """
    return {
        "LLM_HOST": "http://localhost:11000",
        "LANGFUSE_SECRET_KEY": "sk-lf-",
        "LANGFUSE_PUBLIC_KEY": "pk-lf-",
        "LANGFUSE_BASE_URL": "https://localhost:8080",
    }


@pytest.fixture
def clear_settings_cache() -> Generator[None, None, None]:
    """Clear the settings module cache before each test."""
    from data_ingestion_agentic_workflow.llm.setup.llm_options import clear_llm_options_cache

    # Clear the cached settings before test
    clear_llm_options_cache()

    yield

    # Clear the cached settings after test
    clear_llm_options_cache()
