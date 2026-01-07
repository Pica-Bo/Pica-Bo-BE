from typing import List, Optional

from beanie import PydanticObjectId

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    async def get(self, id: str) -> Optional[User]:
        return await User.get(PydanticObjectId(id))

    async def list(self) -> List[User]:
        return await User.find_all().to_list()

    async def create(self, obj: User) -> User:
        await obj.insert()
        return obj

    async def update(self, id: str, obj: dict) -> Optional[User]:
        user = await self.get(id)
        if not user:
            return None
        await user.set(obj)
        await user.save()
        return user

    async def delete(self, id: str) -> None:
        user = await self.get(id)
        if user:
            await user.delete()
