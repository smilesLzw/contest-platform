"""用户模型"""
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Enum, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="工号/账号")
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(Enum("admin", "teacher"), nullable=False, comment="角色")
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="真实姓名")
    department: Mapped[str] = mapped_column(String(100), nullable=True, comment="所属院系")
    avatar_url: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[int] = mapped_column(SmallInteger, default=1, comment="1启用 0禁用")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
