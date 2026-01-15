from . import *


class DestinationLocation(BaseModel):
    country_iso2: str
    city: Optional[str] = None
    region: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Destination(Document):
    name: str
    slug: Indexed(str, unique=True)
    description: Optional[str] = None
    summary: Optional[str] = None
    location: DestinationLocation
    tags: List[str] = []
    featured_image_url: Optional[str] = None
    gallery_image_urls: List[str] = []
    primary_seasons: List[str] = []
    primary_language_codes: List[str] = []

    class Settings:
        name = "destinations"
