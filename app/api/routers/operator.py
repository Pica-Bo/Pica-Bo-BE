from typing import List

from fastapi import APIRouter, Depends, status

from app.schemas.operator import OperatorCreate, OperatorUpdate, OperatorOut
from app.services.operator_service import OperatorService


router = APIRouter()

_operator_service = OperatorService()


def get_operator_service() -> OperatorService:
	return _operator_service


@router.get("/", response_model=List[OperatorOut])
async def list_operators(service: OperatorService = Depends(get_operator_service)) -> List[OperatorOut]:
	return await service.list_operators()


@router.get("/{operator_id}", response_model=OperatorOut)
async def get_operator(operator_id: str, service: OperatorService = Depends(get_operator_service)) -> OperatorOut:
	return await service.get_operator(operator_id)


@router.post("/", response_model=OperatorOut, status_code=status.HTTP_201_CREATED)
async def create_operator(data: OperatorCreate, service: OperatorService = Depends(get_operator_service)) -> OperatorOut:
	return await service.create_operator(data)


@router.put("/{operator_id}", response_model=OperatorOut)
async def update_operator(operator_id: str, data: OperatorUpdate, service: OperatorService = Depends(get_operator_service)) -> OperatorOut:
	return await service.update_operator(operator_id, data)


@router.delete("/{operator_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_operator(operator_id: str, service: OperatorService = Depends(get_operator_service)) -> None:
	await service.delete_operator(operator_id)
