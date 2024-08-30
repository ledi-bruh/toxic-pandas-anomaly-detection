from src.shared.infrastructure import infrastructure_plugin
from .app import App
from .ioc import ioc
from .settings import Settings


__all__ = ['bootstrap']


def bootstrap(
    app: App,
    settings: Settings,
) -> None:
    ioc.register(Settings, instance=settings)

    app.add_plugin(infrastructure_plugin(settings))
