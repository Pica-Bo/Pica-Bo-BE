from . import *
class OperatorUpdate(PB_BaseModel):
	full_name: Optional[str] = Field(None, description="The full name of the operator.")
	profile_image_url: Optional[str] = Field(None, description="URL to the operator's profile image.")
	preferred_language_ids: Optional[list[str]] = Field(default=None, description="List of preferred language IDs for the operator. Each ID should correspond to a valid language in the system.")
	activities_ids: Optional[list[str]] = Field(default=None, description="List of activity IDs associated with the operator. Each ID should correspond to a valid activity in the system.")
	timezone: Optional[str] = Field(None, description="Timezone of the operator (e.g., 'UTC', 'Europe/Berlin').")
	phone: Optional[str] = Field(None, description="Contact phone number for the operator.")
	country: Optional[str] = Field(None, description="Country of residence for the operator.")
	status: Optional[str] = Field(None, description="Account status (e.g., 'active', 'inactive').")


class OperatorOut(PB_BaseModel):
	id: str = Field(..., description="The unique identifier of the operator.")
	email: str = Field(..., description="The operator's email address.")
	full_name: str = Field(..., description="The full name of the operator.")
	profile_image_url: Optional[str] = Field(None, description="URL to the operator's profile image.")
	preferred_language_ids: Optional[list[str]] = Field(default_factory=list, description="List of preferred language IDs for the operator. Each ID should correspond to a valid language in the system.")
	activities_ids: Optional[list[str]] = Field(default_factory=list, description="List of activity IDs associated with the operator. Each ID should correspond to a valid activity in the system.")
	timezone: Optional[str] = Field(None, description="Timezone of the operator (e.g., 'UTC', 'Europe/Berlin').")
	phone: Optional[str] = Field(None, description="Contact phone number for the operator.")
	country: Optional[str] = Field(None, description="Country of residence for the operator.")
	status: str = Field(..., description="Account status (e.g., 'active', 'inactive').")
	created_at: datetime = Field(..., description="Datetime when the operator was created.")

	@field_validator("id", mode="before")
	def convert_objectid_to_str(cls, v):
		return str(v)
	
class OperatorListingQuery(ListingQuery):
	verified: Optional[bool] = Field(None, alias="verified", description="Filter by verified status (True/False)")
	blocked: Optional[bool] = Field(None, alias="blocked", description="Filter by blocked status (True/False)")
	activities_ids: Optional[List[str]] = Field(None, alias="activities_ids", description="Filter by activity IDs (list of strings)")
	preferred_language_ids: Optional[List[str]] = Field(None, alias="preferred_language_ids", description="Filter by preferred language IDs (list of strings)")

class OperatorListingResult(ListingResult):
	items: List[OperatorOut]