from . import *

from app.models.experience import (CancellationPolicy, GeoJsonPoint, DifficultyLevel, 
                                   TripStep, PickupInfo, Experience, ExperienceStatus)


class ExperienceCreateSchema(PB_BaseModel):
    trip_title: str = Field(..., description="Title of the experience.")
    images: Optional[List[str]] = Field([], description="List of image URLs.")
    location: Optional[GeoJsonPoint] = Field(None, description="Main experience location as GeoJSON")
    short_description: Optional[str] = Field(None, description="Short description of the experience.")
    tags: List[str] = Field([], description="List of tags associated with the experience.")
    languages: List[str] = Field([], description="List of languages available for the experience.")

    activity_id: Optional[str] = Field(None, description="Associated activity ID.")

    available_seats: Optional[int] = Field(None, description="Number of available seats.")
    duration: Optional[str] = Field(None, description="Duration of the experience.")
    difficulty: Optional[DifficultyLevel] = Field(None, description="Difficulty level (beginner, intermediate, advanced).")

    start_date: Optional[datetime ] = Field(None, description="Start date and time of the experience.")
    end_date: Optional[datetime] = Field(None, description="End date and time of the experience recurrence.")
    timezone: Optional[str] = "UTC"
    booking_cutoff_hours: Optional[int] = Field(default=24, description="Hours before start when booking is cut off.")

    price_per_person: Optional[float] = Field(None, description="Price per person for the experience.")
    cancellation_policy: Optional[CancellationPolicy] = Field(None, description="Cancellation policy for the experience.")

    is_recurring: bool = Field(False, description="Indicates if the experience is recurring.")
    recurring_pattern: Optional[str] = Field(None, description="Pattern for recurring experience.")
    is_upon_request: bool = Field(False, description="Indicates if the experience is upon request.")

    trip_steps: Optional[List[TripStep]] = Field(None, description="List of steps in the trip.")
    included_items: Optional[List[str]] = Field(None, description="List of items included in the experience.")
    excluded_items: Optional[List[str]] = Field(None, description="List of items excluded from the experience.")
    meeting_point: Optional[GeoJsonPoint] = Field(None, description="Meeting point as GeoJSON")
    pickup_info: Optional[PickupInfo] = Field(None, description="Pickup information for the experience.")
    what_to_bring: Optional[List[str]] = Field(None, description="List of items to bring for the experience.")
    age_notes: Optional[str] = Field(None, description="Notes about age restrictions or recommendations.")
    additional_info: Optional[str] = Field(None, description="Any additional information about the experience.")

class ExperienceUpdateSchema(ExperienceCreateSchema):
    pass

class RejectExperienceSchema(PB_BaseModel):
    rejection_reason: str = Field(..., description="Reason for rejecting the experience.")

class ExperienceOutSchema(PB_BaseModel, Experience):
    pass

class ExperienceCompactOutSchema(PB_BaseModel):
    id: str = Field(..., description="Unique identifier for the experience.")
    trip_title: str = Field(..., description="Title of the experience.")
    short_description: Optional[str] = Field(None, description="Short description of the experience.")
    images: List[str] = Field([], description="List of image URLs.")
    price_per_person: Optional[float] = Field(None, description="Price per person for the experience.")
    location: Optional[GeoJsonPoint] = Field(None, description="Main experience location as GeoJSON")
    status: ExperienceStatus = Field(..., description="Current status of the experience.")

class ExperienceListingQuery(ListingQuery):
    operator_id: Optional[str] = Field(None, description="Filter experiences by operator ID.")
    operator_name: Optional[str] = Field(None, description="Filter experiences by operator name.")

    status: Optional[str] = Field(None, description="Filter experiences by status.")

    price_min: Optional[float] = Field(None, description="Minimum price filter.")
    price_max: Optional[float] = Field(None, description="Maximum price filter.")

    activity_ids: Optional[List[str]] = Field(None, description="Filter by a list of activity IDs.")
    location: Optional[GeoJsonPoint] = Field(None, description="Filter experiences near a specific location.")

class ExperienceListOutSchema(ListingResult):
    items: List[ExperienceCompactOutSchema]