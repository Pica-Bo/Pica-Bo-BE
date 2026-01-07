from typing import List

from fastapi import APIRouter, Depends, status

from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityOut
from app.services.activity_service import ActivityService


router = APIRouter()

_activity_service = ActivityService()


def get_activity_service() -> ActivityService:
    return _activity_service


@router.get("/", response_model=List[ActivityOut])
async def list_activities(service: ActivityService = Depends(get_activity_service)) -> List[ActivityOut]:
    return await service.list_activities()


@router.get("/{activity_id}", response_model=ActivityOut)
async def get_activity(activity_id: str, service: ActivityService = Depends(get_activity_service)) -> ActivityOut:
    return await service.get_activity(activity_id)


@router.post("/", response_model=ActivityOut, status_code=status.HTTP_201_CREATED)
async def create_activity(data: ActivityCreate, service: ActivityService = Depends(get_activity_service)) -> ActivityOut:
    return await service.create_activity(data)


@router.put("/{activity_id}", response_model=ActivityOut)
async def update_activity(activity_id: str, data: ActivityUpdate, service: ActivityService = Depends(get_activity_service)) -> ActivityOut:
    return await service.update_activity(activity_id, data)


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(activity_id: str, service: ActivityService = Depends(get_activity_service)) -> None:
    await service.delete_activity(activity_id)
