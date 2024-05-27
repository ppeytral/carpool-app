import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter
from models.car import Car
from schemas.car import CarIn

car_router = APIRouter(
    prefix="/car",
    tags=["Car"],
)


@car_router.get(
    path="/",
    summary="Get all",
)
def get_all():
    with get_session() as s:
        stmt = sa.select(Car)
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
