from models.base import Base
from models.car_make import CarMake
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class CarModel(Base):
    __tablename__ = "car_model"
    __table_args__ = {"schema": "carpool"}

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    car_make_id: Mapped[int] = mapped_column(ForeignKey(column="carpool.car_make.id"))
    car_make: Mapped[CarMake] = relationship()
    model_name: Mapped[str] = mapped_column(String())
    capacity: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"CarModel(ID={self.id!r}, car_make_id={self.car_make_id!r}, car_make={self.car_make!r}, model_name={self.model_name!r}, capacity={self.capacity!r})"
