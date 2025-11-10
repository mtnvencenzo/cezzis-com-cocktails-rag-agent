"""Unit tests for app_settings module."""

from typing import Any, Dict, Generator

import pytest
from pytest_mock import MockerFixture
from test_fixtures import clear_settings_cache, mock_env_vars  # type: ignore[import]


class TestAppSettings:
    """Test suite for AppSettings configuration."""

    @pytest.mark.usefixtures("clear_settings_cache")
    def test_settings_loads_from_environment_variables(
        self,
        mock_env_vars: Dict[str, str],
        clear_settings_cache: Generator[None, None, None],
        mocker: MockerFixture,
    ) -> None:
        """Test that settings are correctly loaded from environment variables."""
        mocker.patch.dict("os.environ", mock_env_vars)
        mocker.patch("builtins.print")  # Suppress print output

        from config.app_settings import settings

        assert settings.bootstrap_servers == "localhost:9092"
        assert settings.consumer_group == "test-consumer-group"
        assert settings.extraction_topic_name == "test-topic-ext"
        assert settings.embedding_topic_name == "test-topic-emb"
        assert settings.num_consumers == 1
        assert settings.otel_exporter_otlp_endpoint == "http://localhost:4316"
        assert settings.otel_service_name == "test-service"
        assert settings.otel_service_namespace == "test-namespace"
        assert settings.otel_otlp_exporter_auth_header == "Bearer test-token"

    @pytest.mark.usefixtures("clear_settings_cache")
    def test_settings_raises_error_when_bootstrap_servers_missing(
        self,
        mock_env_vars: Dict[str, str],
        clear_settings_cache: Generator[None, None, None],
        mocker: MockerFixture,
    ) -> None:
        """Test that missing KAFKA_BOOTSTRAP_SERVERS raises ValueError."""
        mocker.patch.dict(
            "os.environ",
            {key: value for key, value in mock_env_vars.items() if key != "KAFKA_BOOTSTRAP_SERVERS"},
            clear=True,
        )

        with pytest.raises(ValueError, match="KAFKA_BOOTSTRAP_SERVERS.*required"):
            import config.app_settings  # type: ignore[unused-ignore]

    @pytest.mark.usefixtures("clear_settings_cache")
    def test_settings_raises_error_when_consumer_group_missing(
        self,
        mock_env_vars: Dict[str, str],
        clear_settings_cache: Generator[None, None, None],
        mocker: MockerFixture,
    ) -> None:
        """Test that missing KAFKA_CONSUMER_GROUP raises ValueError."""
        mocker.patch.dict(
            "os.environ",
            {key: value for key, value in mock_env_vars.items() if key != "KAFKA_CONSUMER_GROUP"},
            clear=True,
        )

        with pytest.raises(ValueError, match="KAFKA_CONSUMER_GROUP.*required"):
            import config.app_settings  # type: ignore[unused-ignore]

    @pytest.mark.usefixtures("clear_settings_cache")
    def test_settings_raises_error_when_extraction_topic_name_missing(
        self,
        mock_env_vars: Dict[str, str],
        clear_settings_cache: Any,
        mocker: MockerFixture,
    ) -> None:
        """Test that missing KAFKA_TOPIC_NAME raises ValueError."""
        mocker.patch.dict(
            "os.environ",
            {key: value for key, value in mock_env_vars.items() if key != "KAFKA_EXTRACTION_TOPIC_NAME"},
            clear=True,
        )

        with pytest.raises(ValueError, match="KAFKA_EXTRACTION_TOPIC_NAME.*required"):
            import config.app_settings  # type: ignore[unused-ignore]

    @pytest.mark.usefixtures("clear_settings_cache")
    def test_settings_with_env_file(
        self, clear_settings_cache: Generator[None, None, None], mocker: MockerFixture, tmp_path: Any
    ) -> None:
        """Test that settings can be loaded from .env file."""
        env_file = tmp_path / ".env"
        env_file.write_text(
            "KAFKA_BOOTSTRAP_SERVERS=localhost:9092\n"
            "KAFKA_CONSUMER_GROUP=file-consumer-group\n"
            "KAFKA_EXTRACTION_TOPIC_NAME=file-topic-ext\n"
            "KAFKA_EMBEDDING_TOPIC_NAME=file-topic-emb\n"
            "KAFKA_NUM_CONSUMERS=2\n"
            "OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4316\n"
            "OTEL_SERVICE_NAME=file-service\n"
            "OTEL_SERVICE_NAMESPACE=file-namespace\n"
            "OTEL_OTLP_AUTH_HEADER=Bearer file-token\n"
        )

        mocker.patch.dict("os.environ", {"ENV": ""}, clear=True)
        mocker.patch("builtins.print")

        # Change to the temp directory
        import os

        original_dir = os.getcwd()
        os.chdir(tmp_path)

        try:
            from config.app_settings import AppSettings

            settings = AppSettings()

            assert settings.bootstrap_servers == "localhost:9092"
            assert settings.consumer_group == "file-consumer-group"
            assert settings.extraction_topic_name == "file-topic-ext"
            assert settings.embedding_topic_name == "file-topic-emb"
            assert settings.num_consumers == 2
            assert settings.otel_exporter_otlp_endpoint == "http://localhost:4316"
            assert settings.otel_service_name == "file-service"
            assert settings.otel_service_namespace == "file-namespace"
            assert settings.otel_otlp_exporter_auth_header == "Bearer file-token"
        finally:
            os.chdir(original_dir)

    @pytest.mark.usefixtures("clear_settings_cache")
    def test_settings_model_config(
        self,
        mock_env_vars: Dict[str, str],
        clear_settings_cache: Generator[None, None, None],
        mocker: MockerFixture,
    ) -> None:
        """Test that AppSettings has correct model configuration."""
        mocker.patch.dict("os.environ", mock_env_vars)
        mocker.patch("builtins.print")

        from config.app_settings import AppSettings

        # Verify the model has the expected configuration
        assert AppSettings.model_config is not None
        assert "env_file" in AppSettings.model_config
        assert AppSettings.model_config.get("env_file_encoding") == "utf-8"
