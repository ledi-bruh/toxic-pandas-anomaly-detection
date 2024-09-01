from typing import Any


__all__ = [
    'Source2PipelineFactory',
    'SourcePredictionPipelineFactory',
]


class SourcePredictionPipelineFactory:
    def __call__(self) -> Any:
        raise NotImplementedError


class Source2PipelineFactory:
    def __call__(self) -> dict[int, Any]:
        raise NotImplementedError
