from . import *

class BookingStatus(str, Enum):
    PENDING_PAYMENT = "pending_payment"
    PENDING_APPROVAL = "pending_approval"  # For "is_upon_request" trips
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class Booking(Document):
    # Relations
    experience_instance_id: Indexed(str)
    explorer_id: Indexed(str)  # Reference to your User/Explorer entity

    # Quantitative Data
    number_of_people: int
    total_price: float
    currency: str = "USD"

    # Meeting or pickup location (GeoJSON Point)
    pickup_location: Optional[GeoJsonPoint]

    # Metadata
    status: BookingStatus = BookingStatus.PENDING_PAYMENT
    booked_at: datetime = Field(default_factory=datetime.utcnow)
    special_requests: Optional[str] = None

    class Settings:
        name = "bookings"
