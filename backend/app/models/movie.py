from typing import Any
from pydantic import BaseModel, Field
from datetime import datetime


class MovieCreate(BaseModel):
    title: str = Field(max_length=200)
    description: str = Field(max_length=2000)
    duration_minutes: int = Field(gt=0)
    poster_url: str | None = Field(default=None, max_length=500)
    genre_ids: list[int] = Field(min_length=1)

    class Config:
        json_schema_extra: dict[str, Any] = {
            "example": {
                "title": "Iron Man",
                "description": """
                Iron Man (2008) is the origin story of billionaire inventor Tony Stark,
                who is kidnapped by terrorists in Afghanistan and forced to build a weapon.
                Instead, he creates a high-tech suit of armor to escape, and upon returning home,
                he dedicates himself to using the suit to fight evil as the superhero Iron Man.
                The film culminates in a battle against Obadiah Stane, Tony's business partner,
                and ends with Stark publicly revealing his identity as Iron Man. 
                """,
                "duration_minutes": 126,
                "poster_url": "https://media.themoviedb.org/t/p/w440_and_h660_face/78lPtwv72eTNqFW9COBYI0dWDJa.jpg",
                "genre_ids": [1, 3, 5] # List of ids for genres in the db
            }
        }


class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    duration_minutes: int | None = Field(default=None, gt=0)
    poster_url: str | None = Field(default=None, max_length=500)
    genre_ids: list[int] | None = Field(default=None, min_length=1)

    class Config:
        json_schema_extra: dict[str, Any] = {
            "example": {
                "title": "Iron Man",
                "description": """
                Iron Man (2008) is the origin story of billionaire inventor Tony Stark,
                who is kidnapped by terrorists in Afghanistan and forced to build a weapon.
                Instead, he creates a high-tech suit of armor to escape, and upon returning home,
                he dedicates himself to using the suit to fight evil as the superhero Iron Man.
                The film culminates in a battle against Obadiah Stane, Tony's business partner,
                and ends with Stark publicly revealing his identity as Iron Man. 
                """,
                "duration_minutes": 126,
                "poster_url": "https://media.themoviedb.org/t/p/w440_and_h660_face/78lPtwv72eTNqFW9COBYI0dWDJa.jpg",
                "genre_ids": [1, 3, 5]
            }
        }


class MovieResponse(BaseModel):
    id: int
    title: str
    description: str
    duration_minutes: int
    poster_url: str | None
    genre_names: list[str]

    created_at: datetime
    updated_at: datetime
