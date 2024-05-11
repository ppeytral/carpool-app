from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[str] = mapped_column(str)
    postal_code: Mapped[str] = mapped_column(str)
    city: Mapped[str] = mapped_column(str)

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, street={self.street!r}, postal_code={self.postal_code!r}, city={self.city!r})"
