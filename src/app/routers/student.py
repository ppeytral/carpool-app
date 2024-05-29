import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter
from models.student import Student
from models.user import Student
from schemas.car import CarOut

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
        stmt = sa.select(Student).where(Student.id == student_id)
        result = s.scalars(stmt).first()

        if result is None:
            return
        for c in result.cars:
            print(c)
        return result.cars
