from . import *


class AccessibilityNeed(Document):
    code: Indexed(str, unique=True)
    label: str
    description: Optional[str] = None

    class Settings:
        name = "accessibility_needs"
        bson_encoders = {ObjectId: str}
