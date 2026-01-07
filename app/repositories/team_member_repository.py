from typing import List, Optional

from beanie import PydanticObjectId

from app.models.team_member import TeamMember
from app.repositories.base import BaseRepository


class TeamMemberRepository(BaseRepository[TeamMember]):
    async def get(self, id: str) -> Optional[TeamMember]:
        return await TeamMember.get(PydanticObjectId(id))

    async def list(self) -> List[TeamMember]:
        return await TeamMember.find_all().to_list()

    async def create(self, obj: TeamMember) -> TeamMember:
        await obj.insert()
        return obj

    async def update(self, id: str, obj: dict) -> Optional[TeamMember]:
        member = await self.get(id)
        if not member:
            return None
        await member.set(obj)
        await member.save()
        return member

    async def delete(self, id: str) -> None:
        member = await self.get(id)
        if member:
            await member.delete()
