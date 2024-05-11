from pydantic import BaseModel


class AddressOut(BaseModel):

    id: int
    street: str
    postal_code: str
    city: str
