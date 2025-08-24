from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.database import SessionDep
from app.models import Movie, MovieCreate, MovieUpdate, MovieResponse
from app.utils.exceptions import NotImplementedException


# TODO: Implement this class
class MovieService:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    def movie_to_response(self, movie: Movie) -> MovieResponse:
        """"""
        return MovieResponse(**movie.model_dump()) # ? should probably re-implement this
    
    async def create_movie(self, payload: MovieCreate) -> MovieResponse:
        """Create a new movie."""
        raise NotImplementedException("Create movie has not been implemented yet.")

    async def get_one_movie(self, movie_id: int) -> MovieResponse:
        """Get one movie by its ID."""
        raise NotImplementedException("Get one movie has not been implemented yet.")

    async def get_all_movies(self, offset: int = 0, limit: int = 100) -> list[MovieResponse]:
        """Get all movies in the database."""
        raise NotImplementedException("Get all movies has not been implemented yet.")

    async def update_movie(self, movie_id: int, payload: MovieUpdate) -> MovieResponse:
        """Update an existing movie."""
        raise NotImplementedException("Update movie has not been implemented yet.")

    async def delete_movie(self, movie_id: int) -> None:
        """Soft delete a movie."""
        raise NotImplementedException("Delete movie has not been implemented yet.")


def get_movie_service(session: SessionDep) -> MovieService:
    """"""
    return MovieService(session)


MovieServiceDep = Annotated[MovieService, Depends(get_movie_service)]
