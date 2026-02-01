from typing import Optional
from datetime import datetime, date
import pendulum
from dateutil.rrule import rrulestr

from app.repositories import get_user_id_from_auth_id, get_operator_id_from_auth_id
from app.repositories.experience_instance_repository import ExperienceInstanceRepository
from app.repositories.experience_repository import ExperienceRepository

from app.schemas.experience_instance import (
	ExperienceInstanceUpdateSchema,
	ExperienceInstanceCancelSchema,
	ExperienceInstanceOutSchema,
	ExperienceInstanceCompactOutSchema,
	ExperienceInstanceListingQuery,
	ExperienceInstanceListingResult,
)
from app.models.experience_instance import ExperienceInstance, ExperienceInstanceStatus
from app.services.base import BaseService


# async def create_experience_instance(data: ExperienceInstanceUpdateSchema) -> ExperienceInstanceOutSchema:
# 	"""Create a new ExperienceInstance from the provided schema.

# 	Implementation pending.
# 	"""
# 	raise NotImplementedError()

class ExperienceInstanceService(BaseService):
    def __init__(self):
        self.experience_instance_repository = ExperienceInstanceRepository()
        self.experience_repository = ExperienceRepository()

    def __validate_changes(self, instance: ExperienceInstance, data: ExperienceInstanceUpdateSchema) -> bool:
        """Validate if there are any changes between the instance and the update data.

        Implementation pending.
        """
        
        if data.available_seats < instance.booked_count:
            return False

        if instance.status != ExperienceInstanceStatus.cancelled and instance.booked_count == 0:
            return True
        
        return False

    async def update_experience_instance(self, experience_id: str, date: date, data: ExperienceInstanceUpdateSchema, operator_auth_id: str) -> ExperienceInstanceOutSchema:
        """Update an existing ExperienceInstance identified by `instance_id`.

        Implementation pending.
        """
        experience_instance = await self.experience_instance_repository.get_by_experience_and_date(experience_id, date)
        if not experience_instance:
            experience = await self.experience_repository.get(experience_id)
            if not experience:
                self._not_found("Experience not found")     
            experience_instance = await self.experience_instance_repository.create_instance(experience, date, operator_auth_id)

        else:
            if not self.__validate_changes(experience_instance, data):
                self._bad_request("No valid fields to update for ExperienceInstance")
            experience_instance = await self.experience_instance_repository.update_experience_instance(experience_instance, data)

        return experience_instance


    async def cancel_experience_instance(self, data: ExperienceInstanceCancelSchema, operator_auth_id: str) -> ExperienceInstanceOutSchema:
        """Cancel an ExperienceInstance with cancellation reason.

        Implementation pending.
        """
        operator_id = await get_operator_id_from_auth_id(operator_auth_id)

        experience_instance = await self.experience_instance_repository.get_by_experience_and_date(data.experience_id, data.date)
        if experience_instance and experience_instance.booked_count > 0:
            self._bad_request("Cannot cancel an ExperienceInstance with existing bookings")

        elif experience_instance is None:
            experience_instance = await self.experience_instance_repository.create_cancelled_instance(data.experience_id, data.reason, operator_id)
        else:
            experience_instance = await self.experience_instance_repository.cancel_experience_instance(experience_instance, data.cancellation_reason, None)

        return experience_instance

    async def cancel_experience_instance_by_admin(self, data: ExperienceInstanceCancelSchema, admin_auth_id: str) -> ExperienceInstanceOutSchema:
        """Cancel an ExperienceInstance by an admin/internal service.

        Implementation pending.
        """
        admin_id = await get_user_id_from_auth_id(admin_auth_id)

        experience_instance = await self.experience_instance_repository.get_by_experience_and_date(data.experience_id, data.date)
        if not experience_instance:
            experience = await self.experience_repository.get(data.experience_id)
            if not experience:
                self._not_found("Experience not found")
            experience_instance = await self.experience_instance_repository.create_cancelled_instance(experience, data, admin_id)

        elif experience_instance.status == "cancelled":
            self._bad_request("ExperienceInstance is already cancelled")

        else:
            try:
                experience_instance = await self.experience_instance_repository.cancel_experience_instance(experience_instance, data.cancellation_reason, admin_id)
            except Exception as e:
                self._internal_error(f"Failed to cancel ExperienceInstance: {str(e)}")

        return experience_instance

    async def get_experience_instance(self, instance_id: str) -> ExperienceInstanceOutSchema:
        """Retrieve a full ExperienceInstance by id and return out schema.

        Implementation pending.
        """
        instance = await self.experience_instance_repository.get(instance_id)
        return instance


    def __from_experince_to_instance(
        self,
        experiences,
        window_start: Optional[datetime] = None,
        window_end: Optional[datetime] = None,
    ) -> list[ExperienceInstance]:
        """Convert an Experience model to an ExperienceInstance model.

        Implementation pending.
        """
        # NOTE: keep this method simple: expects an iterable of experience-like objects
        # and returns a list of `ExperienceInstance` generated by their recurring patterns.
        experience_instances: list[ExperienceInstance] = []

        for experience in experiences:
            recurring_pattern = getattr(experience, "recurring_pattern", None)
            if not recurring_pattern:
                continue

            start_date = getattr(experience, "start_date", None)
            if not start_date:
                continue

            tz = getattr(experience, "timezone", "UTC") or "UTC"
            # build dtstart using pendulum to respect timezone
            try:
                start = pendulum.instance(start_date).in_timezone(tz)
            except Exception:
                # fallback to naive pendulum datetime
                start = pendulum.instance(start_date)

            rule = rrulestr(recurring_pattern, dtstart=start)

            # Determine generation window. Prefer caller-provided window; otherwise
            # default to starting at the experience start and extending 90 days.
            if window_start is not None:
                try:
                    ws = pendulum.instance(window_start).in_timezone(tz)
                except Exception:
                    ws = pendulum.instance(window_start)
            else:
                ws = start

            if window_end is not None:
                try:
                    we = pendulum.instance(window_end).in_timezone(tz)
                except Exception:
                    we = pendulum.instance(window_end)
            else:
                we = start.add(days=90)

            try:
                occurrences = list(rule.between(ws, we, inc=True))
            except Exception:
                occurrences = []

            for occ in occurrences:
                instance = ExperienceInstance(
                    experience_id=getattr(experience, "id", None) or getattr(experience, "_id", None),
                    trip_title=getattr(experience, "trip_title", None),
                    date=occ,
                    status=getattr(experience, "status", None),
                    booked_count=0,
                    available_count=getattr(experience, "available_count", None),
                    location=getattr(experience, "location", None),
                    images=getattr(experience, "images", None) or [],
                )
                experience_instances.append(instance)

        return experience_instances



    async def list_experience_instances(self, query: ExperienceInstanceListingQuery) -> ExperienceInstanceListingResult:
        """Return a paginated/filtered listing of compact experience instances.

        Implementation pending.
        """
        #1- get physical experience instances
        experience_instances = await self.experience_instance_repository.list(query)

        #2- get experience instances based on recurring patters
        experiences = await self.experience_repository.list(query)

        #3- process recurring experiences into instances (use query window if present)
        # repository returns a ListingResult for experiences; extract items if needed
        exp_items = getattr(experiences, "items", experiences)
        recurring_instances = self.__from_experince_to_instance(
            exp_items, window_start=query.date_from, window_end=query.date_to
        )

        #4- subtract physical instances from recurring instances to avoid duplicates
        # Build maps keyed by ISO timestamp to detect collisions
        def key_for(dt: datetime) -> str:
            # Recurring instances are day-based; use the UTC date as the key
            if getattr(dt, "tzinfo", None) is not None:
                return dt.astimezone(pendulum.UTC).date().isoformat()
            return pendulum.instance(dt).in_timezone(pendulum.UTC).date().isoformat()

        phys_map: dict[str, ExperienceInstanceCompactOutSchema] = {}
        for inst in experience_instances:
            # inst may already be a compact schema
            dt = getattr(inst, "date", None)
            if dt is None:
                continue
            phys_map[key_for(dt)] = inst

        final_items: list[ExperienceInstanceCompactOutSchema] = []

        # start with physical instances (they take precedence)
        for inst in experience_instances:
            final_items.append(inst)

        # add recurring instances that don't collide with physical ones
        for rec in recurring_instances:
            rec_key = key_for(getattr(rec, "date"))
            if rec_key in phys_map:
                # skip because physical instance supersedes recurring
                continue
            # convert recurring model to compact schema
            compact = await self.to_compact_schema(rec)
            final_items.append(compact)

        # return as listing result (no pagination available on query)
        total = len(final_items)
        return ExperienceInstanceListingResult(items=final_items, total=total, page=1, page_size=total)


    async def to_compact_schema(self, instance: ExperienceInstance) -> ExperienceInstanceCompactOutSchema:
        """Convert a model `ExperienceInstance` to `ExperienceInstanceCompactOutSchema`.

        Implementation pending.
        """
        # If already compact schema, return as-is
        if isinstance(instance, ExperienceInstanceCompactOutSchema):
            return instance

        data = instance.model_dump() if hasattr(instance, "model_dump") else instance.dict()
        images = data.get("images") or []
        image = images[0] if images else None

        payload = {
            "trip_title": data.get("trip_title"),
            "date": data.get("date"),
            "status": data.get("status"),
            "booked_count": data.get("booked_count", 0),
            "available_count": data.get("available_count"),
            "location": data.get("location"),
            "image": image,
        }

        if hasattr(ExperienceInstanceCompactOutSchema, "model_validate"):
            return ExperienceInstanceCompactOutSchema.model_validate(payload)
        return ExperienceInstanceCompactOutSchema(**payload)

