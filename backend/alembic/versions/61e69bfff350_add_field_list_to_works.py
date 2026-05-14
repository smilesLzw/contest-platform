"""add field_list to works

Revision ID: 61e69bfff350
Revises: 52dce5a8b4f1
Create Date: 2026-05-13 16:56:25.294590

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision: str = "61e69bfff350"
down_revision: Union[str, Sequence[str], None] = "52dce5a8b4f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "works",
        "cover_url",
        existing_type=mysql.VARCHAR(collation="utf8mb4_unicode_ci", length=2048),
        comment="封面图",
        existing_nullable=True,
    )
    op.alter_column(
        "works",
        "demo_url",
        existing_type=mysql.VARCHAR(collation="utf8mb4_unicode_ci", length=2048),
        comment="演示链接",
        existing_nullable=True,
    )
    op.alter_column(
        "works",
        "attachment_url",
        existing_type=mysql.VARCHAR(collation="utf8mb4_unicode_ci", length=2048),
        comment="附件链接",
        existing_nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "works",
        "attachment_url",
        existing_type=mysql.VARCHAR(collation="utf8mb4_unicode_ci", length=2048),
        comment=None,
        existing_comment="附件链接",
        existing_nullable=True,
    )
    op.alter_column(
        "works",
        "demo_url",
        existing_type=mysql.VARCHAR(collation="utf8mb4_unicode_ci", length=2048),
        comment=None,
        existing_comment="演示链接",
        existing_nullable=True,
    )
    op.alter_column(
        "works",
        "cover_url",
        existing_type=mysql.VARCHAR(collation="utf8mb4_unicode_ci", length=2048),
        comment=None,
        existing_comment="封面图",
        existing_nullable=True,
    )
