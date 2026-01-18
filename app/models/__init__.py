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
from app.models.explorer import Explorer
from app.models.contact_channel_lookup import ContactChannelLookup

# Newly added models
from app.models.experience import Experience, TripStep, GeoJsonPoint, PickupInfo
from app.models.experience_instance import ExperienceInstance, ExperienceInstanceStatus
from app.models.booking import Booking, BookingStatus
from app.models.operator_payout_profile import OperatorPayoutProfile, PayoutType, PayoutStatus
from app.models.saved_payment_method import SavedPaymentMethod
from app.models.payment import Payment
from app.models.settlement import Settlement, SettlementStatus, PayoutBatch
from app.models.experience_review import ExperienceReview
from app.models.explorer_review import ExplorerReview
from app.models.notification import Notification, OperatorNotification, ExplorerNotification, AdminNotification