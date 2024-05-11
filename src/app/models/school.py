from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.address import Address
from models.base import Base


class School(Base):
    __tablename__ = "school"
    __table_args__ = {"schema": "carpool"}

    id: Mapped[int] = mapped_column(primary_key=True)
    address_id: Mapped[int] = mapped_column(ForeignKey(column="carpool.address.id"))
    address: Mapped["Address"] = relationship(cascade="all")
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"School(id={self.id!r}, name={self.name!r}, address={self.address!r})"
