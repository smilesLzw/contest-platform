"""专业模型"""
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Major(Base):
    __tablename__ = "majors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    grade: Mapped[str] = mapped_column(String(20), nullable=False, default="", comment="年级，如2022级")
    duration: Mapped[str] = mapped_column(String(10), nullable=False, default="", comment="学制：三年制/五年制")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="专业名称")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序")
