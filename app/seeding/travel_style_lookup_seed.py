from __future__ import annotations

from typing import List, Dict, Any

from app.seeding.base import get_client, run_seed, seed_documents

TRAVEL_STYLES: List[Dict[str, Any]] = [
    {
        "code": "solo",
        "label": "Solo Explorer",
        "description": "Prefers traveling independently with curated support.",
        "is_active": True,
    },
    {
        "code": "couple",
        "label": "Couple Retreat",
        "description": "Experiences tailored for two travelers.",
        "is_active": True,
    },
    {
        "code": "family",
        "label": "Family Adventure",
        "description": "Family-friendly experiences for multiple generations.",
        "is_active": True,
    },
    {
        "code": "group",
        "label": "Group Journey",
        "description": "Small-group experiences with shared interests.",
        "is_active": True,
    },
    {
        "code": "adventure",
        "label": "Adventure Seeker",
        "description": "High-energy trips focusing on outdoor thrills.",
        "is_active": True,
    },
    {
        "code": "relaxation",
        "label": "Relaxation & Wellness",
        "description": "Slow-paced escapes for rest and rejuvenation.",
        "is_active": True,
    },
    {
        "code": "luxury",
        "label": "Luxury Experience",
        "description": "Premium itineraries with elevated amenities and services.",
        "is_active": True,
    },
    {
        "code": "budget",
        "label": "Budget Friendly",
        "description": "Value-driven experiences optimizing cost without sacrificing quality.",
        "is_active": True,
    },
]


async def seed() -> None:
    client = get_client()
    try:
        db = client.get_default_database()
        await seed_documents(db["travel_style_lookup"], TRAVEL_STYLES, "code")
    finally:
        client.close()


if __name__ == "__main__":
    run_seed(seed())
