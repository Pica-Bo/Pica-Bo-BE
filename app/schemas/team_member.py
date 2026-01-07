from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field

from app.util.enums.enums import TeamRole, TeamMemberStatus


class TeamMemberCreate(BaseModel):
    team_id: str
    user_id: str

    role: TeamRole
    title: Optional[str] = None

    languages: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)

    profile_image_url: Optional[str] = None

    status: Optional[TeamMemberStatus] = TeamMemberStatus.invited


class TeamMemberUpdate(BaseModel):
    role: Optional[TeamRole] = None
    title: Optional[str] = None

    languages: Optional[List[str]] = None
    certifications: Optional[List[str]] = None

    profile_image_url: Optional[str] = None

    status: Optional[TeamMemberStatus] = None
    joined_at: Optional[datetime] = None


class TeamMemberOut(BaseModel):
    id: str
    team_id: str
    user_id: str

    role: TeamRole
    title: Optional[str] = None

    languages: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)

    profile_image_url: Optional[str] = None

    status: TeamMemberStatus
    joined_at: Optional[datetime] = None

    class Config:
        orm_mode = True
