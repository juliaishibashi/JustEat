"""add menu detail

Revision ID: 86e36e4dc83b
Revises: 98c31cc18716
Create Date: 2026-04-20 05:42:24.076895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86e36e4dc83b'
down_revision: Union[str, Sequence[str], None] = '98c31cc18716'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "menus",
        sa.Column("detail", sa.String(), nullable=True)
    )

def downgrade():
    op.drop_column("menus", "detail")
