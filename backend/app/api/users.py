"""用户管理接口（仅管理员）"""
import math
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from app.database import get_db
from app.models.user import User
from app.core.deps import require_admin
from app.core.security import hash_password
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.common import ApiResponse, PageData
from app.crud.log import create_log

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("/teachers")
async def list_teachers(db: AsyncSession = Depends(get_db)):
    """教师下拉列表（公开）"""
    result = await db.execute(
        select(User.id, User.name).where(User.role.in_(["teacher", "admin"]), User.status == 1).order_by(User.name)
    )
    rows = result.all()
    return ApiResponse(data=[{"id": r[0], "name": r[1]} for r in rows])


@router.get("/", response_model=ApiResponse[PageData[UserResponse]])
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """教师列表"""
    query = select(User).where(User.role == "teacher").order_by(desc(User.created_at))

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    users = result.scalars().all()

    return ApiResponse(data=PageData(
        items=[UserResponse.model_validate(u) for u in users],
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if page_size > 0 else 0,
    ))


@router.post("/", response_model=ApiResponse[UserResponse])
async def create_user(
    req: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """创建教师账号"""
    # 检查工号是否已存在
    result = await db.execute(select(User).where(User.username == req.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="工号已存在")

    user = User(
        username=req.username,
        password_hash=hash_password(req.password),
        name=req.name,
        department=req.department,
        role="teacher",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    await create_log(db, current_user.id, "create_user", "user", user.id, f"创建教师账号: {user.name}")
    return ApiResponse(data=UserResponse.model_validate(user))


@router.put("/{user_id}", response_model=ApiResponse[UserResponse])
async def update_user(
    user_id: int,
    req: UserUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """编辑教师信息"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    if req.name is not None:
        user.name = req.name
    if req.department is not None:
        user.department = req.department
    await db.commit()
    await db.refresh(user)
    return ApiResponse(data=UserResponse.model_validate(user))


@router.put("/{user_id}/status", response_model=ApiResponse[UserResponse])
async def toggle_user_status(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """启用/禁用账号"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    if user.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="不能禁用自己")
    user.status = 0 if user.status == 1 else 1
    await db.commit()
    await db.refresh(user)
    action = "禁用" if user.status == 0 else "启用"
    await create_log(db, current_user.id, f"{action}用户", "user", user_id, f"{action}账号: {user.name}")
    return ApiResponse(data=UserResponse.model_validate(user))


@router.put("/{user_id}/reset-password", response_model=ApiResponse)
async def reset_password(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """重置密码为默认密码"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    default_password = "Teacher@123"
    user.password_hash = hash_password(default_password)
    await db.commit()
    await create_log(db, current_user.id, "reset_password", "user", user_id, f"重置密码: {user.name}")
    return ApiResponse(message=f"密码已重置为: {default_password}")
