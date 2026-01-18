from . import *

class SavedPaymentMethod(Document):
    explorer_id: Indexed(str)
    provider: str  # e.g., "stripe", "paymob"
    provider_payment_method_id: str
    card_fingerprint: Indexed(str)
    brand: str  # e.g., "Visa", "Mastercard"
    last4: str
    exp_month: int
    exp_year: int
    is_default: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "payment_methods"
        indexes = [
            [("explorer_id", 1), ("card_fingerprint", 1)]
        ]
