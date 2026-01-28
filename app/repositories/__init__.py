from .activity_repository import ActivityRepository
from .team_repository import TeamRepository
from .team_member_repository import TeamMemberRepository
from .user_repository import UserRepository
from .operator_repository import OperatorRepository

from typing import Optional
from fastapi_cache.decorator import cache
from app.models.operator import Operator
from app.models.user import User
from app.models.explorer import Explorer


@cache(expire=300, namespace="auth:operator")
async def get_operator_id(auth_id: str) -> Optional[str]:
	op = await Operator.find_one({"authenticator_id": auth_id})
	return str(op.id) if op else None


async def get_operator_id_from_auth_id(auth_id: str) -> Optional[str]:
	"""Resolve operator.id (string) from `authenticator_id` using fastapi-cache2.

	Note: TTL is controlled by the decorator (`expire=300`); `cache_ttl` parameter is accepted for
	API compatibility but currently ignored. FastAPI app must initialize FastAPICache (Redis backend)
	at startup for caching to work.
	"""
	return await get_operator_id(auth_id)


@cache(expire=300, namespace="auth:user")
async def get_user_id(auth_id: str) -> Optional[str]:
	u = await User.find_one({"authenticator_id": auth_id})
	return str(u.id) if u else None


async def get_user_id_from_auth_id(auth_id: str) -> Optional[str]:
	"""Resolve user.id (string) from `authenticator_id` using fastapi-cache2."""
	return await get_user_id(auth_id)


@cache(expire=300, namespace="auth:explorer")
async def get_explorer_id(auth_id: str) -> Optional[str]:
	e = await Explorer.find_one({"authenticator_id": auth_id})
	return str(e.id) if e else None


async def get_explorer_id_from_auth_id(auth_id: str) -> Optional[str]:
	"""Resolve explorer.id (string) from `authenticator_id` using fastapi-cache2."""
	return await get_explorer_id(auth_id)
