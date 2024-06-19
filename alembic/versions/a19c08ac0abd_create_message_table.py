"""create message table

Revision ID: a19c08ac0abd
Revises: 1b024f3d7be2
Create Date: 2024-06-19 08:19:23.128161

"""

from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a19c08ac0abd"
down_revision: Union[str, None] = "1b024f3d7be2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    message_table = op.create_table(
        "message",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "sender_id",
            sa.Integer(),
            sa.ForeignKey(
                column="carpool.student.id",
                name="sender_fk",
                ondelete="CASCADE",
                onupdate="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "recipient_id",
            sa.Integer(),
            sa.ForeignKey(
                column="carpool.student.id",
                name="recipient_fk",
                ondelete="CASCADE",
                onupdate="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column("message", sa.String()),
        sa.Column("created_at", sa.DateTime(timezone=True)),
        schema="carpool",
    )

    op.bulk_insert(
        message_table,
        [
            {
                "sender_id": 1,
                "recipient_id": 2,
                "message": "Salut Raph!",
                "created_at": datetime(2024, 6, 19, 8, 32),
            },
            {
                "sender_id": 2,
                "recipient_id": 1,
                "message": "Coucou Patrice",
                "created_at": datetime(2024, 6, 19, 8, 33),
            },
            {
                "sender_id": 1,
                "recipient_id": 2,
                "message": "Ca va ?",
                "created_at": datetime(2024, 6, 19, 8, 34),
            },
            {
                "sender_id": 2,
                "recipient_id": 1,
                "message": "Oui et toi ?",
                "created_at": datetime(2024, 6, 19, 8, 35),
            },
        ],
    )


def downgrade() -> None:
    op.drop_table(
        "message",
        schema="carpool",
    )
