from typing import List, Optional

from beanie import PydanticObjectId

from app.models.team import Team
from app.repositories.base import BaseRepository


class TeamRepository(BaseRepository[Team]):
    async def get(self, id: str) -> Optional[Team]:
        return await Team.get(PydanticObjectId(id))

    async def list(self) -> List[Team]:
        return await Team.find_all().to_list()

    async def get_by_slug(self, slug: str) -> Optional[Team]:
        return await Team.find_one(Team.slug == slug)

    async def create(self, obj: Team) -> Team:
        await obj.insert()
        return obj

    async def update(self, id: str, obj: dict) -> Optional[Team]:
        team = await self.get(id)
        if not team:
            return None
        await team.set(obj)
        await team.save()
        return team

    async def delete(self, id: str) -> None:
        team = await self.get(id)
        if team:
            await team.delete()
