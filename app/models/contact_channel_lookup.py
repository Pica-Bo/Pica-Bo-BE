from . import *


class ContactChannelLookup(Document):
    code: Indexed(str, unique=True)
    label: str
    description: Optional[str] = None
    is_active: bool = True

    class Settings:
        name = "contact_channel_lookup"
