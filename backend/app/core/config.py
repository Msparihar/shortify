from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "shortify.tech"
    MONGODB_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "shortify"
    BASE_URL: str = "https://shortify.tech"

    # Redis settings
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_TTL: int = 3600  # 1 hour cache TTL
    REDIS_CLICK_SYNC_INTERVAL: int = 60  # Sync clicks every 60 seconds

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
