from __future__ import annotations

from typing import List, Dict, Any

from app.seeding.base import get_client, run_seed, seed_documents

COUNTRIES: List[Dict[str, Any]] = [
    {
        "iso2_code": "EG",
        "iso3_code": "EGY",
        "name": "Egypt",
        "nationality": "Egyptian",
        "region": "Africa",
        "subregion": "Northern Africa",
        "phone_code": "+20",
    },
]


async def seed() -> None:
    client = get_client()
    try:
        db = client.get_default_database()
        await seed_documents(db["country_lookup"], COUNTRIES, "iso2_code")
    finally:
        client.close()


if __name__ == "__main__":
    run_seed(seed())
