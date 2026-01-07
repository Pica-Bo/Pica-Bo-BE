"""User-related business logic for operator profiles (no auth)."""

from typing import List

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services.base import BaseService


class UserService(BaseService):
	def __init__(self, repository: UserRepository | None = None) -> None:
		self.repository = repository or UserRepository()

	async def list_users(self) -> List[UserOut]:
		users = await self.repository.list()
		return [self._to_schema(u) for u in users]

	async def get_user(self, user_id: str) -> UserOut:
		user = await self.repository.get(user_id)
		if not user:
			self._not_found("User")
		return self._to_schema(user)

	async def create_user(self, data: UserCreate) -> UserOut:
		user = User(**data.dict())
		user = await self.repository.create(user)
		return self._to_schema(user)

	async def update_user(self, user_id: str, data: UserUpdate) -> UserOut:
		existing = await self.repository.get(user_id)
		if not existing:
			self._not_found("User")

		update_data = data.dict(exclude_unset=True)
		updated = await self.repository.update(user_id, update_data)
		assert updated is not None
		return self._to_schema(updated)

	async def delete_user(self, user_id: str) -> None:
		existing = await self.repository.get(user_id)
		if not existing:
			self._not_found("User")
		await self.repository.delete(user_id)

	def _to_schema(self, user: User) -> UserOut:
		return UserOut(
			id=str(user.id),
			email=user.email,
			full_name=user.full_name,
			profile_image_url=user.profile_image_url,
			preferred_language=user.preferred_language,
			timezone=user.timezone,
			phone=user.phone,
			country=user.country,
			status=user.status,
			created_at=user.created_at,
		)
