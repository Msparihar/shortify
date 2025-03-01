from redis.asyncio import Redis
import json
from ..core.config import settings
from ..core.logging import setup_logging
from typing import Optional, Any, Dict
from datetime import datetime
from bson import ObjectId

logger = setup_logging("shortify.redis")


def serialize_mongodb_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB document to JSON serializable format"""
    serialized = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
        elif isinstance(value, datetime):
            serialized[key] = value.isoformat()
        else:
            serialized[key] = value
    return serialized


class RedisClient:
    client: Redis = None

    async def connect_to_redis(self):
        """Connect to Redis"""
        try:
            self.client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
            await self.client.ping()
            logger.info("Successfully connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            raise

    async def close_redis_connection(self):
        """Close Redis connection"""
        if self.client:
            try:
                await self.client.close()
                logger.info("Redis connection closed")
            except Exception as e:
                logger.error(f"Error closing Redis connection: {str(e)}")

    async def get_url(self, short_code: str) -> Optional[Dict[str, Any]]:
        """Get URL data from cache"""
        try:
            data = await self.client.get(f"url:{short_code}")
            if data:
                logger.debug(f"Cache hit for URL {short_code}")
                return json.loads(data)
            logger.debug(f"Cache miss for URL {short_code}")
            return None
        except Exception as e:
            logger.error(f"Error getting URL from cache: {str(e)}")
            return None

    async def set_url(self, short_code: str, url_data: Dict[str, Any]):
        """Cache URL data"""
        try:
            serialized_data = serialize_mongodb_doc(url_data)
            await self.client.set(f"url:{short_code}", json.dumps(serialized_data), ex=settings.REDIS_CACHE_TTL)
            logger.debug(f"URL {short_code} cached successfully")
        except Exception as e:
            logger.error(f"Error caching URL {short_code}: {str(e)}")
            raise

    async def increment_clicks(self, short_code: str) -> int:
        """Increment click counter in Redis"""
        try:
            clicks = await self.client.incr(f"clicks:{short_code}")
            logger.debug(f"Incremented clicks for {short_code} to {clicks}")
            return clicks
        except Exception as e:
            logger.error(f"Error incrementing clicks for {short_code}: {str(e)}")
            raise

    async def get_pending_clicks(self, short_code: str) -> int:
        """Get pending click count for a URL"""
        try:
            clicks = await self.client.get(f"clicks:{short_code}")
            count = int(clicks) if clicks else 0
            logger.debug(f"Pending clicks for {short_code}: {count}")
            return count
        except Exception as e:
            logger.error(f"Error getting pending clicks for {short_code}: {str(e)}")
            return 0

    async def reset_clicks(self, short_code: str):
        """Reset click counter after syncing to MongoDB"""
        try:
            await self.client.delete(f"clicks:{short_code}")
            logger.debug(f"Reset click counter for {short_code}")
        except Exception as e:
            logger.error(f"Error resetting clicks for {short_code}: {str(e)}")
            raise

    async def cache_url_list(self, urls: list):
        """Cache list of URLs"""
        try:
            serialized_urls = [serialize_mongodb_doc(url) for url in urls]
            await self.client.set("urls:list", json.dumps(serialized_urls), ex=settings.REDIS_CACHE_TTL)
            logger.debug(f"Cached {len(urls)} URLs in list")
        except Exception as e:
            logger.error(f"Error caching URL list: {str(e)}")
            raise

    async def get_url_list(self) -> Optional[list]:
        """Get cached URL list"""
        try:
            data = await self.client.get("urls:list")
            if data:
                urls = json.loads(data)
                logger.debug(f"Retrieved {len(urls)} URLs from cache")
                return urls
            logger.debug("URL list cache miss")
            return None
        except Exception as e:
            logger.error(f"Error getting URL list from cache: {str(e)}")
            return None


# Create a singleton instance
redis_client = RedisClient()
