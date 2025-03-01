from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings
from ..core.logging import setup_logging

logger = setup_logging("shortify.mongodb")


class MongoDB:
    client: AsyncIOMotorClient = None
    database = None

    async def connect_to_database(self):
        """Connect to MongoDB database"""
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            self.database = self.client[settings.DB_NAME]

            # Test the connection
            await self.database.command("ping")
            logger.info(f"Connected to MongoDB database: {settings.DB_NAME}")

        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    async def close_database_connection(self):
        """Close database connection"""
        if self.client:
            try:
                self.client.close()
                logger.info("Closed MongoDB connection")
            except Exception as e:
                logger.error(f"Error closing MongoDB connection: {str(e)}")


# Create a singleton instance
db = MongoDB()
