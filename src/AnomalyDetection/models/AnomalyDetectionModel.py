from datetime import datetime

from pydantic import BaseModel


class AnomalyDetectionModel(BaseModel):
    timestamp: datetime
    valves: float
    pumps: float
    fans: float
    slide: float
