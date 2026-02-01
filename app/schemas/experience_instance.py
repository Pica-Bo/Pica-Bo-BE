from app.models.experience_instance import ExperienceInstance, ExperienceInstanceStatus, GeoJsonPoint
from . import *
from app.schemas.experience import ExperienceUpdateSchema

class ExperienceInstanceUpdateSchema(ExperienceUpdateSchema):
    pass
    
class ExperienceInstanceCancelSchema(PB_BaseModel):
    experience_id: str = Field(..., description="ID of the experience instance to cancel.")
    date: datetime = Field(..., description="Date of the experience instance to cancel.")
    cancellation_reason: str = Field(..., description="Reason for cancellation.")

class ExperienceInstanceOutSchema(PB_BaseModel, ExperienceInstance):
    pass

class ExperienceInstanceCompactOutSchema(PB_BaseModel):
    trip_title: str = Field(..., description="Title of the experience.")
    date: datetime = Field(..., description="Date of the experience instance.")
    status: ExperienceInstanceStatus = Field(..., description="Current status of the experience instance.")
    booked_count: int = Field(..., description="Number of bookings for this instance.")
    available_count: Optional[int] = Field(..., description="Number of available seats for this instance.")
    location: Optional[GeoJsonPoint] = Field(..., description="Main experience location as GeoJSON")
    images: List[str] = Field(..., description="Image URLs for the experience instance.")

class ExperienceInstanceListingQuery(ListingQuery):
    experience_id: Optional[str] = Field(None, description="Filter by experience ID.")
    
    operator_id: Optional[str] = Field(None, description="Filter by operator ID.")
    
    status: Optional[ExperienceInstanceStatus] = Field(None, description="Filter by instance status.")
    
    date_from: Optional[datetime] = Field(None, description="Filter instances starting from this date.")
    date_to: Optional[datetime] = Field(None, description="Filter instances ending by this date.")


class ExperienceInstanceListingResult(ListingResult):
    items: List[ExperienceInstanceCompactOutSchema]