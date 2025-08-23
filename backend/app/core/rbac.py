from fastapi import Depends
from app.models import UserRole, UserResponse
from app.services import AuthService
from app.utils.exceptions import UnauthorizedException


def require_role(*allowed_roles: UserRole):
    """Dependency generator for role-based access."""
    async def _role_checker(
        current_user: UserResponse = Depends(AuthService.get_current_user)
    ) -> UserResponse:
        if current_user.role not in allowed_roles:
            raise UnauthorizedException()
        return current_user
    return _role_checker

