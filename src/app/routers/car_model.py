import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter
from models.car_model import CarModel

car_model_router = APIRouter(
    prefix="/car_model",
    tags=["Car Model"],
)


@car_model_router.get(
    path="/",
    summary="Get all",
)
def get_all():
    with get_session() as s:
        stmt = sa.select(CarModel)
        result = s.scalars(stmt).all()

        return list(result)
