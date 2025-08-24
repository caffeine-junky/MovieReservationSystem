from fastapi import APIRouter, Query
from app.services import MovieServiceDep
from app.models import MovieCreate, MovieUpdate, MovieResponse

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.post("/", response_model=MovieResponse, status_code=201)
async def create_movie(payload: MovieCreate, service: MovieServiceDep) -> MovieResponse:
    """Create a new movie."""
    return await service.create_movie(payload)


@router.get("/", response_model=list[MovieResponse], status_code=200)
async def get_all_movies(
    service: MovieServiceDep,
    offset: int = Query(0),
    limit: int = Query(100, le=1000)
) -> list[MovieResponse]:
    """Get all movies in the database (limit is 1000)"""
    return await service.get_all_movies(offset, limit)


@router.get("/{movie_id}", response_model=MovieResponse, status_code=200)
async def get_one_movie(movie_id: int, service: MovieServiceDep) -> MovieResponse:
    """Get one movie by its ID."""
    return await service.get_one_movie(movie_id)


@router.put("/{movie_id}", response_model=MovieResponse, status_code=200)
async def update_movie(
    movie_id: int,
    payload: MovieUpdate,
    service: MovieServiceDep
) -> MovieResponse:
    """Update an existing movie"""
    return await service.update_movie(movie_id, payload)


@router.delete("/{movie_id}", response_model=None, status_code=204)
async def delete_movie(movie_id: int, service: MovieServiceDep) -> None:
    """Soft delete an existing movie."""
    await service.delete_movie(movie_id)
