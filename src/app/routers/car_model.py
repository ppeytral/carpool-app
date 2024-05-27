import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter
from models.car_model import CarModel
from schemas.car_model import CarModelOut

car_model_router = APIRouter(prefix="/car_model")


@car_model_router.get(
    path="/",
    summary="Get all",
    # response_model=list[CarModelOut],
)
def get_all():
    with get_session() as s:
        stmt = sa.select(CarModel)
        result = s.scalars(stmt).all()

        return list(result)
