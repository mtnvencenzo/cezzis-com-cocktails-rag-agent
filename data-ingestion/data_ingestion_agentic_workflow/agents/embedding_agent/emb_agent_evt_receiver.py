import json
import logging
from typing import ContextManager

from cezzis_kafka import IAsyncKafkaMessageProcessor, KafkaConsumerSettings
from confluent_kafka import Message
from opentelemetry import trace
from opentelemetry.propagate import extract
from opentelemetry.trace import Span

from data_ingestion_agentic_workflow.agents.base_agent_evt_receiver import BaseAgentEventReceiver
from data_ingestion_agentic_workflow.agents.embedding_agent.emb_agent_options import get_emb_agent_options
from data_ingestion_agentic_workflow.models.cocktail_chunking_model import CocktailChunkingModel
from data_ingestion_agentic_workflow.models.cocktail_models import CocktailModel


class EmbeddingAgentEventReceiver(BaseAgentEventReceiver):
    """Concrete implementation of IAsyncKafkaMessageProcessor for processing cocktail embedding messages from Kafka.

    Attributes:
        _logger (logging.Logger): Logger instance for logging messages.
        _kafka_settings (KafkaConsumerSettings): Kafka consumer settings.
        _tracer (trace.Tracer): OpenTelemetry tracer for creating spans.

    Methods:
        message_received(msg: Message) -> None:
            Process a received Kafka message.
    """

    def __init__(self, kafka_consumer_settings: KafkaConsumerSettings) -> None:
        """Initialize the CocktailsEmbeddingProcessor
        Args:
            kafka_consumer_settings (KafkaConsumerSettings): The Kafka consumer settings.

        Returns:
            None
        """
        super().__init__(kafka_consumer_settings=kafka_consumer_settings)

        self._logger: logging.Logger = logging.getLogger("embedding_agent")
        self._tracer = trace.get_tracer("embedding_agent")
        self._options = get_emb_agent_options()

    @staticmethod
    def CreateNew(kafka_settings: KafkaConsumerSettings) -> IAsyncKafkaMessageProcessor:
        """Factory method to create a new instance of EmbeddingAgentEventReceiver.

        Args:
            kafka_settings (KafkaConsumerSettings): The Kafka consumer settings.

        Returns:
            IAsyncKafkaMessageProcessor: A new instance of EmbeddingAgentEventReceiver.
        """
        return EmbeddingAgentEventReceiver(kafka_consumer_settings=kafka_settings)

    async def message_received(self, msg: Message) -> None:
        # Create a span for processing this Kafka message, linked to the API trace
        with super().create_kafka_consumer_read_span(self._tracer, "cocktail-embedding-message-processing", msg):
            try:
                value = msg.value()
                if value is not None:
                    self._logger.info(
                        "Received cocktail embedding message",
                        extra={
                            "messaging.kafka.consumer_id": self._kafka_consumer_settings.consumer_id,
                            "messaging.kafka.bootstrap_servers": self._kafka_consumer_settings.bootstrap_servers,
                            "messaging.kafka.consumer_group": self._kafka_consumer_settings.consumer_group,
                            "messaging.kafka.topic_name": self._kafka_consumer_settings.topic_name,
                            "messaging.kafka.partition": msg.partition(),
                        },
                    )

                    data = json.loads(value.decode("utf-8"))
                    chunking_model = CocktailChunkingModel(
                        cocktail_model=CocktailModel.model_validate(data["cocktail_model"]),
                        chunks=data["chunks"],
                    )

                    if not chunking_model.chunks or not chunking_model.cocktail_model:
                        self._logger.warning(
                            "Received empty cocktail chunking model",
                            extra={
                                "messaging.kafka.consumer_id": self._kafka_consumer_settings.consumer_id,
                                "messaging.kafka.bootstrap_servers": self._kafka_consumer_settings.bootstrap_servers,
                                "messaging.kafka.consumer_group": self._kafka_consumer_settings.consumer_group,
                                "messaging.kafka.topic_name": self._kafka_consumer_settings.topic_name,
                                "messaging.kafka.partition": msg.partition(),
                            },
                        )
                        return

                    # ----------------------------------------
                    # Process the individual cocktail message
                    # ----------------------------------------
                    self._process_message(chunking_model=chunking_model)
                else:
                    self._logger.warning(
                        "Received cocktail embedding message with no value",
                        extra={
                            "messaging.kafka.consumer_id": self._kafka_consumer_settings.consumer_id,
                            "messaging.kafka.bootstrap_servers": self._kafka_consumer_settings.bootstrap_servers,
                            "messaging.kafka.consumer_group": self._kafka_consumer_settings.consumer_group,
                            "messaging.kafka.topic_name": self._kafka_consumer_settings.topic_name,
                            "messaging.kafka.partition": msg.partition(),
                        },
                    )
            except Exception as e:
                self._logger.error(
                    "Error processing cocktail embedding message",
                    extra={
                        "messaging.kafka.consumer_id": self._kafka_consumer_settings.consumer_id,
                        "messaging.kafka.bootstrap_servers": self._kafka_consumer_settings.bootstrap_servers,
                        "messaging.kafka.consumer_group": self._kafka_consumer_settings.consumer_group,
                        "messaging.kafka.topic_name": self._kafka_consumer_settings.topic_name,
                        "messaging.kafka.partition": msg.partition(),
                        "error": str(e),
                    },
                )

    def _process_message(self, chunking_model: CocktailChunkingModel) -> None:
        with super().create_processing_read_span(
            self._tracer,
            "cocktail-embedding-processing",
            span_attributes={"cocktail_id": chunking_model.cocktail_model.id},
        ):
            self._logger.info(
                "Processing cocktail embedding message item",
                extra={
                    "cocktail.id": chunking_model.cocktail_model.id,
                },
            )

            self._logger.info(
                "Sending cocktail embedding result to vector database",
                extra={
                    "messaging.kafka.bootstrap_servers": self._kafka_consumer_settings.bootstrap_servers,
                    "messaging.kafka.topic_name": self._options.consumer_topic_name,
                    "cocktail.id": chunking_model.cocktail_model.id,
                },
            )
