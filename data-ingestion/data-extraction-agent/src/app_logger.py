import logging

from otel import close as otel_close
from otel import initialize_otel

_with_otel = False


def initialize_logger(with_otel: bool = False) -> None:
    """Initialize the application logger with desired settings."""
    global _with_otel
    _with_otel = with_otel

    if with_otel:
        initialize_otel()
    else:
        logging.basicConfig(level=logging.INFO)


def shutdown_logger() -> None:
    """Shutdown the application logger and close OpenTelemetry if initialized."""

    if _with_otel:
        otel_close()
