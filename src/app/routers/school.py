import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter
from models.car import Car
from models.school import School
from schemas.school import SchoolOut

school_router = APIRouter(
    prefix="/school",
    tags=["School"],
)


@school_router.get(path="/", summary="Get all", response_model=list[SchoolOut])
def get_all():
    with get_session() as s:
        stmt = sa.select(School)
        result = s.scalars(stmt).all()
        for r in result:
            print(r.address)

        return list(result)
