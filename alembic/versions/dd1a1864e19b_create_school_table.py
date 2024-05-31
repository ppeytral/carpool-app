"""create school table

Revision ID: dd1a1864e19b
Revises: e61ba5a79344
Create Date: 2024-05-11 12:10:10.226747

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dd1a1864e19b"
down_revision: Union[str, None] = "e61ba5a79344"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    school_table = op.create_table(
        "school",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String()),
        sa.Column(
            "address_id",
            sa.Integer(),
            sa.ForeignKey("carpool.address.id", ondelete="CASCADE"),
        ),
        schema="carpool",
    )

    op.bulk_insert(
        school_table,
        [
            {
                "name": "Nextech Avignon",
                "address_id": 4,
            },
            {
                "name": "Nextech Pertuis",
                "address_id": 5,
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("school", schema="carpool")
