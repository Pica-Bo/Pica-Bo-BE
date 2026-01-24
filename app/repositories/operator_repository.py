from typing import List, Optional


from fastapi import HTTPException
import pymongo
from beanie import PydanticObjectId

from app.models.operator import Operator
from app.models.language_lookup import LanguageLookup
from app.models.activity_lookup import Activity
from app.util.functions.phone import is_valid_phone
from app.repositories.base import BaseRepository


class OperatorRepository(BaseRepository[Operator]):

	async def _validate_language_ids(self, language_ids: list[str]):
		if language_ids:
			langs = await LanguageLookup.find(LanguageLookup.code.in_(language_ids)).to_list()
			if len(langs) != len(language_ids):
				raise HTTPException(status_code=400, detail="One or more preferred_language_ids do not exist.")
		return True

	async def _validate_activity_ids(self, activity_ids: list[str]):
		if activity_ids:
			acts = await Activity.find(Activity.id.in_(activity_ids)).to_list()
			if len(acts) != len(activity_ids):
				raise HTTPException(status_code=400, detail="One or more activities_ids do not exist.")
		return True

	def _validate_phone(self, phone: str):
		if phone and not is_valid_phone(phone):
			raise HTTPException(status_code=400, detail="Invalid phone number format.")

	async def _validate_update_fields(self, obj: dict):
		# Validate preferred_language_ids exist (all or none)
		if "preferred_language_ids" in obj and obj["preferred_language_ids"]:
			await self._validate_language_ids(obj["preferred_language_ids"])

		# Validate activities_ids exist (all or none)
		if "activities_ids" in obj and obj["activities_ids"]:
			await self._validate_activity_ids(obj["activities_ids"])

		# Validate phone format
		if "phone" in obj:
			self._validate_phone(obj["phone"])

	async def get(self, id: str) -> Optional[Operator]:
		return await Operator.get(PydanticObjectId(id))

	async def list(
		self,
		verified: Optional[bool] = None,
		blocked: Optional[bool] = None,
		activities_ids: Optional[List[str]] = None,
		preferred_language_ids: Optional[List[str]] = None,
	) -> List[Operator]:
		query = {}
		if verified is not None:
			query["verified"] = verified
		if blocked is not None:
			query["blocked"] = blocked
		if preferred_language_ids:
			query["preferred_language_ids"] = {"$in": preferred_language_ids}
		if activities_ids:
			query["activities_ids"] = {"$in": activities_ids}
		return await Operator.find(query).to_list()


	async def create(self, obj: Operator) -> Operator:
		# Validate preferred_language_ids exist
		try:
			await obj.insert()
		except pymongo.errors.DuplicateKeyError as e:
			raise HTTPException(status_code=409, detail="Duplicate value for a unique field (email or authenticator_id already exists).")
		except Exception as e:
			raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
		return obj


	async def update(self, id: str, obj: dict) -> Optional[Operator]:
		operator = await self.get(id)
		if not operator:
			raise HTTPException(status_code=403, detail="Not authorized to update this operator or operator does not exist.")

		await self._validate_update_fields(obj)

		try:
			await operator.set(obj)
			await operator.save()
		except pymongo.errors.DuplicateKeyError:
			raise HTTPException(status_code=409, detail="Duplicate value for a unique field (email or authenticator_id already exists).")
		except Exception as e:
			raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
		return operator

	async def delete(self, id: str) -> None:
		operator = await self.get(id)
		if operator:
			await operator.delete()
