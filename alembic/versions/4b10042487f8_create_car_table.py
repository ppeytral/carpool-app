"""create car table

Revision ID: 4b10042487f8
Revises: 4468bb21356e
Create Date: 2024-05-12 21:41:52.589767

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4b10042487f8"
down_revision: Union[str, None] = "4468bb21356e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    car_table = op.create_table(
        "car",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "student_id",
            sa.Integer(),
            sa.ForeignKey(
                "carpool.student.id",
                ondelete="CASCADE",
                onupdate="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "car_model_id",
            sa.Integer(),
            sa.ForeignKey(
                "carpool.car_model.id",
                ondelete="CASCADE",
                onupdate="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "vin",
            sa.String(),
            nullable=False,
        ),
        # sa.Column(
        #     "color_id",
        #     sa.Integer(),
        #     sa.ForeignKey("carpool.color.id", ondelete="CASCADE"),
        # ),
        schema="carpool",
    )

    op.bulk_insert(
        car_table,
        [
            {
                "student_id": 1,
                "car_model_id": 4,
                "vin": "AT-710-TL",
                # "color_id": 1,
            },
            {
                "student_id": 2,
                "car_model_id": 3,
                "vin": "CQ-346-RQ",
                # "color_id": 2,
            },
            {
                "student_id": 3,
                "car_model_id": 1,
                "vin": "RH-636-ZF",
                # "color_id": 2,
            },
            {
                "student_id": 4,
                "car_model_id": 8,
                "vin": "EH-174-JF",
                # "color_id": 2,
            },
            {
                "student_id": 5,
                "car_model_id": 11,
                "vin": "JH-743-ID",
                # "color_id": 2,
            },
            {
                "student_id": 6,
                "car_model_id": 9,
                "vin": "BS-638-AN",
                # "color_id": 2,
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("car", schema="carpool")
