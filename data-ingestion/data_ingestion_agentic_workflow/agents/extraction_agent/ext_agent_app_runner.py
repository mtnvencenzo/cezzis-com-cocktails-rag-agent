import logging
from types import CoroutineType
from typing import Any, Coroutine

from cezzis_kafka import spawn_consumers_async

from .ext_agent_app_settings import get_ext_agent_settings
from .ext_agent_evt_processor import CocktailsExtractionProcessor

logger: logging.Logger = logging.getLogger(__name__)


def run_extraction_agent() -> Coroutine[Any, Any, None]:
    """Main function to run the extraction Kafka agent

    Returns:
        CoroutineType[Any, Any, None]: Coroutine object to run the extraction agent consumers
    """

    settings = get_ext_agent_settings()
    logger = logging.getLogger(__name__)
    logger.info("Starting Cocktail Extraction Agent")

    return spawn_consumers_async(
        factory_type=CocktailsExtractionProcessor,
        num_consumers=settings.num_consumers,
        bootstrap_servers=settings.bootstrap_servers,
        consumer_group=settings.consumer_group,
        topic_name=settings.extraction_topic_name,
    )
