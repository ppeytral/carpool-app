import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter
from models.student import Student

student_router = APIRouter(prefix="/student")


@student_router.get(
    path="/",
    summary="Get all",
)
def get_all():
    with get_session() as s:
        stmt = sa.select(Student)
        result = s.scalars(stmt).all()

        return list(result)
