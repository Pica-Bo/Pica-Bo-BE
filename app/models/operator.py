from . import *


class Operator(Document):
	email: Indexed(str, unique=True)
	full_name: str

	profile_image_url: Optional[str] = None

	preferred_language: Optional[str] = "en"
	timezone: Optional[str] = None

	phone: Optional[str] = None
	country: Optional[str] = None

	status: str = "active"
	created_at: datetime = Field(default_factory=datetime.utcnow)

	class Settings:
		# Keep underlying collection name for backward compatibility
		name = "users"
