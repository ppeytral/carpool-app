"""create student_ride association table

Revision ID: 1b024f3d7be2
Revises: 38a1390d1f4a
Create Date: 2024-06-17 22:16:56.986534

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1b024f3d7be2"
down_revision: Union[str, None] = "38a1390d1f4a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    table = op.create_table(
        "passenger",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "student_id",
            sa.Integer(),
            sa.ForeignKey(
                "carpool.student.id", ondelete="CASCADE", onupdate="CASCADE"
            ),
            nullable=False,
        ),
        sa.Column(
            "ride_id",
            sa.Integer(),
            sa.ForeignKey(
                "carpool.ride.id", ondelete="CASCADE", onupdate="CASCADE"
            ),
            nullable=False,
        ),
        schema="carpool",
    )

    op.bulk_insert(
        table,
        [
            {"student_id": 1, "ride_id": 1},
            {"student_id": 2, "ride_id": 1},
            {"student_id": 3, "ride_id": 1},
        ],
    )


def downgrade() -> None:
    op.drop_table("passenger", schema="carpool")
