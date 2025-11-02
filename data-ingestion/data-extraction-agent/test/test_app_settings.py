"""Unit tests for app_settings module."""

from typing import Any, Dict, Generator

import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def mock_env_vars() -> Dict[str, str]:
    """Fixture to provide mock environment variables."""
    return {
        "KAFKA_BOOTSTRAP_SERVERS": "localhost:9092",
        "KAFKA_CONSUMER_GROUP": "test-consumer-group",
        "KAFKA_TOPIC_NAME": "test-topic",
    }


@pytest.fixture
def clear_settings_cache() -> Generator[None, None, None]:
    """Clear the settings module cache before each test."""
    import sys

    # Remove the module from sys.modules to force a fresh import
    modules_to_remove = [
        key for key in sys.modules.keys() if key.startswith("app_settings")
    ]
    for module in modules_to_remove:
        del sys.modules[module]

    yield

    # Clean up after test
    modules_to_remove = [
        key for key in sys.modules.keys() if key.startswith("app_settings")
    ]
    for module in modules_to_remove:
        del sys.modules[module]


class TestAppSettings:
    """Test suite for AppSettings configuration."""

    def test_settings_loads_from_environment_variables(
        self,
        mock_env_vars: Dict[str, str],
        clear_settings_cache: Any,
        mocker: MockerFixture,
    ) -> None:
        """Test that settings are correctly loaded from environment variables."""
        mocker.patch.dict("os.environ", mock_env_vars)
        mocker.patch("builtins.print")  # Suppress print output

        from app_settings import settings

        assert settings.bootstrap_servers == "localhost:9092"
        assert settings.consumer_group == "test-consumer-group"
        assert settings.topic_name == "test-topic"

    def test_settings_raises_error_when_bootstrap_servers_missing(
        self, clear_settings_cache: Any, mocker: MockerFixture
    ) -> None:
        """Test that missing KAFKA_BOOTSTRAP_SERVERS raises ValueError."""
        mocker.patch.dict(
            "os.environ",
            {
                "KAFKA_CONSUMER_GROUP": "test-group",
                "KAFKA_TOPIC_NAME": "test-topic",
            },
            clear=True,
        )

        with pytest.raises(ValueError, match="KAFKA_BOOTSTRAP_SERVERS.*required"):
            import app_settings  # type: ignore[unused-ignore]

    def test_settings_raises_error_when_consumer_group_missing(
        self, clear_settings_cache: Any, mocker: MockerFixture
    ) -> None:
        """Test that missing KAFKA_CONSUMER_GROUP raises ValueError."""
        mocker.patch.dict(
            "os.environ",
            {
                "KAFKA_BOOTSTRAP_SERVERS": "localhost:9092",
                "KAFKA_TOPIC_NAME": "test-topic",
            },
            clear=True,
        )

        with pytest.raises(ValueError, match="KAFKA_CONSUMER_GROUP.*required"):
            import app_settings  # type: ignore[unused-ignore]

    def test_settings_raises_error_when_topic_name_missing(
        self, clear_settings_cache: Any, mocker: MockerFixture
    ) -> None:
        """Test that missing KAFKA_TOPIC_NAME raises ValueError."""
        mocker.patch.dict(
            "os.environ",
            {
                "KAFKA_BOOTSTRAP_SERVERS": "localhost:9092",
                "KAFKA_CONSUMER_GROUP": "test-group",
            },
            clear=True,
        )

        with pytest.raises(ValueError, match="KAFKA_TOPIC_NAME.*required"):
            import app_settings  # type: ignore[unused-ignore]

    def test_settings_with_env_file(
        self, clear_settings_cache: Any, mocker: MockerFixture, tmp_path: Any
    ) -> None:
        """Test that settings can be loaded from .env file."""
        env_file = tmp_path / ".env"
        env_file.write_text(
            "KAFKA_BOOTSTRAP_SERVERS=localhost:9092\n"
            "KAFKA_CONSUMER_GROUP=file-consumer-group\n"
            "KAFKA_TOPIC_NAME=file-topic\n"
        )

        mocker.patch.dict("os.environ", {"ENV": ""}, clear=True)
        mocker.patch("builtins.print")

        # Change to the temp directory
        import os

        original_dir = os.getcwd()
        os.chdir(tmp_path)

        try:
            from app_settings import AppSettings

            settings = AppSettings()

            assert settings.bootstrap_servers == "localhost:9092"
            assert settings.consumer_group == "file-consumer-group"
            assert settings.topic_name == "file-topic"
        finally:
            os.chdir(original_dir)

    def test_settings_field_aliases(
        self, clear_settings_cache: Any, mocker: MockerFixture
    ) -> None:
        """Test that field aliases work correctly."""
        mocker.patch.dict(
            "os.environ",
            {
                "KAFKA_BOOTSTRAP_SERVERS": "kafka:9092",
                "KAFKA_CONSUMER_GROUP": "alias-test-group",
                "KAFKA_TOPIC_NAME": "alias-test-topic",
            },
            clear=True,
        )
        mocker.patch("builtins.print")

        from app_settings import AppSettings

        settings = AppSettings()

        # Verify the aliases map correctly to the internal field names
        assert hasattr(settings, "bootstrap_servers")
        assert hasattr(settings, "consumer_group")
        assert hasattr(settings, "topic_name")

    def test_settings_prints_success_message(
        self,
        mock_env_vars: Dict[str, str],
        clear_settings_cache: Any,
        mocker: MockerFixture,
    ) -> None:
        """Test that successful loading prints success message."""
        mocker.patch.dict("os.environ", mock_env_vars)
        mock_print = mocker.patch("builtins.print")

        import app_settings  # type: ignore[unused-ignore]

        mock_print.assert_called_with("App settings loaded successfully.")

    def test_settings_model_config(
        self,
        mock_env_vars: Dict[str, str],
        clear_settings_cache: Any,
        mocker: MockerFixture,
    ) -> None:
        """Test that AppSettings has correct model configuration."""
        mocker.patch.dict("os.environ", mock_env_vars)
        mocker.patch("builtins.print")

        from app_settings import AppSettings

        # Verify the model has the expected configuration
        assert AppSettings.model_config is not None
        assert "env_file" in AppSettings.model_config
        assert AppSettings.model_config.get("env_file_encoding") == "utf-8"
