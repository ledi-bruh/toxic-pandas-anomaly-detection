from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ['MlSettings']


class MlSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='ignore',
        case_sensitive=False,
    )

    source_prediction_pipeline_path: Path
