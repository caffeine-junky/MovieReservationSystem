from pydantic import BaseModel
from enum import StrEnum


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: str | None = None
    role: UserRole | None = None
