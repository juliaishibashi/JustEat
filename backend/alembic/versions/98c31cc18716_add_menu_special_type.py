"""add menu special type

Revision ID: 98c31cc18716
Revises: 5cbd957f177e
Create Date: 2026-04-20 05:23:19.283047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from enum import Enum

# revision identifiers, used by Alembic.
revision: str = '98c31cc18716'
down_revision: Union[str, Sequence[str], None] = '5cbd957f177e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


menu_special_type = sa.Enum(
    "NONE",
    "TODAYS_SPECIAL",
    "DEAL_OF_THE_DAY",
    name="menu_special_type",
)

def upgrade():
    menu_special_type.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "menus",
        sa.Column(
            "special_type",
            menu_special_type,
            nullable=False,
            server_default="NONE",
        ),
    )

def downgrade():
    op.drop_column("menus", "special_type")
    menu_special_type.drop(op.get_bind(), checkfirst=True)