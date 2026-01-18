import asyncio
import logging
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import os

from app.core.config import settings
from app.models import *
from app.lookups import LOOKUP_DOCUMENTS
from app.migrations.runner import MigrationRunner
from app.migrations.registry import MIGRATIONS

logger = logging.getLogger(__name__)


async def init_db():
    client = AsyncIOMotorClient(settings.mongo_uri)
    
    # Run migrations before initializing Beanie
    # logger.info("Running database migrations...")
    # runner = MigrationRunner(client)
    # await runner.run_migrations(MIGRATIONS)
    # logger.info("Migrations completed.")
    

    # Add all new models for Beanie initialization
    from app.models import (
        Experience,
        ExperienceInstance, Booking,
        OperatorPayoutProfile,
        SavedPaymentMethod, Payment,
        Settlement, PayoutBatch,
        ExperienceReview, ExplorerReview,
        Notification, OperatorNotification, ExplorerNotification, AdminNotification
    )

    base_documents = [Operator, Team, TeamMember, User, Explorer, OperatorPayoutProfile,
        Experience, ExperienceInstance, Booking, SavedPaymentMethod, Payment,
        Settlement, PayoutBatch, ExperienceReview, ExplorerReview,
        Notification, OperatorNotification, ExplorerNotification, AdminNotification
    ] #OperatorPayoutProfile
    document_models = base_documents + list(LOOKUP_DOCUMENTS)

    await init_beanie(
        database=client.get_default_database(),
        document_models=document_models,
    )

# Run init in background when module is imported (fast, simple)
_loop = asyncio.get_event_loop()
try:
    _loop.create_task(init_db())
except RuntimeError:
    # If no running loop, schedule via new loop
    loop = asyncio.new_event_loop()
    loop.run_until_complete(init_db())
