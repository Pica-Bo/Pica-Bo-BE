from typing import List, Optional

from beanie import PydanticObjectId

from app.models.activity_lookup import Activity
from app.repositories.base import BaseRepository


class ActivityRepository(BaseRepository[Activity]):
    async def get(self, id: str) -> Optional[Activity]:
        return await Activity.get(PydanticObjectId(id))

    async def list(self) -> List[Activity]:
        return await Activity.find_all().to_list()

    async def get_by_slug(self, slug: str) -> Optional[Activity]:
        return await Activity.find_one(Activity.slug == slug)

    async def create(self, obj: Activity) -> Activity:
        await obj.insert()
        return obj

    async def update(self, id: str, obj: dict) -> Optional[Activity]:
        activity = await self.get(id)
        if not activity:
            return None
        await activity.set(obj)
        await activity.save()
        return activity

    async def delete(self, id: str) -> None:
        activity = await self.get(id)
        if activity:
            await activity.delete()
