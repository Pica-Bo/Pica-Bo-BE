from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.models.placeholders.user import User
from app.services.user_service import verify_password
from app.services.auth_service import create_access_token

router = APIRouter()

class LoginIn(BaseModel):
    email: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'

@router.post('/login', response_model=TokenOut)
async def login(data: LoginIn):
    user = await User.find_one(User.email == data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    token = create_access_token(subject=user.email, role=user.role.value)
    return {'access_token': token}
