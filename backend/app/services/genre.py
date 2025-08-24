from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionDep
from app.models import Genre, GenreCreate, GenreUpdate, GenreResponse
from app.utils.exceptions import NotFoundException


class GenreService:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    def genre_to_response(self, genre: Genre) -> GenreResponse:
        """"""
        return GenreResponse(**genre.model_dump())
    
    async def create_genre(self, payload: GenreCreate) -> GenreResponse:
        """"""
        try:
            genre = Genre(**payload.model_dump())
            self._session.add(genre)
            await self._session.commit()
            await self._session.refresh(genre)
            return self.genre_to_response(genre)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Genre already exists")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_genre(self, genre_id: int) -> GenreResponse:
        """"""
        genre: Genre | None = await self._session.get(Genre, genre_id)
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")
        return self.genre_to_response(genre)
    
    async def get_all_genres(self, offset: int = 0, limit: int = 100) -> list[GenreResponse]:
        """"""
        statement = select(Genre).offset(offset).limit(limit)
        results = (await self._session.execute(statement)).scalars().all()
        return [self.genre_to_response(genre) for genre in results]
    
    async def update_genre(self, genre_id: int, payload: GenreUpdate) -> GenreResponse:
        """"""
        genre: Genre | None = await self._session.get(Genre, genre_id)
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")
        updated = False

        for key, value in payload.model_dump(exclude_defaults=True, exclude_unset=True, exclude_none=True).items():
            setattr(genre, key, value)
            updated = True
        
        if updated:
            genre.touch()
            await self._session.commit()
            await self._session.refresh(genre)
        
        return self.genre_to_response(genre)
    
    async def delete_genre(self, genre_id: int) -> None:
        """"""
        genre: Genre | None = await self._session.get(Genre, genre_id)
        if not genre:
            raise NotFoundException("Genre not found")
        genre.soft_delete()
        await self._session.commit()


def get_genre_service(session: SessionDep) -> GenreService:
    """"""
    return GenreService(session)


GenreServiceDep = Annotated[GenreService, Depends(get_genre_service)]
