"""操作日志写入工具"""
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.operation_log import OperationLog


async def create_log(
    db: AsyncSession,
    user_id: int,
    action: str,
    target_type: str | None = None,
    target_id: int | None = None,
    detail: str | None = None,
):
    """写入操作日志"""
    log = OperationLog(
        user_id=user_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        detail=detail,
    )
    db.add(log)
    await db.commit()
