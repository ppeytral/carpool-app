from pydantic import BaseModel


class AddressUpdate(BaseModel):
    street: str | None = None
    postal_code: str | None = None
    city: str | None = None


class AddressOut(BaseModel):

    id: int
    street: str
    postal_code: str
    city: str
