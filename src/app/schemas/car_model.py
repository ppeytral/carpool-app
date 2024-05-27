from models.car_make import CarMake
from pydantic import BaseModel


class CarModelOut(BaseModel):

    id: int
    car_make: CarMake
    name: str
    capacity: int

    class Config:
        arbitrary_types_allowed = True
