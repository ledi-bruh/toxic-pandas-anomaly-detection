from datetime import datetime

from sqlalchemy import Float, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.infrastructure import Base


__all__ = ['DbAnomalyDetection']


class DbAnomalyDetection(Base):
    __tablename__ = 'anomaly_detections'

    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), primary_key=True)
    valves: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
    pumps: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
    fans: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
    slide: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
