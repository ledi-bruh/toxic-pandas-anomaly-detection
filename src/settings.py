from pydantic_settings import BaseSettings, SettingsConfigDict
import toml


__all__ = [
    'Settings',
    'load_settings',
]


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        extra='ignore',
        case_sensitive=False,
    )


class Settings(BaseConfig):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
    )


def load_settings() -> Settings:
    return Settings(**toml.load('config.toml'))
