from datetime import datetime
from os import walk

import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from models.address import Address
from models.car import Car
from models.car_model import CarModel
from models.passenger import passenger
from models.ride import Ride
from models.school import School
from models.student import Student
from models.user import User
from routers.auth import get_current_user
from schemas.ride import RideIn, RideOut, RideUpdate
from schemas.student import StudentOut
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import joinedload

ride_router = APIRouter(
    prefix="/ride",
    tags=["Ride"],
)


@ride_router.get(
    path="/",
    summary="Get all",
    response_model=list[RideOut],
)
def get_all(
    start_location: str | None = None,
    end_location: str | None = None,
    show_full: bool = False,
):

    filters = []

    if start_location is not None:
        filters.append((Address.city, start_location))
    if end_location is not None:
        filters.append((School.name, end_location))

    stmt = (
        sa.select(Ride)
        .join(Ride.car)
        .join(Car.student)
        .join(Student.address)
        .join(Ride.car)
        .join(Car.student)
        .join(Student.school)
        .options(
            joinedload(Ride.car)
            .joinedload(Car.car_model)
            .joinedload(CarModel.car_make)
        )
        .options(
            joinedload(Ride.car)
            .joinedload(Car.student)
            .joinedload(Student.address)
        )
        .options(
            joinedload(Ride.car)
            .joinedload(Car.student)
            .joinedload(Student.school)
            .joinedload(School.address)
        )
    )
    for f in filters:
        stmt = stmt.where(f[0] == f[1])

    with get_session() as s:

        trips = s.scalars(stmt).all()
        if show_full is False:
            result = []
            for t in trips:
                if len(t.passengers) < t.seats_offered:
                    print(t.passengers)
                    result.append(t)
            return list(result)
        return trips


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
    "/{ride_id}/subscribers",
    summary="Get subscribers of a ride",
    response_model=list[StudentOut],
)
def get_subs(ride_id: int):

    with get_session() as s:
        stmt = sa.select(Ride).where(Ride.id == ride_id)
        ride = s.scalars(stmt).first()

        if ride is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ride id not found: '{ride_id}'",
            )
        print(ride.passengers)

    return ride.passengers


@ride_router.post(
    "/{ride_id}/subscribe", summary="Subscribe connected user to ride"
)
def subscribe_ride(ride_id: int, user: User = Depends(get_current_user)):

    with get_session() as s:
        stmt = sa.select(Ride).where(Ride.id == ride_id)
        ride = s.scalars(stmt).first()

        if ride is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ride id not found: '{ride_id}'",
            )

        if ride.seats_offered <= len(ride.passengers):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Ce trajet est complet.",
            )
        try:
            ride.passengers.append(user.student)
            s.commit()
        except InvalidRequestError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Vous êtes déjà enregistré sur ce trajet.",
            )

    return {"msg": "successfully subscribed"}


@ride_router.post(
    "/{ride_id}/unsubscribe", summary="Unsubscribe connected user from ride"
)
def unsubscribe_ride(ride_id: int, user: User = Depends(get_current_user)):

    with get_session() as s:
        stmt = (
            sa.select(Ride)
            .join(passenger)
            .where(Ride.id == ride_id)
            .options(joinedload(Ride.passengers))
        )
        ride = s.scalars(stmt).first()

        studentstmt = sa.select(Student).where(Student.id == user.student_id)
        user_student = s.scalar(studentstmt)

        if ride is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ride id not found: '{ride_id}'",
            )

        if user.student_id not in [
            passenger.id for passenger in ride.passengers
        ]:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous n'êtes pas inscrit sur ce trajet.",
            )
        ride.passengers.remove(user_student)
        s.commit()

    return {"msg": "successfully unsubscribed"}
