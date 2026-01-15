from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping

from beanie import Document

from app.lookups import LOOKUP_DEFINITIONS, LookupDefinition
from app.repositories.lookup_repository import LookupRepository
from app.services.base import BaseService


class LookupService(BaseService):
    def __init__(self) -> None:
        self._definitions: dict[str, LookupDefinition] = {definition.key: definition for definition in LOOKUP_DEFINITIONS}
        self._repositories: dict[str, LookupRepository] = {
            key: LookupRepository(definition.model)
            for key, definition in self._definitions.items()
        }

    def supported_types(self) -> Iterable[str]:
        return self._definitions.keys()

    def _get_definition(self, lookup_type: str) -> LookupDefinition:
        definition = self._definitions.get(lookup_type)
        if not definition:
            self._not_found("Lookup Type", {"lookup_type": lookup_type})
        assert definition is not None  # for type checkers
        return definition

    def _get_repository(self, lookup_type: str) -> LookupRepository:
        repo = self._repositories.get(lookup_type)
        if not repo:
            self._not_found("Lookup Type", {"lookup_type": lookup_type})
        return repo

    async def list_items(self, lookup_type: str) -> list[dict[str, Any]]:
        repository = self._get_repository(lookup_type)
        documents = await repository.list()
        return [self._serialize(doc) for doc in documents]

    async def get_item(self, lookup_type: str, item_id: str) -> dict[str, Any]:
        repository = self._get_repository(lookup_type)
        document = await repository.get(item_id)
        if not document:
            self._not_found(self._get_definition(lookup_type).display_name, {"id": item_id})
        assert document is not None
        return self._serialize(document)

    async def create_item(self, lookup_type: str, data: Mapping[str, Any]) -> dict[str, Any]:
        definition = self._get_definition(lookup_type)
        repository = self._get_repository(lookup_type)
        payload = dict(data)
        await self._ensure_uniques(definition, repository, payload)
        document = await repository.create(payload)
        return self._serialize(document)

    async def update_item(self, lookup_type: str, item_id: str, data: Mapping[str, Any]) -> dict[str, Any]:
        definition = self._get_definition(lookup_type)
        repository = self._get_repository(lookup_type)
        document = await repository.get(item_id)
        if not document:
            self._not_found(definition.display_name, {"id": item_id})
        assert document is not None

        payload = dict(data)
        await self._ensure_uniques(definition, repository, payload, current=document)
        updated = await repository.update(document, payload)
        return self._serialize(updated)

    async def _ensure_uniques(
        self,
        definition: LookupDefinition,
        repository: LookupRepository,
        payload: Dict[str, Any],
        *,
        current: Document | None = None,
    ) -> None:
        for field in definition.unique_fields:
            value = payload.get(field)
            if value is None:
                continue
            existing = await repository.find_by_field(field, value)
            if existing and (current is None or str(existing.id) != str(current.id)):
                self._conflict(
                    f"{definition.display_name} with {field} '{value}' already exists",
                    {"field": field, "value": value},
                )

    def _serialize(self, document: Document) -> dict[str, Any]:
        payload = document.dict()
        payload.pop("_id", None)
        payload["id"] = str(document.id)
        return payload
