"""enum order status

Revision ID: 5cbd957f177e
Revises: 6a73df4e9d9d
Create Date: 2026-04-20 05:11:27.125523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5cbd957f177e'
down_revision: Union[str, Sequence[str], None] = '6a73df4e9d9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
