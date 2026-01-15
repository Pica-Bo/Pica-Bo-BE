from __future__ import annotations

from typing import List, Dict, Any

from app.seeding.base import get_client, run_seed, seed_documents

LOYALTY_STATUSES: List[Dict[str, Any]] = [
    {
        "code": "new",
        "label": "New",
        "description": "Recently joined explorer with no bookings yet.",
        "rank": 1,
        "is_active": True,
    },
    {
        "code": "engaged",
        "label": "Engaged",
        "description": "Explorer has interacted and completed an initial experience.",
        "rank": 2,
        "is_active": True,
    },
    {
        "code": "loyal",
        "label": "Loyal",
        "description": "Repeat explorer with multiple bookings.",
        "rank": 3,
        "is_active": True,
    },
    {
        "code": "ambassador",
        "label": "Ambassador",
        "description": "High-value explorer who advocates or refers others.",
        "rank": 4,
        "is_active": True,
    },
]


async def seed() -> None:
    client = get_client()
    try:
        db = client.get_default_database()
        await seed_documents(db["loyalty_status_lookup"], LOYALTY_STATUSES, "code")
    finally:
        client.close()


if __name__ == "__main__":
    run_seed(seed())
