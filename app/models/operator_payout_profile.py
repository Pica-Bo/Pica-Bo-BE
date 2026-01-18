from . import *

class PayoutType(str, Enum):
    BANK_ACCOUNT = "bank_account"
    MOBILE_WALLET = "mobile_wallet"
    STRIPE_CONNECT = "stripe_connect"

class PayoutStatus(str, Enum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    REJECTED = "rejected"

class OperatorPayoutProfile(Document):
    operator_id: Indexed(str) # pyright: ignore[reportInvalidTypeForm]
    payout_type: Indexed(PayoutType, unique=False)  # pyright: ignore[reportInvalidTypeForm] # Uniqueness enforced below
    destination_reference: str  # Encrypted or tokenized destination
    status: PayoutStatus = PayoutStatus.UNVERIFIED
    kyc_status: bool = False  # Know Your Customer (Legal requirement)
    default: bool = False  # Indicates if this is the default payout profile
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "operator_payout_profiles"
        indexes = [
            {"fields": ["operator_id", "payout_type"], "unique": True}
        ]
