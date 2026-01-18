from . import *
from beanie import Link
from app.models.booking import Booking

class ExplorerReview(Document):
    # Relationships
    explorer_id: Indexed(str)  # The person being reviewed
    operator_id: Indexed(str)  # The person writing the review
    booking: Link[Booking]

    # Ratings (Can be specific metrics)
    punctuality_rating: int = Field(ge=1, le=5)
    communication_rating: int = Field(ge=1, le=5)
    respect_rating: int = Field(ge=1, le=5)

    comment: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "explorer_reviews"
