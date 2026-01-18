from . import *

class Notification(Document):
    user_id: Indexed(str)  # Can be Explorer or Operator
    type: str  # "booking_confirmed", "new_message", "payout_sent"
    title: str
    body: str
    link: str  # URL to redirect the user when they click
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "notifications"

class OperatorNotification(Notification):
    class Settings:
        name = "operator_notifications"

class ExplorerNotification(Notification):
    class Settings:
        name = "explorer_notifications"

class AdminNotification(Notification):
    class Settings:
        name = "admin_notifications"
