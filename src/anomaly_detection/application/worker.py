import asyncio
from time import sleep

import numpy as np

from src.shared import now
from src.shared.infrastructure import ArrayBuffer
from ...shared.infrastructure.types import SessionFactory
from ..domain.models import AnomalyDetection
from ..infrastructure.repositories import AnomalyDetectionRepositoryImpl


__all__ = ['Worker']


class Worker:
    def __init__(
        self,
        session_factory: SessionFactory,
        array_buffer: ArrayBuffer,
    ):
        self._session = session_factory()
        self._anomaly_detection_repository = AnomalyDetectionRepositoryImpl(self._session)
        self._array_buffer = array_buffer
        self._task: asyncio.Task | None = None
        self._executor = None
        self._loop = asyncio.get_event_loop()

    def _predict(self, ar: np.ndarray):
        sleep(3)
        print('predicted', ar.shape, ar[:, 0])
        return np.random.sample(), np.random.sample(), np.random.sample(), np.random.sample()

    async def _run(self):
        while not self._task.cancelled():
            array = self._array_buffer()
            # print('-> worker')

            if array is None:
                await asyncio.sleep(1)
                continue

            timestamp = now()
            valves, pumps, fans, slide = await self._loop.run_in_executor(
                self._executor,
                self._predict,
                array,
            )

            anomaly_detection = AnomalyDetection(
                timestamp=timestamp,
                valves=valves,
                pumps=pumps,
                fans=fans,
                slide=slide,
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
