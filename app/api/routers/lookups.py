from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Body, Depends

from app.services.lookup_service import LookupService

router = APIRouter()

_lookup_service = LookupService()


def get_lookup_service() -> LookupService:
    return _lookup_service


@router.get("/", response_model=List[str])
async def list_lookup_types(service: LookupService = Depends(get_lookup_service)) -> List[str]:
    """Return supported lookup collections."""
    return list(service.supported_types())


@router.get("/{lookup_type}", response_model=List[Dict[str, Any]])
async def list_lookup_items(lookup_type: str, service: LookupService = Depends(get_lookup_service)) -> List[Dict[str, Any]]:
    """Fetch lookup values. Accessible to explorer/operator/admin."""
    return await service.list_items(lookup_type)


@router.get("/{lookup_type}/{item_id}", response_model=Dict[str, Any])
async def get_lookup_item(lookup_type: str, item_id: str, service: LookupService = Depends(get_lookup_service)) -> Dict[str, Any]:
    """Fetch a single lookup entry. Accessible to explorer/operator/admin."""
    return await service.get_item(lookup_type, item_id)


@router.post("/{lookup_type}", response_model=Dict[str, Any], status_code=201)
async def create_lookup_item(
    lookup_type: str,
    payload: Dict[str, Any] = Body(...),
    service: LookupService = Depends(get_lookup_service),
) -> Dict[str, Any]:
    """Create a lookup entry. Intended for admin usage."""
    return await service.create_item(lookup_type, payload)


@router.put("/{lookup_type}/{item_id}", response_model=Dict[str, Any])
async def update_lookup_item(
    lookup_type: str,
    item_id: str,
    payload: Dict[str, Any] = Body(...),
    service: LookupService = Depends(get_lookup_service),
) -> Dict[str, Any]:
    """Update a lookup entry. Intended for admin usage."""
    return await service.update_item(lookup_type, item_id, payload)
