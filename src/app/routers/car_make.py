import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter
from models.car_make import CarMake

car_make_router = APIRouter(
    prefix="/car_make",
    tags=["Car Make"],
)


@car_make_router.get(
    path="/",
    summary="Get all",
)
def get_all():
    with get_session() as s:
        stmt = sa.select(CarMake)
        result = s.scalars(stmt).all()

        return list(result)
