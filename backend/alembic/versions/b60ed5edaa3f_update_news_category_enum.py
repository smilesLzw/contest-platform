"""update_news_category_enum

Revision ID: b60ed5edaa3f
Revises: e85e4565cafc
Create Date: 2026-04-29 18:46:34.350413

将 news.category 枚举值从 contest/notice/honor/other 改为 tutorial/tech/lab
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b60ed5edaa3f'
down_revision: Union[str, Sequence[str], None] = 'e85e4565cafc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. 先扩展 ENUM 加入新值（保留旧值，否则 UPDATE 会失败）
    op.execute(
        "ALTER TABLE news MODIFY COLUMN category "
        "ENUM('contest','notice','honor','other','tutorial','tech','lab') "
        "NOT NULL DEFAULT 'tutorial' "
        "COMMENT '分类（过渡）'"
    )

    # 2. 迁移已有数据
    op.execute(
        "UPDATE news SET category = 'lab' "
        "WHERE category IN ('contest', 'notice', 'honor', 'other')"
    )

    # 3. 收缩 ENUM 只保留新值
    op.execute(
        "ALTER TABLE news MODIFY COLUMN category "
        "ENUM('tutorial','tech','lab') "
        "NOT NULL DEFAULT 'tutorial' "
        "COMMENT '分类：tutorial教程指南 tech科技前沿 lab教研室动态'"
    )


def downgrade() -> None:
    # 1. 扩展 ENUM 加入旧值
    op.execute(
        "ALTER TABLE news MODIFY COLUMN category "
        "ENUM('tutorial','tech','lab','contest','notice','honor','other') "
        "NOT NULL DEFAULT 'tutorial' "
        "COMMENT '分类（过渡）'"
    )

    # 2. 所有新分类数据映射回 other
    op.execute(
        "UPDATE news SET category = 'other' "
        "WHERE category IN ('tutorial', 'tech', 'lab')"
    )

    # 3. 收缩 ENUM 只保留旧值
    op.execute(
        "ALTER TABLE news MODIFY COLUMN category "
        "ENUM('contest','notice','honor','other') "
        "NOT NULL DEFAULT 'contest' "
        "COMMENT '分类：contest赛事报道 notice活动通知 honor荣誉展示 other其他'"
    )
