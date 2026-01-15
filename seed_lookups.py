import asyncio
import logging
from typing import Callable, Awaitable

from app.seeding import (
    activity_lookup_seed,
    country_lookup_seed,
    destination_seed,
    dietary_preference_lookup_seed,
    explorer_preference_type_lookup_seed,
    language_lookup_seed,
    loyalty_status_lookup_seed,
    travel_style_lookup_seed,
)

logger = logging.getLogger("seed.lookups")
logging.basicConfig(level=logging.INFO)

SeedCoroutine = Callable[[], Awaitable[None]]

SEED_TASKS: list[tuple[str, SeedCoroutine]] = [
    ("country_lookup", country_lookup_seed.seed),
    ("language_lookup", language_lookup_seed.seed),
    ("activity_lookup", activity_lookup_seed.seed),
    ("destination", destination_seed.seed),
    ("dietary_preference_lookup", dietary_preference_lookup_seed.seed),
    ("explorer_preference_type_lookup", explorer_preference_type_lookup_seed.seed),
    ("loyalty_status_lookup", loyalty_status_lookup_seed.seed),
    ("travel_style_lookup", travel_style_lookup_seed.seed),
]


async def _run_all() -> None:
    for key, coroutine in SEED_TASKS:
        logger.info("Seeding %s", key)
        await coroutine()
    logger.info("Lookup seeding complete")


def main() -> None:
    asyncio.run(_run_all())


if __name__ == "__main__":
    main()
