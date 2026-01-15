from typing import List

from app.models.activity_lookup import Activity
from app.repositories.activity_repository import ActivityRepository
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityOut
from app.services.base import BaseService


class ActivityService(BaseService):
    def __init__(self, repository: ActivityRepository | None = None) -> None:
        self.repository = repository or ActivityRepository()

    async def list_activities(self) -> List[ActivityOut]:
        activities = await self.repository.list()
        return [self._to_schema(a) for a in activities]

    async def get_activity(self, activity_id: str) -> ActivityOut:
        activity = await self.repository.get(activity_id)
        if not activity:
            self._not_found("Activity")
        return self._to_schema(activity)

    async def create_activity(self, data: ActivityCreate) -> ActivityOut:
        existing = await self.repository.get_by_slug(data.slug)
        if existing:
            self._bad_request("Slug already exists")

        activity = Activity(name=data.name, slug=data.slug, icon=data.icon)
        activity = await self.repository.create(activity)
        return self._to_schema(activity)

    async def update_activity(self, activity_id: str, data: ActivityUpdate) -> ActivityOut:
        activity = await self.repository.get(activity_id)
        if not activity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")

        update_data = data.dict(exclude_unset=True)

        new_slug = update_data.get("slug")
        if new_slug and new_slug != activity.slug:
            existing = await self.repository.get_by_slug(new_slug)
            if existing and str(existing.id) != str(activity.id):
                self._bad_request("Slug already exists")

        updated = await self.repository.update(activity_id, update_data)
        assert updated is not None
        return self._to_schema(updated)

    async def delete_activity(self, activity_id: str) -> None:
        activity = await self.repository.get(activity_id)
        if not activity:
            self._not_found("Activity")
        await self.repository.delete(activity_id)

    def _to_schema(self, activity: Activity) -> ActivityOut:
        return ActivityOut(id=str(activity.id), name=activity.name, slug=activity.slug, icon=activity.icon)
