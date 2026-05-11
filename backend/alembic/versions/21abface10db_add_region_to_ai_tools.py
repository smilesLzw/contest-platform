"""add_region_to_ai_tools

Revision ID: 21abface10db
Revises: b60ed5edaa3f
Create Date: 2026-04-29 20:25:51.877445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21abface10db'
down_revision: Union[str, Sequence[str], None] = 'b60ed5edaa3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'ai_tools',
        sa.Column(
            'region',
            sa.String(20),
            nullable=False,
            server_default='domestic',
            comment='区域：domestic国内 / international国外'
        )
    )


def downgrade() -> None:
    op.drop_column('ai_tools', 'region')
