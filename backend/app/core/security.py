from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

from app.core import settings
from app.models import Token, TokenData


class SecurityUtils:

    _pwd_context: CryptContext = CryptContext(schemes=["bcrypt"])

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash a password using the `bcrypt` algorithm."""
        return cls._pwd_context.hash(password)
    
    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        """Verify if the password matches the `bcrypt` hash."""
        return cls._pwd_context.verify(password, hashed_password)
    
    @classmethod
    def create_access_token(cls, payload: TokenData, expires_minutes: int | None = None) -> Token:
        """Creates a JWT access token."""
        to_encode = payload.model_dump()
        to_encode.update({
            "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or settings.JWT_TOKEN_EXPIRE_MINUTES)
        })
        token = Token(
            access_token=jwt.encode(
                to_encode,
                key=settings.JWT_SECRET,
                algorithm=settings.JWT_ALGORITHM
                )
            )
        return token
    
    @classmethod
    def decode_token(cls, token: str) -> TokenData:
        """Decodes the encoded JWT token."""
        data = TokenData(**jwt.decode(token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]))
        return data
