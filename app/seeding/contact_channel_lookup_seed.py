from __future__ import annotations

from typing import Dict, List

from app.seeding.base import get_client, run_seed, seed_documents

CONTACT_CHANNELS: List[Dict[str, str]] = [
    {
        "code": "email",
        "label": "Email",
        "description": "Contact via email messages.",
        "is_active": True,
    },
    {
        "code": "phone",
        "label": "Phone Call",
        "description": "Direct phone call communication.",
        "is_active": True,
    },
    {
        "code": "whatsapp",
        "label": "WhatsApp",
        "description": "WhatsApp messaging channel.",
        "is_active": True,
    },
    {
        "code": "sms",
        "label": "SMS",
        "description": "Text message communication.",
        "is_active": True,
    },
    {
        "code": "in_app",
        "label": "In-App Chat",
        "description": "Messaging through the Pica-Bo app.",
        "is_active": True,
    },
]


async def seed() -> None:
    client = get_client()
    try:
        db = client.get_default_database()
        await seed_documents(db["contact_channel_lookup"], CONTACT_CHANNELS, "code")
    finally:
        client.close()


if __name__ == "__main__":
    run_seed(seed())
