import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter
from models.car import Car

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
