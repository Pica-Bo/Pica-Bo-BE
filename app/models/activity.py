from . import *

class Activity(Document):
    name: str
    slug: Indexed(str, unique=True)
    icon: Optional[str] = None

    class Settings:
        name = "activities"
