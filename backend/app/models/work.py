"""作品模型"""
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    String, Integer, DateTime, Text, SmallInteger, Enum, ForeignKey, BigInteger
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Work(Base):
    __tablename__ = "works"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, comment="作品名称")
    author_names: Mapped[str] = mapped_column(String(200), nullable=False, comment="参赛学生姓名，逗号分隔")
    guide_teacher: Mapped[str] = mapped_column(String(100), nullable=True, comment="指导教师")
    major_id: Mapped[int] = mapped_column(Integer, ForeignKey("majors.id"), nullable=True, comment="专业ID")
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False, comment="学年，如2024-2025")
    semester: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="1上学期 2下学期")
    contest_name: Mapped[str] = mapped_column(String(200), nullable=True, comment="赛事名称")
    award: Mapped[str] = mapped_column(String(50), nullable=True, comment="获奖情况")
    cover_url: Mapped[str] = mapped_column(String(500), nullable=True, comment="封面图")
    content: Mapped[str] = mapped_column(Text, nullable=True, comment="Markdown内容")
    demo_url: Mapped[str] = mapped_column(String(500), nullable=True, comment="演示链接")
    attachment_url: Mapped[str] = mapped_column(String(500), nullable=True, comment="附件链接")
    status: Mapped[str] = mapped_column(
        Enum("draft", "published", "archived"), default="draft", comment="状态"
    )
    publisher_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, comment="发布者ID")
    published_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关联
    major: Mapped[Optional["Major"]] = relationship("Major", lazy="joined")
    publisher: Mapped[Optional["User"]] = relationship("User", lazy="joined")
