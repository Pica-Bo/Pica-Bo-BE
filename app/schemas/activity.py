from . import *

class ActivityBase(PB_BaseModel):
    name: str
    slug: str
    icon: Optional[str] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(PB_BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    icon: Optional[str] = None


class ActivityOut(ActivityBase):
    id: str