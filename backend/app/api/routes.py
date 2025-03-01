from fastapi import APIRouter, HTTPException, Response, BackgroundTasks
from ..models.url import URLCreate, URL, URLList
from ..core.shortener import create_short_code
from ..db.mongodb import db
from ..db.redis import redis_client
from datetime import datetime
from ..core.config import settings
from ..core.tasks import sync_click_counts
from ..core.logging import setup_logging
from bson import ObjectId
from fastapi.responses import RedirectResponse

router = APIRouter()
logger = setup_logging("shortify.api")


@router.post("/shorten", response_model=URL)
async def create_short_url(url: URLCreate):
    """Create a shortened URL"""
    logger.info(f"Shortening URL: {url.target_url}")

    try:
        # Create short code
        short_code = create_short_code()
        logger.debug(f"Generated short code: {short_code}")

        # Create URL document
        url_doc = {
            "target_url": str(url.target_url),
            "short_code": short_code,
            "clicks": 0,
            "created_at": datetime.utcnow(),
        }

        # Insert into database
        result = await db.database["urls"].insert_one(url_doc)
        logger.debug(f"Inserted URL into MongoDB with ID: {result.inserted_id}")

        # Get the created document
        created_url = await db.database["urls"].find_one({"_id": result.inserted_id})

        # Cache the URL data in Redis
        await redis_client.set_url(short_code, created_url)
        logger.debug(f"Cached URL data in Redis for {short_code}")

        # Invalidate the cached URL list
        await redis_client.client.delete("urls:list")
        logger.debug("Invalidated URL list cache")

        response = format_url_response(created_url)
        logger.info(f"Successfully created shortened URL: {response.short_code}")
        return response

    except Exception as e:
        logger.error(f"Error creating shortened URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating shortened URL")


@router.get("/urls", response_model=URLList)
async def get_urls():
    """Get all shortened URLs"""
    logger.info("Fetching all URLs")

    try:
        # Try to get from cache first
        cached_urls = await redis_client.get_url_list()

        if cached_urls:
            logger.debug("Returning URLs from cache")
            return URLList(urls=[format_url_response(url) for url in cached_urls])

        # If not in cache, get from MongoDB
        logger.debug("Cache miss, fetching from MongoDB")
        cursor = db.database["urls"].find().sort("created_at", -1)
        urls = await cursor.to_list(length=50)

        # Cache the results
        await redis_client.cache_url_list(urls)
        logger.debug(f"Cached {len(urls)} URLs")

        return URLList(urls=[format_url_response(url) for url in urls])

    except Exception as e:
        logger.error(f"Error fetching URLs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching URLs")


@router.get("/urls/{url_id}", response_model=URL)
async def get_url(url_id: str):
    """Get details of a specific shortened URL"""
    logger.info(f"Fetching URL details for ID: {url_id}")

    try:
        url = await db.database["urls"].find_one({"_id": ObjectId(url_id)})
        if url is None:
            logger.warning(f"URL not found with ID: {url_id}")
            raise HTTPException(status_code=404, detail="URL not found")

        logger.debug(f"Found URL: {url['short_code']}")
        return format_url_response(url)

    except Exception as e:
        logger.error(f"Error fetching URL {url_id}: {str(e)}")
        raise HTTPException(status_code=404, detail="URL not found")


@router.get("/{short_code}")
async def redirect_to_url(short_code: str, background_tasks: BackgroundTasks):
    """Redirect to the original URL and increment click count"""
    logger.info(f"Processing redirect for short code: {short_code}")

    try:
        # Try to get URL from cache
        url_data = await redis_client.get_url(short_code)

        if not url_data:
            logger.debug(f"Cache miss for {short_code}, fetching from MongoDB")
            # If not in cache, get from MongoDB
            url_data = await db.database["urls"].find_one({"short_code": short_code})
            if not url_data:
                logger.warning(f"URL not found for short code: {short_code}")
                raise HTTPException(status_code=404, detail="URL not found")
            # Cache the URL data
            await redis_client.set_url(short_code, url_data)
            logger.debug(f"Cached URL data for {short_code}")

        # Increment click count in Redis (non-blocking)
        await redis_client.increment_clicks(short_code)
        logger.debug(f"Incremented click count for {short_code}")

        # Schedule background task to sync clicks to MongoDB
        background_tasks.add_task(sync_click_counts, short_code)
        logger.debug(f"Scheduled click sync for {short_code}")

        target_url = str(url_data["target_url"])
        logger.info(f"Redirecting {short_code} to {target_url}")
        return RedirectResponse(url=target_url)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing redirect for {short_code}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing redirect")


def format_url_response(url_doc: dict) -> URL:
    """Helper function to format URL response"""
    return URL(
        id=str(url_doc["_id"]),
        short_code=f"{settings.BASE_URL}/{url_doc['short_code']}",
        target_url=url_doc["target_url"],
        clicks=url_doc["clicks"],
        created_at=url_doc["created_at"],
    )
