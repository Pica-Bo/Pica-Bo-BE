from . import *

from app.models.team import TeamLocation, TeamContact
from app.util.enums.enums import TeamVerificationStatus


class TeamCreate(PB_BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    short_description: Optional[str] = None

    profile_image_url: Optional[str] = None
    cover_image_url: Optional[str] = None

    categories: List[str] = Field(default_factory=list)
    primary_category: Optional[str] = None

    languages_supported: List[str] = Field(default_factory=list)

    location: Optional[TeamLocation] = None
    contact: Optional[TeamContact] = None

    business_type: Optional[str] = None
    license_id: Optional[str] = None
    license_doc_url: Optional[str] = None

    owner_user_id: str


class TeamUpdate(PB_BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None

    profile_image_url: Optional[str] = None
    cover_image_url: Optional[str] = None

    categories: Optional[List[str]] = None
    primary_category: Optional[str] = None

    languages_supported: Optional[List[str]] = None

    location: Optional[TeamLocation] = None
    contact: Optional[TeamContact] = None

    verification_status: Optional[TeamVerificationStatus] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None

    business_type: Optional[str] = None
    license_id: Optional[str] = None
    license_doc_url: Optional[str] = None


class TeamOut(PB_BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    short_description: Optional[str] = None

    profile_image_url: Optional[str] = None
    cover_image_url: Optional[str] = None

    categories: List[str] = Field(default_factory=list)
    primary_category: Optional[str] = None

    languages_supported: List[str] = Field(default_factory=list)

    location: Optional[TeamLocation] = None
    contact: Optional[TeamContact] = None

    verification_status: TeamVerificationStatus
    rating: float
    reviews_count: int

    business_type: Optional[str] = None
    license_id: Optional[str] = None
    license_doc_url: Optional[str] = None

    owner_user_id: str