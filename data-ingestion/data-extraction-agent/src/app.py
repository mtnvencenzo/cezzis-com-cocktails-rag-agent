import atexit
import logging
import signal
from multiprocessing import Event, Process
from multiprocessing.synchronize import Event as EventType
from types import FrameType
from typing import Optional

# Application specific imports
from app_settings import settings
from kafka_consumer import start_consumer
from otel import close as otel_close
from otel import get_logger, initialize_otel

logger: logging.Logger = logging.getLogger(__name__)


def main() -> None:
    """Main function to run the Kafka consumer."""
    global logger

    initialize_otel()
    logger = get_logger(__name__)
    logger.info("OpenTelemetry initialized successfully.")

    stop_event = Event()
    # Registering the signal handler for SIGINT (Ctrl+C) and SIGTERM
    # so we can gracefully shutdown the kafka consumers
    signal.signal(
        signal.SIGINT, lambda signum, frame: signal_handler(signum, frame, stop_event)
    )
    signal.signal(
        signal.SIGTERM, lambda signum, frame: signal_handler(signum, frame, stop_event)
    )

    num_consumers = 4  # settings.num_kafka_consumers
    processes: list[Process] = []

    for i in range(num_consumers):
        p = Process(
            target=start_consumer,
            args=(
                i,
                stop_event,
                settings.bootstrap_servers,
                settings.consumer_group,
                settings.topic_name,
            ),
        )

        processes.append(p)
        p.start()
        logger.info(f"Started Kafka consumer process {i} with PID {p.pid}")

    for p in processes:
        p.join()  # waiting for all to complete
        logger.info(f"Waiting for Kafka consumer process with PID {p.pid} to complete")


def signal_handler(signum: int, _frame: Optional[FrameType], event: EventType) -> None:
    logger.info(f"Parent process received signal {signum}. Setting stop event.")
    event.set()  # Set the event to signal worker processes to stop


def cleanup() -> None:
    """Cleanup function to close all open resources."""
    otel_close()


if __name__ == "__main__":
    atexit.register(cleanup)
    main()
