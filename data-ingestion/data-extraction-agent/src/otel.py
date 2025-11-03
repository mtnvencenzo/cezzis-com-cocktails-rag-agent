# ----------------------------------------------------------------------------------------------
# https://github.com/open-telemetry/opentelemetry-python/blob/main/docs/examples/logs/example.py
# ----------------------------------------------------------------------------------------------
import os
import socket
import logging

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider as TraceProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from version import __version__
from app_settings import settings
from opentelemetry.instrumentation.confluent_kafka import ConfluentKafkaInstrumentor  # type: ignore[import-untyped]

# Define global variables for trace and log providers
trace_provider: TraceProvider
log_provider: LoggerProvider

def initialize_otel() -> None:
    """Initialize OpenTelemetry tracing and logging."""
    global trace_provider
    global log_provider

    resource = Resource(attributes={
        "service.name": settings.otel_service_name,
        "service.namespace": settings.otel_service_namespace,
        "service.instance.id": socket.gethostname(),
        "service.version": __version__,
        "deployment.environment": os.environ.get("ENV", "unknown"),
    })

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

    otlp_exporter = OTLPSpanExporter(
        endpoint=f"{settings.otel_exporter_otlp_endpoint}/v1/traces",
        headers={
            "authorization": settings.otel_otlp_exporter_auth_header
        }
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
    otlp_log_exporter = OTLPLogExporter(
        endpoint=f"{settings.otel_exporter_otlp_endpoint}/v1/logs",
        headers={
            "authorization": settings.otel_otlp_exporter_auth_header
        }
    )
    otlp_log_processor = BatchLogRecordProcessor(otlp_log_exporter)
    log_provider.add_log_record_processor(otlp_log_processor)

    # Add OpenTelemetry handler for OTLP export
    otel_handler = LoggingHandler(level=logging.NOTSET, logger_provider=log_provider)

    # Add simple console handler for readable local output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)

    # Set the root logger level to NOTSET to ensure all messages are captured
    logging.getLogger().setLevel(logging.NOTSET)

    # Attach both handlers to root logger
    logging.getLogger().addHandler(otel_handler)
    logging.getLogger().addHandler(console_handler)


def close() -> None:
    """Shutdown OpenTelemetry providers to flush data."""
    global trace_provider
    global log_provider

    if trace_provider:
        trace_provider.shutdown()

    if log_provider:
        log_provider.shutdown()

def get_logger(name: str) -> logging.Logger:
    """Get an OpenTelemetry-instrumented logger.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The OpenTelemetry-instrumented logger.
    """
    return logging.getLogger(name)