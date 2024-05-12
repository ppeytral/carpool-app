"""create car_model_table table

Revision ID: 4468bb21356e
Revises: df013fe4961b
Create Date: 2024-05-12 21:33:59.046399

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4468bb21356e"
down_revision: Union[str, None] = "df013fe4961b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    car_model_table = op.create_table(
        "car_model",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "car_make_id",
            sa.Integer(),
            sa.ForeignKey(
                "carpool.car_make.id", ondelete="CASCADE", onupdate="CASCADE"
            ),
        ),
        sa.Column("model_name", sa.String()),
        sa.Column("capacity", sa.Integer()),
        schema="carpool",
    )

    op.bulk_insert(
        car_model_table,
        [
            {
                "car_make_id": 1,
                "model_name": "C3",
                "capacity": 4,
            },
            {
                "car_make_id": 2,
                "model_name": "208",
                "capacity": 4,
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("car_model", schema="carpool")
