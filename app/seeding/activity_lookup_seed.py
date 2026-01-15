from __future__ import annotations

from typing import List, Dict, Any

from app.seeding.base import get_client, run_seed, seed_documents

ACTIVITIES: List[Dict[str, Any]] = [
    {
        "name": "Historical Tour",
        "slug": "historical-tour",
        "icon": "mdi:bank",
    },
    {
        "name": "Museum Visit",
        "slug": "museum-visit",
        "icon": "mdi:museum",
    },
    {
        "name": "Nile Cruise",
        "slug": "nile-cruise",
        "icon": "mdi:ferry",
    },
    {
        "name": "Desert Safari",
        "slug": "desert-safari",
        "icon": "mdi:jeepney",
    },
    {
        "name": "Hot Air Balloon",
        "slug": "hot-air-balloon",
        "icon": "mdi:balloon",
    },
    {
        "name": "Snorkeling",
        "slug": "snorkeling",
        "icon": "mdi:snorkel",
    },
    {
        "name": "Scuba Diving",
        "slug": "scuba-diving",
        "icon": "mdi:diving-scuba",
    },
    {
        "name": "Culinary Experience",
        "slug": "culinary-experience",
        "icon": "mdi:silverware-fork-knife",
    },
    {
        "name": "Wellness Retreat",
        "slug": "wellness-retreat",
        "icon": "mdi:spa",
    },
    {
        "name": "Photography Tour",
        "slug": "photography-tour",
        "icon": "mdi:camera",
    },
]


async def seed() -> None:
    client = get_client()
    try:
        db = client.get_default_database()
        await seed_documents(db["activities_lookup"], ACTIVITIES, "slug")
    finally:
        client.close()


if __name__ == "__main__":
    run_seed(seed())
