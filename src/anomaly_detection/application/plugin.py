import asyncio
from collections.abc import AsyncGenerator

import numpy as np

from src.ioc import ioc
from src.py_audio_streamer.impl.py_audio_streamer_impl import PyAudioStreamerImpl
from src.settings import Settings
from ...shared.infrastructure.array_buffer.core import ArrayBuffer
from ...shared.infrastructure.types import SessionFactory
from .worker import Worker


__all__ = ['anomaly_detection_presentation_plugin']


async def s(a):
    while 1:
        await asyncio.sleep(1)
        a.write(np.ones((8, 22050 * 3), dtype=np.float32).tobytes())


async def anomaly_detection_presentation_plugin(settings: Settings) -> AsyncGenerator:
    worker = Worker(
        session_factory=ioc.resolve(SessionFactory),
        array_buffer=ioc.resolve(ArrayBuffer),
    )

    producer = PyAudioStreamerImpl(
        buffer=ioc.resolve(ArrayBuffer),
        chunk_size=settings.freq // 2,
        rate=settings.freq,
        target_channels=settings.channels,
    )

    await worker.start()
    producer.start_streaming()

    yield

    producer.stop_streaming()
    await worker.stop()
