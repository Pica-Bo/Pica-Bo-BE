from typing import List

from app.models.team import Team
from app.repositories.team_repository import TeamRepository
from app.schemas.team import TeamCreate, TeamUpdate, TeamOut
from app.services.base import BaseService


class TeamService(BaseService):
    def __init__(self, repository: TeamRepository | None = None) -> None:
        self.repository = repository or TeamRepository()

    async def list_teams(self) -> List[TeamOut]:
        teams = await self.repository.list()
        return [self._to_schema(t) for t in teams]

    async def get_team(self, team_id: str) -> TeamOut:
        team = await self.repository.get(team_id)
        if not team:
            self._not_found("Team")
        return self._to_schema(team)

    async def create_team(self, data: TeamCreate) -> TeamOut:
        existing = await self.repository.get_by_slug(data.slug)
        if existing:
            self._bad_request("Slug already exists")

        team = Team(**data.dict())
        team = await self.repository.create(team)
        return self._to_schema(team)

    async def update_team(self, team_id: str, data: TeamUpdate) -> TeamOut:
        team = await self.repository.get(team_id)
        if not team:
            self._not_found(team)

        update_data = data.dict(exclude_unset=True)

        new_slug = update_data.get("slug")
        if new_slug and new_slug != team.slug:
            existing = await self.repository.get_by_slug(new_slug)
            if existing and str(existing.id) != str(team.id):
                self._bad_request("Slug already exists")

        updated = await self.repository.update(team_id, update_data)
        assert updated is not None
        return self._to_schema(updated)

    async def delete_team(self, team_id: str) -> None:
        team = await self.repository.get(team_id)
        if not team:
            self._not_found("Team")
        await self.repository.delete(team_id)

    def _to_schema(self, team: Team) -> TeamOut:
        return TeamOut(
            id=str(team.id),
            name=team.name,
            slug=team.slug,
            description=team.description,
            short_description=team.short_description,
            profile_image_url=team.profile_image_url,
            cover_image_url=team.cover_image_url,
            categories=team.categories,
            primary_category=team.primary_category,
            languages_supported=team.languages_supported,
            location=team.location,
            contact=team.contact,
            verification_status=team.verification_status,
            rating=team.rating,
            reviews_count=team.reviews_count,
            business_type=team.business_type,
            license_id=team.license_id,
            license_doc_url=team.license_doc_url,
            owner_user_id=team.owner_user_id,
        )
