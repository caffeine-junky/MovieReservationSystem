from fastapi import APIRouter, Query
from app.models import UserCreate, UserUpdate, UserResponse
from app.services import UserServiceDep

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    payload: UserCreate,
    service: UserServiceDep
) -> UserResponse:
    """Create a new user."""
    return await service.create_user(payload)


@router.get("/{user_id}", response_model=UserResponse, status_code=200)
async def get_one_user(
    user_id: int,
    service: UserServiceDep,
) -> UserResponse:
    """Get users."""
    return await service.get_one_user(user_id)


@router.get("/", response_model=list[UserResponse], status_code=200)
async def get_users(
    service: UserServiceDep,
    active_only: bool = True,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, le=1000)
) -> list[UserResponse]:
    """Get users."""
    return await service.get_all_users(active_only, offset, limit)


@router.put("/{user_id}", response_model=UserResponse, status_code=200)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserServiceDep
) -> UserResponse:
    """Update an existing user."""
    return await service.update_user(user_id, payload)


@router.delete("/{user_id}", response_model=None, status_code=204)
async def delete_user(
    user_id: int,
    service: UserServiceDep
) -> None:
    """Soft delete a user."""
    await service.delete_user(user_id)
