from . import *


class LanguageLookup(Document):
    code: Indexed(str, unique=True)
    name: str
    native_name: Optional[str] = None
    rtl: bool = False

    class Settings:
        name = "language_lookup"
