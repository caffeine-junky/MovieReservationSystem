from fastapi import Depends
from typing import Annotated
from jose import JWTError
from app.models import Token, TokenData, UserRole, UserResponse
from app.core import SecurityUtils
from app.utils.exceptions import (
    InvalidJWTTokenException
)

from .user import UserServiceDep, UserService


class AuthService:

    def __init__(self, user_service: UserService) -> None:
        self._user_service = user_service
    
    async def login_for_access_token(self, username: str, password: str) -> Token:
        """"""
        user = await self._user_service.authenticate(username, password)
        token_data = TokenData(sub=str(user.id), role=user.role)
        token = SecurityUtils.create_access_token(token_data)
        return token
    
    async def get_current_user(self, token: str) -> UserResponse:
        """"""
        try:
            decoded = SecurityUtils.decode_token(token)
            user_id: int | None = int(decoded.sub) if decoded.sub else None
            user_role: UserRole | None = decoded.role
            
            if (not user_id) or (not user_role):
                raise InvalidJWTTokenException()
        except JWTError:
            raise InvalidJWTTokenException()
        
        user = await self._user_service.get_one_user(user_id)
        return user



def get_auth_service(user_service: UserServiceDep) -> AuthService:
    """"""
    return AuthService(user_service)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
