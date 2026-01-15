from . import *


class LoyaltyStatusLookup(Document):
    code: Indexed(str, unique=True)
    label: str
    description: Optional[str] = None
    rank: Optional[int] = None
    is_active: bool = True

    class Settings:
        name = "loyalty_status_lookup"
