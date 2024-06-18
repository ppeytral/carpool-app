from datetime import date, time

from models.base import Base
from models.car import Car
from models.passenger import passenger
from sqlalchemy import Boolean, Date, ForeignKey, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Ride(Base):
    __tablename__ = "ride"
    __table_args__ = {"schema": "carpool"}

    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey(column="carpool.car.id"))
    seats_offered: Mapped[int] = mapped_column(Integer())
    start_time: Mapped[time] = mapped_column(Time())
    start_date: Mapped[date] = mapped_column(Date())
    end_date: Mapped[date] = mapped_column(Date())
    on_monday: Mapped[bool] = mapped_column(Boolean())
    on_tuesday: Mapped[bool] = mapped_column(Boolean())
    on_wednesday: Mapped[bool] = mapped_column(Boolean())
    on_thursday: Mapped[bool] = mapped_column(Boolean())
    on_friday: Mapped[bool] = mapped_column(Boolean())
    on_saturday: Mapped[bool] = mapped_column(Boolean())
    on_sunday: Mapped[bool] = mapped_column(Boolean())

    car: Mapped["Car"] = relationship()
    passengers: Mapped[list["Student"]] = relationship(
        secondary=passenger, back_populates="rides"
    )

    def __repr__(self) -> str:
        return (
            f"Ride("
            f"id={self.id!r}, "
            f"car_id={self.car_id!r}, "
            f"start_time={self.start_time!r}, "
            f"start_date={self.start_date!r},"
            f"seats_offered={self.seats_offered!r},"
            f")"
        )
