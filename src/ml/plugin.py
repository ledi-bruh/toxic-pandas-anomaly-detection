from collections.abc import AsyncGenerator
from typing import Any

import joblib

from src.ioc import ioc
from src.ml.types import SourcePredictionPipelineFactory
from .settings import MlSettings


__all__ = ['ml_plugin']


async def ml_plugin(settings: MlSettings) -> AsyncGenerator:
    source_prediction_pipeline = joblib.load(settings.source_prediction_pipeline_path)

    class SourcePredictionPipelineFactoryImpl(SourcePredictionPipelineFactory):
        def __call__(self) -> Any:
            return source_prediction_pipeline

    ioc.register(SourcePredictionPipelineFactory, instance=SourcePredictionPipelineFactoryImpl())

    yield
