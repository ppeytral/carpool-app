from datetime import datetime

from models.base import Base
from models.student import Student
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Message(Base):
    __tablename__ = "message"
    __table_args__ = {"schema": "carpool"}

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(
        ForeignKey(column="carpool.student.id")
    )
    recipient_id: Mapped[int] = mapped_column(
        ForeignKey(column="carpool.student.id")
    )
    message: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime] = mapped_column(DateTime())

    sender: Mapped[Student] = relationship("Student", foreign_keys=[sender_id])
    recipient: Mapped[Student] = relationship(
        "Student", foreign_keys=[recipient_id]
    )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, "
            f"sender_id={self.sender_id!r}, "
            f"recipient_id={self.recipient_id!r}, "
            f"message={self.message!r},)"
        )
