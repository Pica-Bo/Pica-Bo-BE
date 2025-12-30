from typing import Generic, TypeVar

T = TypeVar('T')

class BaseRepository(Generic[T]):
    async def get(self, id: str) -> T:
        raise NotImplementedError
    async def list(self, *args, **kwargs) -> list[T]:
        raise NotImplementedError
    async def create(self, obj: T) -> T:
        raise NotImplementedError
    async def update(self, id: str, obj: dict) -> T:
        raise NotImplementedError
    async def delete(self, id: str) -> None:
        raise NotImplementedError
