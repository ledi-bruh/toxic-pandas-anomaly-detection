import asyncio

import numpy as np

from src.ml.types import SourcePredictionPipelineFactory
from src.shared import now
from src.shared.infrastructure import ArrayBuffer
from ...ml.utils import extract_features, source2pipeline, source_predict
from ...shared.infrastructure.types import SessionFactory
from ..domain.models import AnomalyDetection
from ..infrastructure.repositories import AnomalyDetectionRepositoryImpl


__all__ = ['Worker']


class Worker:
    def __init__(
        self,
        session_factory: SessionFactory,
        array_buffer: ArrayBuffer,
        source_prediction_pipeline_factory: SourcePredictionPipelineFactory,
    ):
        self._session = session_factory()
        self._anomaly_detection_repository = AnomalyDetectionRepositoryImpl(self._session)
        self._array_buffer = array_buffer
        self._source_prediction_pipeline = source_prediction_pipeline_factory()
        self._task: asyncio.Task | None = None
        self._executor = None
        self._loop = asyncio.get_event_loop()

    def _predict(
        self,
        ar: np.ndarray,
        sample_rate: int,
        source_prediction_pipeline,
    ):
        features = extract_features(
            array=ar,
            sample_rate=sample_rate,
            channel=None,
        )

        source_label = source_predict(
            features=features,
            pipeline=source_prediction_pipeline,
        )

        source_channel = source_label * 2
        print(f'{source_channel=}')

        # pipeline = source2pipeline[source_label]
        # source_features = extract_features(
        #     array=ar,
        #     sample_rate=sample_rate,
        #     channel=source_channel,
        # )
        # anomaly_predict = source_predict(
        #     features=source_features,
        #     pipeline=pipeline,
        # )
        # print(f'{anomaly_predict=}')
        anomaly_predict = np.random.sample()

        res = [0] * len(source2pipeline)
        res[source_label] = anomaly_predict

        return res

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
                22050,
                self._source_prediction_pipeline,
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
