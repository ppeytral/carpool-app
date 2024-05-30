from pydantic import BaseModel
from schemas.car_model import CarModelOut
from schemas.student import StudentOut


class CarIn(BaseModel):
    vin: str
    car_model_id: int
    student_id: int


class CarOut(BaseModel):
    id: int
    vin: str
    car_model: CarModelOut
    student_id: int
