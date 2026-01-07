from typing import List

from fastapi import APIRouter, Depends, status

from app.schemas.team_member import TeamMemberCreate, TeamMemberUpdate, TeamMemberOut
from app.services.team_member_service import TeamMemberService


router = APIRouter()

# Single shared instance; still injectable & overrideable via Depends
_team_member_service = TeamMemberService()


def get_team_member_service() -> TeamMemberService:
    return _team_member_service


@router.get("/", response_model=List[TeamMemberOut])
async def list_team_members(service: TeamMemberService = Depends(get_team_member_service)) -> List[TeamMemberOut]:
    return await service.list_team_members()


@router.get("/{member_id}", response_model=TeamMemberOut)
async def get_team_member(member_id: str, service: TeamMemberService = Depends(get_team_member_service)) -> TeamMemberOut:
    return await service.get_team_member(member_id)


@router.post("/", response_model=TeamMemberOut, status_code=status.HTTP_201_CREATED)
async def create_team_member(data: TeamMemberCreate, service: TeamMemberService = Depends(get_team_member_service)) -> TeamMemberOut:
    return await service.create_team_member(data)


@router.put("/{member_id}", response_model=TeamMemberOut)
async def update_team_member(member_id: str, data: TeamMemberUpdate, service: TeamMemberService = Depends(get_team_member_service)) -> TeamMemberOut:
    return await service.update_team_member(member_id, data)


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team_member(member_id: str, service: TeamMemberService = Depends(get_team_member_service)) -> None:
    await service.delete_team_member(member_id)
