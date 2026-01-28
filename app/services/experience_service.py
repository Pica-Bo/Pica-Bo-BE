from typing import List

from app.models.experience import Experience, ExperienceStatus
from datetime import datetime
from app.repositories.experience_repository import ExperienceRepository
from app.repositories import get_operator_id_from_auth_id, get_user_id_from_auth_id
from app.schemas.experience import (
	ExperienceCreateSchema,
	ExperienceUpdateSchema,
	ExperienceOutSchema,
	ExperienceListOutSchema,
	ExperienceListingQuery,
	RejectExperienceSchema,
)
from app.services.base import BaseService


class ExperienceService(BaseService):
	def __init__(self, repository: ExperienceRepository | None = None) -> None:
		self.repository = repository or ExperienceRepository()

	async def list_experiences(self, query: ExperienceListingQuery) -> ExperienceListOutSchema:
		result = await self.repository.list(query)
		return result

	async def get_experience(self, experience_id: str) -> ExperienceOutSchema:
		experience = await self.repository.get(experience_id)
		if not experience:
			self._not_found("Experience")
		return self._to_schema(experience)

	async def create_experience(self, data: ExperienceCreateSchema, auth_id: str) -> ExperienceOutSchema:
		# Build Experience model from input schema
		payload = data.model_dump() if hasattr(data, "model_dump") else data.dict()
		experience = Experience(**payload)

		# Resolve operator ownership from auth_id
		operator_id = await get_operator_id_from_auth_id(auth_id)
		if not operator_id:
			self._unauthorized("Invalid operator authentication")
		experience.operator_id = operator_id

		# Mark as complete if all required fields are present
		if self._is_complete_experience(experience):
			experience.complete = True

		created = await self.repository.create(experience)
		return self._to_schema(created)

	async def update_experience(self, experience_id: str, data: ExperienceUpdateSchema, auth_id: str) -> ExperienceOutSchema:
		# Ensure caller owns the experience
		operator_id = await get_operator_id_from_auth_id(auth_id)
		if not operator_id:
			self._unauthorized("Invalid operator authentication")
		existing = await self.repository.get(experience_id, operator_id=operator_id)
		if not existing:
			self._not_found("Experience")

		# prepare update dict from pydantic schema (exclude unset)
		update_data = {}
		if hasattr(data, "model_dump"):
			update_data = data.model_dump(exclude_unset=True)
		else:
			update_data = data.dict(exclude_unset=True)

		updated = await self.repository.update(experience_id, update_data)
		if not updated:
			self._not_found("Experience")

		# Re-evaluate completeness and persist if changed
		is_complete = self._is_complete_experience(updated)
		if getattr(updated, "complete", False) != is_complete:
			updated = await self.repository.update(experience_id, {"complete": is_complete})

		return self._to_schema(updated)

	async def delete_experience(self, experience_id: str, auth_id: str) -> None:
		operator_id = await get_operator_id_from_auth_id(auth_id)
		if not operator_id:
			self._unauthorized("Invalid operator authentication")
		experience = await self.repository.get(experience_id, operator_id=operator_id)
		if not experience:
			self._not_found("Experience")
		# Soft delete via repository
		await self.repository.delete(experience_id)

	async def submit_experience(self, experience_id: str, auth_id: str) -> ExperienceOutSchema:
		operator_id = await get_operator_id_from_auth_id(auth_id)
		if not operator_id:
			self._unauthorized("Invalid operator authentication")
		experience = await self.repository.get(experience_id, operator_id=operator_id)
		if not experience:
			self._not_found("Experience")

		# Ensure experience is marked complete before submission
		if not experience.complete:
			self._bad_request("Experience is not complete")

		# perform status transition via repository submit method
		updated = await self.repository.change_status(experience_id, ExperienceStatus.SUBMITTED)
		if not updated:
			self._not_found("Experience")
		return self._to_schema(updated)

	async def approve_experience(self, experience_id: str, auth_id: str) -> ExperienceOutSchema:
		operator_id = await get_operator_id_from_auth_id(auth_id)
		if not operator_id:
			self._unauthorized("Invalid operator authentication")
		experience = await self.repository.get(experience_id, operator_id=operator_id)
		if not experience:
			self._not_found("Experience")

		# Only submitted experiences can be approved
		if experience.status != ExperienceStatus.SUBMITTED:
			self._bad_request("Only submitted experiences can be approved")

		updated = await self.repository.change_status(experience_id, ExperienceStatus.PUBLISHED)
		if not updated:
			self._not_found("Experience")
		return self._to_schema(updated)

	async def reject_experience(self, experience_id: str, data: RejectExperienceSchema, admin_auth_id: str | None = None) -> ExperienceOutSchema:
		existing = await self.repository.get(experience_id)
		if not existing:
			self._not_found("Experience")

		# extract reason from schema
		if hasattr(data, "model_dump"):
			reason = data.model_dump().get("rejection_reason")
		else:
			reason = data.dict().get("rejection_reason")

		# resolve admin_auth_id to internal User.id via cache and record who rejected
		admin_user_id = None
		if admin_auth_id:
			admin_user_id = await get_user_id_from_auth_id(admin_auth_id)
			if not admin_user_id:
				self._unauthorized("Invalid admin authentication")

		# update status and rejection reason via repository.reject, recording admin user id
		updated = await self.repository.reject(experience_id, reason, admin_user_id)
		if not updated:
			self._not_found("Experience")
		return self._to_schema(updated)

	def _to_schema(self, experience: Experience) -> ExperienceOutSchema:
		data = experience.model_dump() if hasattr(experience, "model_dump") else experience.dict()
		# Prefer pydantic v2 model_validate if available
		if hasattr(ExperienceOutSchema, "model_validate"):
			return ExperienceOutSchema.model_validate(data)
		return ExperienceOutSchema(**data)

	def _is_complete_experience(self, experience: Experience) -> bool:
		# Basic completeness rules: required public-facing fields present
		if not experience.trip_title:
			return False
		# Must have either short description or at least one image
		if not experience.short_description and (not experience.images or len(experience.images) == 0):
			return False
		# Price should be specified
		if experience.price_per_person is None:
			return False
		# Location and activity
		if experience.location is None:
			return False
		if not experience.languages or len(experience.languages) == 0:
			return False
		return True

    
