import uuid
import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class RunLog(Base):
    __tablename__ = "run_log"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    start_time: Mapped[datetime.datetime]
    machine_type: Mapped[str]
    sensor_address: Mapped[int]

    sensor_readings: Mapped[list["SensorReading"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"RunLog(id={self.id!r}, start_time={self.start_time!r}, machine_type={self.machine_type!r}, sensor_address={self.sensor_address!r})"


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    run_log_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("run_log.id"))
    x: Mapped[float]
    y: Mapped[float]
    z: Mapped[float]
    sensor_type: Mapped[str]
    timestamp: Mapped[datetime.datetime]

    def __repr__(self) -> str:
        return f"SensorReading(id={self.id!r}, run_log_id={self.run_log_id!r}, x={self.x!r}, y={self.y!r}, z={self.z!r}, sensore_type={self.sensor_type}, timestamp={self.timestamp})"
