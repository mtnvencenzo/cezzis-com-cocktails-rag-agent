from collections.abc import Generator
from typing import Dict

import pytest
from pytest_mock import MockerFixture

from data_ingestion_agentic_workflow.llm.setup.test_fixtures import clear_settings_cache, mock_env_vars


class TestLLMOptions:
    @pytest.mark.usefixtures("clear_settings_cache")
    def test_settings_raises_error_when_llm_host_missing(
        self,
        mock_env_vars: Dict[str, str],
        clear_settings_cache: Generator[None, None, None],
        mocker: MockerFixture,
    ) -> None:
        """Test that missing LLM_HOST raises ValueError."""
        mocker.patch.dict(
            "os.environ",
            {key: value for key, value in mock_env_vars.items() if key != "LLM_HOST"},
            clear=True,
        )

        with pytest.raises(ValueError, match="LLM_HOST.*required"):
            from data_ingestion_agentic_workflow.llm.setup.llm_options import get_llm_options

            get_llm_options()  # type: ignore[unused-ignore]
