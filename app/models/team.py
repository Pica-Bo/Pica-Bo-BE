from . import *

class TeamType(str, Enum):
    independent = "independent" #one person or freelancer
    group = "group"       #small group of people [up to 10 members]
    agency = "agency" #small team [10-50 members]
    enterprise = "enterprise" #large organization

class TeamLocation(BaseModel):
    country: str
    city: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class TeamContact(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    website: Optional[str] = None


class Team(Document):
    name: str
    slug: Indexed(str, unique=True)
    description: Optional[str] = None
    short_description: Optional[str] = None

    profile_image_url: Optional[str] = None
    cover_image_url: Optional[str] = None

    categories: List[str] = []          # references Category.slug or id
    primary_category: Optional[str] = None

    languages_supported: List[str] = [] # ["en", "ar", "fr"]

    location: Optional[TeamLocation] = None
    contact: Optional[TeamContact] = None

    verification_status: TeamVerificationStatus = TeamVerificationStatus.unverified
    rating: float = 0.0
    reviews_count: int = 0

    business_type: Optional[str] = None
    license_id: Optional[str] = None
    license_doc_url: Optional[str] = None

    team_type: Optional[TeamType] = TeamType.independent

    owner_user_id: Indexed(str)

    completed: bool = False #indicates if the team profile is completed

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "teams"
