"""add_major_fields

Revision ID: e8f9a0b1c2d3
Revises: d7e8f9a0b1c2
Create Date: 2026-05-12

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "e8f9a0b1c2d3"
down_revision: Union[str, None] = "d7e8f9a0b1c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("majors", sa.Column("grade", sa.String(20), nullable=False, server_default="", comment="年级，如2022级"))
    op.add_column("majors", sa.Column("duration", sa.String(10), nullable=False, server_default="", comment="学制：三年制/五年制"))


def downgrade() -> None:
    op.drop_column("majors", "duration")
    op.drop_column("majors", "grade")
