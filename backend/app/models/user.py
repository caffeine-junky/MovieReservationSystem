from pydantic import BaseModel, Field as PField, EmailStr
from datetime import datetime
from typing import Any
from app.models import UserRole


class UserCreate(BaseModel):
    username: str = PField(max_length=50)
    email: EmailStr
    password: str

    class Config:
        json_schema_extra: dict[str, Any] = {
            "example": {
                "username": "moses123",
                "email": "mkay.py@gmail.com",
                "password": "python123"
            }
        }


class UserUpdate(BaseModel):
    username: str | None = PField(default=None, max_length=50)
    email: EmailStr | None = PField(default=None)
    password: str | None = PField(default=None)

    class Config:
        json_schema_extra: dict[str, Any] = {
            "example": {
                "username": "moses123",
                "email": "mkay.py@gmail.com",
                "password": "python123"
            }
        }


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AdminUserUpdate(BaseModel):
    role: UserRole | None = PField(default=None)
    is_active: bool | None = PField(default=None)

    class Config:
        json_schema_extra: dict[str, Any] = {
            "example": {
                "role": UserRole.ADMIN,
                "is_active": False,
            }
        }
