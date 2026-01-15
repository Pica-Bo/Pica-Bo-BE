from __future__ import annotations

from typing import List, Dict, Any

from app.seeding.base import get_client, run_seed, seed_documents

LANGUAGES: List[Dict[str, Any]] = [
    {
        "code": "ar",
        "name": "Arabic",
        "native_name": "العربية",
        "rtl": True,
    },
    {
        "code": "en",
        "name": "English",
        "native_name": "English",
        "rtl": False,
    },
    {
        "code": "fr",
        "name": "French",
        "native_name": "Français",
        "rtl": False,
    },
    {
        "code": "de",
        "name": "German",
        "native_name": "Deutsch",
        "rtl": False,
    },
    {
        "code": "it",
        "name": "Italian",
        "native_name": "Italiano",
        "rtl": False,
    },
    {
        "code": "ru",
        "name": "Russian",
        "native_name": "Русский",
        "rtl": False,
    },
]


async def seed() -> None:
    client = get_client()
    try:
        db = client.get_default_database()
        await seed_documents(db["language_lookup"], LANGUAGES, "code")
    finally:
        client.close()


if __name__ == "__main__":
    run_seed(seed())
