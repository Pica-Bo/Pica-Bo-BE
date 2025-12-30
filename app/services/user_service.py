from passlib.context import CryptContext
from app.models.placeholders.user import User, Role
from app.core.config import settings

pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_ctx.verify(password, hashed)

async def ensure_admin_user():
    # Create admin user from env vars if not exists
    if not settings.admin_email or not settings.admin_password:
        return
    existing = await User.find_one(User.email == settings.admin_email)
    if existing:
        return
    hashed = hash_password(settings.admin_password)
    admin = User(email=settings.admin_email, password_hash=hashed, role=Role.admin)
    await admin.insert()
