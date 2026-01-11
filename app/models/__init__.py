from app.util.enums.enums import *
from typing import List, Optional
from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel, Field

from app.models.operator import Operator
from app.models.team import Team
from app.models.team_member import TeamMember
from app.models.user import User
from app.models.activity import Activity