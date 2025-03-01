from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.db.mongodb import db
from app.db.redis import redis_client
from app.core.config import settings
from app.core.tasks import start_click_sync_scheduler
import asyncio

app = FastAPI(title=settings.PROJECT_NAME, description="URL Shortener API for shortify.tech")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Events
@app.on_event("startup")
async def startup():
    # Connect to databases
    await db.connect_to_database()
    await redis_client.connect_to_redis()

    # Start background tasks
    asyncio.create_task(start_click_sync_scheduler())


@app.on_event("shutdown")
async def shutdown():
    # Close database connections
    await db.close_database_connection()
    await redis_client.close_redis_connection()


# Include routers
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
