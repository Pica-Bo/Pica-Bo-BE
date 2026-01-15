from app.util.enums.enums import *
from typing import List, Optional
from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel, Field

from app.models.operator import Operator
from app.models.team import Team
from app.models.team_member import TeamMember
from app.models.user import User
from app.models.activity_lookup import Activity
from app.models.country_lookup import CountryLookup
from app.models.language_lookup import LanguageLookup
from app.models.destination_lookup import Destination
from app.models.dietary_preference_lookup import DietaryPreferenceLookup
from app.models.accessibility_need import AccessibilityNeed
from app.models.travel_style_lookup import TravelStyleLookup
from app.models.loyalty_status_lookup import LoyaltyStatusLookup
from app.models.explorer_preference_type_lookup import ExplorerPreferenceTypeLookup