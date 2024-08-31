from src.anomaly_detection.application import anomaly_detection_presentation_plugin
from src.anomaly_detection.infrastructure import anomaly_detection_infrastructure_plugin
from src.app import App
from src.ioc import ioc
from src.ml import ml_plugin
from src.settings import Settings
from src.shared.infrastructure import infrastructure_plugin
from src.shared.infrastructure.logger import logger_plugin


__all__ = ['bootstrap']


def bootstrap(
    app: App,
    settings: Settings,
) -> None:
    ioc.register(Settings, instance=settings)

    app.add_plugin(logger_plugin(settings.logging))
    app.add_plugin(ml_plugin(settings.ml))
    app.add_plugin(infrastructure_plugin(settings))
    app.add_plugin(anomaly_detection_infrastructure_plugin())
    app.add_plugin(anomaly_detection_presentation_plugin(settings))
