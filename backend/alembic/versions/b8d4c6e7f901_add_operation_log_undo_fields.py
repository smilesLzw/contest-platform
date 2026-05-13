"""add operation log undo fields

Revision ID: b8d4c6e7f901
Revises: a7c9d1e2f3b4
Create Date: 2026-05-13 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b8d4c6e7f901"
down_revision: Union[str, Sequence[str], None] = "a7c9d1e2f3b4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("operation_logs", sa.Column("undo_data", sa.Text(), nullable=True, comment="撤销数据JSON"))
    op.add_column("operation_logs", sa.Column("is_undoable", sa.SmallInteger(), nullable=True, server_default="0", comment="是否可撤销"))
    op.add_column("operation_logs", sa.Column("undone_at", sa.DateTime(), nullable=True, comment="撤销时间"))
    op.add_column("operation_logs", sa.Column("undone_by", sa.Integer(), nullable=True, comment="撤销用户ID"))
    op.create_foreign_key("fk_operation_logs_undone_by_users", "operation_logs", "users", ["undone_by"], ["id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_operation_logs_undone_by_users", "operation_logs", type_="foreignkey")
    op.drop_column("operation_logs", "undone_by")
    op.drop_column("operation_logs", "undone_at")
    op.drop_column("operation_logs", "is_undoable")
    op.drop_column("operation_logs", "undo_data")
