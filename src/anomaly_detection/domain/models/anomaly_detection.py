from datetime import datetime

from pydantic import BaseModel


__all__ = ['AnomalyDetection']


class AnomalyDetection(BaseModel):
    timestamp: datetime
    valves: float
    pumps: float
    fans: float
    slide: float
