import asyncio

from alembic import context
from sqlalchemy import URL
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from src.anomaly_detection.infrastructure.models import *
from src.settings import load_settings
from src.shared.infrastructure import Base


db_settings = load_settings().db

connection_string = URL.create(
    drivername='postgresql+asyncpg',
    username=db_settings.login,
    password=db_settings.password.get_secret_value(),
    host=db_settings.host,
    port=db_settings.port,
    database=db_settings.database,
)

engine = create_async_engine(
    url=connection_string,
    echo=db_settings.echo,
)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=connection_string,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = engine

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
