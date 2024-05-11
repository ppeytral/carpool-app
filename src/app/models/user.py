from models.base import Base
from models.student import Student
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "carpool"}

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey(column="carpool.student.id"))
    student: Mapped["Student"] = relationship(cascade="all")
    username: Mapped[str] = mapped_column(String())
    password: Mapped[str] = mapped_column(String())
    is_active: Mapped[bool] = mapped_column(Boolean())

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password!r}, student={self.student!r})"
