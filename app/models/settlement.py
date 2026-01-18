from . import *
from beanie import Link
from app.models.payment import Payment

class SettlementStatus(str, Enum):
    PENDING = "pending"   # Awaiting trip completion
    BATCHED = "batched"   # Assigned to a PayoutBatch
    PAID = "paid"         # Money sent to operator
    VOID = "void"         # Cancelled/Refunded

class Settlement(Document):
    payment_id: Link[Payment]
    operator_id: Indexed(str)
    net_payout: int  # Amount after pica-bo commission
    status: SettlementStatus = SettlementStatus.PENDING
    payout_batch_id: Optional[Link["PayoutBatch"]] = None
    due_date: datetime  # Usually TripDate + 7*24h
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "settlements"

class PayoutBatch(Document):
    operator_id: Indexed(str)
    total_amount: int
    payout_provider: str  # e.g., "bank_transfer", "vodafone_cash"
    payout_destination_id: str  # Wallet number or IBAN
    status: str = "processing"  # processing, success, failed
    provider_payout_id: Optional[str] = None
    executed_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "payout_batches"
