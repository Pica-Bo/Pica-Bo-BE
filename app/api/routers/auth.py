from fastapi import APIRouter, HTTPException, status


router = APIRouter()


@router.post('/login')
async def login():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail='Authentication is handled outside this service.',
    )
