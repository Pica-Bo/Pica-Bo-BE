"""Create explorers collection and indexes."""

from motor.motor_asyncio import AsyncIOMotorClient

from app.migrations import BaseMigration


class CreateExplorerCollection(BaseMigration):
    @property
    def name(self) -> str:
        return "003_create_explorer_collection"

    async def up(self, client: AsyncIOMotorClient) -> None:
        db = client.get_default_database()
        explorers = db["explorers"]

        await explorers.create_index("email", unique=True)
        await explorers.create_index("user_id", unique=True, sparse=True)
        await explorers.create_index("zitadel_id", unique=True, sparse=True)
        await explorers.create_index("status")
        await explorers.create_index("loyalty_status_code")
        await explorers.create_index("travel_style_codes")
        await explorers.create_index("preferred_destination_ids")
        await explorers.create_index("preferred_activity_slugs")
        await explorers.create_index("created_at")

    async def down(self, client: AsyncIOMotorClient) -> None:
        db = client.get_default_database()
        await db["explorers"].drop()
