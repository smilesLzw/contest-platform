"""背景音乐模型"""
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class BackgroundMusic(Base):
    __tablename__ = "background_music"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="曲目标题")
    artist: Mapped[str] = mapped_column(String(200), nullable=True, comment="艺术家/来源")
    audio_url: Mapped[str] = mapped_column(String(2048), nullable=False, comment="音频文件URL")
    source: Mapped[str] = mapped_column(
        String(20), nullable=False, default="preset", comment="preset管理员预置 / student学生作品"
    )
    work_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("works.id", ondelete="SET NULL"), nullable=True, comment="关联学生作品ID"
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, comment="是否启用")
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="排序")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
