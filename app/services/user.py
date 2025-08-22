from fastapi import Depends
from typing import Annotated
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, UserCreate, UserUpdate, UserResponse
from app.database import SessionDep
from app.core import SecurityUtils
from app.utils.exceptions import (
    UserNotFoundException,
    UserExistsException,
    InvalidCredentialsExeception
)


class UserService:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    def user_to_response(self, user: User) -> UserResponse:
        """Converts a db user to a response model."""
        return UserResponse(**user.model_dump(exclude={"hashed_password"}))
    
    async def check_user_exists(self, username: str, email: str) -> None:
        """Checks if a user exists."""
        statement = select(User).where(User.username == username)
        result = await self._session.execute(statement)
        user: User | None = result.scalar_one_or_none()

        if user:
            raise UserExistsException("username")
        
        statement = select(User).where(User.email == email)
        result = await self._session.execute(statement)
        user: User | None = result.scalar_one_or_none()

        if user:
            raise UserExistsException("email")
    
    async def create_user(self, payload: UserCreate) -> UserResponse:
        """"""
        await self.check_user_exists(payload.username, payload.email)
        
        user = User(
            hashed_password=SecurityUtils.hash_password(payload.password),
            **payload.model_dump(exclude={"password"})
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)

        return self.user_to_response(user)
    
    async def get_one_user(self, user_id: int) -> UserResponse:
        """Get one user by their unique id."""
        user: User | None = await self._session.get(User, user_id)
        if not user:
            raise UserNotFoundException()
        return self.user_to_response(user)
    
    async def get_all_users(
        self,
        active_only: bool = True,
        offset: int = 0,
        limit: int = 100
        ) -> list[UserResponse]:
        """Get all users."""
        statement = select(User)
        if active_only:
            statement = statement.where(User.is_active == True)
        statement = statement.offset(offset).limit(limit)

        users = (await self._session.execute(statement)).scalars().all()
        return [self.user_to_response(user) for user in users]
    
    async def update_user(self, user_id: int, payload: UserUpdate) -> UserResponse:
        """Update an existing user."""
        user: User | None = await self._session.get(User, user_id)
        if not user:
            raise UserNotFoundException()
        updated = False
        
        for key, value in payload.model_dump(exclude_unset=True, exclude_defaults=True, exclude_none=True).items():
            setattr(user, key, value)
            updated = True
        
        if updated:
            user.touch()
        
            await self._session.commit()
            await self._session.refresh(user)

        return self.user_to_response(user)

    async def delete_user(self, user_id: int) -> None:
        """"""
        user: User | None = await self._session.get(User, user_id)
        if not user:
            raise UserNotFoundException()
        user.is_active = False
        await self._session.commit()

    async def authenticate(self, username: str, password: str) -> User:
        """"""
        statement = select(User).where(User.username == username)
        user: User | None = (await self._session.execute(statement)).scalar_one_or_none()
        if (not user) or (not SecurityUtils.verify_password(password, user.hashed_password)):
            raise InvalidCredentialsExeception("Invalid credentials")
        return user


def get_user_service(session: SessionDep) -> UserService:
    """"""
    return UserService(session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
