from models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class CarMake(Base):
    __tablename__ = "car_make"
    __table_args__ = {"schema": "carpool"}

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(String())

    def __repr__(self) -> str:
        return f"CarMake(id={self.id!r}, name={self.name!r})"
