from ..models import AnomalyDetection


__all__ = ['AnomalyDetectionRepository']


class AnomalyDetectionRepository:
    __slots__ = ()

    async def add(self, anomaly_detection: AnomalyDetection) -> None:
        raise NotImplementedError
