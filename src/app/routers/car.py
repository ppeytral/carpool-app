import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter
from models.car import Car
from schemas.car import CarIn, CarOut

car_router = APIRouter(
    prefix="/car",
    tags=["Car"],
)


@car_router.get(path="/", summary="Get all", response_model=list[CarOut])
def get_all():
    with get_session() as s:
        stmt = sa.select(Car)
        result = s.scalars(stmt).all()
        for r in result:
            print(r.car_model)

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
