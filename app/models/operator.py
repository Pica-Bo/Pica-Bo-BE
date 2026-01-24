from . import *
from typing import List, Optional


class Operator(Document):
	authenticator_id: Indexed(str, unique=True)
	email: Indexed(str, unique=True)
	full_name: str

	profile_image_url: Optional[str] = None

	preferred_language_ids: Optional[List[str]] = []
	timezone: Optional[str] = None

	phone: Optional[str] = None
	country: Optional[str] = None

	verified: bool = False
	verified_at: Optional[datetime] = None
	verified_by: Optional[str] = None
	
	blocked: bool = False
	blocked_at: Optional[datetime] = None
	blocked_by: Optional[str] = None
	block_reason: Optional[str] = None

	activities_ids: Optional[List[str]] = []

	status: str = "active"
	created_at: datetime = Field(default_factory=datetime.utcnow)
	updated_at: datetime = Field(default_factory=datetime.utcnow)
	class Settings:
		# Keep underlying collection name for backward compatibility
		name = "users"
