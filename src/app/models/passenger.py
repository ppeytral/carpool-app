from models.base import Base
from sqlalchemy import Column, ForeignKey, Integer, Table

passenger = Table(
    "passenger",
    Base.metadata,
    Column("id", Integer(), primary_key=True),
    Column(
        "student_id",
        ForeignKey("carpool.student.id"),
    ),
    Column(
        "ride_id",
        ForeignKey("carpool.ride.id"),
    ),
    schema="carpool",
)
