import atexit
import json
import logging
import signal
import sys
from types import FrameType
from typing import Optional

# Application specific imports
from confluent_kafka import Consumer, KafkaError
from opentelemetry import trace
from app_settings import settings
from otel import get_logger, initialize_otel, close as otel_close, create_kafka_child_span

consumer: Consumer | None = None
shutdown_requested = False
logger: logging.Logger = logging.getLogger(__name__)  
tracer = trace.get_tracer(__name__)

def signal_handler(signum: int, _frame: Optional[FrameType]) -> None:
    """Handle shutdown signals gracefully.

    Args:
        signum (int): The signal number.
        _frame (Optional[FrameType]): The current stack frame (unused).
    """
    global logger
    global shutdown_requested

    logger.info(f"\nShutdown signal received ({signum}), exiting gracefully...") 
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
            # Create a span for processing this Kafka message, linked to the API trace
            with create_kafka_child_span(tracer, "cocktails-message-processing", msg):
                try:
                    value = msg.value()
                    if value is not None:
                        decoded_value = value.decode("utf-8")
                        json_array = json.loads(decoded_value)
                        logger.info(f"Received cocktail message with item count: {len(json_array)}")

                        for item in json_array:
                            logger.info(f"Processing cocktail: {item['Id']}")
                            # Add your message processing logic here
                    else:
                        logger.warning("Received message with no value")
                except Exception as e:
                    logger.error(f"Error processing message: {e}", exc_info=True)


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
