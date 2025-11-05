import atexit
import logging
import signal
from multiprocessing import Event
from multiprocessing.synchronize import Event as EventType
from types import FrameType
from typing import Optional

# Application specific imports
from app_logger import initialize_logger, shutdown_logger
from app_settings import settings
from kafka_consumer import spawn_consumers

logger: logging.Logger = logging.getLogger(__name__)


def main() -> None:
    """Main function to run the Kafka consumer. Sets up OpenTelemetry and starts consumers."""
    global logger

    initialize_logger(True)
    logger = logging.getLogger(__name__)
    logger.info("OpenTelemetry initialized successfully")

    stop_event = Event()
    # Registering the signal handler for SIGINT (Ctrl+C) and SIGTERM
    # so we can gracefully shutdown the kafka consumers
    signal.signal(signal.SIGINT, lambda signum, frame: signal_handler(signum, frame, stop_event))
    signal.signal(signal.SIGTERM, lambda signum, frame: signal_handler(signum, frame, stop_event))

    spawn_consumers(
        settings.num_consumers,
        stop_event,
        settings.bootstrap_servers,
        settings.consumer_group,
        settings.topic_name,
    )


def signal_handler(signum: int, _frame: Optional[FrameType], event: EventType) -> None:
    logger.info(f"Parent process received signal {signum}. Setting stop event.")
    event.set()  # Set the event to signal worker processes to stop


if __name__ == "__main__":
    atexit.register(shutdown_logger)
    main()
