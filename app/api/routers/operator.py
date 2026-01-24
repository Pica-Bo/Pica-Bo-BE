from typing import List

from fastapi import APIRouter, Depends, status

from app.schemas.operator import OperatorCreate, OperatorUpdate, OperatorOut
from app.services.operator_service import OperatorService
from app.util.functions.auth import operator_auth, AuthContext


router = APIRouter()

_operator_service = OperatorService()


def get_operator_service() -> OperatorService:
	return _operator_service



from typing import Optional
from fastapi import Query

# @router.get("/", response_model=List[OperatorOut], dependencies=[Depends(operator_auth)])
@router.get("/", response_model=List[OperatorOut], dependencies=[])
async def list_operators(
	verified: Optional[bool] = Query(None, description="Filter by verified status (True/False)"),
	blocked: Optional[bool] = Query(None, description="Filter by blocked status (True/False)"),
	activities: Optional[List[str]] = Query(None, description="Filter by activity IDs (list of strings)"),
	languages: Optional[List[str]] = Query(None, description="Filter by preferred language IDs (list of strings)"),
	service: OperatorService = Depends(get_operator_service),
	# current_auth: AuthContext = Depends(operator_auth),
) -> List[OperatorOut]:
	"""
	List all operator profiles.

	What this API does:
	-------------------
	Returns all operators, optionally filtered by:
	  - verified: Only operators with this verified status.
	  - blocked: Only operators with this blocked status.
	  - activities: Only operators associated with any of these activity IDs.
	  - languages: Only operators whose preferred language matches any of these IDs.

	Filters:
	--------
	- verified: bool (optional) — Filter by verification status.
	- blocked: bool (optional) — Filter by blocked status.
	- activities: List[str] (optional) — Filter by activity IDs.
	- languages: List[str] (optional) — Filter by preferred language IDs.

	Authentication:
	---------------
	- Requires a valid AuthContext (JWT-based authentication).

	Authorization:
	--------------
	- Only authenticated operators are authorized to access this API.
	"""
	return await service.list_operators(
		 verified=verified,
		 blocked=blocked,
		 activities=activities,
		 languages=languages
	)


@router.get("/{operator_id}", response_model=OperatorOut, dependencies=[Depends(operator_auth)])
async def get_operator(
	operator_id: str,
	service: OperatorService = Depends(get_operator_service),
	current_auth: AuthContext = Depends(operator_auth),
) -> OperatorOut:
	"""
	Get a single operator profile by ID.

	What this API does:
	-------------------
	Returns the operator profile for the given operator_id.

	Path Variables:
	--------------
	- operator_id: str — The unique identifier of the operator to retrieve.

	Authentication:
	---------------
	- Requires a valid AuthContext (JWT-based authentication).

	Authorization:
	--------------
	- Only authenticated operators are authorized to access this API.
	"""
	return await service.get_operator(operator_id)


@router.post("/", response_model=OperatorOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(operator_auth)])
async def create_operator(
	data: OperatorCreate,
	service: OperatorService = Depends(get_operator_service),
	current_auth: AuthContext = Depends(operator_auth),
) -> OperatorOut:
	"""
	Create a new operator profile.

	What this API does:
	-------------------
	Accepts operator details and creates a new operator profile.

	Body:
	-----
	- data: OperatorCreate — The operator information to create (email, authenticator_id, etc.).

	Authentication:
	---------------
	- Requires a valid AuthContext (JWT-based authentication).

	Authorization:
	--------------
	- Only authenticated operators are authorized to access this API.
	"""
	return await service.create_operator(data)


@router.put("/{operator_id}", response_model=OperatorOut, dependencies=[Depends(operator_auth)])
async def update_operator(
	operator_id: str,
	data: OperatorUpdate,
	service: OperatorService = Depends(get_operator_service),
	current_auth: AuthContext = Depends(operator_auth),
) -> OperatorOut:
	"""
	Update an existing operator profile.

	What this API does:
	-------------------
	Updates the operator profile for the given operator_id with the provided data.

	Path Variables:
	--------------
	- operator_id: str — The unique identifier of the operator to update.

	Body:
	-----
	- data: OperatorUpdate — The fields to update for the operator.

	Authentication:
	---------------
	- Requires a valid AuthContext (JWT-based authentication).

	Authorization:
	--------------
	- Only the operator themselves or an admin is authorized to update this operator profile.
	"""
	return await service.update_operator(operator_id, data)


@router.delete("/{operator_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(operator_auth)])
async def delete_operator(
	operator_id: str,
	service: OperatorService = Depends(get_operator_service),
	current_auth: AuthContext = Depends(operator_auth),
) -> None:
	"""
	Delete an operator profile by ID.

	What this API does:
	-------------------
	Deletes the operator profile for the given operator_id.

	Path Variables:
	--------------
	- operator_id: str — The unique identifier of the operator to delete.

	Authentication:
	---------------
	- Requires a valid AuthContext (JWT-based authentication).

	Authorization:
	--------------
	- Only the operator themselves or an admin is authorized to delete this operator profile.
	"""
	return await service.delete_operator(operator_id)

# async def verify_operator(
# 	operator_id: str,
# 	service: OperatorService = Depends(get_operator_service),
# 	current_auth: AuthContext = Depends(operator_auth),
# ) -> None:
# 	return await service.verify_operator(operator_id)

# async def block_operator(
# 	operator_id: str,
# 	service: OperatorService = Depends(get_operator_service),
# 	current_auth: AuthContext = Depends(operator_auth),
# ) -> None:
# 	return await service.block_operator(operator_id)

# async def unblock_operator(
# 	operator_id: str,
# 	service: OperatorService = Depends(get_operator_service),
# 	current_auth: AuthContext = Depends(operator_auth),
# ) -> None:
# 	return await service.unblock_operator(operator_id)

# async def upload_operator_document(
# 	operator_id: str,
# 	document_type: str,
# 	file: bytes,
# 	service: OperatorService = Depends(get_operator_service),
# 	current_auth: AuthContext = Depends(operator_auth),
# ) -> None:
# 	return await service.upload_operator_document(operator_id, document_type, file)

# async def list_operator_documents(
# 	operator_id: str,
# 	service: OperatorService = Depends(get_operator_service),
# 	current_auth: AuthContext = Depends(operator_auth),
# ) -> List[str]:
# 	return await service.list_operator_documents(operator_id)

# async def delete_operator_document(
# 	operator_id: str,
# 	document_id: str,
# 	service: OperatorService = Depends(get_operator_service),
# 	current_auth: AuthContext = Depends(operator_auth),
# ) -> None:
# 	return await service.delete_operator_document(operator_id, document_id)

