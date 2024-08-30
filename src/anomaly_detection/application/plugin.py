import asyncio
from collections.abc import AsyncGenerator

import numpy as np

from src.ioc import ioc
from ...shared.infrastructure.array_buffer.core import ArrayBuffer
from ...shared.infrastructure.types import SessionFactory
from .worker import Worker


__all__ = ['anomaly_detection_presentation_plugin']



async def anomaly_detection_presentation_plugin() -> AsyncGenerator:
    worker = Worker(
        session_factory=ioc.resolve(SessionFactory),
        array_buffer=ioc.resolve(ArrayBuffer),
    )

    task = asyncio.create_task(s(ioc.resolve(ArrayBuffer)))

    await worker.start()

    yield

    task.cancel()
    await worker.stop()
