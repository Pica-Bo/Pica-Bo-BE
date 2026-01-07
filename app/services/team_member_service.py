from typing import List

from app.models.team_member import TeamMember
from app.repositories.team_member_repository import TeamMemberRepository
from app.schemas.team_member import TeamMemberCreate, TeamMemberUpdate, TeamMemberOut
from app.services.base import BaseService


class TeamMemberService(BaseService):
    def __init__(self, repository: TeamMemberRepository | None = None) -> None:
        self.repository = repository or TeamMemberRepository()

    async def list_team_members(self) -> List[TeamMemberOut]:
        members = await self.repository.list()
        return [self._to_schema(m) for m in members]

    async def get_team_member(self, member_id: str) -> TeamMemberOut:
        member = await self.repository.get(member_id)
        if not member:
            self._not_found("Team member")
        return self._to_schema(member)

    async def create_team_member(self, data: TeamMemberCreate) -> TeamMemberOut:
        member = TeamMember(**data.dict())
        member = await self.repository.create(member)
        return self._to_schema(member)

    async def update_team_member(self, member_id: str, data: TeamMemberUpdate) -> TeamMemberOut:
        member = await self.repository.get(member_id)
        if not member:
            self._not_found("Team member")

        update_data = data.dict(exclude_unset=True)
        updated = await self.repository.update(member_id, update_data)
        assert updated is not None
        return self._to_schema(updated)

    async def delete_team_member(self, member_id: str) -> None:
        member = await self.repository.get(member_id)
        if not member:
            self._not_found("Team member")
        await self.repository.delete(member_id)

    def _to_schema(self, member: TeamMember) -> TeamMemberOut:
        return TeamMemberOut(
            id=str(member.id),
            team_id=member.team_id,
            user_id=member.user_id,
            role=member.role,
            title=member.title,
            languages=member.languages,
            certifications=member.certifications,
            profile_image_url=member.profile_image_url,
            status=member.status,
            joined_at=member.joined_at,
        )
