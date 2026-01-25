from typing import List, Optional, Annotated

from fastapi import APIRouter, Depends, status, Query

from app.schemas.operator import OperatorUpdate, OperatorListingQuery, OperatorListingResult, OperatorOut
from app.services.operator_service import OperatorService
from app.util.functions.auth import operator_auth, AuthContext
from app.util.functions.roles import require_operator


router = APIRouter()

_operator_service = OperatorService()


def get_operator_service() -> OperatorService:
	return _operator_service



from typing import Optional
from fastapi import Query

@router.get("/", response_model=OperatorListingResult, dependencies=[Depends(require_operator)])
async def list_operators(
	query: Annotated[OperatorListingQuery, Query()],
	service: OperatorService = Depends(get_operator_service),
	current_auth: AuthContext = Depends(require_operator),
) -> OperatorListingResult:
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
		verified=query.verified,
		blocked=query.blocked,
		activities_ids=query.activities_ids,
		preferred_language_ids=query.preferred_language_ids,
		page=query.page,
		page_size=query.page_size
	)


@router.get("/", response_model=OperatorOut, dependencies=[Depends(require_operator)])
async def get_operator(
	service: OperatorService = Depends(get_operator_service),
	current_auth: AuthContext = Depends(require_operator),
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
	auth_user_id = current_auth.user_id
	return await service.get_operator(auth_user_id)


@router.post("/", response_model=OperatorOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_operator)])
async def create_operator(
	service: OperatorService = Depends(get_operator_service),
	current_auth: AuthContext = Depends(require_operator),
) -> OperatorOut:
	"""
	Create a new operator profile.

	What this API does:
	-------------------
	Accepts operator details and creates a new operator profile.
	
	Authentication:
	---------------
	- Requires a valid AuthContext (JWT-based authentication).

	Authorization:
	--------------
	- Only authenticated operators are authorized to access this API.
	"""
	auth_user_id = current_auth.user_id
	name = current_auth.name
	email = current_auth.email
	return await service.create_operator(auth_user_id, name, email)

@router.put("/", response_model=OperatorOut, dependencies=[Depends(require_operator)])
async def update_operator(
	data: OperatorUpdate,
	service: OperatorService = Depends(get_operator_service),
	current_auth: AuthContext = Depends(require_operator),
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
	
	auth_user_id = current_auth.user_id
	return await service.update_operator(auth_user_id, data)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_operator)])
async def delete_operator(
	service: OperatorService = Depends(get_operator_service),
	current_auth: AuthContext = Depends(require_operator),
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
	auth_user_id = current_auth.user_id
	return await service.delete_operator(operator_id, auth_user_id)

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

