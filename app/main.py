from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """"""
    yield


app: FastAPI = FastAPI(
    title="Movie Reservation System API",
    version="0.1.0"
)
