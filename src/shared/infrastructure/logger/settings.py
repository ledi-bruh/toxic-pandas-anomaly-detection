from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ['LoggingSettings']


class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='ignore',
        case_sensitive=False,
    )

    dir: Path = 'logs'
    level: str = 'INFO'
