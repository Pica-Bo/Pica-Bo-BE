from . import *


class ExplorerPreferenceTypeLookup(Document):
    code: Indexed(str, unique=True)
    label: str
    description: Optional[str] = None
    allows_reference_id: bool = False
    is_active: bool = True

    class Settings:
        name = "explorer_preference_type_lookup"
