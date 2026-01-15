from . import *


class DietaryPreferenceLookup(Document):
    code: Indexed(str, unique=True)
    label: str
    description: Optional[str] = None
    is_allergen: bool = False

    class Settings:
        name = "dietary_preference_lookup"
