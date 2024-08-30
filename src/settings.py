from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    db: DbSettings


def load_settings() -> Settings:
    return Settings()
