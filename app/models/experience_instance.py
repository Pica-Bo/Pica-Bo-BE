from . import *
from app.models.experience import Experience

class ExperienceInstanceStatus(str, Enum):
    scheduled = "scheduled"
    ongoing = "ongoing"
    completed = "completed"
    cancelled = "cancelled"
    blocked = "blocked"
    confirmed = "confirmed"

class ExperienceInstance(Experience):
    # Foreign key to parent Experience
    experience_id: str
    # Date for this instance (replaces recurrence fields)
    date: datetime
    # Number of bookings for this instance
    booked_count: int = 0
    # Status of the instance
    status: ExperienceInstanceStatus = ExperienceInstanceStatus.scheduled

    class Settings:
        name = "experience_instances"
