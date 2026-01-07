from typing import Optional
from pydantic import BaseModel


class ActivityBase(BaseModel):
    name: str
    slug: str
    icon: Optional[str] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    icon: Optional[str] = None


class ActivityOut(ActivityBase):
    id: str

    class Config:
        orm_mode = True
