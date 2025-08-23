from sqlmodel import SQLModel, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
from loguru import logger
from fastapi import Depends
from typing import Annotated


class Database:

    _engine: AsyncEngine | None = None
    _async_session_factory: async_sessionmaker[AsyncSession] | None = None

    @classmethod
    def connect(cls, db_url: str) -> None:
        """Connect to the postgres database."""
        if cls._engine:
            return
        try:
            cls._engine = create_async_engine(db_url)
            cls._async_session_factory = async_sessionmaker(cls._engine, expire_on_commit=False)
            logger.success("Connected to the database")
        except Exception as e:
            logger.critical(f"Failed to connect to the database: {e}")
    
    @classmethod
    async def disconnect(cls) -> None:
        """Disconnect from the postgres database."""
        if not cls._engine:
            return
        try:
            await cls._engine.dispose()
            logger.success("Disconnected from the database")
        except Exception as e:
            logger.error(f"Failed to disconnect from the database: {e}")
        finally:
            cls._engine = None
            cls._async_session_factory = None
    
    @classmethod
    async def initialize(cls) -> None:
        """Initialize the database by creating the tables."""
        if not cls._engine:
            raise RuntimeError(f"Cannot initialize. Database not connected.")
        try:
            async with cls._engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
            logger.success("Initialized database tables.")
        except Exception as e:
            logger.error(f"Failed to initialize database tables: {e}")

    @classmethod
    async def get_session(cls):
        """Get the db session."""
        if cls._async_session_factory is None:
            raise RuntimeError(f"Cannot get session. Database not connected.")
        async with cls._async_session_factory() as session:
            yield session
    
    @classmethod
    async def ping(cls) -> bool:
        """Ping the database to check the connection."""
        if not cls._engine:
            logger.warning("Cannot ping database while not connected.")
            return False
        try:
            async with cls._engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            logger.success("Database ping successful.")
            return True
        except Exception as e:
            logger.error(f"Failed to ping the database: {e}")
            return False


SessionDep = Annotated[AsyncSession, Depends(Database.get_session)]
