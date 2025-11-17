import json
import logging

from cezzis_kafka import IAsyncKafkaMessageProcessor, KafkaConsumerSettings, KafkaProducer, KafkaProducerSettings
from cezzis_otel import get_propagation_headers
from confluent_kafka import Message
from opentelemetry import trace

from data_ingestion_agentic_workflow.agents.base_agent_evt_receiver import BaseAgentEventReceiver
from data_ingestion_agentic_workflow.agents.chunking_agent.chunking_agent_options import get_chunking_agent_options
from data_ingestion_agentic_workflow.infra.kafka_options import KafkaOptions, get_kafka_options
from data_ingestion_agentic_workflow.llm.content_chunking.llm_content_chunking import LLMContentChunker
from data_ingestion_agentic_workflow.llm.setup.llm_model_options import LLMModelOptions
from data_ingestion_agentic_workflow.llm.setup.llm_options import get_llm_options
from data_ingestion_agentic_workflow.models.cocktail_chunking_model import CocktailChunkingModel
from data_ingestion_agentic_workflow.models.cocktail_extraction_model import CocktailExtractionModel
from data_ingestion_agentic_workflow.models.cocktail_models import CocktailModel


class ChunkingAgentEventReceiver(BaseAgentEventReceiver):
    """Concrete implementation of IAsyncKafkaMessageProcessor for processing cocktail chunking messages from Kafka.

    Attributes:
        _logger (logging.Logger): Logger instance for logging messages.
        _tracer (trace.Tracer): OpenTelemetry tracer for creating spans.

    Methods:
        kafka_settings() -> KafkaConsumerSettings:
            Get the Kafka consumer settings.

        message_received(msg: Message) -> None:
            Process a received Kafka message.
    """

    def __init__(self, kafka_consumer_settings: KafkaConsumerSettings) -> None:
        """Initialize the ChunkingAgentEventReceiver
        Args:
            kafka_consumer_settings (KafkaConsumerSettings): The Kafka consumer settings.
            kafka_producer_settings (KafkaProducerSettings): The Kafka producer settings.

        Returns:
            None
        """
        super().__init__(kafka_consumer_settings=kafka_consumer_settings)

        self._logger: logging.Logger = logging.getLogger("chunking_agent")
        self._tracer = trace.get_tracer("chunking_agent")
        self._options = get_chunking_agent_options()

        kafka_options: KafkaOptions = get_kafka_options()

        self.producer = KafkaProducer(
            settings=KafkaProducerSettings(
                bootstrap_servers=kafka_options.bootstrap_servers,
                on_delivery=lambda err, msg: (
                    self._logger.error(f"Message delivery failed: {err}")
                    if err
                    else self._logger.info(
                        f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
                    )
                ),
            )
        )

        self._content_chunker = LLMContentChunker(
            llm_options=get_llm_options(),
            model_options=LLMModelOptions(
                model="llama3.2:3b",
                temperature=0.5,
                num_predict=2024,
                verbose=True,
                timeout_seconds=180,
                reasoning=False,
            ),
        )

    @staticmethod
    def CreateNew(kafka_settings: KafkaConsumerSettings) -> IAsyncKafkaMessageProcessor:
        """Factory method to create a new instance of ChunkingAgentEventReceiver.

        Args:
            kafka_settings (KafkaConsumerSettings): The Kafka consumer settings.

        Returns:
            IAsyncKafkaMessageProcessor: A new instance of ChunkingAgentEventReceiver.
        """
        return ChunkingAgentEventReceiver(kafka_consumer_settings=kafka_settings)

    async def message_received(self, msg: Message) -> None:
        with super().create_kafka_consumer_read_span(self._tracer, "chunking-agent-message-processing", msg):
            try:
                value = msg.value()
                if value is not None:
                    self._logger.info(
                        "Received cocktail chunking agent message",
                        extra={
                            "messaging.kafka.consumer_id": self._kafka_consumer_settings.consumer_id,
                            "messaging.kafka.bootstrap_servers": self._kafka_consumer_settings.bootstrap_servers,
                            "messaging.kafka.consumer_group": self._kafka_consumer_settings.consumer_group,
                            "messaging.kafka.topic_name": self._kafka_consumer_settings.topic_name,
                            "messaging.kafka.partition": msg.partition(),
                        },
                    )

                    data = json.loads(value.decode("utf-8"))
                    extraction_model = CocktailExtractionModel(
                        cocktail_model=CocktailModel.model_validate(data["cocktail_model"]),
                        extraction_text=data["extraction_text"],
                    )

                    if not extraction_model.extraction_text or not extraction_model.cocktail_model:
                        self._logger.warning(
                            "Received empty cocktail extraction text",
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
                    try:
                        await self._process_message(extraction_model=extraction_model)
                    except Exception as e:
                        self._logger.error(
                            "Error processing cocktail chunking message item",
                            exc_info=True,
                            extra={
                                "messaging.kafka.consumer_id": self._kafka_consumer_settings.consumer_id,
                                "messaging.kafka.bootstrap_servers": self._kafka_consumer_settings.bootstrap_servers,
                                "messaging.kafka.consumer_group": self._kafka_consumer_settings.consumer_group,
                                "messaging.kafka.topic_name": self._kafka_consumer_settings.topic_name,
                                "messaging.kafka.partition": msg.partition(),
                                "cocktail.id": extraction_model.cocktail_model.id,
                                "error": str(e),
                            },
                        )

                else:
                    self._logger.warning(
                        "Received cocktail chunking message with no value",
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
                    "Error processing cocktail chunking message",
                    extra={
                        "messaging.kafka.consumer_id": self._kafka_consumer_settings.consumer_id,
                        "messaging.kafka.bootstrap_servers": self._kafka_consumer_settings.bootstrap_servers,
                        "messaging.kafka.consumer_group": self._kafka_consumer_settings.consumer_group,
                        "messaging.kafka.topic_name": self._kafka_consumer_settings.topic_name,
                        "messaging.kafka.partition": msg.partition(),
                        "error": str(e),
                    },
                )

    async def _process_message(self, extraction_model: CocktailExtractionModel) -> None:
        with super().create_processing_read_span(
            self._tracer,
            "cocktail-chunking-text-processing",
            span_attributes={"cocktail_id": extraction_model.cocktail_model.id},
        ):
            self._logger.info(
                "Processing cocktail chunking message item",
                extra={
                    "cocktail.id": extraction_model.cocktail_model.id,
                },
            )

            chunks = await self._content_chunker.chunk_content(extraction_model.extraction_text)

            if not chunks or len(chunks) == 0:
                self._logger.warning(
                    "No chunks were created from cocktail extraction text, skipping sending to embedding topic",
                    extra={
                        "cocktail.id": extraction_model.cocktail_model.id,
                    },
                )
                return

            self._logger.info(
                "Sending cocktail chunking model to embedding topic",
                extra={
                    "messaging.kafka.bootstrap_servers": self._kafka_consumer_settings.bootstrap_servers,
                    "messaging.kafka.topic_name": self._options.results_topic_name,
                    "cocktail.id": extraction_model.cocktail_model.id,
                },
            )

            chunking_model = CocktailChunkingModel(
                cocktail_model=extraction_model.cocktail_model,
                chunks=chunks,
            )

            self.producer.send_and_wait(
                topic=self._options.results_topic_name,
                key=extraction_model.cocktail_model.id,
                message=chunking_model.as_serializable_json(),
                headers=get_propagation_headers(),
                timeout=30.0,
            )
