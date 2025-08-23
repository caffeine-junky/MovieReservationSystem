from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = ""

    # Secret
    JWT_SECRET: str = ""
    JWT_TOKEN_EXPIRE_MINUTES: int = 0
    JWT_ALGORITHM: str = ""

    class Config:
        env_file = ".env"


settings: Settings = Settings()
