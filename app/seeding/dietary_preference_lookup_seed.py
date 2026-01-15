from __future__ import annotations

from typing import List, Dict, Any

from app.seeding.base import get_client, run_seed, seed_documents

DIETARY_PREFERENCES: List[Dict[str, Any]] = [
    {
        "code": "vegetarian",
        "label": "Vegetarian",
        "description": "Excludes meat, poultry, and seafood.",
        "is_allergen": False,
    },
    {
        "code": "vegan",
        "label": "Vegan",
        "description": "Excludes all animal products.",
        "is_allergen": False,
    },
    {
        "code": "halal",
        "label": "Halal",
        "description": "Requires halal-certified ingredients and preparation.",
        "is_allergen": False,
    },
    {
        "code": "kosher",
        "label": "Kosher",
        "description": "Requires kosher-certified ingredients and preparation.",
        "is_allergen": False,
    },
    {
        "code": "gluten_free",
        "label": "Gluten Free",
        "description": "Avoids wheat, barley, rye, and related grains.",
        "is_allergen": False,
    },
    {
        "code": "lactose_free",
        "label": "Lactose Free",
        "description": "Avoids dairy products containing lactose.",
        "is_allergen": False,
    },
    {
        "code": "nut_allergy",
        "label": "Nut Allergy",
        "description": "Severe allergy to peanuts and tree nuts.",
        "is_allergen": True,
    },
    {
        "code": "shellfish_allergy",
        "label": "Shellfish Allergy",
        "description": "Allergy to crustaceans and mollusks.",
        "is_allergen": True,
    },
]


async def seed() -> None:
    client = get_client()
    try:
        db = client.get_default_database()
        await seed_documents(db["dietary_preference_lookup"], DIETARY_PREFERENCES, "code")
    finally:
        client.close()


if __name__ == "__main__":
    run_seed(seed())
