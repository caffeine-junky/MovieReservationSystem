from typing import Any
from pydantic import BaseModel, Field
from datetime import datetime


class GenreCreate(BaseModel):
    name: str = Field(max_length=50)

    class Config:
        json_schema_extra: dict[str, Any] = {
            "example": {
                "name": "action"
            }
        }


class GenreUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=50)

    class Config:
        json_schema_extra: dict[str, Any] = {
            "example": {
                "name": "action"
            }
        }


class GenreResponse(BaseModel):
    id: int
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
