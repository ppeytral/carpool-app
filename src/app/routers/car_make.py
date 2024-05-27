import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter
from models.car_make import CarMake
from schemas.car_make import CarMakeOut

car_make_router = APIRouter(prefix="/car_make")


@car_make_router.get(
    path="/",
    summary="Get all",
    # response_model=list[CarMakeOut],
)
def get_all():
    with get_session() as s:
        stmt = sa.select(CarMake)
        result = s.scalars(stmt).all()

        return list(result)
