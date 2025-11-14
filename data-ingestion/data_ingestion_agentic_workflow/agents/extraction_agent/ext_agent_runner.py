import logging
from typing import Any, Coroutine

from cezzis_kafka import spawn_consumers_async

from .ext_agent_evt_receiver import CocktailsExtractionEventReceiver
from .ext_agent_options import get_ext_agent_options

logger: logging.Logger = logging.getLogger("ext_agent_app_runner")


def run_extraction_agent() -> Coroutine[Any, Any, None]:
    """Main function to run the extraction Kafka agent

    Returns:
        CoroutineType[Any, Any, None]: Coroutine object to run the extraction agent consumers
    """

    logger.info("Starting Cocktail Extraction Agent")
    options = get_ext_agent_options()

    return spawn_consumers_async(
        factory_type=CocktailsExtractionEventReceiver,
        num_consumers=options.num_consumers,
        bootstrap_servers=options.bootstrap_servers,
        consumer_group=options.consumer_group,
        topic_name=options.extraction_topic_name,
    )
