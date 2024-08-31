from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.ml.settings import MlSettings
from src.shared.infrastructure.logger import LoggingSettings


__all__ = [
    'Settings',
    'load_settings',
]


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        extra='ignore',
        case_sensitive=False,
    )


class DbSettings(BaseConfig):
    echo: bool = False
    login: str
    password: SecretStr
    host: str
    port: int
    database: str


class Settings(BaseConfig):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
    )

    channels: int
    freq: int
    window_seconds: float
    step_seconds: float

    db: DbSettings
    logging: LoggingSettings = LoggingSettings()
    ml: MlSettings


def load_settings() -> Settings:
    return Settings()
