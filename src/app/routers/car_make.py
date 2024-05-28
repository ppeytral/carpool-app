import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter
from models.car_make import CarMake
from models.car_model import CarModel

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


@car_make_router.get(path="/{make_id}/models", summary="Get all models of a make")
def get_models(make_id: int):

    with get_session() as s:
        stmt = sa.select(CarModel).where(CarModel.car_make_id == make_id)
        result = s.scalars(stmt).all()

        return list(result)
