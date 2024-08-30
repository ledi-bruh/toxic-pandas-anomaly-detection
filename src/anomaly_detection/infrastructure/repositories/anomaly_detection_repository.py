from asyncpg import UniqueViolationError
from sqlalchemy.exc import StatementError
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.models import AnomalyDetection
from ...domain.repositories import AnomalyDetectionRepository
from ..mappers import anomaly_detection as anomaly_detection_mapper


__all__ = ['AnomalyDetectionRepositoryImpl']


class AnomalyDetectionRepositoryImpl(AnomalyDetectionRepository):
    __slots__ = ('_session',)

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def add(self, anomaly_detection: AnomalyDetection) -> None:
        db_anomaly_detection = anomaly_detection_mapper.domain_to_db(anomaly_detection)

        self._session.add(db_anomaly_detection)

        try:
            await self._session.flush()
        except StatementError as error:
            error = error.orig.__cause__
            if isinstance(error, UniqueViolationError):
                raise Exception(
                    f'Same anomaly_detection timestamp={db_anomaly_detection.timestamp} already exist.'
                ) from error
            raise Exception(str(error)) from error
