from typing import List, Optional

from beanie import PydanticObjectId

from app.models.operator import Operator
from app.repositories.base import BaseRepository


class OperatorRepository(BaseRepository[Operator]):
	async def get(self, id: str) -> Optional[Operator]:
		return await Operator.get(PydanticObjectId(id))

	async def list(self) -> List[Operator]:
		return await Operator.find_all().to_list()

	async def create(self, obj: Operator) -> Operator:
		await obj.insert()
		return obj

	async def update(self, id: str, obj: dict) -> Optional[Operator]:
		operator = await self.get(id)
		if not operator:
			return None
		await operator.set(obj)
		await operator.save()
		return operator

	async def delete(self, id: str) -> None:
		operator = await self.get(id)
		if operator:
			await operator.delete()
