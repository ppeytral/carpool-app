"""create admin history table

Revision ID: 18fd1412dc26
Revises: a19c08ac0abd
Create Date: 2024-06-30 14:03:35.729413

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "18fd1412dc26"
down_revision: Union[str, None] = "a19c08ac0abd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "personal_data_history",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            autoincrement=True,
        ),
        sa.Column(
            "admin_id",
            sa.Integer(),
            sa.ForeignKey(
                "carpool.student.id",
                onupdate="CASCADE",
            ),
            nullable=False,
        ),
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
        sa.Column("operation", sa.String(), nullable=False),
        sa.Column("datetime", sa.DateTime(timezone=True)),
        schema="carpool",
    )


def downgrade() -> None:
    op.drop_table(
        "personal_data_history",
        schema="carpool",
    )
