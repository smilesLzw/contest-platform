"""赛事管理接口"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.database import get_db
from app.models.competition import Competition
from app.models.user import User
from app.core.deps import require_admin
from app.schemas.competition import CompetitionCreate, CompetitionUpdate, CompetitionResponse
from app.schemas.common import ApiResponse

router = APIRouter(tags=["赛事管理"])


@router.get("/competitions", response_model=ApiResponse[list[CompetitionResponse]])
async def list_active_competitions(db: AsyncSession = Depends(get_db)):
    """获取当前启用的赛事（按时间倒序，老师选赛事用）"""
    result = await db.execute(
        select(Competition)
        .where(Competition.is_active == True)
        .order_by(desc(Competition.academic_year), desc(Competition.semester), desc(Competition.created_at))
    )
    competitions = result.scalars().all()
    return ApiResponse(data=[CompetitionResponse.model_validate(c) for c in competitions])


@router.get("/admin/competitions", response_model=ApiResponse[list[CompetitionResponse]])
async def list_all_competitions(db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    """管理员查看所有赛事"""
    result = await db.execute(
        select(Competition).order_by(desc(Competition.academic_year), desc(Competition.semester))
    )
    competitions = result.scalars().all()
    return ApiResponse(data=[CompetitionResponse.model_validate(c) for c in competitions])


@router.post("/admin/competitions", response_model=ApiResponse[CompetitionResponse])
async def create_competition(
    req: CompetitionCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """管理员创建赛事"""
    competition = Competition(
        name=req.name,
        academic_year=req.academic_year,
        semester=req.semester,
    )
    db.add(competition)
    await db.commit()
    await db.refresh(competition)
    return ApiResponse(data=CompetitionResponse.model_validate(competition))


@router.put("/admin/competitions/{competition_id}", response_model=ApiResponse[CompetitionResponse])
async def update_competition(
    competition_id: int,
    req: CompetitionUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """管理员编辑赛事"""
    result = await db.execute(select(Competition).where(Competition.id == competition_id))
    competition = result.scalar_one_or_none()
    if not competition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="赛事不存在")
    if req.name is not None:
        competition.name = req.name
    if req.academic_year is not None:
        competition.academic_year = req.academic_year
    if req.semester is not None:
        competition.semester = req.semester
    await db.commit()
    await db.refresh(competition)
    return ApiResponse(data=CompetitionResponse.model_validate(competition))


@router.delete("/admin/competitions/{competition_id}", response_model=ApiResponse)
async def delete_competition(
    competition_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """管理员删除赛事"""
    result = await db.execute(select(Competition).where(Competition.id == competition_id))
    competition = result.scalar_one_or_none()
    if not competition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="赛事不存在")
    await db.delete(competition)
    await db.commit()
    return ApiResponse(message="删除成功")


@router.put("/admin/competitions/{competition_id}/toggle", response_model=ApiResponse[CompetitionResponse])
async def toggle_competition(
    competition_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """管理员启用/禁用赛事"""
    result = await db.execute(select(Competition).where(Competition.id == competition_id))
    competition = result.scalar_one_or_none()
    if not competition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="赛事不存在")
    competition.is_active = not competition.is_active
    await db.commit()
    await db.refresh(competition)
    return ApiResponse(data=CompetitionResponse.model_validate(competition))
