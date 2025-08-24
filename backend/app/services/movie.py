from fastapi import Depends
from sqlmodel import Session, select
from typing import Annotated
from app.database import SessionDep
from app.models import Movie, MovieCreate, MovieUpdate, MovieResponse, Genre
from app.utils.exceptions import NotFoundException


class MovieService:

    def __init__(self, session: Session) -> None:
        self._session = session
    
    def movie_to_response(self, movie: Movie) -> MovieResponse:
        """"""
        return MovieResponse(
            **movie.model_dump(),
            genre_names=[g.name for g in movie.genres]
            )
    
    async def create_movie(self, payload: MovieCreate) -> MovieResponse:
        """Create a new movie."""
        statement = select(Genre).where(Genre.id.in_(payload.genre_ids)) # type: ignore
        genres = self._session.exec(statement).all()
        
        movie = Movie(**payload.model_dump(exclude={"genre_ids"}), genres=list(genres))
        self._session.add(movie)
        self._session.commit()
        self._session.refresh(movie)
        
        return self.movie_to_response(movie)

    async def get_one_movie(self, movie_id: int) -> MovieResponse:
        """Get one movie by its ID."""
        movie: Movie | None = self._session.get(Movie, movie_id)
        if not movie:
            raise NotFoundException("Movie not found")
        return self.movie_to_response(movie)

    async def get_all_movies(self, offset: int = 0, limit: int = 100) -> list[MovieResponse]:
        """Get all movies in the database."""
        statement = select(Movie).offset(offset).limit(limit)
        movies = self._session.exec(statement).all()
        return [self.movie_to_response(movie) for movie in movies]

    def update_movie(self, movie_id: int, payload: MovieUpdate) -> MovieResponse:
        """Update an existing movie."""
        movie: Movie | None = self._session.get(Movie, movie_id)
        if not movie:
            raise NotFoundException("Movie not found")

        data = payload.model_dump(exclude_unset=True, exclude_defaults=True, exclude_none=True)

        # Handle genres
        if "genre_ids" in data:
            statement = select(Genre).where(Genre.id.in_(data["genre_ids"])) # type: ignore
            genres = self._session.exec(statement).all()
            movie.genres = list(genres)
            del data["genre_ids"]

        for key, value in data.items():
            setattr(movie, key, value)

        # Touch + persist
        movie.touch()
        self._session.commit()
        self._session.refresh(movie)

        return self.movie_to_response(movie)

    async def delete_movie(self, movie_id: int) -> None:
        """Soft delete a movie."""
        movie: Movie | None = self._session.get(Movie, movie_id)
        if not movie:
            raise NotFoundException("Movie not found")
        movie.soft_delete()


def get_movie_service(session: SessionDep) -> MovieService:
    """"""
    return MovieService(session)


MovieServiceDep = Annotated[MovieService, Depends(get_movie_service)]
