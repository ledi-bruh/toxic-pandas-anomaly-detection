import asyncio

import numpy as np

from src.ml.types import Source2PipelineFactory, SourcePredictionPipelineFactory
from src.shared import now
from src.shared.infrastructure import ArrayBuffer
from ...ml.utils import extract_features, source_predict
from ...settings import Settings
from ...shared.infrastructure.types import SessionFactory
from ..domain.models import AnomalyDetection
from ..infrastructure.repositories import AnomalyDetectionRepositoryImpl


__all__ = ['Worker']


class Worker:
    def __init__(
        self,
        settings: Settings,
        session_factory: SessionFactory,
        array_buffer: ArrayBuffer,
        source_prediction_pipeline_factory: SourcePredictionPipelineFactory,
        source2pipeline_factory: Source2PipelineFactory,
    ):
        self._settings = settings
        self._session = session_factory()
        self._anomaly_detection_repository = AnomalyDetectionRepositoryImpl(self._session)
        self._array_buffer = array_buffer
        self._source_prediction_pipeline = source_prediction_pipeline_factory()
        self._source2pipeline = source2pipeline_factory()
        self._task: asyncio.Task | None = None
        self._executor = None
        self._loop = asyncio.get_event_loop()

    def _predict(
        self,
        ar: np.ndarray,  # 8x220500
        sample_rate: int,  # 22050
        source_prediction_pipeline,
        source2pipeline: dict,
    ):
        features = extract_features(
            array=ar,
            sample_rate=sample_rate,
            channel=None,
        )

        _, source_label = source_predict(
            features=features,
            pipeline=source_prediction_pipeline,
        )

        source_pipeline = source2pipeline[source_label]

        source_channel = source_label * 2
        print(f'{source_channel=}')

        source_features = extract_features(
            array=ar,
            sample_rate=sample_rate,
            channel=source_channel,
        )
        anomaly_probs, anomaly_predict = source_predict(
            features=source_features,
            pipeline=source_pipeline,
        )
        anomaly_prob: float = anomaly_probs[0]

        print(f'{anomaly_predict=} || {anomaly_probs=}')

        res: list[float] = [0] * len(source2pipeline)
        res[source_label] = anomaly_prob

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
                self._settings.freq,
                self._source_prediction_pipeline,
                self._source2pipeline,
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
