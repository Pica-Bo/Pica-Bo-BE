from . import *

class GeoJsonPoint(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [longitude, latitude]

class PickupInfo(BaseModel):
    has_pickup: bool = False
    pickup_instructions: Optional[str] = None
    meeting_point_address: Optional[str] = None
    meeting_point_coordinates: Optional[GeoJsonPoint] = None  # For Map integration

class TripStep(BaseModel):
    title: str
    description: str

class Experience(Document):
    trip_title: str
    images: List[str] = []
    location: Optional[GeoJsonPoint] = None  # Main experience location as GeoJSON
    short_description: Optional[str] = None
    tags: List[str] = []
    languages: List[str] = []

    available_seats: int
    duration: str
    experience_level: Optional[str] = None
    difficulty: Optional[str] = None
    operator_id: Optional[str] = None

    start_date: datetime
    end_date: Optional[datetime] = None
    timezone: Optional[str] = "UTC"
    booking_cutoff_hours: Optional[int] = Field(default=24)

    price_per_person: float
    cancellation_policy: Optional[str] = None

    is_recurring: bool = False
    recurring_pattern: Optional[str] = None
    is_upon_request: bool = False

    trip_steps: List[TripStep] = []
    included_items: List[str] = []
    excluded_items: List[str] = []
    meeting_point: Optional[GeoJsonPoint] = None  # Meeting point as GeoJSON
    pickup_info: Optional[PickupInfo] = None
    what_to_bring: List[str] = []
    age_notes: Optional[str] = None
    additional_info: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "experiences"