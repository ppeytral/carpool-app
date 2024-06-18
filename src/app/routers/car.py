import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter
from models.car import Car
from models.car_model import CarModel
from models.school import School
from models.student import Student
from schemas.car import CarIn, CarOut
from sqlalchemy.orm import joinedload

car_router = APIRouter(
    prefix="/car",
    tags=["Car"],
)


@car_router.get(
    path="/",
    summary="Get all",
    response_model=list[CarOut],
)
def get_all():
    with get_session() as s:
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

        return list(result)


@car_router.post(
    "/",
    summary="Create One",
    tags=["Car"],
)
def create_one(car_infos: CarIn):
    with get_session() as s:
        c = Car(**dict(car_infos))
        s.add(c)
        s.commit()


@car_router.delete(
    "/{car_id}",
    summary="Delete a car",
)
def delete_car(car_id: int):
    with get_session() as s:
        stmt = sa.delete(Car).where(Car.id == car_id)
        s.execute(stmt)
        s.commit()
        return {"msg": f"car successfully deleted: '{car_id}'"}
