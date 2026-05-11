"""新闻模型"""
from datetime import datetime
from sqlalchemy import (
    String, Integer, DateTime, Text, SmallInteger, Enum, ForeignKey
)
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="标题")
    content: Mapped[str] = mapped_column(Text, nullable=True, comment="Markdown内容")
    cover_url: Mapped[str] = mapped_column(String(500), nullable=True, comment="封面图")
    category: Mapped[str] = mapped_column(
        Enum("tutorial", "tech", "lab"), default="tutorial",
        comment="分类：tutorial教程指南 tech科技前沿 lab教研室动态"
    )
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, comment="作者ID")
    status: Mapped[str] = mapped_column(
        Enum("draft", "published"), default="draft", comment="状态"
    )
    is_top: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否置顶")
    published_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关联
    author: Mapped[Optional["User"]] = relationship("User", lazy="joined")
