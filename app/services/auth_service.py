from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
import jwt
from jwt import PyJWTError
from typing import Optional
from app.models.placeholders.user import User

security = HTTPBearer()

class TokenData:
    def __init__(self, sub: str, role: str):
        self.sub = sub
        self.role = role

def create_access_token(subject: str, role: str) -> str:
    from datetime import datetime, timedelta
    payload = {
        'sub': subject,
        'role': role,
        'exp': datetime.utcnow() + timedelta(minutes=settings.jwt_exp_minutes)
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token

async def jwt_required(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Missing credentials')
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        sub = payload.get('sub')
        role = payload.get('role')
        if sub is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token payload')
        # Optionally fetch user from DB to ensure still valid
        user = await User.find_one(User.email == sub)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
        return TokenData(sub=sub, role=role)
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token invalid or expired')
