import json
import logging

from confluent_kafka import Consumer, Message
from opentelemetry import trace

from ikafka_message_processor import IKafkaMessageProcessor
from kafka_consumer_settings import KafkaConsumerSettings
from otel import create_kafka_child_span


class KafkaCocktailMsgProcessor(IKafkaMessageProcessor):
    """Concrete implementation of IKafkaMessageProcessor for processing cocktail messages from Kafka.

    Attributes:
        _logger (logging.Logger): Logger instance for logging messages.
        _kafka_settings (KafkaConsumerSettings): Kafka consumer settings.
        _tracer (trace.Tracer): OpenTelemetry tracer for creating spans.

    Methods:
        kafka_settings() -> KafkaConsumerSettings:
            Get the Kafka consumer settings.

        consumer_creating() -> None:
            Hook called when the consumer is being created.

        consumer_created(consumer: Consumer | None) -> None:
            Hook called after the consumer has been created.

        consumer_subscribed() -> None:
            Hook called after the consumer has subscribed to topics.

        consumer_stopping() -> None:
            Hook called when the consumer is stopping.

        message_received(msg: Message) -> None:
            Process a received Kafka message.

        message_error_received(msg: Message) -> None:
            Hook called when an error message is received.

        message_partition_reached(msg: Message) -> None:
            Hook called when a partition end is reached.
    """

    def __init__(self, kafka_settings: KafkaConsumerSettings) -> None:
        """Initialize the KafkaCocktailMsgProcessor
        Args:
            kafka_settings (KafkaConsumerSettings): The Kafka consumer settings.

        Returns:
            None
        """

        self._logger: logging.Logger = logging.getLogger(__name__)
        self._kafka_settings = kafka_settings
        self._tracer = trace.get_tracer(__name__)

    def kafka_settings(self) -> KafkaConsumerSettings:
        """Get the Kafka consumer settings.

        Args:    None

        Returns:
            KafkaConsumerSettings: The Kafka consumer settings.
        """
        return self._kafka_settings

    def consumer_creating(self) -> None:
        pass

    def consumer_created(self, consumer: Consumer | None) -> None:
        pass

    def consumer_subscribed(self) -> None:
        pass

    def consumer_stopping(self) -> None:
        pass

    def message_received(self, msg: Message) -> None:
        # Create a span for processing this Kafka message, linked to the API trace
        with create_kafka_child_span(self._tracer, "cocktails-message-processing", msg):
            try:
                value = msg.value()
                if value is not None:
                    decoded_value = value.decode("utf-8")
                    json_array = json.loads(decoded_value)
                    self._logger.info(
                        "Received consumer cocktail message",
                        extra={
                            "messaging.kafka.consumer_id": self._kafka_settings.consumer_id,
                            "messaging.kafka.bootstrap_servers": self._kafka_settings.bootstrap_servers,
                            "messaging.kafka.consumer_group": self._kafka_settings.consumer_group,
                            "messaging.kafka.topic_name": self._kafka_settings.topic_name,
                            "messaging.kafka.partition": msg.partition(),
                            "cocktail_item_count": len(json_array),
                        },
                    )

                    for item in json_array:
                        item_id = item.get("Id", "unknown")
                        if item_id == "unknown":
                            self._logger.warning(
                                "Cocktail item missing 'Id' field, skipping",
                                extra={
                                    "messaging.kafka.consumer_id": self._kafka_settings.consumer_id,
                                    "messaging.kafka.bootstrap_servers": self._kafka_settings.bootstrap_servers,
                                    "messaging.kafka.consumer_group": self._kafka_settings.consumer_group,
                                    "messaging.kafka.topic_name": self._kafka_settings.topic_name,
                                    "messaging.kafka.partition": msg.partition(),
                                },
                            )
                            continue

                        self._logger.info(
                            "Processing consumer cocktail message item",
                            extra={
                                "messaging.kafka.consumer_id": self._kafka_settings.consumer_id,
                                "messaging.kafka.bootstrap_servers": self._kafka_settings.bootstrap_servers,
                                "messaging.kafka.consumer_group": self._kafka_settings.consumer_group,
                                "messaging.kafka.topic_name": self._kafka_settings.topic_name,
                                "messaging.kafka.partition": msg.partition(),
                                "cocktail.id": item_id,
                            },
                        )
                        # Add your message processing logic here
                else:
                    self._logger.warning(
                        "Received consumer cocktail message with no value",
                        extra={
                            "messaging.kafka.consumer_id": self._kafka_settings.consumer_id,
                            "messaging.kafka.bootstrap_servers": self._kafka_settings.bootstrap_servers,
                            "messaging.kafka.consumer_group": self._kafka_settings.consumer_group,
                            "messaging.kafka.topic_name": self._kafka_settings.topic_name,
                            "messaging.kafka.partition": msg.partition(),
                        },
                    )
            except Exception as e:
                self._logger.error(
                    "Error processing consumer cocktail message",
                    extra={
                        "messaging.kafka.consumer_id": self._kafka_settings.consumer_id,
                        "messaging.kafka.bootstrap_servers": self._kafka_settings.bootstrap_servers,
                        "messaging.kafka.consumer_group": self._kafka_settings.consumer_group,
                        "messaging.kafka.topic_name": self._kafka_settings.topic_name,
                        "messaging.kafka.partition": msg.partition(),
                        "error": str(e),
                    },
                )

    def message_error_received(self, msg: Message) -> None:
        pass

    def message_partition_reached(self, msg: Message) -> None:
        pass
