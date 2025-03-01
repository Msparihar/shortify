from ..db.redis import redis_client
from ..db.mongodb import db
from ..core.config import settings
import asyncio
import logging

logger = logging.getLogger(__name__)


async def sync_click_counts(short_code: str):
    """
    Sync click counts from Redis to MongoDB
    This runs as a background task to not block the main request
    """
    try:
        # Get pending clicks from Redis
        pending_clicks = await redis_client.get_pending_clicks(short_code)

        if pending_clicks > 0:
            # Update MongoDB with the accumulated clicks
            await db.database["urls"].update_one({"short_code": short_code}, {"$inc": {"clicks": pending_clicks}})

            # Reset Redis click counter
            await redis_client.reset_clicks(short_code)

            logger.info(f"Synced {pending_clicks} clicks for {short_code}")
    except Exception as e:
        logger.error(f"Error syncing clicks for {short_code}: {str(e)}")


async def start_click_sync_scheduler():
    """
    Start the background task scheduler for syncing clicks
    This runs continuously in the background
    """
    while True:
        try:
            # Get all URLs from MongoDB
            cursor = db.database["urls"].find({}, {"short_code": 1})
            urls = await cursor.to_list(length=None)

            # Sync clicks for each URL
            for url in urls:
                await sync_click_counts(url["short_code"])

        except Exception as e:
            logger.error(f"Error in click sync scheduler: {str(e)}")

        # Wait for the next sync interval
        await asyncio.sleep(settings.REDIS_CLICK_SYNC_INTERVAL)
