"""seed restaurants

Revision ID: de81b977954e
Revises: 9521aa45bfef
Create Date: 2026-04-19 05:08:54.242196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de81b977954e'
down_revision: Union[str, Sequence[str], None] = '9521aa45bfef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO restaurants (name, location, cuisine, owner_id)
        VALUES
            ('Restaurant A', 'Location A', 'Cuisine A', 2),
            ('Restaurant B', 'Location B', 'Cuisine B', 2),
            ('Restaurant C', 'Location C', 'Cuisine C', 2);
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM restaurants
        WHERE name IN ('Restaurant A', 'Restaurant B', 'Restaurant C');
        """
    )