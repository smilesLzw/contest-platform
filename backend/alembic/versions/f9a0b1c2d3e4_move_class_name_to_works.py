"""move_class_name_to_works

Revision ID: f9a0b1c2d3e4
Revises: e8f9a0b1c2d3
Create Date: 2026-05-12

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "f9a0b1c2d3e4"
down_revision: Union[str, None] = "e8f9a0b1c2d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("majors", "class_name")
    op.add_column("works", sa.Column("class_name", sa.String(20), nullable=True, comment="班级，如一班"))


def downgrade() -> None:
    op.drop_column("works", "class_name")
    op.add_column("majors", sa.Column("class_name", sa.String(20), nullable=False, server_default="", comment="班级，如一班"))
