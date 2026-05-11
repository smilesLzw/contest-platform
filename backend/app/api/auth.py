"""认证接口"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.deps import get_current_user
from app.schemas.auth import (
    LoginRequest, LoginResponse, UserInfo,
    UpdateProfileRequest, ChangePasswordRequest,
)
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=ApiResponse[LoginResponse])
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    """用户登录"""
    result = await db.execute(select(User).where(User.username == req.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="账号或密码错误")
    if user.status == 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="账号已被禁用")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return ApiResponse(data=LoginResponse(
        access_token=token,
        user=UserInfo.model_validate(user),
    ))


@router.get("/me", response_model=ApiResponse[UserInfo])
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return ApiResponse(data=UserInfo.model_validate(current_user))


@router.put("/me", response_model=ApiResponse[UserInfo])
async def update_me(
    req: UpdateProfileRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """修改个人信息"""
    if req.name is not None:
        current_user.name = req.name
    if req.department is not None:
        current_user.department = req.department
    if req.avatar_url is not None:
        current_user.avatar_url = req.avatar_url
    await db.commit()
    await db.refresh(current_user)
    return ApiResponse(data=UserInfo.model_validate(current_user))


@router.put("/me/password", response_model=ApiResponse)
async def change_password(
    req: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """修改密码"""
    if not verify_password(req.old_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="原密码错误")
    # 校验新密码复杂度
    if not any(c.isalpha() for c in req.new_password) or not any(c.isdigit() for c in req.new_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="密码需包含字母和数字")
    current_user.password_hash = hash_password(req.new_password)
    await db.commit()
    return ApiResponse(message="密码修改成功")
