from __future__ import annotations

from typing import Any, Generic, Optional, Type, TypeVar

from beanie import Document, PydanticObjectId

TDocument = TypeVar("TDocument", bound=Document)


class LookupRepository(Generic[TDocument]):
    """Generic repository for lookup collections."""

    def __init__(self, model: Type[TDocument]) -> None:
        self.model = model

    async def list(self) -> list[TDocument]:
        return await self.model.find_all().to_list()

    async def get(self, item_id: str) -> Optional[TDocument]:
        return await self.model.get(PydanticObjectId(item_id))

    async def find_by_field(self, field: str, value: Any) -> Optional[TDocument]:
        return await self.model.find_one({field: value})

    async def create(self, data: dict[str, Any]) -> TDocument:
        document = self.model(**data)
        await document.insert()
        return document

    async def update(self, document: TDocument, data: dict[str, Any]) -> TDocument:
        if not data:
            return document
        await document.update({"$set": data})
        await document.reload()
        return document

    async def delete(self, document: TDocument) -> None:
        await document.delete()
