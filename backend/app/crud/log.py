"""操作日志写入工具"""
import json
from datetime import datetime
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect
from app.models.operation_log import OperationLog


def model_snapshot(model: Any) -> dict:
    """把 SQLAlchemy 模型当前字段转成可写入 JSON 的快照。"""
    data = {}
    for column in inspect(model).mapper.column_attrs:
        value = getattr(model, column.key)
        data[column.key] = value.isoformat() if isinstance(value, datetime) else value
    return data


async def create_log(
    db: AsyncSession,
    user_id: int,
    action: str,
    target_type: str | None = None,
    target_id: int | None = None,
    detail: str | None = None,
    undo_data: dict | None = None,
    is_undoable: bool = False,
):
    """写入操作日志"""
    log = OperationLog(
        user_id=user_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        detail=detail,
        undo_data=json.dumps(undo_data, ensure_ascii=False) if undo_data else None,
        is_undoable=1 if is_undoable and undo_data else 0,
    )
    db.add(log)
    await db.commit()
