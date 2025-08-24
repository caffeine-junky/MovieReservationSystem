from fastapi import APIRouter, Query
from app.models import TheatreCreate, TheatreUpdate, TheatreResponse
from app.services import TheatreServiceDep

router = APIRouter(prefix="/theatres", tags=["Theatres"])


@router.post("/", response_model=TheatreResponse, status_code=201)
async def create_theatre(payload: TheatreCreate, service: TheatreServiceDep) -> TheatreResponse:
    """Create a new theatre."""
    return await service.create_theatre(payload)


@router.get("/", response_model=list[TheatreResponse], status_code=200)
async def get_theatres(
    service: TheatreServiceDep,
    offset: int = Query(0),
    limit: int = Query(100, le=1000)
    ) -> list[TheatreResponse]:
    """Get all theatres."""
    return await service.get_all_theatres(offset, limit)


@router.get("/{theatre_id}", response_model=TheatreResponse, status_code=200)
async def get_one_theatre(
    theatre_id: int,
    service: TheatreServiceDep,
    ) -> list[TheatreResponse]:
    """Get all theatres."""
    return await service.get_all_theatres(theatre_id)


@router.put("/{theatre_id}", response_model=TheatreResponse, status_code=200)
async def update_theatre(
    theatre_id: int,
    payload: TheatreUpdate,
    service: TheatreServiceDep
) -> TheatreResponse:
    """Update an existing theatre."""
    return await service.update_theatre(theatre_id, payload)


@router.delete("/{theatre_id}", response_model=None, status_code=204)
async def delete_theatre(theatre_id: int, service: TheatreServiceDep) -> None:
    """Soft delete an existing theatre."""
    await service.delete_theatre(theatre_id)
