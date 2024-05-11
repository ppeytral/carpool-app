"""create user table

Revision ID: dc5896a5e31f
Revises: d9c0cd73f52f
Create Date: 2024-05-11 20:40:03.758415

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dc5896a5e31f"
down_revision: Union[str, None] = "d9c0cd73f52f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_table = op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("student_id", sa.Integer()),
        sa.Column("username", sa.String()),
        sa.Column("password", sa.String()),
        sa.Column("is_active", sa.Boolean()),
        schema="carpool",
    )

    op.bulk_insert(
        user_table,
        [
            {
                "student_id": 1,
                "username": "ppeytral",
                "password": "skarhead0410",
                "is_active": True,
            },
            {
                "student_id": 2,
                "username": "rvasseur",
                "password": "16071988",
                "is_active": True,
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("user", schema="carpool")
