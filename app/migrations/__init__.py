"""Base migration interface for database schema/data changes.

Each migration must:
- Have a unique name (used for tracking).
- Implement `up()` method for applying changes.
- Optionally implement `down()` for rollback (not required for data migrations).
"""

from abc import ABC, abstractmethod
from motor.motor_asyncio import AsyncIOMotorClient


class BaseMigration(ABC):
    """Base class for all migrations."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for this migration (e.g., '001_create_users_indexes')."""
        pass

    @abstractmethod
    async def up(self, client: AsyncIOMotorClient) -> None:
        """Apply the migration.
        
        Args:
            client: Motor client connected to the database.
        """
        pass

    async def down(self, client: AsyncIOMotorClient) -> None:
        """Rollback the migration (optional).
        
        Args:
            client: Motor client connected to the database.
        """
        raise NotImplementedError(f"Rollback not implemented for migration: {self.name}")
