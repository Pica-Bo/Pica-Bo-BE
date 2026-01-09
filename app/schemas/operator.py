from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class OperatorCreate(BaseModel):
	email: str
	full_name: str

	profile_image_url: Optional[str] = None
	preferred_language: Optional[str] = "en"
	timezone: Optional[str] = None

	phone: Optional[str] = None
	country: Optional[str] = None

	status: Optional[str] = "active"


class OperatorUpdate(BaseModel):
	full_name: Optional[str] = None

	profile_image_url: Optional[str] = None
	preferred_language: Optional[str] = None
	timezone: Optional[str] = None

	phone: Optional[str] = None
	country: Optional[str] = None

	status: Optional[str] = None


class OperatorOut(BaseModel):
	id: str
	email: str
	full_name: str

	profile_image_url: Optional[str] = None
	preferred_language: Optional[str] = "en"
	timezone: Optional[str] = None

	phone: Optional[str] = None
	country: Optional[str] = None

	status: str
	created_at: datetime

	class Config:
		orm_mode = True
