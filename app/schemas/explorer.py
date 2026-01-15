from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.util.enums.enums import ExplorerStatus


class ExplorerBase(BaseModel):
    user_id: Optional[str] = None
    zitadel_id: Optional[str] = None

    email: str
    full_name: str
    birth_date: Optional[date] = None

    nationality_code: Optional[str] = None
    primary_language_code: Optional[str] = None
    spoken_language_codes: List[str] = Field(default_factory=list)

    phone_number: Optional[str] = None
    preferred_contact_channel_code: Optional[str] = None
    timezone: Optional[str] = None

    home_country_iso2: Optional[str] = None
    home_city: Optional[str] = None
    home_region: Optional[str] = None

    loyalty_status_code: Optional[str] = None
    travel_style_codes: List[str] = Field(default_factory=list)
    preferred_activity_slugs: List[str] = Field(default_factory=list)
    preferred_destination_ids: List[str] = Field(default_factory=list)
    dietary_preference_codes: List[str] = Field(default_factory=list)
    accessibility_need_codes: List[str] = Field(default_factory=list)

    preference_type_ids: List[str] = Field(default_factory=list)

    marketing_opt_in: bool = False
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class ExplorerCreate(ExplorerBase):
    status: ExplorerStatus = ExplorerStatus.active


class ExplorerUpdate(BaseModel):
    user_id: Optional[str] = None
    zitadel_id: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    birth_date: Optional[date] = None

    nationality_code: Optional[str] = None
    primary_language_code: Optional[str] = None
    spoken_language_codes: Optional[List[str]] = None

    phone_number: Optional[str] = None
    preferred_contact_channel_code: Optional[str] = None
    timezone: Optional[str] = None

    home_country_iso2: Optional[str] = None
    home_city: Optional[str] = None
    home_region: Optional[str] = None

    loyalty_status_code: Optional[str] = None
    travel_style_codes: Optional[List[str]] = None
    preferred_activity_slugs: Optional[List[str]] = None
    preferred_destination_ids: Optional[List[str]] = None
    dietary_preference_codes: Optional[List[str]] = None
    accessibility_need_codes: Optional[List[str]] = None

    preference_type_ids: Optional[List[str]] = None

    marketing_opt_in: Optional[bool] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[ExplorerStatus] = None


class ExplorerOut(ExplorerBase):
    id: str
    status: ExplorerStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
