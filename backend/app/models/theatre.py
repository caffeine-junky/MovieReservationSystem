from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any


class BaseTheatre(BaseModel):
    name: str = Field(max_length=200)
    address: str | None = Field(default=None, max_length=500)


class TheatreCreate(BaseTheatre):

    class Config:
        json_schema_extra: dict[str, Any] = {
            "example": {
                "name": "Towers Theatre",
                "address": "123 Main Street, Downtown, Johannesburg, South Africa"
            }
        }


class TheatreUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=200)
    address: str | None = Field(default=None, max_length=500)

    class Config:
        json_schema_extra: dict[str, Any] = {
            "example": {
                "name": "Cineplex Grand",
                "address": "456 Ocean Drive, Cape Town, South Africa"
            }
        }


class TheatreResponse(BaseTheatre):
    id: int
    auditorium_names: list[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
