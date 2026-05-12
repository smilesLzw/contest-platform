"""add_work_type_and_bg_music

Revision ID: c1a2b3c4d5e6
Revises: 21abface10db
Create Date: 2026-05-12

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'c1a2b3c4d5e6'
down_revision: Union[str, Sequence[str], None] = '21abface10db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # works 表新增字段
    op.add_column('works', sa.Column('work_type', sa.String(20), nullable=True, comment='作品类型: music/graphic/video/website'))
    op.add_column('works', sa.Column('audio_url', sa.String(2048), nullable=True, comment='音频URL'))
    op.add_column('works', sa.Column('video_url', sa.String(2048), nullable=True, comment='视频URL'))
    op.add_column('works', sa.Column('embed_url', sa.String(2048), nullable=True, comment='嵌入链接'))
    op.add_column('works', sa.Column('gallery_urls', sa.Text, nullable=True, comment='图库JSON数组'))

    # 扩大现有 URL 字段
    op.alter_column('works', 'cover_url', existing_type=sa.String(500), type_=sa.String(2048), existing_nullable=True)
    op.alter_column('works', 'demo_url', existing_type=sa.String(500), type_=sa.String(2048), existing_nullable=True)
    op.alter_column('works', 'attachment_url', existing_type=sa.String(500), type_=sa.String(2048), existing_nullable=True)

    # 建背景音乐表
    op.create_table(
        'background_music',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(200), nullable=False, comment='曲目标题'),
        sa.Column('artist', sa.String(200), nullable=True, comment='艺术家/来源'),
        sa.Column('audio_url', sa.String(2048), nullable=False, comment='音频文件URL'),
        sa.Column('source', sa.String(20), nullable=False, server_default='preset', comment='preset管理员预置 / student学生作品'),
        sa.Column('work_id', sa.BigInteger(), nullable=True, comment='关联学生作品ID'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1'), comment='是否启用'),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0', comment='排序'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['work_id'], ['works.id'], ondelete='SET NULL'),
    )


def downgrade() -> None:
    op.drop_table('background_music')
    op.alter_column('works', 'attachment_url', existing_type=sa.String(2048), type_=sa.String(500), existing_nullable=True)
    op.alter_column('works', 'demo_url', existing_type=sa.String(2048), type_=sa.String(500), existing_nullable=True)
    op.alter_column('works', 'cover_url', existing_type=sa.String(2048), type_=sa.String(500), existing_nullable=True)
    op.drop_column('works', 'gallery_urls')
    op.drop_column('works', 'embed_url')
    op.drop_column('works', 'video_url')
    op.drop_column('works', 'audio_url')
    op.drop_column('works', 'work_type')
