from enum import Enum

class TeamRole(str, Enum):
    owner = "owner"
    admin = "admin"
    guide = "guide"
    ops = "ops"


class TeamMemberStatus(str, Enum):
    invited = "invited"
    active = "active"
    suspended = "suspended"


class TeamVerificationStatus(str, Enum):
    unverified = "unverified"
    pending = "pending"
    verified = "verified"
