from typing import List, Optional


from fastapi import HTTPException
import pymongo
from datetime import datetime
from beanie.operators import In

from app.models.operator import Operator
from app.models.language_lookup import LanguageLookup
from app.models.activity_lookup import Activity
from app.schemas.operator import OperatorListingResult
from app.util.functions.phone import is_valid_phone
from app.repositories.base import BaseRepository
from bson import ObjectId


class OperatorRepository(BaseRepository[Operator]):

	async def _validate_language_ids(self, language_ids: list[str]):
		language_ids = [ObjectId(id) for id in language_ids]
		if language_ids:
			langs = await LanguageLookup.find(In(LanguageLookup.id, language_ids)).to_list()
			if len(langs) != len(language_ids):
				raise HTTPException(status_code=400, detail="One or more preferred_language_ids do not exist.")
		return True

	async def _validate_activity_ids(self, activity_ids: list[str]):
		activity_ids = [ObjectId(id) for id in activity_ids]
		if activity_ids:
			acts = await Activity.find(In(Activity.id, activity_ids)).to_list()
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

	async def get(self, auth_user_id: str) -> Optional[Operator]:
		return await Operator.find_one({"authenticator_id": auth_user_id})
		

	async def list(
		self,
		page: int = 1,
		page_size: int = 20,
		verified: Optional[bool] = None,
		blocked: Optional[bool] = None,
		activities_ids: Optional[List[str]] = None,
		preferred_language_ids: Optional[List[str]] = None,
	) -> OperatorListingResult:
		query = {}
		if verified is not None:
			query["verified"] = verified
		if blocked is not None:
			query["blocked"] = blocked
		if preferred_language_ids:
			query["preferred_language_ids"] = {"$in": preferred_language_ids}
		if activities_ids:
			query["activities_ids"] = {"$in": activities_ids}
		items = await Operator.find(query).skip((page - 1) * page_size).limit(page_size).to_list()
		return OperatorListingResult(items=items, total=await Operator.find(query).count(), page=page, page_size=page_size)


	async def create(self, obj: Operator) -> Operator:
		# Validate preferred_language_ids exist
		try:
			await obj.insert()
		except pymongo.errors.DuplicateKeyError as e:
			raise HTTPException(status_code=409, detail="Duplicate value for a unique field (email or authenticator_id already exists).")
		except Exception as e:
			raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
		return obj


	def is_complete(self, operator: Operator) -> bool:
		if not operator.full_name:
			return False
		
		if not operator.email:
			return False
		
		if not operator.preferred_language_ids or len(operator.preferred_language_ids) == 0:
			return False
		
		if not operator.activities_ids or len(operator.activities_ids) == 0:
			return False
		
		if not operator.phone:
			return False
		
		if not operator.country:
			return False
		
		return True
		

	async def update(self, auth_user_id: str, obj: dict) -> Optional[Operator]:
		await self._validate_update_fields(obj)
		
		operator = await Operator.find_one(Operator.authenticator_id == auth_user_id)
		if not operator:
			raise HTTPException(status_code=403, detail="Not authorized to update this operator or operator does not exist.")

		# Set updated_at to now
		obj["updated_at"] = datetime.utcnow()

		try:
			print(obj)
			await operator.set(obj)

			if self.is_complete(operator):
				operator.complete = True
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
