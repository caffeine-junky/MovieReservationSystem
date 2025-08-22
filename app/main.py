from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.core import settings
from app.database import Database
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """"""
    Database.connect(settings.DATABASE_URL)
    await Database.initialize()
    yield
    await Database.disconnect()


app: FastAPI = FastAPI(
    title="Movie Reservation System API",
    version="0.1.0",
    description="A system that allows users to reserve movie tickets.",
    lifespan=lifespan
)
app.include_router(router)


@app.get("/")
async def root():
    """"""
    return {"title": app.title, "version": app.version}


@app.get("/health")
async def health():
    """"""
    return {"serverRunning": True, "databaseConnected": await Database.ping()}
