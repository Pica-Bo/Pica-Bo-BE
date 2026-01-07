import asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import os

from app.core.config import settings
from app.models.user import User

async def init_db():
    client = AsyncIOMotorClient(settings.mongo_uri)
    await init_beanie(database=client.get_default_database(), document_models=[User])

# Run init in background when module is imported (fast, simple)
_loop = asyncio.get_event_loop()
try:
    _loop.create_task(init_db())
except RuntimeError:
    # If no running loop, schedule via new loop
    loop = asyncio.new_event_loop()
    loop.run_until_complete(init_db())
