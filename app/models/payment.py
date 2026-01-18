from . import *
from beanie import Link
from app.models.booking import Booking

class Payment(Document):
    booking: Link[Booking]
    explorer_id: Indexed(str)
    amount: int  # Stored in cents
    gateway_name: str  # e.g., "paymob"
    gateway_type: str  # e.g., "card", "wallet"
    status: str  # pending, captured, failed, refunded
    provider_tx_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "payments"
