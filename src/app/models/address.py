from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from models.base import Base


class Address(Base):
    __tablename__ = "address"
    __table_args__ = {"schema": "carpool"}

    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[str] = mapped_column(String())
    postal_code: Mapped[str] = mapped_column(String())
    city: Mapped[str] = mapped_column(String())

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, street={self.street!r}, postal_code={self.postal_code!r}, city={self.city!r})"
