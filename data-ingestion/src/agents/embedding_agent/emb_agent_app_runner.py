import asyncio
import logging

from cezzis_kafka import spawn_consumers_async

from .emb_agent_app_settings import get_emb_agent_settings
from .emb_agent_evt_processor import CocktailsEmbeddingProcessor

logger: logging.Logger = logging.getLogger(__name__)


async def run_embedding_agent() -> None:
    """Main function to run the Kafka consumer. Sets up OpenTelemetry and starts consumers."""
    global logger

    # Get application settings
    settings = get_emb_agent_settings()

    logger = logging.getLogger(__name__)
    logger.info("Starting Cocktail Embedding Agent")

    try:
        await asyncio.gather(
            spawn_consumers_async(
                factory_type=CocktailsEmbeddingProcessor,
                num_consumers=settings.num_consumers,
                bootstrap_servers=settings.bootstrap_servers,
                consumer_group=settings.consumer_group,
                topic_name=settings.embedding_topic_name,
            ),
        )
    except asyncio.CancelledError:
        logger.info("Application cancelled")
    except Exception as e:
        logger.error("Application error", exc_info=True, extra={"error": str(e)})
        raise
