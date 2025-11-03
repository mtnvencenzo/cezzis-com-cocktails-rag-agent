import atexit
import logging
import signal
import sys
from types import FrameType
from typing import Optional

# Application specific imports
from confluent_kafka import Consumer, KafkaError
from opentelemetry import trace
from opentelemetry.propagate import extract
from opentelemetry.trace import SpanKind
from app_settings import settings
from otel import get_logger, initialize_otel, close as otel_close

consumer: Consumer | None = None
shutdown_requested = False
logger: logging.Logger
tracer = trace.get_tracer(__name__)

def signal_handler(signum: int, _frame: Optional[FrameType]) -> None:
    """Handle shutdown signals gracefully.

    Args:
        signum (int): The signal number.
        _frame (Optional[FrameType]): The current stack frame (unused).
    """
    global logger
    global shutdown_requested

    logger.info(msg = f"\nShutdown signal received ({signum}), exiting gracefully...")
    shutdown_requested = True

def main() -> None:
    """Main function to run the Kafka consumer."""
    global shutdown_requested
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    global logger
    print("Initializing OpenTelemetry")
    initialize_otel()
    logger = get_logger(__name__)
    logger.info("OpenTelemetry initialized successfully.")

    logger.info("Starting Kafka consumer")

    # Initialize the kafka consumer to read messages from 'cocktails-topic'
    # Registering atexit handler to ensure proper cleanup on exit
    logger.info("Creating Kafka consumer")

    try:
        global consumer

        consumer = Consumer(
            {
                "bootstrap.servers": settings.bootstrap_servers,
                "group.id": settings.consumer_group,
                "auto.offset.reset": "earliest",
            }
        )

    except Exception as e:
        logger.error(f"Error creating Kafka consumer: {e}", exc_info=True)
        sys.exit(1)

    try:
        logger.info(f"Subscribing to '{settings.topic_name}'")

        consumer.subscribe([settings.topic_name])

    except Exception as e:
        logger.error(f"Error subscribing to topic: {e}", exc_info=True)
        sys.exit(1)

    logger.info("Polling for messages...")

    # Loop until the app is being shutdown
    while not shutdown_requested:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        elif msg.error():
            error = msg.error()
            if error is not None and error.code() == KafkaError._PARTITION_EOF:
                logger.info(
                    "End of partition reached {0}/{1}".format(
                        msg.topic(), msg.partition()
                    )
                )
            else:
                logger.error("Consumer error: {}".format(error))
            continue
        else:
            # Extract trace context from Kafka message headers
            carrier: dict[str, str] = {}
            headers = msg.headers()
            if headers is not None:
                for key, value in headers:
                    if isinstance(value, bytes):
                        carrier[key] = value.decode('utf-8')
            
            # Extract the parent context from headers
            parent_context = extract(carrier)
            
            # Process message within a trace span
            span_attributes: dict[str, str | int | bool] = {
                "messaging.system": "kafka",
                "messaging.destination": msg.topic() or "unknown",
                "messaging.operation": "process",
            }
            
            # Add optional attributes if available
            partition = msg.partition()
            if partition is not None:
                span_attributes["messaging.kafka.partition"] = partition
            
            offset = msg.offset()
            if offset is not None:
                span_attributes["messaging.kafka.offset"] = offset
            
            # Start span as a child of the extracted context
            with tracer.start_as_current_span(
                "process_kafka_message",
                context=parent_context,
                kind=SpanKind.CONSUMER,
                attributes=span_attributes,
            ) as span:
                # Log trace ID for debugging
                span_context = span.get_span_context()
                trace_id = format(span_context.trace_id, '032x')
                logger.debug(f"Processing message with trace_id: {trace_id}")
                
                try:
                    value = msg.value()

                    if value is not None:
                        decoded_value = value.decode("utf-8")
                        logger.info(f"Received message: {decoded_value}")
                        span.set_attribute("messaging.message.size", len(value))
                        # Add your message processing logic here
                    else:
                        logger.warning("Received message with no value")
                        span.set_attribute("messaging.message.empty", True)
                    
                    # Mark span as successful
                    span.set_status(trace.Status(trace.StatusCode.OK))
                    
                except Exception as e:
                    logger.error(f"Error processing message: {e}", exc_info=True)
                    span.set_status(
                        trace.Status(trace.StatusCode.ERROR, str(e))
                    )
                    span.record_exception(e)
def cleanup() -> None:
    """Cleanup function to close the Kafka consumer."""
    global consumer
    global logger

    logger.info("Performing cleanup before exit.")

    if consumer is not None:
        try:
            consumer.commit()
        except Exception as e:
            logger.error(f"Error committing offsets: {e}", exc_info=True)

        consumer.close()

    otel_close()


if __name__ == "__main__":
    atexit.register(cleanup)
    main()
