import asyncio
import atexit
import logging
import os
import socket
from multiprocessing.synchronize import Event as EventType
from types import FrameType
from typing import Optional

from cezzis_kafka import shutdown_consumers, spawn_consumers_async
from cezzis_otel import OTelSettings, __version__, initialize_otel, shutdown_otel
from opentelemetry.instrumentation.confluent_kafka import (  # type: ignore
    ConfluentKafkaInstrumentor,
)

# Application specific imports
from app_settings import settings
from cocktails_embedding_processor import CocktailsEmbeddingProcessor
from cocktails_extraction_processor import CocktailsExtractionProcessor

logger: logging.Logger = logging.getLogger(__name__)


async def main() -> None:
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

    try:
        # Start both consumer groups concurrently
        await asyncio.gather(
            spawn_consumers_async(
                factory_type=CocktailsExtractionProcessor,
                num_consumers=settings.num_consumers,
                bootstrap_servers=settings.bootstrap_servers,
                consumer_group=settings.consumer_group,
                topic_name=settings.extraction_topic_name,
            ),
            spawn_consumers_async(
                factory_type=CocktailsEmbeddingProcessor,
                num_consumers=settings.num_consumers,
                bootstrap_servers=settings.bootstrap_servers,
                consumer_group=settings.consumer_group,
                topic_name=settings.embedding_topic_name,
            ),
        )
    except asyncio.CancelledError:
        logger.info("Application cancelled")
    except Exception as e:
        logger.error("Application error", exc_info=True, extra={"error": str(e)})


def signal_handler(signum: int, _frame: Optional[FrameType], event: EventType) -> None:
    logger.info(f"Received signal {signum}. Setting stop event.")
    event.set()  # Set the event to signal consumer threads to stop


if __name__ == "__main__":
    atexit.register(shutdown_otel)

    try:
        print("Starting Cocktail Data Ingestion Agent...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Shutting down...")
    finally:
        shutdown_consumers()
