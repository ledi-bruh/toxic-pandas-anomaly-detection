from collections.abc import AsyncGenerator
from logging import Logger

import numpy as np
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, create_async_engine

from src.ioc import ioc
from src.settings import Settings
from .array_buffer.core import ArrayBuffer
from .array_buffer.impl import ArrayBufferImpl
from .types import SessionFactory


__all__ = ['infrastructure_plugin']


async def infrastructure_plugin(settings: Settings) -> AsyncGenerator:
    connection_string = URL.create(
        drivername='postgresql+asyncpg',
        username=settings.db.login,
        password=settings.db.password.get_secret_value(),
        host=settings.db.host,
        port=settings.db.port,
        database=settings.db.database,
    )
    engine = create_async_engine(
        url=connection_string,
        echo=settings.db.echo,
    )
    session_factory = async_sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
    ioc.register('db_connection_url', instance=connection_string)
    ioc.register(AsyncEngine, instance=engine)
    ioc.register(SessionFactory, instance=session_factory)

    ioc.register(
        ArrayBuffer,
        instance=ArrayBufferImpl(
            logger=ioc.resolve(Logger),
            window_size=round(settings.freq * settings.window_seconds),
            step_size=round(settings.freq * settings.step_seconds),
            channels=settings.channels,
            dtype=np.float32,
        ),
    )

    yield

    await engine.dispose()
