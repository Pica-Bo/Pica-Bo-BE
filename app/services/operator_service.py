"""Operator-related business logic for operator profiles (no auth)."""

from typing import List, Optional

from app.models.operator import Operator
from app.repositories.operator_repository import OperatorRepository
from app.schemas.operator import OperatorCreate, OperatorUpdate, OperatorOut
from app.services.base import BaseService


class OperatorService(BaseService):
	def __init__(self, repository: OperatorRepository | None = None) -> None:
		self.repository = repository or OperatorRepository()

	async def list_operators(
		self,
		verified: Optional[bool] = None,
		blocked: Optional[bool] = None,
		activities: Optional[List[str]] = None,
		languages: Optional[List[str]] = None,
	) -> List[OperatorOut]:
		operators = await self.repository.list(
			verified=verified,
			blocked=blocked,
			activities=activities,
			languages=languages
		)
		return [self._to_schema(o) for o in operators]

	async def get_operator(self, operator_id: str) -> OperatorOut:
		operator = await self.repository.get(operator_id)
		if not operator:
			self._not_found("Operator")
		return self._to_schema(operator)

	async def create_operator(self, data: OperatorCreate) -> OperatorOut:
		operator = Operator(**data.dict())
		operator = await self.repository.create(operator)
		return self._to_schema(operator)

	async def update_operator(self, operator_id: str, data: OperatorUpdate) -> OperatorOut:
		existing = await self.repository.get(operator_id)
		if not existing:
			self._not_found("Operator")

		update_data = data.dict(exclude_unset=True)
		updated = await self.repository.update(operator_id, update_data)
		assert updated is not None
		return self._to_schema(updated)

	async def delete_operator(self, operator_id: str) -> None:
		existing = await self.repository.get(operator_id)
		if not existing:
			self._not_found("Operator")
		await self.repository.delete(operator_id)

	def _to_schema(self, operator: Operator) -> OperatorOut:
		return OperatorOut(
			id=str(operator.id),
			email=operator.email,
			full_name=operator.full_name,
			profile_image_url=operator.profile_image_url,
			preferred_language=operator.preferred_language,
			timezone=operator.timezone,
			phone=operator.phone,
			country=operator.country,
			status=operator.status,
			created_at=operator.created_at,
		)
