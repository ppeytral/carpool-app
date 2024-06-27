from datetime import date, time

from pydantic import BaseModel
from schemas.car import CarOut


class RideOut(BaseModel):
    id: int
    car: CarOut
    seats_offered: int
    start_time: time
    start_date: date
    end_date: date | None
    on_monday: bool | None
    on_tuesday: bool | None
    on_wednesday: bool | None
    on_thursday: bool | None
    on_friday: bool | None
    on_saturday: bool | None
    on_sunday: bool | None


class RideUpdate(BaseModel):
    seats_offered: int | None = None
    start_time: time | None = None
    start_date: date | None = None
    end_date: date | None = None
    on_monday: bool | None = None
    on_tuesday: bool | None = None
    on_wednesday: bool | None = None
    on_thursday: bool | None = None
    on_friday: bool | None = None
    on_saturday: bool | None = None
    on_sunday: bool | None = None


class RideIn(BaseModel):
    seats_offered: int
    car_id: int
    start_time: time
    start_date: date
    end_date: date | None
    on_monday: bool
    on_tuesday: bool
    on_wednesday: bool
    on_thursday: bool
    on_friday: bool
    on_saturday: bool
    on_sunday: bool
