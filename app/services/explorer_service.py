from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from beanie import PydanticObjectId

from app.models.accessibility_need import AccessibilityNeed
from app.models.activity_lookup import Activity
from app.models.contact_channel_lookup import ContactChannelLookup
from app.models.country_lookup import CountryLookup
from app.models.destination_lookup import Destination
from app.models.dietary_preference_lookup import DietaryPreferenceLookup
from app.models.explorer import Explorer
from app.models.explorer_preference_type_lookup import ExplorerPreferenceTypeLookup
from app.models.language_lookup import LanguageLookup
from app.models.loyalty_status_lookup import LoyaltyStatusLookup
from app.models.travel_style_lookup import TravelStyleLookup
from app.repositories.explorer_repository import ExplorerRepository
from app.schemas.explorer import ExplorerCreate, ExplorerOut, ExplorerUpdate
from app.services.base import BaseService
from app.util.enums.enums import ExplorerStatus


class ExplorerService(BaseService):
    def __init__(self, repository: Optional[ExplorerRepository] = None) -> None:
        self.repository = repository or ExplorerRepository()

    async def list_explorers(
        self,
        *,
        status: Optional[ExplorerStatus] = None,
        loyalty_status_code: Optional[str] = None,
        travel_style_code: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[ExplorerOut]:
        explorers = await self.repository.list(
            status=status.value if isinstance(status, ExplorerStatus) else status,
            loyalty_status_code=loyalty_status_code,
            travel_style_code=travel_style_code,
            search=search,
        )
        return [self._to_schema(explorer) for explorer in explorers]

    async def get_explorer(self, explorer_id: str) -> ExplorerOut:
        explorer = await self.repository.get(explorer_id)
        if not explorer:
            self._not_found("Explorer", {"id": explorer_id})
        assert explorer is not None
        return self._to_schema(explorer)

    async def create_explorer(self, data: ExplorerCreate) -> ExplorerOut:
        payload = data.dict()
        self._normalize_lists(payload)
        await self._ensure_unique_identifiers(payload)
        await self._validate_lookups(payload)

        explorer = Explorer(**payload)
        explorer = await self.repository.create(explorer)
        return self._to_schema(explorer)

    async def update_explorer(self, explorer_id: str, data: ExplorerUpdate) -> ExplorerOut:
        explorer = await self.repository.get(explorer_id)
        if not explorer:
            self._not_found("Explorer", {"id": explorer_id})
        assert explorer is not None

        payload = data.dict(exclude_unset=True)
        if not payload:
            return self._to_schema(explorer)

        self._normalize_lists(payload)
        await self._ensure_unique_identifiers(payload, existing=explorer)
        await self._validate_lookups(payload, existing=explorer)

        payload["updated_at"] = datetime.utcnow()
        updated = await self.repository.update(explorer_id, payload)
        if not updated:
            self._not_found("Explorer", {"id": explorer_id})
        return self._to_schema(updated)

    async def archive_explorer(self, explorer_id: str) -> None:
        explorer = await self.repository.get(explorer_id)
        if not explorer:
            self._not_found("Explorer", {"id": explorer_id})
        await self.repository.update(
            explorer_id,
            {
                "status": ExplorerStatus.archived,
                "updated_at": datetime.utcnow(),
            },
        )

    async def _ensure_unique_identifiers(
        self,
        payload: Dict[str, Any],
        *,
        existing: Optional[Explorer] = None,
    ) -> None:
        email = payload.get("email")
        if email and (not existing or email != existing.email):
            duplicate = await self.repository.get_by_email(email)
            if duplicate:
                self._conflict("Explorer email already exists", {"email": email})

        user_id = payload.get("user_id")
        if user_id and (not existing or user_id != existing.user_id):
            duplicate = await self.repository.get_by_user_id(user_id)
            if duplicate:
                self._conflict("Explorer user_id already exists", {"user_id": user_id})

        zitadel_id = payload.get("zitadel_id")
        if zitadel_id and (not existing or zitadel_id != existing.zitadel_id):
            duplicate = await self.repository.get_by_zitadel_id(zitadel_id)
            if duplicate:
                self._conflict("Explorer zitadel_id already exists", {"zitadel_id": zitadel_id})

    async def _validate_lookups(
        self,
        payload: Dict[str, Any],
        *,
        existing: Optional[Explorer] = None,
    ) -> None:
        values = self._resolve_effective_values(payload, existing)

        await self._validate_code(values["nationality_code"], CountryLookup, "iso2_code", "Nationality code")
        await self._validate_code(values["primary_language_code"], LanguageLookup, "code", "Primary language code")
        await self._validate_codes(values["spoken_language_codes"], LanguageLookup, "code", "Spoken language code")
        await self._validate_code(values["home_country_iso2"], CountryLookup, "iso2_code", "Home country code")
        await self._validate_code(
            values["loyalty_status_code"], LoyaltyStatusLookup, "code", "Loyalty status code"
        )
        await self._validate_codes(values["travel_style_codes"], TravelStyleLookup, "code", "Travel style code")
        await self._validate_codes(
            values["dietary_preference_codes"], DietaryPreferenceLookup, "code", "Dietary preference code"
        )
        await self._validate_codes(
            values["accessibility_need_codes"], AccessibilityNeed, "code", "Accessibility need code"
        )
        await self._validate_code(
            values["preferred_contact_channel_code"], ContactChannelLookup, "code", "Preferred contact channel"
        )
        await self._validate_destination_ids(values["preferred_destination_ids"])
        await self._validate_activity_slugs(values["preferred_activity_slugs"])
        await self._validate_lookup_ids(
            values["preference_type_ids"], ExplorerPreferenceTypeLookup, "Preference type identifier"
        )

    async def _validate_code(
        self,
        code: Optional[str],
        model,
        field: str,
        label: str,
    ) -> None:
        if not code:
            return
        exists = await model.find_one({field: code})
        if not exists:
            self._validation_error(f"{label} '{code}' not found", {"code": code})

    async def _validate_codes(
        self,
        codes: Iterable[str],
        model,
        field: str,
        label: str,
    ) -> None:
        for code in codes:
            await self._validate_code(code, model, field, label)

    async def _validate_destination_ids(self, destination_ids: Iterable[str]) -> None:
        for destination_id in destination_ids:
            try:
                object_id = PydanticObjectId(destination_id)
            except Exception:
                self._validation_error(
                    "Destination identifier is invalid",
                    {"destination_id": destination_id},
                )
            destination = await Destination.get(object_id)
            if not destination:
                self._validation_error(
                    "Destination not found",
                    {"destination_id": destination_id},
                )

    async def _validate_activity_slugs(self, slugs: Iterable[str]) -> None:
        for slug in slugs:
            activity = await Activity.find_one(Activity.slug == slug)
            if not activity:
                self._validation_error("Activity not found", {"slug": slug})

    async def _validate_lookup_ids(
        self,
        ids: Iterable[str],
        model,
        label: str,
    ) -> None:
        for lookup_id in ids:
            try:
                object_id = PydanticObjectId(lookup_id)
            except Exception:
                self._validation_error(
                    f"{label} is invalid",
                    {"id": lookup_id},
                )
            exists = await model.get(object_id)
            if not exists:
                self._validation_error(
                    f"{label} not found",
                    {"id": lookup_id},
                )

    def _normalize_lists(self, payload: Dict[str, Any]) -> None:
        list_fields = [
            "spoken_language_codes",
            "travel_style_codes",
            "preferred_activity_slugs",
            "preferred_destination_ids",
            "dietary_preference_codes",
            "accessibility_need_codes",
            "preference_type_ids",
            "tags",
        ]
        for field in list_fields:
            if field in payload and payload[field] is not None:
                payload[field] = self._dedupe(payload[field])
            elif field in payload and payload[field] is None:
                payload[field] = []

    def _dedupe(self, values: Iterable[str]) -> List[str]:
        seen = set()
        result: List[str] = []
        for value in values:
            if value not in seen:
                seen.add(value)
                result.append(value)
        return result

    def _resolve_effective_values(
        self,
        payload: Dict[str, Any],
        existing: Optional[Explorer],
    ) -> Dict[str, Any]:
        def resolve(key: str, default: Any) -> Any:
            if key in payload:
                return payload[key]
            if existing is not None:
                return getattr(existing, key)
            return default

        return {
            "nationality_code": resolve("nationality_code", None),
            "primary_language_code": resolve("primary_language_code", None),
            "spoken_language_codes": resolve("spoken_language_codes", []),
            "home_country_iso2": resolve("home_country_iso2", None),
            "loyalty_status_code": resolve("loyalty_status_code", None),
            "travel_style_codes": resolve("travel_style_codes", []),
            "dietary_preference_codes": resolve("dietary_preference_codes", []),
            "accessibility_need_codes": resolve("accessibility_need_codes", []),
            "preferred_contact_channel_code": resolve("preferred_contact_channel_code", None),
            "preferred_destination_ids": resolve("preferred_destination_ids", []),
            "preferred_activity_slugs": resolve("preferred_activity_slugs", []),
            "preference_type_ids": resolve("preference_type_ids", []),
        }

    def _to_schema(self, explorer: Explorer) -> ExplorerOut:
        return ExplorerOut(
            id=str(explorer.id),
            user_id=explorer.user_id,
            zitadel_id=explorer.zitadel_id,
            email=explorer.email,
            full_name=explorer.full_name,
            birth_date=explorer.birth_date,
            nationality_code=explorer.nationality_code,
            primary_language_code=explorer.primary_language_code,
            spoken_language_codes=list(explorer.spoken_language_codes),
            phone_number=explorer.phone_number,
            preferred_contact_channel_code=explorer.preferred_contact_channel_code,
            timezone=explorer.timezone,
            home_country_iso2=explorer.home_country_iso2,
            home_city=explorer.home_city,
            home_region=explorer.home_region,
            loyalty_status_code=explorer.loyalty_status_code,
            travel_style_codes=list(explorer.travel_style_codes),
            preferred_activity_slugs=list(explorer.preferred_activity_slugs),
            preferred_destination_ids=list(explorer.preferred_destination_ids),
            dietary_preference_codes=list(explorer.dietary_preference_codes),
            accessibility_need_codes=list(explorer.accessibility_need_codes),
            preference_type_ids=list(explorer.preference_type_ids),
            marketing_opt_in=explorer.marketing_opt_in,
            notes=explorer.notes,
            tags=list(explorer.tags),
            status=explorer.status,
            created_at=explorer.created_at,
            updated_at=explorer.updated_at,
        )
