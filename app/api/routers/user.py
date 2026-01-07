from typing import List

from fastapi import APIRouter, Depends, status

from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services.user_service import UserService


router = APIRouter()

_user_service = UserService()


def get_user_service() -> UserService:
    return _user_service


@router.get("/", response_model=List[UserOut])
async def list_users(service: UserService = Depends(get_user_service)) -> List[UserOut]:
    return await service.list_users()


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str, service: UserService = Depends(get_user_service)) -> UserOut:
    return await service.get_user(user_id)


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, service: UserService = Depends(get_user_service)) -> UserOut:
    return await service.create_user(data)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: str, data: UserUpdate, service: UserService = Depends(get_user_service)) -> UserOut:
    return await service.update_user(user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, service: UserService = Depends(get_user_service)) -> None:
    await service.delete_user(user_id)
