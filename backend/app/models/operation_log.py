"""操作日志模型"""
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class OperationLog(Base):
    __tablename__ = "operation_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, comment="操作用户ID")
    action: Mapped[str] = mapped_column(String(100), nullable=False, comment="操作类型")
    target_type: Mapped[str] = mapped_column(String(50), nullable=True, comment="操作对象类型")
    target_id: Mapped[int] = mapped_column(Integer, nullable=True, comment="操作对象ID")
    detail: Mapped[str] = mapped_column(Text, nullable=True, comment="详情")
    undo_data: Mapped[str | None] = mapped_column(Text, nullable=True, comment="撤销数据JSON")
    is_undoable: Mapped[int] = mapped_column(SmallInteger, default=0, comment="是否可撤销")
    undone_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="撤销时间")
    undone_by: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, comment="撤销用户ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
