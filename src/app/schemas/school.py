from pydantic import BaseModel
from schemas.address import AddressOut


class SchoolOut(BaseModel):

    id: int
    address_id: int
    address: AddressOut
    name: str
