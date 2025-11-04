# ----------------------------------------------------------------------------------------------
# https://github.com/open-telemetry/opentelemetry-python/blob/main/docs/examples/logs/example.py
# ----------------------------------------------------------------------------------------------
import logging
import os
import socket
from typing import ContextManager

from confluent_kafka import Message
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.confluent_kafka import (  # type: ignore
    ConfluentKafkaInstrumentor,
)
from opentelemetry.propagate import extract
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider as TraceProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Span

from app_settings import settings
from version import __version__

# Define global variables for trace and log providers
trace_provider: TraceProvider | None = None
log_provider: LoggerProvider | None = None


def initialize_otel() -> None:
    """Initialize OpenTelemetry tracing and logging."""

    print("Initializing OpenTelemetry")

    resource = Resource(
        attributes={
            "service.name": settings.otel_service_name,
            "service.namespace": settings.otel_service_namespace,
            "service.instance.id": socket.gethostname(),
            "service.version": __version__,
            "deployment.environment": os.environ.get("ENV", "unknown"),
        }
    )

    initialize_tracing(resource)
    initialize_logging(resource)


def initialize_tracing(resource: Resource) -> None:
    """Initialize only OpenTelemetry tracing.

    ARGS:
        resource (Resource): The OpenTelemetry resource describing the service.
    """
    global trace_provider

    # Setup tracing with the otlp exporter to an otel collector
    trace_provider = TraceProvider(resource=resource)
    trace.set_tracer_provider(trace_provider)

    # Wire up auto instrumentation for Kafka
    ConfluentKafkaInstrumentor().instrument()  # type: ignore[no-untyped-call]

    if settings.otel_exporter_otlp_endpoint:
        otlp_exporter = OTLPSpanExporter(
            endpoint=f"{settings.otel_exporter_otlp_endpoint}/v1/traces",
            headers={"authorization": settings.otel_otlp_exporter_auth_header},
        )
        span_processor = BatchSpanProcessor(otlp_exporter)
        trace_provider.add_span_processor(span_processor)


def initialize_logging(resource: Resource) -> None:
    """Initialize only OpenTelemetry logging.

    ARGS:
        resource (Resource): The OpenTelemetry resource describing the service.
    """
    global log_provider

    log_provider = LoggerProvider(resource=resource)
    set_logger_provider(log_provider)

    # Add OTLP exporter for remote telemetry
    if settings.otel_exporter_otlp_endpoint:
        otlp_log_exporter = OTLPLogExporter(
            endpoint=f"{settings.otel_exporter_otlp_endpoint}/v1/logs",
            headers={"authorization": settings.otel_otlp_exporter_auth_header},
        )
        otlp_log_processor = BatchLogRecordProcessor(otlp_log_exporter)
        log_provider.add_log_record_processor(otlp_log_processor)

    # Add OpenTelemetry handler for OTLP export
    otel_handler = LoggingHandler(level=logging.NOTSET, logger_provider=log_provider)

    # Set the root logger level to NOTSET to ensure all messages are captured
    logging.getLogger().setLevel(logging.NOTSET)

    # Attach both handlers to root logger
    logging.getLogger().addHandler(otel_handler)

    # Add simple console handler for readable local output
    if os.environ.get("ENV") == "local":
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(console_formatter)

        logging.getLogger().addHandler(console_handler)


def close() -> None:
    """Shutdown OpenTelemetry providers to flush data."""
    global trace_provider
    global log_provider

    logger = logging.getLogger(__name__)
    logger.info("Shutting down opentelemetry providers")

    if trace_provider:
        logging.info("Flushing and shutting down trace provider")
        trace_provider.force_flush()
        trace_provider.shutdown()

    if log_provider:
        logging.info("Flushing and shutting down log provider")
        log_provider.force_flush()
        log_provider.shutdown()


def get_logger(name: str) -> logging.Logger:
    """Get an OpenTelemetry-instrumented logger.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The OpenTelemetry-instrumented logger.
    """
    return logging.getLogger(name)


def create_kafka_child_span(
    tracer: trace.Tracer, span_name: str, msg: Message
) -> ContextManager[Span]:
    """Create a child span for Kafka message processing.

    Args:
        tracer (trace.Tracer): The OpenTelemetry tracer.
        span_name (str): The name of the span.
        msg (Message): The Kafka message object.

    Returns:
        ContextManager[Span]: A context manager that yields the created child span.
    """
    # Extract trace context from Kafka message headers for distributed tracing
    carrier: dict[str, str] = {}
    headers = msg.headers()
    if headers is not None:
        for key, value in headers:
            if isinstance(value, bytes):
                try:
                    carrier[key] = value.decode("utf-8")
                except UnicodeDecodeError:
                    logger = logging.getLogger(__name__)
                    logger.warning(
                        f"Failed to decode header '{key}' as UTF-8, skipping"
                    )

    # Extract parent context and create a span as a child of the API trace
    parent_context = extract(carrier)

    # Add Kafka-specific attributes to the span using OpenTelemetry semantic conventions
    span_attributes: dict[str, str | int] = {
        "messaging.system": "kafka",
        "messaging.destination.name": msg.topic()
        or "unknown",  # Updated to semantic convention
        "messaging.operation": "process",
    }

    # Add optional attributes if available
    partition = msg.partition()
    if partition is not None:
        span_attributes["messaging.kafka.partition"] = partition

    offset = msg.offset()
    if offset is not None:
        span_attributes["messaging.kafka.offset"] = offset

    return tracer.start_as_current_span(
        span_name,
        context=parent_context,
        attributes=span_attributes,
    )
