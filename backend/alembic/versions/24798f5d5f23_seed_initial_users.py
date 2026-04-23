"""seed initial users

Revision ID: 24798f5d5f23
Revises: 5b17f90d6c3c
Create Date: 2026-04-14 08:48:29.581204

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from passlib.context import CryptContext


# revision identifiers, used by Alembic.
revision: str = '24798f5d5f23'
down_revision: Union[str, Sequence[str], None] = '5b17f90d6c3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _hash_password(password: str) -> str:
    return pwd_context.hash(password)

def upgrade() -> None:
    bind = op.get_bind()
    customer_hash = _hash_password("customer123")
    owner_hash = _hash_password("owner123")

    bind.execute(
       sa.text("INSERT INTO users (email, hashed_password, name, role) VALUES "
        "(:email, :hash, :name, :role)"),
        {"email": "customer@test.com", "hash": customer_hash, "name": "Test Customer", "role": "CUSTOMER"}
    )
    
    bind.execute(
        sa.text("INSERT INTO users (email, hashed_password, name, role) VALUES "
        "(:email, :hash, :name, :role)"),
        {"email": "owner@test.com", "hash": owner_hash, "name": "Restaurant Owner", "role": "RESTAURANT_OWNER"}
    )

def downgrade() -> None:
    bind = op.get_bind()
    bind.execute(sa.text("DELETE FROM users WHERE email IN (:c1, :c2)"), {"c1": "customer@test.com", "c2": "owner@test.com"})