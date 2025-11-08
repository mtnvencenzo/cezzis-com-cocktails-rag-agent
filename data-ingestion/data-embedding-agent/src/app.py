import atexit
import logging
import os
import signal
import socket
from multiprocessing import Event
from multiprocessing.synchronize import Event as EventType
from types import FrameType
from typing import Optional

from cezzis_kafka import spawn_consumers
from cezzis_otel import OTelSettings, __version__, initialize_otel, shutdown_otel
from opentelemetry.instrumentation.confluent_kafka import (  # type: ignore
    ConfluentKafkaInstrumentor,
)

# Application specific imports
from app_settings import settings
from kafka_cocktail_msg_processor import KafkaCocktailMsgProcessor

logger: logging.Logger = logging.getLogger(__name__)


def main() -> None:
    """Main function to run the Kafka consumer. Sets up OpenTelemetry and starts consumers."""
    global logger

    initialize_otel(
        settings=OTelSettings(
            service_name=settings.otel_service_name,
            service_namespace=settings.otel_service_namespace,
            otlp_exporter_endpoint=settings.otel_exporter_otlp_endpoint,
            otlp_exporter_auth_header=settings.otel_otlp_exporter_auth_header,
            service_version=__version__,
            environment=os.environ.get("ENV", "unknown"),
            instance_id=socket.gethostname(),
            enable_logging=True,
            enable_tracing=True,
        ),
        configure_tracing=lambda _: ConfluentKafkaInstrumentor().instrument(),
    )

    logger = logging.getLogger(__name__)
    logger.info("OpenTelemetry initialized successfully")

    stop_event = Event()
    # Registering the signal handler for SIGINT (Ctrl+C) and SIGTERM
    # so we can gracefully shutdown the kafka consumers
    signal.signal(signal.SIGINT, lambda signum, frame: signal_handler(signum, frame, stop_event))
    signal.signal(signal.SIGTERM, lambda signum, frame: signal_handler(signum, frame, stop_event))

    spawn_consumers(
        KafkaCocktailMsgProcessor,
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
    atexit.register(shutdown_otel)
    main()
