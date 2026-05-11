"""AI工具分类模型"""
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class AiCategory(Base):
    __tablename__ = "ai_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="分类名称")
    icon: Mapped[str] = mapped_column(String(50), nullable=True, comment="Element Plus图标名")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序")
