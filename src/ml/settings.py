from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ['MlSettings']


class MlSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='ignore',
        case_sensitive=False,
    )

    source_prediction_pipeline_path: Path
    valve_anomaly_prediction_pipeline_path: Path
    pump_anomaly_prediction_pipeline_path: Path
    fan_anomaly_prediction_pipeline_path: Path
    slider_anomaly_prediction_pipeline_path: Path
