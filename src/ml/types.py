from typing import Any


__all__ = ['SourcePredictionPipelineFactory']


class SourcePredictionPipelineFactory:
    def __call__(self) -> Any:
        raise NotImplementedError
