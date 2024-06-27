import sqlalchemy as sa
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from config.database import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User
from routers.auth import get_current_user
from schemas.user import UserOut, UserPasswordUpdate, UserUpdate

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


@user_router.put(
    "/{user_id}",
    summary="Update a user",
)
def update_user_by_id(user_id: int, new_user: UserUpdate):
    with get_session() as s:
        user_to_update = s.scalars(
            sa.select(User).where(User.id == user_id)
        ).first()
        if not user_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user_id not found: '{user_id}'",
            )
        stmt = (
            sa.update(User)
            .where(User.id == user_id)
            .values(
                student_id=new_user.student_id or user_to_update.student_id,
                is_active=new_user.is_active or user_to_update.is_active,
                username=new_user.username or user_to_update.username,
                updated_at=new_user.updated_at,
            )
        )
        s.execute(stmt)
        s.commit()
        return {"msg": f"Updated user: '{user_id}'"}


@user_router.post(
    "/update_password",
    summary="Change password of user",
)
def update_password(
    new_password: UserPasswordUpdate, user: User = Depends(get_current_user)
):
    if new_password.new_password != new_password.verified_new_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"mismatching password",
        )
    ph = PasswordHasher()
    try:
        ph.verify(user.password, new_password.current_password)

        hashed_pw = ph.hash(new_password.new_password)
        with get_session() as s:
            stmt = (
                sa.update(User)
                .where(User.id == user.id)
                .values(password=hashed_pw)
            )
        s.execute(stmt)
        s.commit()
        return {"msg": "password updated successfully"}

    except VerifyMismatchError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"mismatching password",
        )
