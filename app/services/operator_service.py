"""Operator-related business logic for operator profiles (no auth)."""

from typing import List, Optional

from app.models.operator import Operator
from app.repositories.operator_repository import OperatorRepository
from app.schemas.operator import OperatorUpdate, OperatorOut
from app.services.base import BaseService


class OperatorService(BaseService):
	def __init__(self, repository: OperatorRepository | None = None) -> None:
		self.repository = repository or OperatorRepository()

	async def list_operators(
		self,
		page: int = 1,
		page_size: int = 20,
		verified: Optional[bool] = None,
		blocked: Optional[bool] = None,
		activities_ids: Optional[List[str]] = None,
		preferred_language_ids: Optional[List[str]] = None,
	) -> List[OperatorOut]:
		operators = await self.repository.list(
			page=page,
			page_size=page_size,
			verified=verified,
			blocked=blocked,
			activities_ids=activities_ids,
			preferred_language_ids=preferred_language_ids
		)
		return operators

	async def get_operator(self, auth_user_id: str) -> OperatorOut:
		operator = await self.repository.get(auth_user_id)
		if not operator:
			self._not_found("Operator")
		return self._to_schema(operator)

	async def create_operator(self, auth_user_id: str, name: str, email: str) -> OperatorOut:
		operator = Operator(authenticator_id=auth_user_id, full_name=name, email=email)
		operator = await self.repository.create(operator)
		return self._to_schema(operator)

	async def update_operator(self, auth_user_id: str, data: OperatorUpdate) -> OperatorOut:
		update_data = data.dict(exclude_unset=True)
		updated = await self.repository.update(auth_user_id, update_data)
		assert updated is not None
		return self._to_schema(updated)

	async def delete_operator(self, operator_id: str) -> None:
		existing = await self.repository.get(operator_id)
		if not existing:
			self._not_found("Operator")
		await self.repository.delete(operator_id)

	def _to_schema(self, operator: Operator) -> OperatorOut:
		return OperatorOut(**operator.dict())
