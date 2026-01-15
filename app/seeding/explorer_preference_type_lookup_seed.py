from __future__ import annotations

from typing import List, Dict, Any

from app.seeding.base import get_client, run_seed, seed_documents

PREFERENCE_TYPES: List[Dict[str, Any]] = [
    {
        "code": "activity",
        "label": "Activity",
        "description": "Preference for specific activity categories.",
        "allows_reference_id": True,
        "is_active": True,
    },
    {
        "code": "destination",
        "label": "Destination",
        "description": "Preferred destinations or regions.",
        "allows_reference_id": True,
        "is_active": True,
    },
    {
        "code": "travel_style",
        "label": "Travel Style",
        "description": "Exploration style such as adventure or relaxation.",
        "allows_reference_id": True,
        "is_active": True,
    },
    {
        "code": "dietary",
        "label": "Dietary",
        "description": "Dietary preferences or requirements.",
        "allows_reference_id": True,
        "is_active": True,
    },
    {
        "code": "accessibility",
        "label": "Accessibility",
        "description": "Accessibility needs to accommodate.",
        "allows_reference_id": True,
        "is_active": True,
    },
    {
        "code": "accommodation",
        "label": "Accommodation",
        "description": "Preferred accommodation types and amenities.",
        "allows_reference_id": False,
        "is_active": True,
    },
    {
        "code": "budget",
        "label": "Budget",
        "description": "Budget range or spending expectations.",
        "allows_reference_id": False,
        "is_active": True,
    },
    {
        "code": "custom",
        "label": "Custom",
        "description": "Free-form preference captured from explorer conversations.",
        "allows_reference_id": False,
        "is_active": True,
    },
]


async def seed() -> None:
    client = get_client()
    try:
        db = client.get_default_database()
        await seed_documents(db["explorer_preference_type_lookup"], PREFERENCE_TYPES, "code")
    finally:
        client.close()


if __name__ == "__main__":
    run_seed(seed())
