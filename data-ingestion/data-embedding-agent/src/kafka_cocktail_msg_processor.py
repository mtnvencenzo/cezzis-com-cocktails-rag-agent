import json
import logging
from typing import ContextManager

from cezzis_kafka import IKafkaMessageProcessor, KafkaConsumerSettings
from confluent_kafka import Consumer, Message
from opentelemetry import trace
from opentelemetry.propagate import extract
from opentelemetry.trace import Span


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

    @staticmethod
    def CreateNew(kafka_settings: KafkaConsumerSettings) -> IKafkaMessageProcessor:
        """Factory method to create a new instance of KafkaCocktailMsgProcessor.

        Args:
            kafka_settings (KafkaConsumerSettings): The Kafka consumer settings.

        Returns:
            IKafkaMessageProcessor: A new instance of KafkaCocktailMsgProcessor.
        """
        return KafkaCocktailMsgProcessor(kafka_settings)

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
        with self._create_kafka_child_span(self._tracer, "cocktails-embedding-message-processing", msg):
            try:
                value = msg.value()
                if value is not None:
                    decoded_value = value.decode("utf-8")
                    json_array = json.loads(decoded_value)
                    self._logger.info(
                        "Received consumer cocktail embedding message",
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
                            "Processing consumer cocktail embedding message item",
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
                        "Received consumer cocktail embedding message with no value",
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
                    "Error processing consumer cocktail embedding message",
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

    def _create_kafka_child_span(self, tracer: trace.Tracer, span_name: str, msg: Message) -> ContextManager[Span]:
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
                        logger.warning(f"Failed to decode header '{key}' as UTF-8, skipping")

        # Extract parent context and create a span as a child of the API trace
        parent_context = extract(carrier)

        # Add Kafka-specific attributes to the span using OpenTelemetry semantic conventions
        span_attributes: dict[str, str | int] = {
            "messaging.system": "kafka",
            "messaging.destination.name": msg.topic() or "unknown",  # Updated to semantic convention
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
