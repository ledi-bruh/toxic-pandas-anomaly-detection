from collections.abc import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from .anomaly_detection_repository import AnomalyDetectionRepository


__all__ = ['AnomalyDetectionRepositoryFactory']


AnomalyDetectionRepositoryFactory = Callable[[AsyncSession], AnomalyDetectionRepository]
