from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from app.models import Token, LoginForm, UserResponse
from app.services import AuthServiceDep

router = APIRouter(prefix="/auth", tags=["Authentication"])

# OAuth2PasswordBearer tells FastAPI to look for the "Authorization: Bearer <token>" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/login", response_model=Token, status_code=201)
async def login(
    form: LoginForm,
    service: AuthServiceDep
) -> Token:
    """Authenticate a user and return an access token."""
    return await service.login_for_access_token(form.username, form.password)


@router.get("/me", response_model=UserResponse, status_code=200)
async def get_current_me(
    service: AuthServiceDep,
    token: str = Depends(oauth2_scheme),
) -> UserResponse:
    """Get the currently authenticated user based on the provided token."""
    return await service.get_current_user(token)
