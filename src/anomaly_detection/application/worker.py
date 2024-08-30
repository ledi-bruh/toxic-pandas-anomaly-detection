import asyncio

import numpy as np

from src.shared import now
from ...shared.infrastructure.types import SessionFactory
from ..domain.models import AnomalyDetection
from ..infrastructure.repositories import AnomalyDetectionRepositoryImpl


__all__ = ['Worker']


class Worker:
    def __init__(
        self,
        session_factory: SessionFactory,
    ):
        self._session = session_factory()
        self._anomaly_detection_repository = AnomalyDetectionRepositoryImpl(self._session)
        self._task: asyncio.Task | None = None

    async def _run(self):
        while not self._task.cancelled():
            await asyncio.sleep(3)
            anomaly_detection = AnomalyDetection(
                timestamp=now(),
                valves=np.random.sample(),
                pumps=np.random.sample(),
                fans=np.random.sample(),
                slide=np.random.sample(),
            )
            try:
                await self._anomaly_detection_repository.add(anomaly_detection)
                await self._session.commit()
            except Exception as e:
                print(e)

    async def start(self):
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        if self._task is not None:
            self._task.cancel()
