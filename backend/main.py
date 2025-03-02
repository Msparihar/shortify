from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.db.mongodb import db
from app.db.redis import redis_client
from app.core.config import settings
from app.core.tasks import start_click_sync_scheduler
import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to databases
    await db.connect_to_database()
    await redis_client.connect_to_redis()

    # Start background tasks
    task = asyncio.create_task(start_click_sync_scheduler())

    yield

    # Close database connections
    await db.close_database_connection()
    await redis_client.close_redis_connection()
    task.cancel()


app = FastAPI(title=settings.PROJECT_NAME, description="URL Shortener API for shortify.tech", lifespan=lifespan)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)


@app.get("/health")
def health():
    return {"status": "ok"}


# Include routers
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
