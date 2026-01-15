import asyncio
import logging
from typing import Iterable, Mapping

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

logger = logging.getLogger("app.seeding")


def _ensure_event_loop() -> asyncio.AbstractEventLoop:
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


def get_client() -> AsyncIOMotorClient:
    """Create a Mongo client using shared settings."""
    return AsyncIOMotorClient(settings.mongo_uri)


async def seed_documents(collection, documents: Iterable[Mapping], unique_field: str) -> None:
    """Upsert documents into the given collection by unique field."""
    for document in documents:
        if unique_field not in document:
            raise ValueError(f"Document missing unique field '{unique_field}'")
        key_value = document[unique_field]
        await collection.update_one(
            {unique_field: key_value},
            {"$set": document},
            upsert=True,
        )
        logger.info("Upserted %s=%s into %s", unique_field, key_value, collection.name)


def run_seed(coroutine) -> None:
    """Execute a seed coroutine, ensuring the loop closes when complete."""
    loop = _ensure_event_loop()
    if loop.is_running():
        raise RuntimeError("Cannot run seed while event loop is active")
    loop.run_until_complete(coroutine)
    loop.close()
