import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter
from models.user import User
from schemas.user import UserOut

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@user_router.get(
    path="/",
    summary="Get all",
    response_model=list[UserOut],
)
def get_all():
    with get_session() as s:
        stmt = sa.select(User)
        result = s.scalars(stmt).all()
        for r in result:
            print(r)

        return list(result)


@user_router.get(
    path="/{user_id}",
    summary="Get user by id",
    response_model=UserOut,
)
def get_user_by_id(user_id: int):
    with get_session() as s:
        stmt = sa.select(User).where(User.id == user_id)
        result = s.scalars(stmt).first()
        print(result)
        return result


@user_router.delete(
    "/{user_id}",
    summary="Delete user by id",
)
def delete_user_by_id(user_id: int):
    with get_session() as s:
        stmt = sa.delete(User).where(User.id == user_id)
        s.execute(stmt)
        s.commit()

    return {"msg": f"Deleted user: '{user_id}'"}
