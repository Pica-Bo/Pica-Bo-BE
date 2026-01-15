from __future__ import annotations

from typing import Dict, List, Optional

from beanie import PydanticObjectId

from app.models.explorer import Explorer
from app.repositories.base import BaseRepository


class ExplorerRepository(BaseRepository[Explorer]):
    async def get(self, id: str) -> Optional[Explorer]:
        try:
            object_id = PydanticObjectId(id)
        except Exception:
            return None
        return await Explorer.get(object_id)

    async def get_by_email(self, email: str) -> Optional[Explorer]:
        return await Explorer.find_one(Explorer.email == email)

    async def get_by_user_id(self, user_id: str) -> Optional[Explorer]:
        return await Explorer.find_one(Explorer.user_id == user_id)

    async def get_by_zitadel_id(self, zitadel_id: str) -> Optional[Explorer]:
        return await Explorer.find_one(Explorer.zitadel_id == zitadel_id)

    async def list(
        self,
        *,
        status: Optional[str] = None,
        loyalty_status_code: Optional[str] = None,
        travel_style_code: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Explorer]:
        filters: Dict[str, object] = {}
        if status:
            filters["status"] = status
        if loyalty_status_code:
            filters["loyalty_status_code"] = loyalty_status_code
        if travel_style_code:
            filters["travel_style_codes"] = travel_style_code

        if search:
            query = Explorer.find(
                {
                    **filters,
                    "$or": [
                        {"full_name": {"$regex": search, "$options": "i"}},
                        {"email": {"$regex": search, "$options": "i"}},
                    ],
                }
            )
        else:
            query = Explorer.find(filters)

        return await query.sort("-created_at").to_list()

    async def create(self, obj: Explorer) -> Explorer:
        await obj.insert()
        return obj

    async def update(self, id: str, data: dict) -> Optional[Explorer]:
        explorer = await self.get(id)
        if not explorer:
            return None
        if data:
            await explorer.update({"$set": data})
            await explorer.reload()
        return explorer

    async def delete(self, id: str) -> None:
        explorer = await self.get(id)
        if explorer:
            await explorer.delete()
