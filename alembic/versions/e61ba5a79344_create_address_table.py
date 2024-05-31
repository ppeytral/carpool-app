"""create address table

Revision ID: e61ba5a79344
Revises: 
Create Date: 2024-05-11 11:30:42.355404

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e61ba5a79344"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    address_table = op.create_table(
        "address",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("street", sa.String()),
        sa.Column("postal_code", sa.String()),
        sa.Column("city", sa.String()),
        schema="carpool",
    )

    op.bulk_insert(
        address_table,
        [
            {
                "street": "13 impasse du flourege",
                "postal_code": "84000",
                "city": "Avignon",
            },
            {
                "street": "rue de la coquillade",
                "postal_code": "13540",
                "city": "Puyricard",
            },
            {
                "street": "rue de mon cul sur la commode",
                "postal_code": "84140",
                "city": "Montfavet",
            },
            {
                "street": "60, chemin de Fontanille",
                "postal_code": "84140",
                "city": "Avignon",
            },
            {
                "street": "180, rue Philippe de Girard",
                "postal_code": "84120",
                "city": "Pertuis",
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("address", schema="carpool")
