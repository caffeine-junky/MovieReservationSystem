from pydantic import BaseModel, Field
from enum import StrEnum
from typing import Any


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: str | None = None
    role: UserRole | None = None


class LoginForm(BaseModel):
    username: str = Field(max_length=50)
    password: str

    class Config:
        json_schema_extra: dict[str, Any] = {
            "example": {
                "username": "john123",
                "password": "password123"
            }
        }
