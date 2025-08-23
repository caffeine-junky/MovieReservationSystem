from sqlmodel import SQLModel, Field, Column, DateTime
from pydantic import BaseModel, Field as PField, EmailStr
from datetime import datetime, timezone
from typing import Any
from app.models import UserRole


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False, max_length=50)
    email: EmailStr = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    role: UserRole = Field(default=UserRole.USER, nullable=False)
    is_active: bool = Field(default=True, nullable=False)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=lambda: datetime.now(timezone.utc)
        )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=lambda: datetime.now(timezone.utc)
        )

    def touch(self) -> None:
        """"""
        self.updated_at = datetime.now(timezone.utc)


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
