from . import *
from pymongo import IndexModel


class TeamMember(Document):
    team_id: Indexed(str)
    user_id: Indexed(str)

    role: TeamRole
    title: Optional[str] = None

    languages: List[str] = []
    certifications: List[str] = []

    profile_image_url: Optional[str] = None

    status: TeamMemberStatus = TeamMemberStatus.invited
    joined_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "team_members"
        indexes = [
            IndexModel([("team_id", 1), ("user_id", 1)], unique=True),
        ]
