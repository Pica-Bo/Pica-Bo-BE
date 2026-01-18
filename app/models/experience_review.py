from . import *
from beanie import Link
from app.models.experience import Experience
from app.models.experience_instance import ExperienceInstance
from app.models.booking import Booking

class ExperienceReview(Document):
    # Relationships
    experience: Link[Experience]
    experience_instance: Link[ExperienceInstance]
    booking: Link[Booking]
    explorer_id: Indexed(str)

    # Quantitative Data
    rating: int = Field(ge=1, le=5)  # 1 to 5 stars

    # Qualitative Data
    title: Optional[str] = None
    comment: str
    images: List[str] = []  # Travelers love seeing real photos

    # Metadata
    is_verified: bool = True
    is_hidden: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "experience_reviews"
