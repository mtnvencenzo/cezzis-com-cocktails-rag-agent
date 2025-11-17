import json
import logging

from cezzis_kafka import IAsyncKafkaMessageProcessor, KafkaConsumerSettings, KafkaProducer, KafkaProducerSettings
from cezzis_otel import get_propagation_headers
from confluent_kafka import Message
from opentelemetry import trace
from pydantic import ValidationError

from data_ingestion_agentic_workflow.agents.base_agent_evt_receiver import BaseAgentEventReceiver
from data_ingestion_agentic_workflow.agents.extraction_agent.ext_agent_options import get_ext_agent_options
from data_ingestion_agentic_workflow.infra.kafka_options import KafkaOptions, get_kafka_options
from data_ingestion_agentic_workflow.llm.markdown_converter.llm_markdown_converter import LLMMarkdownConverter
from data_ingestion_agentic_workflow.llm.setup.llm_model_options import LLMModelOptions
from data_ingestion_agentic_workflow.llm.setup.llm_options import get_llm_options
from data_ingestion_agentic_workflow.models.cocktail_extraction_model import CocktailExtractionModel
from data_ingestion_agentic_workflow.models.cocktail_models import CocktailModel


class CocktailsExtractionEventReceiver(BaseAgentEventReceiver):
    """Concrete implementation of IAsyncKafkaMessageProcessor for processing cocktail extraction messages from Kafka.

    Attributes:
        _logger (logging.Logger): Logger instance for logging messages.
        _kafka_settings (KafkaConsumerSettings): Kafka consumer settings.
        _tracer (trace.Tracer): OpenTelemetry tracer for creating spans.

    Methods:
        kafka_settings() -> KafkaConsumerSettings:
            Get the Kafka consumer settings.

        message_received(msg: Message) -> None:
            Process a received Kafka message.
    """

    def __init__(self, kafka_consumer_settings: KafkaConsumerSettings) -> None:
        """Initialize the CocktailsExtractionEventReceiver
        Args:
            kafka_consumer_settings (KafkaConsumerSettings): The Kafka consumer settings.
            kafka_producer_settings (KafkaProducerSettings): The Kafka producer settings.

        Returns:
            None
        """
        super().__init__(kafka_consumer_settings=kafka_consumer_settings)

        self._logger: logging.Logger = logging.getLogger("ext_agent_evt_processor")
        self._tracer = trace.get_tracer("ext_agent_evt_processor")
        self._options = get_ext_agent_options()

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

        self._markdown_converter = LLMMarkdownConverter(
            llm_options=get_llm_options(),
            model_options=LLMModelOptions(
                model="llama3.2:3b",
                temperature=0.0,
                num_predict=2024,
                verbose=True,
                timeout_seconds=180,
                reasoning=False,
            ),
        )

    @staticmethod
    def CreateNew(kafka_settings: KafkaConsumerSettings) -> IAsyncKafkaMessageProcessor:
        """Factory method to create a new instance of CocktailsExtractionEventReceiver.

        Args:
            kafka_settings (KafkaConsumerSettings): The Kafka consumer settings.

        Returns:
            IAsyncKafkaMessageProcessor: A new instance of CocktailsExtractionEventReceiver.
        """
        return CocktailsExtractionEventReceiver(kafka_consumer_settings=kafka_settings)

    async def message_received(self, msg: Message) -> None:
        # Create a span for processing this Kafka message, linked to the API trace
        with super().create_kafka_consumer_read_span(self._tracer, "cocktail-extraction-message-processing", msg):
            try:
                value = msg.value()
                if value is not None:
                    decoded_value = value.decode("utf-8")
                    json_array = json.loads(decoded_value)

                    span = trace.get_current_span()
                    span.set_attribute("cocktail_item_count", len(json_array))

                    self._logger.info(
                        "Received cocktail extraction message",
                        extra={
                            "messaging.kafka.consumer_id": self._kafka_consumer_settings.consumer_id,
                            "messaging.kafka.bootstrap_servers": self._kafka_consumer_settings.bootstrap_servers,
                            "messaging.kafka.consumer_group": self._kafka_consumer_settings.consumer_group,
                            "messaging.kafka.topic_name": self._kafka_consumer_settings.topic_name,
                            "messaging.kafka.partition": msg.partition(),
                            "cocktail_item_count": len(json_array),
                        },
                    )

                    for item in json_array:
                        try:
                            cocktail_model = CocktailModel(**item)
                        except ValidationError as ve:
                            self._logger.error(
                                "Failed to parse cocktail extraction message item",
                                exc_info=True,
                                extra={
                                    "messaging.kafka.consumer_id": self._kafka_consumer_settings.consumer_id,
                                    "messaging.kafka.bootstrap_servers": self._kafka_consumer_settings.bootstrap_servers,
                                    "messaging.kafka.consumer_group": self._kafka_consumer_settings.consumer_group,
                                    "messaging.kafka.topic_name": self._kafka_consumer_settings.topic_name,
                                    "messaging.kafka.partition": msg.partition(),
                                    "error": str(ve),
                                },
                            )
                            continue

                        cocktail_id = cocktail_model.id
                        if cocktail_id == "unknown":
                            self._logger.warning(
                                "Cocktail item missing 'Id' field, skipping",
                                extra={
                                    "messaging.kafka.consumer_id": self._kafka_consumer_settings.consumer_id,
                                    "messaging.kafka.bootstrap_servers": self._kafka_consumer_settings.bootstrap_servers,
                                    "messaging.kafka.consumer_group": self._kafka_consumer_settings.consumer_group,
                                    "messaging.kafka.topic_name": self._kafka_consumer_settings.topic_name,
                                    "messaging.kafka.partition": msg.partition(),
                                },
                            )
                            continue

                        # ----------------------------------------
                        # Process the individual cocktail message
                        # ----------------------------------------
                        try:
                            await self._process_message(model=cocktail_model)
                        except Exception as e:
                            self._logger.error(
                                "Error processing cocktail extraction message item",
                                exc_info=True,
                                extra={
                                    "messaging.kafka.consumer_id": self._kafka_consumer_settings.consumer_id,
                                    "messaging.kafka.bootstrap_servers": self._kafka_consumer_settings.bootstrap_servers,
                                    "messaging.kafka.consumer_group": self._kafka_consumer_settings.consumer_group,
                                    "messaging.kafka.topic_name": self._kafka_consumer_settings.topic_name,
                                    "messaging.kafka.partition": msg.partition(),
                                    "cocktail.id": cocktail_id,
                                    "error": str(e),
                                },
                            )
                            continue
                else:
                    self._logger.warning(
                        "Received cocktail extraction message with no value",
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
                    "Error processing cocktail extraction message",
                    extra={
                        "messaging.kafka.consumer_id": self._kafka_consumer_settings.consumer_id,
                        "messaging.kafka.bootstrap_servers": self._kafka_consumer_settings.bootstrap_servers,
                        "messaging.kafka.consumer_group": self._kafka_consumer_settings.consumer_group,
                        "messaging.kafka.topic_name": self._kafka_consumer_settings.topic_name,
                        "messaging.kafka.partition": msg.partition(),
                        "error": str(e),
                    },
                )

    async def _process_message(self, model: CocktailModel) -> None:
        with super().create_processing_read_span(
            self._tracer, "cocktail-extraction-item-processing", span_attributes={"cocktail_id": model.id}
        ):
            self._logger.info(
                "Processing cocktail extraction message item",
                extra={
                    "cocktail.id": model.id,
                },
            )

            extraction_text = await self._markdown_converter.convert_markdown(model.content or "")

            self._logger.info(
                "Sending cocktail extraction model to chunking topic",
                extra={
                    "messaging.kafka.bootstrap_servers": self._kafka_consumer_settings.bootstrap_servers,
                    "messaging.kafka.topic_name": self._options.results_topic_name,
                    "cocktail.id": model.id,
                },
            )

            extraction_model = CocktailExtractionModel(
                cocktail_model=model,
                extraction_text=(extraction_text or ""),
            )

            self.producer.send_and_wait(
                topic=self._options.results_topic_name,
                key=model.id,
                message=extraction_model.as_serializable_json(),
                headers=get_propagation_headers(),
                timeout=30.0,
            )
