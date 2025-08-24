from fastapi import Depends
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from app.database import SessionDep
from app.models import Theatre, TheatreCreate, TheatreUpdate, TheatreResponse
from app.utils.exceptions import NotFoundException, EntityExistsException, ServerError


class TheatreService:

    def __init__(self, session: Session) -> None:
        self._session = session
    
    def theatre_to_response(self, theatre: Theatre) -> TheatreResponse:
        """Convert theatre db model to response."""
        auditorium_names: list[str] = [a.name for a in theatre.auditoriums]
        return TheatreResponse(**theatre.model_dump(), auditorium_names=auditorium_names)
    
    async def create_theatre(self, payload: TheatreCreate) -> TheatreResponse:
        """Create a new theatre."""
        try:
            theatre = Theatre(**payload.model_dump())
            self._session.add(theatre)
            self._session.commit()
            self._session.refresh(theatre)
            return self.theatre_to_response(theatre)
        except IntegrityError:
            raise EntityExistsException("Theatre already exists.")
        except Exception as e:
            raise ServerError(f"Failed to create theatre: {e}")

    async def get_one_theatre(self, theatre_id: int) -> TheatreResponse:
        """Get one theatre by its ID."""
        theatre: Theatre | None = self._session.get(Theatre, theatre_id)
        if not theatre:
            raise NotFoundException("Theatre not found.")
        return self.theatre_to_response(theatre)
    
    async def get_all_theatres(
        self,
        offset: int = 0,
        limit: int = 0
        ) -> list[TheatreResponse]:
        """Get all theatres."""
        statement = select(Theatre).offset(offset).limit(limit)
        theatres = self._session.exec(statement).all()
        return [self.theatre_to_response(theatre) for theatre in theatres]
    
    async def update_theatre(self, theatre_id: int, payload: TheatreUpdate) -> TheatreResponse:
        """Update an existing theatre."""
        theatre: Theatre | None = self._session.get(Theatre, theatre_id)
        if not theatre:
            raise NotFoundException("Theatre not found.")
        
        data = payload.model_dump(exclude_unset=True, exclude_defaults=True, exclude_none=True)
        updated = False

        for key, value in data.items():
            setattr(theatre, key, value)
            updated = True
        
        if updated:
            theatre.touch()
            self._session.commit()
            self._session.refresh(theatre)
        
        return self.theatre_to_response(theatre)
    
    async def delete_theatre(self, theatre_id: int) -> None:
        """Soft delete a theatre."""
        theatre: Theatre | None = self._session.get(Theatre, theatre_id)
        if not theatre:
            raise NotFoundException("Theatre not found.")
        theatre.soft_delete()
        self._session.commit()


def get_theatre_service(session: SessionDep) -> TheatreService:
    """"""
    return TheatreService(session)


TheatreServiceDep = Annotated[TheatreService, Depends(get_theatre_service)]
