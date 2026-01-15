from . import *


class CountryLookup(Document):
    iso2_code: Indexed(str, unique=True)
    iso3_code: Optional[str] = None
    name: str
    nationality: Optional[str] = None
    region: Optional[str] = None
    subregion: Optional[str] = None
    phone_code: Optional[str] = None

    class Settings:
        name = "country_lookup"
