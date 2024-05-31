"""create ride table

Revision ID: 38a1390d1f4a
Revises: 4b10042487f8
Create Date: 2024-05-31 14:27:31.723641

"""

from datetime import date, time
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "38a1390d1f4a"
down_revision: Union[str, None] = "4b10042487f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    ride_table = op.create_table(
        "ride",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "car_id",
            sa.Integer(),
            sa.ForeignKey(
                "carpool.car.id",
                ondelete="CASCADE",
                onupdate="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column("seats_offered", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("start_date", sa.Date()),
        sa.Column("end_date", sa.Date()),
        sa.Column("on_monday", sa.Boolean()),
        sa.Column("on_tuesday", sa.Boolean()),
        sa.Column("on_wednesday", sa.Boolean()),
        sa.Column("on_thursday", sa.Boolean()),
        sa.Column("on_friday", sa.Boolean()),
        sa.Column("on_saturday", sa.Boolean()),
        sa.Column("on_sunday", sa.Boolean()),
        schema="carpool",
    )

    op.bulk_insert(
        ride_table,
        [
            {
                "car_id": 1,
                "seats_offered": 4,
                "start_time": time(8, 0, 0),
                "start_date": date(2024, 6, 12),
                "end_date": None,
                "on_monday": None,
                "on_tuesday": None,
                "on_wednesday": None,
                "on_thursday": None,
                "on_friday": None,
                "on_saturday": None,
                "on_sunday": None,
            },
            {
                "car_id": 1,
                "seats_offered": 4,
                "start_time": time(14, 0, 0),
                "start_date": date(2024, 6, 12),
                "end_date": date(2024, 8, 1),
                "on_monday": None,
                "on_tuesday": None,
                "on_wednesday": None,
                "on_thursday": None,
                "on_friday": None,
                "on_saturday": None,
                "on_sunday": None,
            },
            {
                "car_id": 2,
                "seats_offered": 2,
                "start_time": time(7, 30, 0),
                "start_date": date(2024, 6, 12),
                "end_date": date(2024, 6, 23),
                "on_monday": True,
                "on_tuesday": True,
                "on_wednesday": True,
                "on_thursday": False,
                "on_friday": False,
                "on_saturday": False,
                "on_sunday": False,
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("ride", schema="carpool")
