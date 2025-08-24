from fastapi import APIRouter
from app.models import GenreCreate, GenreUpdate, GenreResponse
from app.services import GenreServiceDep

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.post("/", response_model=GenreResponse, status_code=200)
async def create_genre(payload: GenreCreate, service: GenreServiceDep) -> GenreResponse:
    """"""
    return await service.create_genre(payload)


@router.get("/{genre_id}", response_model=GenreResponse, status_code=200)
async def get_one_genre(genre_id: int, service: GenreServiceDep) -> GenreResponse:
    """"""
    return await service.get_genre(genre_id)


@router.get("/", response_model=list[GenreResponse], status_code=200)
async def get_genres(
    service: GenreServiceDep,
    offset: int = 0,
    limit: int = 100
) -> list[GenreResponse]:
    """"""
    return await service.get_all_genres(offset, limit)


@router.put("/{genre_id}", response_model=GenreResponse, status_code=200)
async def update_genre(
    genre_id: int,
    payload: GenreUpdate,
    service: GenreServiceDep
) -> GenreResponse:
    """"""
    return await service.update_genre(genre_id, payload)


@router.delete("/{genre_id}", response_model=None, status_code=204)
async def delete_genre(genre_id: int, service: GenreServiceDep) -> None:
    """"""
    await service.delete_genre(genre_id)
