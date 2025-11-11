from collections.abc import Coroutine
import logging
from types import CoroutineType
from typing import Any

from cezzis_kafka import spawn_consumers_async

from .emb_agent_app_settings import get_emb_agent_settings
from .emb_agent_evt_processor import CocktailsEmbeddingProcessor

logger: logging.Logger = logging.getLogger(__name__)


def run_embedding_agent() -> Coroutine[Any, Any, None]:
    """Main function to run the embedding Kafka agent

    Returns:
        CoroutineType[Any, Any, None]: Coroutine object to run the embedding agent consumers
    """

    settings = get_emb_agent_settings()
    logger = logging.getLogger(__name__)
    logger.info("Starting Cocktail Embedding Agent")

    return spawn_consumers_async(
        factory_type=CocktailsEmbeddingProcessor,
        num_consumers=settings.num_consumers,
        bootstrap_servers=settings.bootstrap_servers,
        consumer_group=settings.consumer_group,
        topic_name=settings.embedding_topic_name,
    )

