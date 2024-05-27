import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter
from models.address import Address
from schemas.address import AddressOut

address_router = APIRouter(
    prefix="/address",
    tags=["Address"],
)


@address_router.get(path="/", summary="Get all", response_model=list[AddressOut])
def get_all():
    with get_session() as s:
        stmt = sa.select(Address)
        result = s.scalars(stmt).all()

        return list(result)


@address_router.get(path="/{id}", summary="Get one", response_model=AddressOut)
def get_one(id: int):
    with get_session() as s:
        result = s.get(Address, id)
        return result
