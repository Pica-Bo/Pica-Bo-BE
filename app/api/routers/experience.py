from fastapi import APIRouter, Depends
from typing import Optional

from app.util.functions.auth import operator_auth, internal_service_auth, AuthContext
from app.schemas.experience import (
    ExperienceCreateSchema,
    ExperienceUpdateSchema,
    ExperienceOutSchema,
    ExperienceListOutSchema,
    ExperienceListingQuery,
    RejectExperienceSchema,
)
from app.services.experience_service import ExperienceService

router = APIRouter()
service = ExperienceService()


@router.get("/", response_model=ExperienceListOutSchema, summary="List experiences")
async def list_experiences(query: ExperienceListingQuery = Depends()):
    """Return a paginated list of experiences. Supports filtering by operator, status, price and location."""
    return await service.list_experiences(query)


@router.get("/{experience_id}", response_model=ExperienceOutSchema, summary="Get experience")
async def get_experience(experience_id: str):
    """Retrieve a single experience by id."""
    return await service.get_experience(experience_id)


@router.post("/", response_model=ExperienceOutSchema, dependencies=[Depends(operator_auth)], summary="Create experience")
async def create_experience(data: ExperienceCreateSchema, current_auth: AuthContext = Depends(operator_auth)):
    """Create a new experience as the authenticated operator."""
    return await service.create_experience(data, current_auth.user_id)


@router.put("/{experience_id}", response_model=ExperienceOutSchema, dependencies=[Depends(operator_auth)], summary="Update experience")
async def update_experience(experience_id: str, data: ExperienceUpdateSchema, current_auth: AuthContext = Depends(operator_auth)):
    """Update an existing experience owned by the authenticated operator."""
    return await service.update_experience(experience_id, data, current_auth.user_id)


@router.delete("/{experience_id}", dependencies=[Depends(operator_auth)], summary="Delete experience")
async def delete_experience(experience_id: str, current_auth: AuthContext = Depends(operator_auth)):
    """Soft-delete an experience owned by the authenticated operator."""
    await service.delete_experience(experience_id, current_auth.user_id)
    return {"status": "deleted"}


@router.post("/{experience_id}/submit", response_model=ExperienceOutSchema, dependencies=[Depends(operator_auth)], summary="Submit experience")
async def submit_experience(experience_id: str, current_auth: AuthContext = Depends(operator_auth)):
    """Mark an operator's experience as submitted for review."""
    return await service.submit_experience(experience_id, current_auth.user_id)


@router.post("/{experience_id}/approve", response_model=ExperienceOutSchema, dependencies=[Depends(internal_service_auth)], summary="Approve experience")
async def approve_experience(experience_id: str, current_auth: AuthContext = Depends(internal_service_auth)):
    """Approve a submitted experience (admin/internal service)."""
    return await service.approve_experience(experience_id, current_auth.user_id)


@router.post("/{experience_id}/reject", response_model=ExperienceOutSchema, dependencies=[Depends(internal_service_auth)], summary="Reject experience")
async def reject_experience(experience_id: str, data: RejectExperienceSchema, current_auth: AuthContext = Depends(internal_service_auth)):
    """Reject a submitted experience and provide a rejection reason (admin/internal service)."""
    return await service.reject_experience(experience_id, data, current_auth.user_id)
