import json
import logging
from multiprocessing.synchronize import Event as EventType

from confluent_kafka import Consumer, KafkaError
from opentelemetry import trace

from otel import create_kafka_child_span

tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)


def start_consumer(
    consumer_id: int,
    stop_event: EventType,
    bootstrap_servers: str,
    consumer_group: str,
    topic_name: str,
) -> None:
    """Start the Kafka consumer and begin polling for messages.

    Args:
        bootstrap_servers (str): The Kafka bootstrap servers.
        consumer_group (str): The consumer group ID.
        topic_name (str): The topic name to subscribe to.
    """
    global logger

    consumer = _create_consumer(consumer_id, bootstrap_servers, consumer_group)
    if consumer is None:
        logger.error(f"Failed to create Kafka consumer {consumer_id}. Exiting")
        return

    try:
        _subscribe_consumer(consumer_id, consumer, topic_name)
        _start_polling(consumer_id, stop_event, consumer)

    except KeyboardInterrupt:
        logger.info(
            f"Keyboard interrupt received in consumer {consumer_id}. Shutting down"
        )
    except Exception as e:
        logger.error(
            f"Unexpected error in consumer {consumer_id}: {e}. Shutting down",
            exc_info=True,
        )
    finally:
        _close_consumer(consumer_id, consumer)


def _create_consumer(
    consumer_id: int, bootstrap_servers: str, consumer_group: str
) -> Consumer | None:
    """Create and start a Kafka consumer.

    Args:
        bootstrap_servers (str): The Kafka bootstrap servers.
        consumer_group (str): The consumer group ID.

    Returns:
        Consumer: The created Kafka consumer.
    """
    global logger

    logger.info(
        f"Creating Kafka consumer {consumer_id} for group '{consumer_group}' connecting to '{bootstrap_servers}'"
    )

    try:
        consumer = Consumer(
            {
                "bootstrap.servers": bootstrap_servers,
                "group.id": consumer_group,
                "auto.offset.reset": "earliest",
            }
        )

        logger.info(f"Consumer {consumer_id} created successfully")
        return consumer

    except Exception as e:
        logger.error(f"Error creating Kafka consumer {consumer_id}: {e}", exc_info=True)
        return None


def _subscribe_consumer(consumer_id: int, consumer: Consumer, topic_name: str) -> None:
    """Subscribe the Kafka consumer to the specified topic.

    Args:
        consumer (Consumer): The Kafka consumer.
        topic_name (str): The topic name to subscribe to.
    """
    global logger

    logger.info(f"Subscribing consumer {consumer_id} to topic {topic_name}")

    try:
        consumer.subscribe([topic_name])
        logger.info(f"Consumer {consumer_id} subscribed successfully")

    except Exception as e:
        logger.error(
            f"Error subscribing consumer {consumer_id} to Kafka topic {topic_name}: {e}",
            exc_info=True,
        )
        raise


def _start_polling(consumer_id: int, stop_event: EventType, consumer: Consumer) -> None:
    """Start polling for messages from the Kafka consumer.

    Args:
        consumer (Consumer): The Kafka consumer.
    """
    global logger
    global tracer

    logger.info(f"Start polling for messages for consumer {consumer_id}...")

    # Loop until the app is being shutdown
    while stop_event.is_set() is False:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        elif msg.error():
            error = msg.error()
            if error is not None and error.code() == KafkaError._PARTITION_EOF:
                logger.info(
                    "End of partition reached in consumer {0} {1}/{2}".format(
                        consumer_id, msg.topic(), msg.partition()
                    )
                )
            else:
                logger.error(f"Consumer {consumer_id} error: {error}", exc_info=True)

            continue
        else:
            # Create a span for processing this Kafka message, linked to the API trace
            with create_kafka_child_span(tracer, "cocktails-message-processing", msg):
                try:
                    value = msg.value()
                    if value is not None:
                        decoded_value = value.decode("utf-8")
                        json_array = json.loads(decoded_value)
                        logger.info(
                            f"Received consumer {consumer_id} cocktail message with item count: {len(json_array)}"
                        )

                        for item in json_array:
                            logger.info(
                                f"Processing consumer {consumer_id} cocktail: {item['Id']}"
                            )
                            # Add your message processing logic here
                    else:
                        logger.warning(
                            f"Received consumer {consumer_id} message with no value"
                        )
                except Exception as e:
                    logger.error(
                        f"Error processing consumer {consumer_id} message: {e}",
                        exc_info=True,
                    )


def _close_consumer(consumer_id: int, consumer: Consumer) -> None:
    """Cleanup function to close the Kafka consumer.

    Args:
        consumer (Consumer): The Kafka consumer.
    """
    global logger

    logger.info(f"Shutting down kafka consumer {consumer_id}")

    try:
        logger.info(f"Committing offsets for kafka consumer {consumer_id}")
        consumer.commit()
    except Exception as e:
        logger.error(
            f"Error committing offsets for kafka consumer {consumer_id}: {e}",
            exc_info=True,
        )

    logger.info(f"Closing kafka consumer {consumer_id}")
    consumer.close()
