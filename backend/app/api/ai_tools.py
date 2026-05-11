"""AI工具接口"""
import math
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc, func
from sqlalchemy.orm import joinedload
from fastapi.security import HTTPAuthorizationCredentials

from app.database import get_db
from app.models.ai_tool import AiTool
from app.models.ai_category import AiCategory
from app.models.user import User
from app.core.deps import get_optional_user, require_admin
from app.schemas.ai_tool import (
    AiCategoryCreate, AiCategoryUpdate, AiCategoryResponse,
    AiToolCreate, AiToolUpdate, AiToolResponse,
)
from app.schemas.common import ApiResponse, PageData
from app.crud.log import create_log

router = APIRouter(prefix="/ai-tools", tags=["AI工具"])


# ---------- 分类接口 ----------

@router.get("/categories", response_model=ApiResponse[list[AiCategoryResponse]])
async def list_categories(db: AsyncSession = Depends(get_db)):
    """获取所有分类"""
    result = await db.execute(select(AiCategory).order_by(asc(AiCategory.sort_order)))
    categories = result.scalars().all()
    return ApiResponse(data=[AiCategoryResponse.model_validate(c) for c in categories])


@router.post("/categories", response_model=ApiResponse[AiCategoryResponse])
async def create_category(
    req: AiCategoryCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """新建分类"""
    cat = AiCategory(name=req.name, icon=req.icon, sort_order=req.sort_order)
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return ApiResponse(data=AiCategoryResponse.model_validate(cat))


@router.put("/categories/{cat_id}", response_model=ApiResponse[AiCategoryResponse])
async def update_category(
    cat_id: int,
    req: AiCategoryUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """编辑分类"""
    result = await db.execute(select(AiCategory).where(AiCategory.id == cat_id))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="分类不存在")
    cat.name = req.name
    cat.icon = req.icon
    cat.sort_order = req.sort_order
    await db.commit()
    await db.refresh(cat)
    return ApiResponse(data=AiCategoryResponse.model_validate(cat))


@router.delete("/categories/{cat_id}", response_model=ApiResponse)
async def delete_category(
    cat_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """删除分类"""
    result = await db.execute(select(AiCategory).where(AiCategory.id == cat_id))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="分类不存在")
    await db.delete(cat)
    await db.commit()
    return ApiResponse(message="删除成功")


# ---------- 工具接口 ----------

def _tool_to_response(tool: AiTool) -> AiToolResponse:
    return AiToolResponse(
        id=tool.id,
        name=tool.name,
        logo_url=tool.logo_url,
        url=tool.url,
        description=tool.description,
        category_id=tool.category_id,
        category_name=tool.category.name if tool.category else None,
        region=tool.region,
        is_free=tool.is_free,
        rating=tool.rating,
        is_featured=tool.is_featured,
        sort_order=tool.sort_order,
        created_at=tool.created_at,
    )


@router.get("/", response_model=ApiResponse[PageData[AiToolResponse]])
async def list_tools(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    region: str | None = None,
    is_free: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    """工具列表：按 sort_order 排序，支持分页、按区域和免费/付费筛选"""
    base = select(AiTool).options(joinedload(AiTool.category))
    if region:
        base = base.where(AiTool.region == region)
    if is_free is not None:
        base = base.where(AiTool.is_free == is_free)

    # total count
    count_q = select(func.count()).select_from(base.subquery())
    total = (await db.execute(count_q)).scalar() or 0

    # data
    data_q = base.order_by(asc(AiTool.sort_order), asc(AiTool.id))
    data_q = data_q.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(data_q)
    tools = result.unique().scalars().all()

    return ApiResponse(data=PageData(
        items=[_tool_to_response(t) for t in tools],
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if page_size > 0 else 0,
    ))


@router.post("/", response_model=ApiResponse[AiToolResponse])
async def create_tool(
    req: AiToolCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """新建工具"""
    tool = AiTool(**req.model_dump())
    db.add(tool)
    await db.commit()
    await db.refresh(tool)
    await create_log(db, current_user.id, "create_ai_tool", "ai_tool", tool.id, f"新增AI工具: {tool.name}")
    return ApiResponse(data=_tool_to_response(tool))


@router.put("/{tool_id}", response_model=ApiResponse[AiToolResponse])
async def update_tool(
    tool_id: int,
    req: AiToolUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """编辑工具"""
    result = await db.execute(
        select(AiTool).options(joinedload(AiTool.category)).where(AiTool.id == tool_id)
    )
    tool = result.unique().scalar_one_or_none()
    if not tool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="工具不存在")
    for field, value in req.model_dump().items():
        setattr(tool, field, value)
    await db.commit()
    await db.refresh(tool)
    return ApiResponse(data=_tool_to_response(tool))


@router.delete("/{tool_id}", response_model=ApiResponse)
async def delete_tool(
    tool_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """删除工具"""
    result = await db.execute(select(AiTool).where(AiTool.id == tool_id))
    tool = result.scalar_one_or_none()
    if not tool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="工具不存在")
    await db.delete(tool)
    await db.commit()
    await create_log(db, current_user.id, "delete_ai_tool", "ai_tool", tool_id, f"删除AI工具: {tool.name}")
    return ApiResponse(message="删除成功")
