from models.base import Base
from models.car_model import CarModel
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, Relationship, mapped_column


class Car(Base):
    __tablename__ = "car"
    __table_args__ = {"schema": "carpool"}

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    student_id: Mapped[int] = mapped_column(
        ForeignKey(column="carpool.student.id"),
    )
    car_model_id: Mapped[int] = mapped_column(
        ForeignKey(column="carpool.car_model.id"),
    )
    car_model: Mapped[CarModel] = Relationship()
    vin: Mapped[str] = mapped_column(String())

    def __repr__(self) -> str:
        return (
            f"Car(id={self.id!r}, "
            f"car_model={self.car_model!r},"
            f"vin={self.vin!r})"
        )
