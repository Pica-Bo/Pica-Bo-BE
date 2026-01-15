from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Sequence, Tuple, Type

from beanie import Document

from app.models.accessibility_need import AccessibilityNeed
from app.models.activity_lookup import Activity
from app.models.country_lookup import CountryLookup
from app.models.destination_lookup import Destination
from app.models.dietary_preference_lookup import DietaryPreferenceLookup
from app.models.explorer_preference_type_lookup import ExplorerPreferenceTypeLookup
from app.models.language_lookup import LanguageLookup
from app.models.loyalty_status_lookup import LoyaltyStatusLookup
from app.models.travel_style_lookup import TravelStyleLookup


@dataclass(frozen=True)
class LookupDefinition:
    key: str
    display_name: str
    model: Type[Document]
    unique_fields: Tuple[str, ...]


LOOKUP_DEFINITIONS: Tuple[LookupDefinition, ...] = (
    LookupDefinition(key="activities", display_name="Activity", model=Activity, unique_fields=("slug",)),
    LookupDefinition(key="destinations", display_name="Destination", model=Destination, unique_fields=("slug",)),
    LookupDefinition(key="countries", display_name="Country", model=CountryLookup, unique_fields=("iso2_code", "iso3_code")),
    LookupDefinition(key="dietary-preferences", display_name="Dietary Preference", model=DietaryPreferenceLookup, unique_fields=("code",)),
    LookupDefinition(key="preference-types", display_name="Preference Type", model=ExplorerPreferenceTypeLookup, unique_fields=("code",)),
    LookupDefinition(key="languages", display_name="Language", model=LanguageLookup, unique_fields=("code",)),
    LookupDefinition(key="loyalty-statuses", display_name="Loyalty Status", model=LoyaltyStatusLookup, unique_fields=("code",)),
    LookupDefinition(key="travel-styles", display_name="Travel Style", model=TravelStyleLookup, unique_fields=("code",)),
    LookupDefinition(key="accessibility-needs", display_name="Accessibility Need", model=AccessibilityNeed, unique_fields=("code",)),
)


def iter_definitions() -> Iterator[LookupDefinition]:
    return iter(LOOKUP_DEFINITIONS)


LOOKUP_DOCUMENTS: Tuple[Type[Document], ...] = tuple(defn.model for defn in LOOKUP_DEFINITIONS)
