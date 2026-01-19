from . import *

class Role(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    CUSTOMER_SUPPORT = "customer_support"
    FINANCE_TEAM = "finance_team"
    MARKETING_TEAM = "marketing_team"
    OPERATION_TEAM = "operation_team"
    SALES_TEAM = "sales_team"
class User(Document):
    email: Indexed(str, unique=True)
    full_name: str

    profile_image_url: Optional[str] = None

    preferred_language: Optional[str] = "en"
    timezone: Optional[str] = None

    phone: Optional[str] = None
    country: Optional[str] = None

    roles: List[Role] = Field(default_factory=lambda: [Role.MEMBER])

    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
