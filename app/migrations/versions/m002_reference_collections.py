"""Create reference collections for explorer normalization.

Collections:
- country_lookup
- language_lookup
- destinations
- dietary_preference_lookup
- accessibility_needs
- travel_style_lookup
- loyalty_status_lookup
- explorer_preference_type_lookup
- contact_channel_lookup
"""

from motor.motor_asyncio import AsyncIOMotorClient

from app.migrations import BaseMigration


class CreateReferenceCollections(BaseMigration):
    @property
    def name(self) -> str:
        return "002_create_reference_collections"

    async def up(self, client: AsyncIOMotorClient) -> None:
        db = client.get_default_database()

        countries = db["country_lookup"]
        await countries.create_index("iso2_code", unique=True)
        await countries.create_index("iso3_code")
        await countries.create_index("name")

        languages = db["language_lookup"]
        await languages.create_index("code", unique=True)
        await languages.create_index("name")

        destinations = db["destinations"]
        await destinations.create_index("slug", unique=True)
        await destinations.create_index("name")
        await destinations.create_index("location.country_iso2")
        await destinations.create_index("tags")

        dietary_preferences = db["dietary_preference_lookup"]
        await dietary_preferences.create_index("code", unique=True)
        await dietary_preferences.create_index("is_allergen")

        accessibility_needs = db["accessibility_needs"]
        await accessibility_needs.create_index("code", unique=True)

        travel_styles = db["travel_style_lookup"]
        await travel_styles.create_index("code", unique=True)
        await travel_styles.create_index("is_active")

        loyalty_statuses = db["loyalty_status_lookup"]
        await loyalty_statuses.create_index("code", unique=True)
        await loyalty_statuses.create_index("rank")

        preference_types = db["explorer_preference_type_lookup"]
        await preference_types.create_index("code", unique=True)
        await preference_types.create_index("allows_reference_id")

        contact_channels = db["contact_channel_lookup"]
        await contact_channels.create_index("code", unique=True)
        await contact_channels.create_index("is_active")

    async def down(self, client: AsyncIOMotorClient) -> None:
        db = client.get_default_database()

        await db["contact_channel_lookup"].drop()
        await db["explorer_preference_type_lookup"].drop()
        await db["loyalty_status_lookup"].drop()
        await db["travel_style_lookup"].drop()
        await db["accessibility_needs"].drop()
        await db["dietary_preference_lookup"].drop()
        await db["destinations"].drop()
        await db["language_lookup"].drop()
        await db["country_lookup"].drop()
