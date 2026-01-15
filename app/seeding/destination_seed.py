from __future__ import annotations

from typing import List, Dict, Any

from app.seeding.base import get_client, run_seed, seed_documents

DESTINATIONS: List[Dict[str, Any]] = [
    {
        "name": "Cairo",
        "slug": "cairo",
        "summary": "Bustling capital blending ancient wonders with modern culture.",
        "description": "Home to the Pyramids of Giza, the Egyptian Museum, and a vibrant food scene.",
        "location": {
            "country_iso2": "EG",
            "city": "Cairo",
            "region": "Greater Cairo",
            "latitude": 30.0444,
            "longitude": 31.2357,
        },
        "tags": ["culture", "history", "urban"],
        "featured_image_url": "https://example.com/images/destinations/cairo.jpg",
        "gallery_image_urls": [],
        "primary_seasons": ["winter", "spring"],
        "primary_language_codes": ["ar", "en"],
    },
    {
        "name": "Giza",
        "slug": "giza",
        "summary": "Iconic pyramids and sprawling desert vistas beside the Nile.",
        "description": "Features the Great Pyramids, Sphinx, and sound-and-light evening experiences.",
        "location": {
            "country_iso2": "EG",
            "city": "Giza",
            "region": "Giza Governorate",
            "latitude": 29.9773,
            "longitude": 31.1325,
        },
        "tags": ["history", "unesco", "desert"],
        "featured_image_url": "https://example.com/images/destinations/giza.jpg",
        "gallery_image_urls": [],
        "primary_seasons": ["autumn", "winter"],
        "primary_language_codes": ["ar", "en"],
    },
    {
        "name": "Luxor",
        "slug": "luxor",
        "summary": "Open-air museum along the Nile with pharaonic temples.",
        "description": "Covers Karnak Temple, Valley of the Kings, and hot-air balloon rides at sunrise.",
        "location": {
            "country_iso2": "EG",
            "city": "Luxor",
            "region": "Luxor Governorate",
            "latitude": 25.6872,
            "longitude": 32.6396,
        },
        "tags": ["archaeology", "nile", "culture"],
        "featured_image_url": "https://example.com/images/destinations/luxor.jpg",
        "gallery_image_urls": [],
        "primary_seasons": ["winter", "spring"],
        "primary_language_codes": ["ar", "en", "fr"],
    },
    {
        "name": "Aswan",
        "slug": "aswan",
        "summary": "Relaxed Nile-side city with Nubian heritage.",
        "description": "Gateway to Philae Temple, Abu Simbel excursions, and Nubian village stays.",
        "location": {
            "country_iso2": "EG",
            "city": "Aswan",
            "region": "Aswan Governorate",
            "latitude": 24.0889,
            "longitude": 32.8998,
        },
        "tags": ["nile", "culture", "heritage"],
        "featured_image_url": "https://example.com/images/destinations/aswan.jpg",
        "gallery_image_urls": [],
        "primary_seasons": ["winter", "spring"],
        "primary_language_codes": ["ar", "en"],
    },
    {
        "name": "Siwa Oasis",
        "slug": "siwa-oasis",
        "summary": "Remote desert oasis famed for salt lakes and starry skies.",
        "description": "Offers eco-lodges, desert safaris, and ancient Oracle temple ruins.",
        "location": {
            "country_iso2": "EG",
            "city": "Siwa",
            "region": "Matrouh Governorate",
            "latitude": 29.2056,
            "longitude": 25.5194,
        },
        "tags": ["desert", "wellness", "adventure"],
        "featured_image_url": "https://example.com/images/destinations/siwa.jpg",
        "gallery_image_urls": [],
        "primary_seasons": ["autumn", "winter", "spring"],
        "primary_language_codes": ["ar", "en"],
    },
    {
        "name": "Hurghada",
        "slug": "hurghada",
        "summary": "Red Sea resort town with coral reefs and water sports.",
        "description": "Popular for diving, snorkeling, and nearby desert quad adventures.",
        "location": {
            "country_iso2": "EG",
            "city": "Hurghada",
            "region": "Red Sea Governorate",
            "latitude": 27.2574,
            "longitude": 33.8129,
        },
        "tags": ["beach", "diving", "resort"],
        "featured_image_url": "https://example.com/images/destinations/hurghada.jpg",
        "gallery_image_urls": [],
        "primary_seasons": ["autumn", "winter", "spring", "summer"],
        "primary_language_codes": ["ar", "en", "de", "ru"],
    },
    {
        "name": "Sharm El Sheikh",
        "slug": "sharm-el-sheikh",
        "summary": "Sinai Peninsula getaway with marine life and mountains.",
        "description": "Known for Ras Mohammed National Park, diving, and St. Catherine excursions.",
        "location": {
            "country_iso2": "EG",
            "city": "Sharm El Sheikh",
            "region": "South Sinai Governorate",
            "latitude": 27.9158,
            "longitude": 34.3299,
        },
        "tags": ["beach", "diving", "adventure"],
        "featured_image_url": "https://example.com/images/destinations/sharm.jpg",
        "gallery_image_urls": [],
        "primary_seasons": ["autumn", "winter", "spring"],
        "primary_language_codes": ["ar", "en", "it"],
    },
    {
        "name": "Alexandria",
        "slug": "alexandria",
        "summary": "Mediterranean port with cosmopolitan flair and Hellenistic history.",
        "description": "Highlights include the Bibliotheca Alexandrina, Citadel of Qaitbay, and seaside promenades.",
        "location": {
            "country_iso2": "EG",
            "city": "Alexandria",
            "region": "Alexandria Governorate",
            "latitude": 31.2001,
            "longitude": 29.9187,
        },
        "tags": ["coastal", "history", "culture"],
        "featured_image_url": "https://example.com/images/destinations/alexandria.jpg",
        "gallery_image_urls": [],
        "primary_seasons": ["spring", "autumn"],
        "primary_language_codes": ["ar", "en", "fr"],
    },
]


async def seed() -> None:
    client = get_client()
    try:
        db = client.get_default_database()
        await seed_documents(db["destinations"], DESTINATIONS, "slug")
    finally:
        client.close()


if __name__ == "__main__":
    run_seed(seed())
