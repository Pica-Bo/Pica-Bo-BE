from typing import List, Optional

from beanie import PydanticObjectId

from app.models.experience import Experience
from app.repositories.base import BaseRepository
from app.models.experience_instance import ExperienceInstance, ExperienceInstanceStatus

from app.schemas.experience_instance import (
    ExperienceInstanceCancelSchema,
    ExperienceInstanceListingQuery,
    ExperienceInstanceCompactOutSchema,
    ExperienceInstanceUpdateSchema,
)
from datetime import datetime, date

class ExperienceInstanceRepository(BaseRepository[ExperienceInstance]):
    collection_model = "ExperienceInstance"  # Replace with actual model
    
    def _build_filters(self, query: ExperienceInstanceListingQuery) -> dict:
        q: dict = {}
        if query.experience_id:
            q["experience_id"] = query.experience_id
        if query.operator_id:
            q["operator_id"] = query.operator_id
        if query.status:
            q["status"] = query.status

        self._apply_date_filter(q, query.date_from, query.date_to)
        return q

    def _apply_date_filter(self, q: dict, date_from: Optional[datetime], date_to: Optional[datetime]) -> None:
        if date_from is None and date_to is None:
            return
        date_q: dict = {}
        if date_from is not None:
            date_q["$gte"] = date_from
        if date_to is not None:
            date_q["$lte"] = date_to
        q["date"] = date_q

    async def _query_items(self, q: dict) -> list[ExperienceInstance]:
        # use projection to return only fields required by compact schema
        projection = {
            "trip_title": 1,
            "date": 1,
            "status": 1,
            "booked_count": 1,
            "available_count": 1,
            "location": 1,
            "images": 1,
        }

        return await (
            ExperienceInstance.find(q)
            .project(projection)
            .sort("date")
            .to_list()
        )

    async def get(self, id: str) -> Optional[ExperienceInstance]:
        """Retrieve an ExperienceInstance by id. Raises HTTPException(404) if not found."""
        try:
            oid = PydanticObjectId(id)
        except Exception:
            return None

        instance = await ExperienceInstance.get(oid)
        if not instance:
            return None
        
        return instance

    async def get_by_experience_and_date(self, experience_id: str, date: date) -> Optional[ExperienceInstance]:
        """Retrieve an ExperienceInstance by experience_id and date. Raises HTTPException(404) if not found."""
        instance = await ExperienceInstance.find_one(
            {"experience_id": experience_id, "date": date}
        )
        if not instance:
            return None
        return instance

    # Note: compact payload mapping is done inline in `list` to avoid a tiny helper method.

    async def list(self, query: ExperienceInstanceListingQuery) -> list[ExperienceInstanceCompactOutSchema]:
        q = self._build_filters(query)
        items = await self._query_items(q)
        return items
    
    async def cancel_experience_instance(self, experience_instance: ExperienceInstance, reason: str, admin_id: str) -> ExperienceInstance:
        """Cancel an ExperienceInstance by an admin/internal service."""
        experience_instance.status = ExperienceInstanceStatus.CANCELLED
        experience_instance.cancellation_reason = reason
        experience_instance.cancelled_by_admin_id = admin_id
        experience_instance.cancelled_at = datetime.utcnow()
        experience_instance.updated_at = datetime.utcnow()
        await experience_instance.save()
        return experience_instance
    

    
    async def create_cancelled_instance(self, experience: Experience, data: ExperienceInstanceCancelSchema, admin_id: str) -> ExperienceInstance:
        """Create a cancelled ExperienceInstance record for an instance that does not exist."""
        instance = ExperienceInstance(
            experience_id=str(experience.id),
            operator_id=experience.operator_id,
            trip_title=experience.trip_title,
            date=data.date,
            status=ExperienceInstanceStatus.CANCELLED,
            cancellation_reason=data.reason,
            cancelled_by_admin_id=admin_id,
            cancelled_at=datetime.utcnow(),
            booked_count=0,
            available_count=0,
            location=experience.location,
            images=experience.images,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        await instance.insert()
        return instance
    
    async def update_experience_instance(self, instance: ExperienceInstance, data: ExperienceInstanceUpdateSchema) -> ExperienceInstance:
        """Update an existing ExperienceInstance with provided data."""
        data_dict = data.dict(exclude_unset=True)
        instance.set(**data_dict)
        await instance.save()
        return instance
    
    async def create_instance(self, experience: Experience, date: date) -> ExperienceInstance:
        """Create a new ExperienceInstance for the given experience and date."""
        data_dict = experience.dict(exclude_unset=True)
        data_dict.pop("id", None)  # Remove id to avoid conflicts
        instance = ExperienceInstance(
            **data_dict,
            experience_id=str(experience.id),
            date=date,
            operator_id=experience.operator_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        await instance.insert()
        return instance