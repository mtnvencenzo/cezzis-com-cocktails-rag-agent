import logging

from confluent_kafka import KafkaError, Message

logger: logging.Logger = logging.getLogger(__name__)


def on_delivered_to_embedding_topic(err: KafkaError | None, msg: Message) -> None:
    """Callback function to handle message delivery reports for the embedding topic.

    Args:
        err (KafkaError | None): The error if the message delivery failed, else None.
        msg (Message): The Kafka message that was delivered.

    Returns:
        None

    """
    if err:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
