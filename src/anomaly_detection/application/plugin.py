from collections.abc import AsyncGenerator

from src.ioc import ioc
from ...shared.infrastructure.types import SessionFactory
from .worker import Worker


__all__ = ['anomaly_detection_presentation_plugin']


async def anomaly_detection_presentation_plugin() -> AsyncGenerator:
    worker = Worker(
        session_factory=ioc.resolve(SessionFactory),
    )

    await worker.start()

    yield

    await worker.stop()
