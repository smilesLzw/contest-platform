"""赛事模型"""
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Boolean, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Competition(Base):
    __tablename__ = "competitions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="赛事名称")
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False, comment="学年")
    semester: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="1上 2下")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否启用")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
