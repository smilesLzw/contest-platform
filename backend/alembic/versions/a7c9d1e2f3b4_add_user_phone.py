"""add user phone

Revision ID: a7c9d1e2f3b4
Revises: 52dce5a8b4f1
Create Date: 2026-05-13 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a7c9d1e2f3b4"
down_revision: Union[str, Sequence[str], None] = "52dce5a8b4f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("phone", sa.String(length=30), nullable=True, comment="联系电话"))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "phone")
