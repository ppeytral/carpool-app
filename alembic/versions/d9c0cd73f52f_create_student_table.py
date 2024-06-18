"""create student table

Revision ID: d9c0cd73f52f
Revises: dd1a1864e19b
Create Date: 2024-05-11 14:20:45.866038

"""

from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d9c0cd73f52f"
down_revision: Union[str, None] = "dd1a1864e19b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    student_table = op.create_table(
        "student",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("firstname", sa.String()),
        sa.Column("lastname", sa.String()),
        sa.Column("email", sa.String()),
        sa.Column("driving_licence_nb", sa.String()),
        sa.Column("driving_licence_validity", sa.DateTime()),
        sa.Column(
            "address_id",
            sa.Integer(),
            sa.ForeignKey(
                "carpool.address.id",
                ondelete="CASCADE",
                onupdate="CASCADE",
            ),
        ),
        sa.Column(
            "school_id",
            sa.Integer(),
            sa.ForeignKey(
                "carpool.school.id",
                ondelete="CASCADE",
                onupdate="CASCADE",
            ),
        ),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
        schema="carpool",
    )

    op.bulk_insert(
        student_table,
        [
            {
                "firstname": "Patrice",
                "lastname": "Peytral",
                "email": "p.peytral@gmail.com",
                "password": "password",
                "driving_licence_nb": "13224",
                "driving_licence_validity": datetime.now(),
                "address_id": 1,
                "school_id": 1,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
            {
                "firstname": "Raphaelle",
                "lastname": "Vasseur",
                "email": "r.vasseur@gmail.com",
                "password": "16071988",
                "driving_licence_nb": "235663",
                "driving_licence_validity": datetime.now(),
                "address_id": 2,
                "school_id": 2,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
            {
                "firstname": "Clément",
                "lastname": "Couturier",
                "email": "ouliwliw@gmail.com",
                "password": "password",
                "driving_licence_nb": "123456789",
                "driving_licence_validity": datetime.now(),
                "address_id": 3,
                "school_id": 1,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
            {
                "firstname": "Julien",
                "lastname": "Peytral",
                "email": "jpeytral@gmail.com",
                "password": "password",
                "driving_licence_nb": "123456789",
                "driving_licence_validity": datetime.now(),
                "address_id": 4,
                "school_id": 1,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
            {
                "firstname": "Caroline",
                "lastname": "Onderbeke",
                "email": "caro@gmail.com",
                "password": "password",
                "driving_licence_nb": "123456789",
                "driving_licence_validity": datetime.now(),
                "address_id": 5,
                "school_id": 2,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
            {
                "firstname": "Alix",
                "lastname": "Tournier",
                "email": "atournier@gmail.com",
                "password": "password",
                "driving_licence_nb": "123456789",
                "driving_licence_validity": datetime.now(),
                "address_id": 6,
                "school_id": 2,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("student", schema="carpool")
