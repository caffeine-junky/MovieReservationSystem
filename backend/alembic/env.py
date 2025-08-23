import sys
import os
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models import BaseSQLModel
from app.core import settings

config = context.config
fileConfig(config.config_file_name) if config.config_file_name is not None else None

target_metadata = BaseSQLModel.metadata
DATABASE_URL = settings.DATABASE_URL

# ----------------------------
# Offline migrations (no DB connection)
# ----------------------------
def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ----------------------------
# Online migrations (with async DB connection)
# ----------------------------
async def run_migrations_online():
    from sqlalchemy.ext.asyncio import create_async_engine

    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection: Connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
