from . import *


class TravelStyleLookup(Document):
    code: Indexed(str, unique=True)
    label: str
    description: Optional[str] = None
    is_active: bool = True

    class Settings:
        name = "travel_style_lookup"
