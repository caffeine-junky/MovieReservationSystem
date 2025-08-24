from fastapi import APIRouter
from .auth import router as auth_router
from .user import router as user_router
from .genre import router as genre_router
from .movie import router as movie_router
from .theatre import router as theatre_router

router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(genre_router)
router.include_router(movie_router)
router.include_router(theatre_router)
