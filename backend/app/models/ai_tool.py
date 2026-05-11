"""AI工具模型"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, SmallInteger, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class AiTool(Base):
    __tablename__ = "ai_tools"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="工具名称")
    logo_url: Mapped[str] = mapped_column(String(500), nullable=True, comment="Logo URL")
    url: Mapped[str] = mapped_column(String(500), nullable=False, comment="官网链接")
    description: Mapped[str] = mapped_column(String(300), nullable=True, comment="简介")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("ai_categories.id"), nullable=True, comment="分类ID")
    is_free: Mapped[int] = mapped_column(SmallInteger, default=1, comment="1免费 0付费")
    rating: Mapped[int] = mapped_column(SmallInteger, default=5, comment="评分1-5")
    region: Mapped[str] = mapped_column(String(20), default="domestic", comment="区域：domestic国内 / international国外")
    is_featured: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否精选")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # 关联
    category: Mapped[Optional["AiCategory"]] = relationship("AiCategory", lazy="joined")
