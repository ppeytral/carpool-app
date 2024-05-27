from pydantic import BaseModel


class CarIn(BaseModel):
    vin: str
    car_model_id: int
    student_id: int
