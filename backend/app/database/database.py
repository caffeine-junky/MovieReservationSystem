from sqlmodel import SQLModel, Session, create_engine, text
from sqlalchemy import Engine
from loguru import logger
from fastapi import Depends
from typing import Annotated


class Database:

    _engine: Engine | None = None

    @classmethod
    def connect(cls, url: str) -> None:
        """Connect to the postgres database."""
        if cls._engine:
            return
        try:
            cls._engine = create_engine(url)
            logger.success("Connected to the database")
        except Exception as e:
            logger.critical(f"Failed to connect to the database: {e}")
    
    @classmethod
    def disconnect(cls) -> None:
        """Disconnect from the postgres database."""
        if not cls._engine:
            return
        try:
            cls._engine.dispose()
            logger.success("Disconnected from the database")
        except Exception as e:
            logger.error(f"Failed to disconnect from the database: {e}")
        finally:
            cls._engine = None
    
    @classmethod
    def initialize(cls) -> None:
        """Initialize the database by creating the tables."""
        if not cls._engine:
            raise RuntimeError(f"Cannot initialize. Database not connected.")
        try:
            SQLModel.metadata.create_all(cls._engine)
            logger.success("Initialized database tables.")
        except Exception as e:
            logger.error(f"Failed to initialize database tables: {e}")

    @classmethod
    def get_session(cls):
        """Get the db session."""
        if cls._engine is None:
            raise RuntimeError(f"Cannot get session. Database not connected.")
        with Session(cls._engine) as session:
            yield session
    
    @classmethod
    def ping(cls) -> bool:
        """Ping the database to check the connection."""
        if not cls._engine:
            logger.warning("Cannot ping database while not connected.")
            return False
        try:
            with cls._engine.begin() as conn:
                conn.execute(text("SELECT 1"))
            logger.success("Database ping successful.")
            return True
        except Exception as e:
            logger.error(f"Failed to ping the database: {e}")
            return False


SessionDep = Annotated[Session, Depends(Database.get_session)]
