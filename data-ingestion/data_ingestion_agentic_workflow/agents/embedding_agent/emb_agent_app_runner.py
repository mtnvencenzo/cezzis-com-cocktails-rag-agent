import logging
from collections.abc import Coroutine
from typing import Any

from cezzis_kafka import spawn_consumers_async

from .emb_agent_app_options import get_emb_agent_options
from .emb_agent_evt_processor import CocktailsEmbeddingProcessor

logger: logging.Logger = logging.getLogger(__name__)


def run_embedding_agent() -> Coroutine[Any, Any, None]:
    """Main function to run the embedding agent

    Returns:
        CoroutineType[Any, Any, None]: Coroutine object to run the embedding agent consumers
    """

    options = get_emb_agent_options()
    logger = logging.getLogger(__name__)
    logger.info("Starting Cocktail Embedding Agent")

    return spawn_consumers_async(
        factory_type=CocktailsEmbeddingProcessor,
        num_consumers=options.num_consumers,
        bootstrap_servers=options.bootstrap_servers,
        consumer_group=options.consumer_group,
        topic_name=options.embedding_topic_name,
    )
