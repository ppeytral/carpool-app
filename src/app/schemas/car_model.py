from pydantic import BaseModel
from schemas.car_make import CarMakeOut


class CarModelOut(BaseModel):

    id: int
    car_make: CarMakeOut
    model_name: str
    capacity: int
