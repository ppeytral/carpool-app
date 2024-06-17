from datetime import datetime

import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter, HTTPException, status
from models.car import Car
from models.ride import Ride
from models.student import Student
from models.user import User
from schemas.ride import RideIn, RideOut, RideUpdate
from sqlalchemy.orm import joinedload

ride_router = APIRouter(
    prefix="/ride",
    tags=["Ride"],
)


@ride_router.get(
    path="/",
    summary="Get all",
    # response_model=list[RideOut],
)
def get_all(
    start_location: str | None = None,
    end_location: str | None = None,
):
    with get_session() as s:
        stmt = (
            sa.select(Ride)
            .options(
                joinedload(Ride.car)
                .joinedload(Car.student)
                .joinedload(Student.address)
            )
            .options(
                joinedload(Ride.car)
                .joinedload(Car.student)
                .joinedload(Student.school)
            )
        )
        trips = s.scalars(stmt).all()

    if start_location is None and end_location is None:
        return trips

    result = []
    for r in trips:
        if (
            start_location is not None
            and str(r.car.student.address.city).lower()
            == start_location.lower()
        ):
            result.append(r)
        if (
            end_location is not None
            and str(r.car.student.school.name).lower() == end_location.lower()
        ):
            result.append(r)

    return list(result)


@ride_router.delete(
    "/{ride_id}",
    summary="Delete ride by id",
)
def delete_ride_by_id(ride_id: int):
    with get_session() as s:
        stmt = sa.delete(Ride).where(Ride.id == ride_id)
        s.execute(stmt)
        s.commit()

    return {"msg": f"Deleted ride: '{ride_id}'"}


def update_ride_by_id(ride_id: int, new_ride: RideUpdate):
    with get_session() as s:
        ride_to_update = s.scalars(
            sa.select(Ride).where(Ride.id == ride_id)
        ).first()
        if not ride_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ride_id not found: '{ride_id}'",
            )
        stmt = (
            sa.update(Ride)
            .where(Ride.id == ride_id)
            .values(
                seats_offered=new_ride.seats_offered
                or ride_to_update.seats_offered,
                start_time=new_ride.start_time or ride_to_update.start_time,
                start_date=new_ride.start_date or ride_to_update.start_date,
                end_date=new_ride.end_date or ride_to_update.end_date,
                on_monday=new_ride.on_monday or ride_to_update.on_monday,
                on_tuesday=new_ride.on_tuesday or ride_to_update.on_tuesday,
                on_wednesday=new_ride.on_wednesday
                or ride_to_update.on_wednesday,
                on_thursday=new_ride.on_thursday or ride_to_update.on_thursday,
                on_friday=new_ride.on_friday or ride_to_update.on_friday,
                on_saturday=new_ride.on_saturday or ride_to_update.on_saturday,
                on_sunday=new_ride.on_sunday or ride_to_update.on_sunday,
            )
        )
        s.execute(stmt)
        s.commit()
        return {"msg": f"Updated user: '{ride_id}'"}


@ride_router.post(
    "/",
    summary="Create a ride",
)
def create_ride(ride: RideIn):
    with get_session() as s:
        car_stmt = sa.select(Car).where(Car.id == ride.car_id)
        car = s.scalars(car_stmt).first()
        if not car:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"car_id not found: '{ride.car_id}'",
            )
        stmt = sa.insert(Ride).values(
            seats_offered=ride.seats_offered,
            car_id=ride.car_id,
            start_time=ride.start_time,
            start_date=ride.start_date,
            end_date=ride.end_date,
            on_monday=ride.on_monday,
            on_tuesday=ride.on_tuesday,
            on_wednesday=ride.on_wednesday,
            on_thursday=ride.on_thursday,
            on_friday=ride.on_friday,
            on_saturday=ride.on_saturday,
            on_sunday=ride.on_sunday,
        )
        s.execute(stmt)
        s.commit()
        return {"msg": "ride created successfully"}


@ride_router.get(
    "/start_end_locations", summary="Get all start and end locations"
)
def get_start_locations():
    with get_session() as s:
        stmt = sa.select(Ride)
        rides = s.scalars(stmt).all()
