from datetime import datetime

from models.base import Base
from models.school import Address, School
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Student(Base):
    __tablename__ = "student"
    __table_args__ = {"schema": "carpool"}

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String())
    lastname: Mapped[str] = mapped_column(String())
    school_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="carpool.school.id",
        ),
    )
    school: Mapped["School"] = relationship(cascade="all")
    address_id: Mapped[int] = mapped_column(ForeignKey(column="carpool.address.id"))
    address: Mapped["Address"] = relationship()
    email: Mapped[str] = mapped_column(String())
    driving_licence_nb: Mapped[str] = mapped_column(String())
    driving_licence_validity: Mapped[datetime] = mapped_column(DateTime())

    def __repr__(self) -> str:
        return f"Student(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r}, school={self.school!r}, address={self.address!r}, email={self.email!r}, driving_licence_nb={self.driving_licence_nb!r}, driving_licence_validity={self.driving_licence_validity!r})"
