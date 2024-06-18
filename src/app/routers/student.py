import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter, HTTPException, status
from models.car import Car
from models.car_model import CarModel
from models.ride import Ride
from models.school import School
from models.student import Student
from models.user import Student
from schemas.car import CarOut
from schemas.ride import RideOut
from schemas.student import StudentUpdate
from sqlalchemy.orm import joinedload

student_router = APIRouter(
    prefix="/student",
    tags=["Student"],
)


@student_router.get(
    path="/",
    summary="Get all",
)
def get_all():
    with get_session() as s:
        stmt = sa.select(Student)
        result = s.scalars(stmt).all()

        return list(result)


@student_router.get(
    "/{student_id}/cars",
    summary="Get all cars by student_id",
    response_model=list[CarOut],
)
def get_cars_by_student_id(student_id: int):
    with get_session() as s:
        stmt = sa.select(Student).where(Student.id == student_id).options()
        result = s.scalars(stmt).first()

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        stmt = (
            sa.select(Car)
            .options(joinedload(Car.car_model).joinedload(CarModel.car_make))
            .options(
                joinedload(Car.student)
                .joinedload(Student.school)
                .joinedload(School.address)
            )
            .options(joinedload(Car.student).joinedload(Student.address))
        )
        result = s.scalars(stmt).all()
        return result


@student_router.put(
    "/{student_id}",
    summary="Update a student",
)
def update_student_by_id(student_id: int, new_student: StudentUpdate):
    with get_session() as s:
        student_to_update = s.scalars(
            sa.select(Student).where(Student.id == student_id)
        ).first()
        if not student_to_update:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user_id not found: '{student_id}'",
            )
        stmt = (
            sa.update(Student)
            .where(Student.id == student_id)
            .values(
                firstname=new_student.firstname or student_to_update.firstname,
                lastname=new_student.lastname or student_to_update.lastname,
                school_id=new_student.school_id or student_to_update.school_id,
                address_id=new_student.address_id
                or student_to_update.address_id,
                email=new_student.email or student_to_update.email,
                driving_licence_nb=new_student.driving_licence_nb
                or student_to_update.driving_licence_nb,
                driving_licence_validity=new_student.driving_licence_validity
                or student_to_update.driving_licence_validity,
            )
        )
        s.execute(stmt)
        s.commit()
        return {"msg": f"Updated student: '{student_id}'"}


@student_router.get(
    "/{student_id}/offered_rides",
    summary="Get offered rides by students",
    response_model=list[RideOut],
)
def get_student_offered_rides(student_id: int):
    with get_session() as s:
        student = s.scalars(
            sa.select(Student).where(Student.id == student_id)
        ).first()
        if not student:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user_id not found: '{student_id}'",
            )
        stmt = (
            sa.select(Ride)
            .join(Car)
            .where(Car.student_id == student_id)
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
            .options(
                joinedload(Ride.car)
                .joinedload(Car.car_model)
                .joinedload(CarModel.car_make)
            )
        )
        result = s.scalars(stmt).all()

        return result
