from typing import List, Optional

from beanie import PydanticObjectId

from app.models.experience import Experience, ExperienceStatus
from app.repositories.base import BaseRepository
from app.schemas.experience import ExperienceListingQuery, ExperienceListOutSchema
from beanie import PydanticObjectId
from datetime import datetime
import pymongo
from fastapi import HTTPException
import pymongo
from fastapi import HTTPException

class ExperienceRepository(BaseRepository[Experience]):
    async def get(self, id:str) -> Optional[Experience]:
        oid = PydanticObjectId(id)
        experience = await Experience.get(oid)
        return experience
    
    async def get(self, id: str, operator_id: Optional[str] = None) -> Optional[Experience]:
        """Retrieve an Experience by id.

        If `operator_id` is provided, verify that the experience's `operator_id` matches.
        Raises HTTPException(404) when not found and HTTPException(403) when ownership doesn't match.
        """
        oid = PydanticObjectId(id)

        experience = await Experience.get(oid)
        if not experience:
            raise HTTPException(status_code=404, detail="Experience not found")

        if operator_id is not None:
            if not experience.operator_id or str(experience.operator_id) != str(operator_id):
                raise HTTPException(status_code=403, detail="Not owner of this experience")

        return experience

    async def list(self, query: ExperienceListingQuery) -> ExperienceListOutSchema:
        # Build query and paginate
        q: dict = self._build_query(query)
        page = query.page
        page_size = query.page_size

        # Project compact fields to match ExperienceCompactOutSchema
        projection = {
            "trip_title": 1,
            "short_description": 1,
            "images": 1,
            "price_per_person": 1,
            "location": 1,
            "status": 1,
            "recurring_pattern": 1,
        }

        items = await (
            Experience.find(q)
            .project(projection)
            .skip((page - 1) * page_size)
            .limit(page_size)
            .to_list()
        )
        total = await Experience.find(q).count()
        return ExperienceListOutSchema(items=items, total=total, page=page, page_size=page_size)

    def _build_query(self, query: ExperienceListingQuery) -> dict:
        q: dict = {}
        if query.operator_id:
            q["operator_id"] = query.operator_id

        if query.__getattribute__("experience_id"):
            q["_id"] = query.experience_id

        if query.status:
            q["status"] = query.status

        if query.activity_ids:
            q["activity_id"] = {"$in": query.activity_ids}

        # apply price filter
        self._add_price_filter(q, query.price_min, query.price_max)

        # apply location filter
        self._add_location_filter(q, query.location)

        self._add_date_filter(q, query.date_from, query.date_to)

        return q

    def _add_price_filter(self, q: dict, price_min: Optional[float], price_max: Optional[float]) -> None:
        if price_min is None and price_max is None:
            return
        price_q: dict = {}
        if price_min is not None:
            price_q["$gte"] = price_min
        if price_max is not None:
            price_q["$lte"] = price_max
        q["price_per_person"] = price_q

    def _add_location_filter(self, q: dict, location) -> None:
        if not location or not getattr(location, "coordinates", None):
            return
        coords = location.coordinates
        if isinstance(coords, (list, tuple)) and len(coords) == 2:
            q["location"] = {
                "$near": {
                    "$geometry": {"type": "Point", "coordinates": coords},
                    # default to 50km radius
                    "$maxDistance": 50000,
                }
            }

    def _add_date_filter(self, q: dict, date_from: Optional[datetime], date_to: Optional[datetime]) -> None:
        if date_from is not None:
            q["start_date"] = {"$gte": date_from}

        if date_to is not None:
            q["end_date"] = {"$lte": date_to}

        return q

    async def create(self, obj: Experience) -> Experience:
        try:
            await obj.insert()
        except pymongo.errors.DuplicateKeyError:
            raise HTTPException(status_code=409, detail="Duplicate value for a unique field.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
        return obj

    async def update(self, id: str, obj: dict) -> Experience:
        experience = await self.get(id)
        if not experience:
            return None

        # set updated_at
        obj["updated_at"] = datetime.utcnow()
        try:
            await experience.set(obj)
            await experience.save()
        except pymongo.errors.DuplicateKeyError:
            raise HTTPException(status_code=409, detail="Duplicate value for a unique field.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
        return experience

    async def change_status(self, id: str, new_status: ExperienceStatus = ExperienceStatus.SUBMITTED) -> Optional[Experience]:
        """Set the experience status to `new_status` and save. Returns updated Experience or None."""
        experience = await self.get(id)
        if not experience:
            return None

        experience.status = new_status
        experience.updated_at = datetime.utcnow()
        try:
            await experience.save()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
        return experience

    async def reject(self, id: str, reason: str, admin_auth_id: Optional[str] = None) -> Optional[Experience]:
        """Mark an experience as rejected, persist the rejection reason and record the admin auth id."""
        experience = await self.get(id)
        if not experience:
            return None

        experience.status = ExperienceStatus.REJECTED
        experience.rejection_reason = reason
        experience.rejected_by = admin_auth_id
        experience.updated_at = datetime.utcnow()
        try:
            await experience.save()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
        return experience

    async def delete(self, id: str) -> None:
        # Soft delete: mark as archived
        await self.change_status(id, ExperienceStatus.ARCHIVED)