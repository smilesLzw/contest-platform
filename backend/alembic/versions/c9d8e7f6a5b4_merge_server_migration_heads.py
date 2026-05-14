"""merge server migration heads

Revision ID: c9d8e7f6a5b4
Revises: b8d4c6e7f901, 61e69bfff350
Create Date: 2026-05-14 09:12:00.000000

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "c9d8e7f6a5b4"
down_revision: Union[str, Sequence[str], None] = ("b8d4c6e7f901", "61e69bfff350")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Merge migration branches."""
    pass


def downgrade() -> None:
    """Unmerge migration branches."""
    pass
