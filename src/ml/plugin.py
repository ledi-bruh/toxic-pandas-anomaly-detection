from collections.abc import AsyncGenerator
from typing import Any

import joblib

from src.ioc import ioc
from src.ml.types import SourcePredictionPipelineFactory, Source2PipelineFactory
from .settings import MlSettings


__all__ = ['ml_plugin']


async def ml_plugin(settings: MlSettings) -> AsyncGenerator:
    source_prediction_pipeline = joblib.load(settings.source_prediction_pipeline_path)

    class SourcePredictionPipelineFactoryImpl(SourcePredictionPipelineFactory):
        def __call__(self) -> Any:
            return source_prediction_pipeline

    ioc.register(SourcePredictionPipelineFactory, instance=SourcePredictionPipelineFactoryImpl())

    valve_anomaly_prediction_pipeline = joblib.load(settings.valve_anomaly_prediction_pipeline_path)
    pump_anomaly_prediction_pipeline = joblib.load(settings.pump_anomaly_prediction_pipeline_path)
    fan_anomaly_prediction_pipeline = joblib.load(settings.fan_anomaly_prediction_pipeline_path)
    slider_anomaly_prediction_pipeline = joblib.load(settings.slider_anomaly_prediction_pipeline_path)

    source2pipeline = {
        0: valve_anomaly_prediction_pipeline,  # valve
        1: pump_anomaly_prediction_pipeline,  # pump
        2: fan_anomaly_prediction_pipeline,  # fan
        3: slider_anomaly_prediction_pipeline,  # slider
    }

    class Source2PipelineFactoryImpl(Source2PipelineFactory):
        def __call__(self) -> dict[int, Any]:
            return source2pipeline

    ioc.register(Source2PipelineFactory, instance=Source2PipelineFactoryImpl())

    yield
