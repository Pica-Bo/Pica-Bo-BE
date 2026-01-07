from typing import List

from fastapi import APIRouter, Depends, status

from app.schemas.team import TeamCreate, TeamUpdate, TeamOut
from app.services.team_service import TeamService


router = APIRouter()

_team_service = TeamService()


def get_team_service() -> TeamService:
    return _team_service


@router.get("/", response_model=List[TeamOut])
async def list_teams(service: TeamService = Depends(get_team_service)) -> List[TeamOut]:
    return await service.list_teams()


@router.get("/{team_id}", response_model=TeamOut)
async def get_team(team_id: str, service: TeamService = Depends(get_team_service)) -> TeamOut:
    return await service.get_team(team_id)


@router.post("/", response_model=TeamOut, status_code=status.HTTP_201_CREATED)
async def create_team(data: TeamCreate, service: TeamService = Depends(get_team_service)) -> TeamOut:
    return await service.create_team(data)


@router.put("/{team_id}", response_model=TeamOut)
async def update_team(team_id: str, data: TeamUpdate, service: TeamService = Depends(get_team_service)) -> TeamOut:
    return await service.update_team(team_id, data)


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: str, service: TeamService = Depends(get_team_service)) -> None:
    await service.delete_team(team_id)
