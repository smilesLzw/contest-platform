"""add_work_cover_variants

Revision ID: 52dce5a8b4f1
Revises: f9a0b1c2d3e4
Create Date: 2026-05-13

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "52dce5a8b4f1"
down_revision: Union[str, Sequence[str], None] = "f9a0b1c2d3e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _work_columns() -> dict[str, dict]:
    inspector = sa.inspect(op.get_bind())
    return {column["name"]: column for column in inspector.get_columns("works")}


def _ensure_text_column(name: str, comment: str) -> None:
    columns = _work_columns()
    if name in columns:
        op.alter_column(
            "works",
            name,
            existing_type=columns[name]["type"],
            type_=sa.Text(),
            existing_nullable=True,
            comment=comment,
            existing_comment=columns[name].get("comment"),
        )
        return

    op.add_column("works", sa.Column(name, sa.Text(), nullable=True, comment=comment))


def upgrade() -> None:
    _ensure_text_column("cover_original_url", "封面原图")
    _ensure_text_column("cover_card_url", "列表卡片封面")
    _ensure_text_column("cover_detail_url", "详情页封面")
    _ensure_text_column("cover_thumb_url", "缩略封面")
    _ensure_text_column("cover_crop_data", "封面裁剪参数JSON")


def downgrade() -> None:
    columns = _work_columns()
    for name in (
        "cover_crop_data",
        "cover_thumb_url",
        "cover_detail_url",
        "cover_card_url",
        "cover_original_url",
    ):
        if name in columns:
            op.drop_column("works", name)
