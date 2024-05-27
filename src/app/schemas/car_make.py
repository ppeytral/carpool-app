from pydantic import BaseModel


class CarMakeOut(BaseModel):

    id: int
    name: str
