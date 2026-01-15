"""Initial migration: Create all collections and indexes for the project.

This creates collections and indexes for:
- users
- teams
- team_members
- activities
"""

from motor.motor_asyncio import AsyncIOMotorClient
from app.migrations import BaseMigration


class CreateCollectionsAndIndexes(BaseMigration):
    @property
    def name(self) -> str:
        return "001_create_collections_and_indexes"

    async def up(self, client: AsyncIOMotorClient) -> None:
        """Create all collections and indexes."""
        db = client.get_default_database()
        
        # ===== Users Collection =====
        users = db["users"]
        await users.create_index("email", unique=True)
        await users.create_index("status")
        await users.create_index("created_at")
        
        # ===== Teams Collection =====
        teams = db["teams"]
        await teams.create_index("slug", unique=True)
        await teams.create_index("owner_user_id")
        await teams.create_index("verification_status")
        await teams.create_index("primary_category")
        await teams.create_index("categories")
        await teams.create_index("rating")
        await teams.create_index("created_at")
        await teams.create_index("updated_at")
        # Compound index for filtering teams
        await teams.create_index([("verification_status", 1), ("rating", -1)])
        
        # ===== Team Members Collection =====
        team_members = db["team_members"]
        await team_members.create_index("team_id")
        await team_members.create_index("user_id")
        await team_members.create_index("status")
        # Compound index for uniqueness and queries
        await team_members.create_index([("team_id", 1), ("user_id", 1)], unique=True)
        await team_members.create_index([("team_id", 1), ("status", 1)])
        
        # ===== Activities Collection =====
        activities = db["activities_lookup"]
        await activities.create_index("slug", unique=True)
        await activities.create_index("name")

    async def down(self, client: AsyncIOMotorClient) -> None:
        """Drop all collections (WARNING: destructive operation)."""
        db = client.get_default_database()
        
        # Drop all collections
        await db["users"].drop()
        await db["teams"].drop()
        await db["team_members"].drop()
        await db["activities_lookup"].drop()
