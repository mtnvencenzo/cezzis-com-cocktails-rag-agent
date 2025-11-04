import json
import logging
from multiprocessing import Process
from multiprocessing.synchronize import Event as EventType

from confluent_kafka import Consumer, KafkaError
from opentelemetry import trace

# Application specific imports
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
        consumer_id (int): The ID of the consumer.
        stop_event (EventType): An event to signal when to stop the consumer.
        bootstrap_servers (str): The Kafka bootstrap servers.
        consumer_group (str): The consumer group ID.
        topic_name (str): The topic name to subscribe to.
    """
    global logger

    consumer = _create_consumer(consumer_id, bootstrap_servers, consumer_group)
    if consumer is None:
        logger.error(
            "Failed to create Kafka consumer. Exiting",
            extra={
                "messaging.kafka.consumer_id": consumer_id,
                "messaging.kafka.bootstrap_servers": bootstrap_servers,
                "messaging.kafka.consumer_group": consumer_group,
                "messaging.kafka.topic_name": topic_name,
            },
        )
        return

    try:
        _subscribe_consumer(consumer_id, consumer, topic_name)
        _start_polling(consumer_id, stop_event, consumer)

    except KeyboardInterrupt as i:
        logger.info(
            "Keyboard interrupt received, shutting down consumer",
            extra={
                "messaging.kafka.consumer_id": consumer_id,
                "process.interrupt": str(i),
            },
        )
    except Exception as e:
        logger.error(
            "Unexpected error in consumer, shutting down consumer",
            exc_info=True,
            extra={"messaging.kafka.consumer_id": consumer_id, "error": str(e)},
        )
    finally:
        _close_consumer(consumer_id, consumer)


def spawn_consumers(
    num_consumers: int,
    stop_event: EventType,
    bootstrap_servers: str,
    consumer_group: str,
    topic_name: str,
) -> None:
    """Spawn multiple Kafka consumers based on settings.

    Args:
        num_consumers (int): The number of consumers to spawn.
        stop_event (EventType): An event to signal when to stop the consumer.
        bootstrap_servers (str): The Kafka bootstrap servers.
        consumer_group (str): The consumer group ID.
        topic_name (str): The topic name to subscribe to.
    """

    logger.info(
        "Spawning Kafka consumers",
        extra={
            "messaging.kafka.num_consumers": num_consumers,
            "messaging.kafka.bootstrap_servers": bootstrap_servers,
            "messaging.kafka.consumer_group": consumer_group,
            "messaging.kafka.topic_name": topic_name,
        },
    )

    processes: list[Process] = []

    for i in range(num_consumers):
        p = Process(
            target=start_consumer,
            args=(
                i,
                stop_event,
                bootstrap_servers,
                consumer_group,
                topic_name,
            ),
        )

        processes.append(p)
        p.start()
        logger.info(
            "Started Kafka consumer process",
            extra={"messaging.kafka.consumer_id": i, "process.pid": p.pid},
        )

    for i, p in enumerate(processes):
        p.join()  # waiting for all to complete
        logger.info(
            "Kafka consumer process completed",
            extra={
                "messaging.kafka.consumer_id": i,
                "process.pid": p.pid,
                "process.exitcode": p.exitcode,
                "process.name": p.name,
            },
        )


def _create_consumer(
    consumer_id: int, bootstrap_servers: str, consumer_group: str
) -> Consumer | None:
    """Create and start a Kafka consumer.

    Args:
        consumer_id (int): The ID of the consumer.
        bootstrap_servers (str): The Kafka bootstrap servers.
        consumer_group (str): The consumer group ID.

    Returns:
        Consumer: The created Kafka consumer or None.
    """
    global logger

    logger.info(
        "Creating Kafka consumer",
        extra={
            "messaging.kafka.consumer_id": consumer_id,
            "messaging.kafka.bootstrap_servers": bootstrap_servers,
            "messaging.kafka.consumer_group": consumer_group,
        },
    )

    try:
        consumer = Consumer(
            {
                "bootstrap.servers": bootstrap_servers,
                "group.id": consumer_group,
                "auto.offset.reset": "earliest",
            }
        )

        logger.info(
            "Consumer created successfully",
            extra={"messaging.kafka.consumer_id": consumer_id},
        )

        return consumer

    except Exception as e:
        logger.error(
            "Error creating Kafka consumer",
            exc_info=True,
            extra={"messaging.kafka.consumer_id": consumer_id, "error": str(e)},
        )
        return None


def _subscribe_consumer(consumer_id: int, consumer: Consumer, topic_name: str) -> None:
    """Subscribe the Kafka consumer to the specified topic.

    Args:
        consumer_id (int): The ID of the consumer.
        consumer (Consumer): The Kafka consumer.
        topic_name (str): The topic name to subscribe to.
    """
    global logger

    logger.info(
        "Subscribing consumer to topic",
        extra={
            "messaging.kafka.consumer_id": consumer_id,
            "messaging.kafka.topic_name": topic_name,
        },
    )

    try:
        consumer.subscribe([topic_name])
        logger.info(
            "Consumer subscribed successfully",
            extra={
                "messaging.kafka.consumer_id": consumer_id,
                "messaging.kafka.topic_name": topic_name,
            },
        )

    except Exception as e:
        logger.error(
            "Error subscribing consumer to Kafka topic",
            exc_info=True,
            extra={
                "messaging.kafka.consumer_id": consumer_id,
                "messaging.kafka.topic_name": topic_name,
                "error": str(e),
            },
        )
        raise


def _start_polling(consumer_id: int, stop_event: EventType, consumer: Consumer) -> None:
    """Start polling for messages from the Kafka consumer.

    Args:
        consumer_id (int): The ID of the consumer.
        stop_event (EventType): An event to signal when to stop the consumer.
        consumer (Consumer): The Kafka consumer.
    """
    global logger
    global tracer

    logger.info(
        "Start consumer polling for messages...",
        extra={"messaging.kafka.consumer_id": consumer_id},
    )

    # Loop until the app is being shutdown
    while stop_event.is_set() is False:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        elif msg.error():
            error = msg.error()
            if error is not None and error.code() == KafkaError._PARTITION_EOF:
                logger.info(
                    "End of partition reached",
                    extra={
                        "messaging.kafka.consumer_id": consumer_id,
                        "messaging.kafka.topic_name": msg.topic(),
                        "messaging.kafka.partition": msg.partition(),
                    },
                )
            else:
                logger.error(
                    "Consumer message error",
                    exc_info=True,
                    extra={
                        "messaging.kafka.consumer_id": consumer_id,
                        "messaging.kafka.error": str(error),
                        "messaging.kafka.topic_name": msg.topic(),
                        "messaging.kafka.partition": msg.partition(),
                    },
                )

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
                            "Received consumer cocktail message",
                            extra={
                                "messaging.kafka.consumer_id": consumer_id,
                                "cocktail_item_count": len(json_array),
                            },
                        )

                        for item in json_array:
                            logger.info(
                                "Processing consumer cocktail message item",
                                extra={
                                    "messaging.kafka.consumer_id": consumer_id,
                                    "cocktail.id": item["Id"],
                                },
                            )
                            # Add your message processing logic here
                    else:
                        logger.warning(
                            "Received consumer cocktail message with no value",
                            extra={"messaging.kafka.consumer_id": consumer_id},
                        )
                except Exception as e:
                    logger.error(
                        "Error processing consumer cocktail message",
                        extra={
                            "messaging.kafka.consumer_id": consumer_id,
                            "error": str(e),
                        },
                    )


def _close_consumer(consumer_id: int, consumer: Consumer) -> None:
    """Cleanup function to close the Kafka consumer.

    Args:
        consumer_id (int): The ID of the consumer.
        consumer (Consumer): The Kafka consumer.
    """
    global logger

    logger.info(
        "Shutting down kafka consumer",
        extra={"messaging.kafka.consumer_id": consumer_id},
    )

    try:
        logger.info(
            "Committing offsets for kafka consumer",
            extra={"messaging.kafka.consumer_id": consumer_id},
        )
        consumer.commit()
    except Exception as e:
        logger.error(
            "Error committing offsets for kafka consumer",
            extra={"messaging.kafka.consumer_id": consumer_id, "error": str(e)},
        )

    logger.info(
        "Closing kafka consumer", extra={"messaging.kafka.consumer_id": consumer_id}
    )

    consumer.close()
