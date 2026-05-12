"""专业管理接口（管理员）"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.major import Major
from app.models.user import User
from app.core.deps import require_admin
from app.schemas.major import MajorCreate, MajorUpdate, MajorResponse
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/admin/majors", tags=["专业管理"])


@router.get("/", response_model=ApiResponse[list[MajorResponse]])
async def list_majors(db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    result = await db.execute(select(Major).order_by(Major.sort_order, Major.id))
    majors = result.scalars().all()
    return ApiResponse(data=[MajorResponse.model_validate(m) for m in majors])


@router.post("/", response_model=ApiResponse[MajorResponse])
async def create_major(
    req: MajorCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    major = Major(name=req.name, sort_order=0)
    db.add(major)
    await db.commit()
    await db.refresh(major)
    return ApiResponse(data=MajorResponse.model_validate(major))


@router.put("/{major_id}", response_model=ApiResponse[MajorResponse])
async def update_major(
    major_id: int,
    req: MajorUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    result = await db.execute(select(Major).where(Major.id == major_id))
    major = result.scalar_one_or_none()
    if not major:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="专业不存在")
    if req.name is not None:
        major.name = req.name
    await db.commit()
    await db.refresh(major)
    return ApiResponse(data=MajorResponse.model_validate(major))


@router.delete("/{major_id}", response_model=ApiResponse)
async def delete_major(
    major_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    result = await db.execute(select(Major).where(Major.id == major_id))
    major = result.scalar_one_or_none()
    if not major:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="专业不存在")
    await db.delete(major)
    await db.commit()
    return ApiResponse(message="删除成功")
