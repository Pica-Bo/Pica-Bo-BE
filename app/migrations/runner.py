"""Migration runner for executing and tracking database migrations.

Migrations are stored in a `migrations_log` collection tracking which ones have run.
"""

import logging
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from datetime import datetime

from app.migrations import BaseMigration

logger = logging.getLogger(__name__)


class MigrationRunner:
    """Handles running and tracking migrations."""

    def __init__(self, client: AsyncIOMotorClient, database_name: Optional[str] = None):
        self.client = client
        self.db: AsyncIOMotorDatabase = (
            client.get_database(database_name) if database_name else client.get_default_database()
        )
        self.migrations_collection = self.db["migrations_log"]

    async def has_run(self, migration_name: str) -> bool:
        """Check if a migration has already been applied."""
        doc = await self.migrations_collection.find_one({"name": migration_name})
        return doc is not None

    async def mark_as_run(self, migration_name: str) -> None:
        """Mark a migration as completed."""
        await self.migrations_collection.insert_one(
            {
                "name": migration_name,
                "applied_at": datetime.utcnow(),
            }
        )

    async def run_migrations(self, migrations: List[BaseMigration]) -> None:
        """Run all pending migrations in order.
        
        Args:
            migrations: List of migration instances to run.
        """
        for migration in migrations:
            if await self.has_run(migration.name):
                logger.info(f"Migration '{migration.name}' already applied, skipping.")
                continue

            logger.info(f"Running migration: {migration.name}")
            try:
                await migration.up(self.client)
                await self.mark_as_run(migration.name)
                logger.info(f"Migration '{migration.name}' completed successfully.")
            except Exception as e:
                logger.error(f"Migration '{migration.name}' failed: {e}")
                raise

    async def rollback_migration(self, migration: BaseMigration) -> None:
        """Rollback a specific migration (if supported).
        
        Args:
            migration: Migration instance to rollback.
        """
        if not await self.has_run(migration.name):
            logger.warning(f"Migration '{migration.name}' was not applied, nothing to rollback.")
            return

        logger.info(f"Rolling back migration: {migration.name}")
        try:
            await migration.down(self.client)
            await self.migrations_collection.delete_one({"name": migration.name})
            logger.info(f"Migration '{migration.name}' rolled back successfully.")
        except NotImplementedError:
            logger.error(f"Migration '{migration.name}' does not support rollback.")
            raise
        except Exception as e:
            logger.error(f"Rollback of '{migration.name}' failed: {e}")
            raise
