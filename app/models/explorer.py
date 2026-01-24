from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from . import *


class Explorer(Document):
    explorer_id: Optional[str] = Indexed(str, unique=True)
    authenticator_id: Optional[str] = Indexed(str, unique=True)

    email: Indexed(str, unique=True)
    full_name: str
    birth_date: Optional[date] = None

    nationality_code: Optional[str] = None
    primary_language_code: Optional[str] = None
    spoken_language_codes: List[str] = []

    phone_number: Optional[str] = None
    preferred_contact_channel_code: Optional[str] = None
    timezone: Optional[str] = None

    home_country_iso2: Optional[str] = None
    home_city: Optional[str] = None
    home_region: Optional[str] = None

    loyalty_status_code: Optional[str] = None
    travel_style_codes: List[str] = []
    preferred_activity_slugs: List[str] = []
    preferred_destination_ids: List[str] = []
    dietary_preference_codes: List[str] = []
    accessibility_need_codes: List[str] = []

    preference_type_ids: List[str] = []

    status: ExplorerStatus = ExplorerStatus.active
    marketing_opt_in: bool = False
    notes: Optional[str] = None

    tags: List[str] = []

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "explorers"
