"""create car_make table

Revision ID: df013fe4961b
Revises: dc5896a5e31f
Create Date: 2024-05-12 21:28:32.492774

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "df013fe4961b"
down_revision: Union[str, None] = "dc5896a5e31f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    car_make_table = op.create_table(
        "car_make",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String()),
        schema="carpool",
    )

    op.bulk_insert(
        car_make_table,
        [
            {
                "name": "Citroen",
            },
            {
                "name": "Peugeot",
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("car_make", schema="carpool")
