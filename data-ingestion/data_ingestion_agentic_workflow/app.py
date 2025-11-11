import asyncio
import atexit
import logging
import os
import socket
from importlib.metadata import version

# Application specific imports
from agents import run_embedding_agent, run_extraction_agent
from behaviors.otel import get_otel_options
from cezzis_kafka import shutdown_consumers
from cezzis_otel import OTelSettings, initialize_otel, shutdown_otel
from opentelemetry.instrumentation.confluent_kafka import (  # type: ignore
    ConfluentKafkaInstrumentor,
)

logger: logging.Logger = logging.getLogger(__name__)


async def main() -> None:
    """Main function to run the Kafka consumer. Sets up OpenTelemetry and starts consumers."""
    global logger

    otel_options = get_otel_options()

    initialize_otel(
        settings=OTelSettings(
            service_name=otel_options.otel_service_name,
            service_namespace=otel_options.otel_service_namespace,
            otlp_exporter_endpoint=otel_options.otel_exporter_otlp_endpoint,
            otlp_exporter_auth_header=otel_options.otel_otlp_exporter_auth_header,
            service_version=version("data_ingestion_agentic_workflow"),
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
        await asyncio.gather(
            run_extraction_agent(),
            run_embedding_agent(),
        )
    except asyncio.CancelledError:
        logger.info("Application cancelled")
    except Exception as e:
        logger.error("Application error", exc_info=True, extra={"error": str(e)})
        raise


if __name__ == "__main__":
    atexit.register(shutdown_otel)

    try:
        logger.info("Starting Cocktail Ingestion Agentic Workflow...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Shutting down...")
    finally:
        shutdown_consumers()
