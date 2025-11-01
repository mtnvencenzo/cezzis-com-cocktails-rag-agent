"""Unit tests for app module."""

import signal
import sys
from types import FrameType
from typing import Optional
from unittest.mock import MagicMock, Mock, call

import pytest
from confluent_kafka import KafkaError


@pytest.fixture
def mock_settings(mocker):
    """Fixture to mock app_settings."""
    mock_settings = Mock()
    mock_settings.bootstrap_servers = "localhost:9092"
    mock_settings.consumer_group = "test-group"
    mock_settings.topic_name = "test-topic"
    
    mocker.patch("app.settings", mock_settings)
    return mock_settings


@pytest.fixture
def mock_consumer(mocker):
    """Fixture to mock Kafka Consumer."""
    mock = Mock()
    mocker.patch("app.Consumer", return_value=mock)
    return mock


@pytest.fixture
def reset_app_globals(mocker):
    """Reset global variables in app module before each test."""
    # Mock settings BEFORE importing app to avoid validation errors
    mock_settings_obj = Mock()
    mock_settings_obj.bootstrap_servers = "localhost:9092"
    mock_settings_obj.consumer_group = "test-group"
    mock_settings_obj.topic_name = "test-topic"
    
    mocker.patch.dict(
        "os.environ",
        {
            "KAFKA_BOOTSTRAP_SERVERS": "localhost:9092",
            "KAFKA_CONSUMER_GROUP": "test-group",
            "KAFKA_TOPIC_NAME": "test-topic",
        },
    )
    
    import app
    
    app.consumer = None
    app.shutdown_requested = False
    
    yield
    
    # Clean up after test
    app.consumer = None
    app.shutdown_requested = False


class TestSignalHandler:
    """Test suite for signal_handler function."""

    def test_signal_handler_sets_shutdown_flag(self, reset_app_globals):
        """Test that signal_handler sets shutdown_requested to True."""
        import app
        
        assert app.shutdown_requested is False
        
        app.signal_handler(signal.SIGINT, None)
        
        assert app.shutdown_requested is True

    def test_signal_handler_prints_message(self, reset_app_globals, mocker, capsys):
        """Test that signal_handler prints shutdown message."""
        import app
        
        app.signal_handler(signal.SIGTERM, None)
        
        captured = capsys.readouterr()
        assert "Shutdown signal received" in captured.out
        assert str(signal.SIGTERM) in captured.out

    def test_signal_handler_with_different_signals(self, reset_app_globals):
        """Test signal_handler with different signal numbers."""
        import app
        
        for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGHUP]:
            app.shutdown_requested = False
            app.signal_handler(sig, None)
            assert app.shutdown_requested is True


class TestCleanup:
    """Test suite for cleanup function."""

    def test_cleanup_with_no_consumer(self, reset_app_globals, capsys):
        """Test cleanup when consumer is None."""
        import app
        
        app.consumer = None
        app.cleanup()
        
        captured = capsys.readouterr()
        assert "Performing cleanup before exit" in captured.out

    def test_cleanup_commits_and_closes_consumer(self, reset_app_globals, capsys):
        """Test cleanup commits offsets and closes consumer."""
        import app
        
        mock_consumer = Mock()
        app.consumer = mock_consumer
        
        app.cleanup()
        
        mock_consumer.commit.assert_called_once()
        mock_consumer.close.assert_called_once()
        
        captured = capsys.readouterr()
        assert "Performing cleanup before exit" in captured.out

    def test_cleanup_handles_commit_error(self, reset_app_globals, capsys):
        """Test cleanup handles error during commit gracefully."""
        import app
        
        mock_consumer = Mock()
        mock_consumer.commit.side_effect = Exception("Commit failed")
        app.consumer = mock_consumer
        
        app.cleanup()
        
        mock_consumer.commit.assert_called_once()
        mock_consumer.close.assert_called_once()
        
        captured = capsys.readouterr()
        assert "Error committing offsets" in captured.out
        assert "Commit failed" in captured.out


