from datetime import datetime, timedelta, timezone
from typing import Annotated

import sqlalchemy as sa
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from config.config import get_setting
from config.database import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from models.user import User
from passlib.context import CryptContext
from pydantic import BaseModel
from schemas.user import UserOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_router = APIRouter(tags=["Auth"])

SECRET_KEY = get_setting("jwt_secret_key")
ALGORITHM = get_setting("jwt_algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = get_setting("jwt_access_token_expire_minutes")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    with get_session() as s:
        stmt = sa.select(User).where(User.username == username)
        user = s.scalar(stmt)

        if user is None:
            raise credentials_exception
        user.student.school.address
        user.student.address
    return user


def authenticate_user(username: str, password: str) -> User:
    ph = PasswordHasher()

    with get_session() as s:
        stmt = sa.select(User).where(User.username == username)
        user = s.scalar(stmt)
        if not user:
            raise HTTPException(
                status_code=400, detail="incorrect username or password"
            )
        try:
            ph.verify(user.password, password)
        except VerifyMismatchError:
            raise HTTPException(
                status_code=400, detail="incorrect username or password"
            )
        return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@auth_router.post("/token", response_model=Token)
def login(formdata: Annotated[OAuth2PasswordRequestForm, Depends()]):

    user = authenticate_user(formdata.username, formdata.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=token, token_type="Bearer")


@auth_router.get("/me", response_model=UserOut)
def whoami(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
