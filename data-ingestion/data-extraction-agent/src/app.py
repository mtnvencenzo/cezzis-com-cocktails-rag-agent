import atexit
import logging
import os
import signal
import socket
import threading
from multiprocessing import Event
from multiprocessing.synchronize import Event as EventType
from types import FrameType
from typing import Optional

from cezzis_kafka import start_consumer, KafkaConsumerSettings
from cezzis_otel import OTelSettings, __version__, initialize_otel, shutdown_otel
from opentelemetry.instrumentation.confluent_kafka import (  # type: ignore
    ConfluentKafkaInstrumentor,
)

# Application specific imports
from app_settings import settings
from cocktails_extraction_processor import CocktailsExtractionProcessor
from cocktails_embedding_processor import CocktailsEmbeddingProcessor

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

    # Create and start the extraction consumer thread
    extraction_thread = threading.Thread(
        target=start_consumer,
        args=(
            stop_event,
            CocktailsExtractionProcessor(
                kafka_consumer_settings=KafkaConsumerSettings(
                    consumer_id=1,
                    bootstrap_servers=settings.bootstrap_servers,
                    topic_name=settings.extraction_topic_name,
                    consumer_group=settings.consumer_group,
                )
            ),
        ),
        name="ExtractionConsumer",
        daemon=False,
    )
    extraction_thread.start()
    logger.info("Started extraction consumer thread")

    # Create and start the embedding consumer thread
    embedding_thread = threading.Thread(
        target=start_consumer,
        args=(
            stop_event,
            CocktailsEmbeddingProcessor(
                kafka_consumer_settings=KafkaConsumerSettings(
                    consumer_id=2,  # Different consumer ID
                    bootstrap_servers=settings.bootstrap_servers,
                    topic_name=settings.embedding_topic_name,
                    consumer_group=settings.consumer_group,
                )
            ),
        ),
        name="EmbeddingConsumer",
        daemon=False,
    )
    embedding_thread.start()
    logger.info("Started embedding consumer thread")

    try:
        # Wait for both threads to complete
        while extraction_thread.is_alive() or embedding_thread.is_alive():
            extraction_thread.join(timeout=1)
            embedding_thread.join(timeout=1)
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down consumers")
        stop_event.set()
        
        # Wait for threads to finish gracefully
        extraction_thread.join(timeout=10)
        embedding_thread.join(timeout=10)
        
        if extraction_thread.is_alive():
            logger.warning("Extraction consumer thread did not shut down gracefully")
        if embedding_thread.is_alive():
            logger.warning("Embedding consumer thread did not shut down gracefully")



def signal_handler(signum: int, _frame: Optional[FrameType], event: EventType) -> None:
    logger.info(f"Received signal {signum}. Setting stop event.")
    event.set()  # Set the event to signal consumer threads to stop


if __name__ == "__main__":
    atexit.register(shutdown_otel)
    main()
