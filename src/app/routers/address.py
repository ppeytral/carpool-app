import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter, HTTPException, status
from models.address import Address
from schemas.address import AddressOut, AddressUpdate

address_router = APIRouter(
    prefix="/address",
    tags=["Address"],
)


@address_router.get(
    path="/", summary="Get all", response_model=list[AddressOut]
)
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


@address_router.put(path="/{address_id}", summary="Update an address")
def update_address(address_id: int, new_address: AddressUpdate):
    with get_session() as s:
        address_to_update = s.scalars(
            sa.select(Address).where(Address.id == address_id)
        ).first()
        if not address_to_update:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user_id not found: '{address_id}'",
            )
        stmt = (
            sa.update(Address)
            .where(Address.id == address_id)
            .values(
                street=new_address.street or address_to_update.street,
                postal_code=new_address.postal_code
                or address_to_update.postal_code,
                city=new_address.city or address_to_update.city,
            )
        )
        s.execute(stmt)
        s.commit()
        return {"msg": f"Updated address: '{address_id}'"}
