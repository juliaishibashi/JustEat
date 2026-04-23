"""add created_at to orders

Revision ID: 921ddd4ab100
Revises: 86e36e4dc83b
Create Date: 2026-04-23 01:04:08.846047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '921ddd4ab100'
down_revision: Union[str, Sequence[str], None] = '86e36e4dc83b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('orders', sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('orders', 'created_at')
