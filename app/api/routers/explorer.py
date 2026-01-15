from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status

from app.schemas.explorer import ExplorerCreate, ExplorerOut, ExplorerUpdate
from app.services.explorer_service import ExplorerService
from app.util.enums.enums import ExplorerStatus

router = APIRouter()

_explorer_service = ExplorerService()


def get_explorer_service() -> ExplorerService:
    return _explorer_service


@router.get("/", response_model=List[ExplorerOut])
async def list_explorers(
    status: Optional[ExplorerStatus] = Query(default=None),
    loyalty_status_code: Optional[str] = Query(default=None),
    travel_style_code: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    service: ExplorerService = Depends(get_explorer_service),
) -> List[ExplorerOut]:
    return await service.list_explorers(
        status=status,
        loyalty_status_code=loyalty_status_code,
        travel_style_code=travel_style_code,
        search=search,
    )


@router.get("/{explorer_id}", response_model=ExplorerOut)
async def get_explorer(explorer_id: str, service: ExplorerService = Depends(get_explorer_service)) -> ExplorerOut:
    return await service.get_explorer(explorer_id)


@router.post("/", response_model=ExplorerOut, status_code=status.HTTP_201_CREATED)
async def create_explorer(data: ExplorerCreate, service: ExplorerService = Depends(get_explorer_service)) -> ExplorerOut:
    return await service.create_explorer(data)


@router.put("/{explorer_id}", response_model=ExplorerOut)
async def update_explorer(
    explorer_id: str,
    data: ExplorerUpdate,
    service: ExplorerService = Depends(get_explorer_service),
) -> ExplorerOut:
    return await service.update_explorer(explorer_id, data)


@router.delete("/{explorer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def archive_explorer(explorer_id: str, service: ExplorerService = Depends(get_explorer_service)) -> None:
    await service.archive_explorer(explorer_id)
