from beanie import Document, Indexed
from pydantic import Field, EmailStr
from typing import Optional
from enum import Enum

class Role(str, Enum):
    admin = 'admin'
    rest_admin = 'rest_admin'

class User(Document):
    email: EmailStr = Field(...)
    password_hash: str = Field(...)
    role: Role = Field(default=Role.rest_admin)

    class Settings:
        name = 'users'