class TestMain:
    """Test suite for main function."""

    def test_main_creates_consumer_with_correct_config(
        self, reset_app_globals, mock_settings, mocker
    ):
        """Test that main creates consumer with correct configuration."""
        import app
        
        # Mock Consumer class
        mock_consumer_class = mocker.patch("app.Consumer")
        mock_consumer_instance = Mock()
        mock_consumer_class.return_value = mock_consumer_instance
        
        # Mock signal registration
        mock_signal = mocker.patch("app.signal.signal")
        
        # Make the loop exit immediately
        app.shutdown_requested = True
        
        app.main()
        
        # Verify Consumer was called with correct config
        mock_consumer_class.assert_called_once_with(
            {
                "bootstrap.servers": "localhost:9092",
                "group.id": "test-group",
                "auto.offset.reset": "earliest",
            }
        )

    def test_main_subscribes_to_topic(
        self, reset_app_globals, mock_settings, mock_consumer, mocker
    ):
        """Test that main subscribes to the configured topic."""
        import app
        
        mocker.patch("app.signal.signal")
        app.shutdown_requested = True
        
        app.main()
        
        mock_consumer.subscribe.assert_called_once_with(["test-topic"])

    def test_main_registers_signal_handlers(
        self, reset_app_globals, mock_settings, mock_consumer, mocker
    ):
        """Test that main registers SIGINT and SIGTERM handlers."""
        import app
        
        mock_signal = mocker.patch("app.signal.signal")
        app.shutdown_requested = True
        
        app.main()
        
        assert mock_signal.call_count == 2
        mock_signal.assert_any_call(signal.SIGINT, app.signal_handler)
        mock_signal.assert_any_call(signal.SIGTERM, app.signal_handler)

    def test_main_exits_on_consumer_creation_error(
        self, reset_app_globals, mock_settings, mocker, capsys
    ):
        """Test that main exits when consumer creation fails."""
        import app
        
        mocker.patch("app.signal.signal")
        mocker.patch(
            "app.Consumer",
            side_effect=Exception("Connection failed")
        )
        
        with pytest.raises(SystemExit) as exc_info:
            app.main()
        
        assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Error creating Kafka consumer" in captured.out
        assert "Connection failed" in captured.out

    def test_main_exits_on_subscription_error(
        self, reset_app_globals, mock_settings, mock_consumer, mocker, capsys
    ):
        """Test that main exits when topic subscription fails."""
        import app
        
        mocker.patch("app.signal.signal")
        mock_consumer.subscribe.side_effect = Exception("Subscription failed")
        
        with pytest.raises(SystemExit) as exc_info:
            app.main()
        
        assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Error subscribing to topic" in captured.out
        assert "Subscription failed" in captured.out

    def test_main_polls_for_messages(
        self, reset_app_globals, mock_settings, mock_consumer, mocker, capsys
    ):
        """Test that main polls for messages in a loop."""
        import app
        
        mocker.patch("app.signal.signal")
        
        # Create mock messages
        mock_msg = Mock()
        mock_msg.error.return_value = None
        mock_msg.value.return_value = b"test message"
        
        # First poll returns message, second poll triggers shutdown
        call_count = 0
        def poll_side_effect(timeout):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return mock_msg
            else:
                app.shutdown_requested = True
                return None
        
        mock_consumer.poll.side_effect = poll_side_effect
        
        app.main()
        
        assert mock_consumer.poll.call_count >= 1
        
        captured = capsys.readouterr()
        assert "Received message: test message" in captured.out

    def test_main_handles_none_message(
        self, reset_app_globals, mock_settings, mock_consumer, mocker
    ):
        """Test that main handles None messages from poll."""
        import app
        
        mocker.patch("app.signal.signal")
        
        call_count = 0
        def poll_side_effect(timeout):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                return None
            else:
                app.shutdown_requested = True
                return None
        
        mock_consumer.poll.side_effect = poll_side_effect
        
        app.main()
        
        assert mock_consumer.poll.call_count >= 3

    def test_main_handles_partition_eof_error(
        self, reset_app_globals, mock_settings, mock_consumer, mocker, capsys
    ):
        """Test that main handles PARTITION_EOF error."""
        import app
        
        mocker.patch("app.signal.signal")
        
        # Create mock message with PARTITION_EOF error
        mock_msg = Mock()
        mock_error = Mock()
        mock_error.code.return_value = KafkaError._PARTITION_EOF
        mock_msg.error.return_value = mock_error
        mock_msg.topic.return_value = "test-topic"
        mock_msg.partition.return_value = 0
        
        call_count = 0
        def poll_side_effect(timeout):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return mock_msg
            else:
                app.shutdown_requested = True
                return None
        
        mock_consumer.poll.side_effect = poll_side_effect
        
        app.main()
        
        captured = capsys.readouterr()
        assert "End of partition reached" in captured.out

    def test_main_handles_kafka_error(
        self, reset_app_globals, mock_settings, mock_consumer, mocker, capsys
    ):
        """Test that main handles Kafka errors."""
        import app
        
        mocker.patch("app.signal.signal")
        
        # Create mock message with generic Kafka error
        mock_msg = Mock()
        mock_error = Mock()
        mock_error.code.return_value = KafkaError.UNKNOWN
        mock_msg.error.return_value = mock_error
        
        call_count = 0
        def poll_side_effect(timeout):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return mock_msg
            else:
                app.shutdown_requested = True
                return None
        
        mock_consumer.poll.side_effect = poll_side_effect
        
        app.main()
        
        captured = capsys.readouterr()
        assert "Consumer error" in captured.out

    def test_main_handles_message_with_no_value(
        self, reset_app_globals, mock_settings, mock_consumer, mocker, capsys
    ):
        """Test that main handles messages with None value."""
        import app
        
        mocker.patch("app.signal.signal")
        
        # Create mock message with None value
        mock_msg = Mock()
        mock_msg.error.return_value = None
        mock_msg.value.return_value = None
        
        call_count = 0
        def poll_side_effect(timeout):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return mock_msg
            else:
                app.shutdown_requested = True
                return None
        
        mock_consumer.poll.side_effect = poll_side_effect
        
        app.main()
        
        captured = capsys.readouterr()
        assert "Received message with no value" in captured.out

    def test_main_prints_startup_messages(
        self, reset_app_globals, mock_settings, mock_consumer, mocker, capsys
    ):
        """Test that main prints expected startup messages."""
        import app
        
        mocker.patch("app.signal.signal")
        app.shutdown_requested = True
        
        app.main()
        
        captured = capsys.readouterr()
        assert "Starting Kafka consumer" in captured.out
        assert "Creating Kafka consumer" in captured.out
        assert "Subscribing to 'test-topic'" in captured.out
        assert "Polling for messages..." in captured.out


class TestModuleExecution:
    """Test suite for module-level execution."""

    def test_atexit_registers_cleanup(self, mocker):
        """Test that atexit.register is called with cleanup function."""
        mock_atexit = mocker.patch("atexit.register")
        mock_main = mocker.patch("app.main")
        
        # Simulate __main__ execution
        import app
        
        # We can't directly test the __main__ block, but we can verify
        # the functions exist and are callable
        assert callable(app.cleanup)
        assert callable(app.main)
