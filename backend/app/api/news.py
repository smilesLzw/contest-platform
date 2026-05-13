"""新闻接口"""
import math
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models.news import News
from app.models.user import User
from app.core.deps import get_optional_user, require_teacher_or_admin
from app.schemas.news import NewsCreate, NewsUpdate, NewsResponse
from app.schemas.common import ApiResponse, PageData
from app.crud.log import create_log, model_snapshot

router = APIRouter(prefix="/news", tags=["新闻"])


def _news_to_response(news: News) -> NewsResponse:
    return NewsResponse(
        id=news.id,
        title=news.title,
        content=news.content,
        cover_url=news.cover_url,
        category=news.category,
        author_id=news.author_id,
        author_name=news.author.name if news.author else None,
        status=news.status,
        is_top=news.is_top,
        published_at=news.published_at,
        created_at=news.created_at,
        updated_at=news.updated_at,
    )


@router.get("/", response_model=ApiResponse[PageData[NewsResponse]])
async def list_news(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    category: str | None = None,
    keyword: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """新闻列表（公开仅 published）"""
    query = (
        select(News)
        .options(joinedload(News.author))
        .where(News.status == "published")
    )

    if category:
        query = query.where(News.category == category)
    if keyword:
        query = query.where(News.title.contains(keyword))

    # 置顶优先，按发布时间排序
    query = query.order_by(desc(News.is_top), desc(News.published_at))

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    news_list = result.unique().scalars().all()

    return ApiResponse(data=PageData(
        items=[_news_to_response(n) for n in news_list],
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if page_size > 0 else 0,
    ))


@router.get("/my", response_model=ApiResponse[PageData[NewsResponse]])
async def list_my_news(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """我发布的新闻"""
    query = (
        select(News)
        .options(joinedload(News.author))
        .where(News.author_id == current_user.id)
        .order_by(desc(News.created_at))
    )

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    news_list = result.unique().scalars().all()

    return ApiResponse(data=PageData(
        items=[_news_to_response(n) for n in news_list],
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if page_size > 0 else 0,
    ))


@router.get("/admin/all", response_model=ApiResponse[PageData[NewsResponse]])
async def admin_list_news(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    status: str | None = None,
    category: str | None = None,
    keyword: str | None = None,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_teacher_or_admin),
):
    """管理员查看所有新闻（含草稿）"""
    query = select(News).options(joinedload(News.author))

    if status:
        query = query.where(News.status == status)
    if category:
        query = query.where(News.category == category)
    if keyword:
        query = query.where(News.title.contains(keyword))

    query = query.order_by(desc(News.is_top), desc(News.created_at))

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    news_list = result.unique().scalars().all()

    return ApiResponse(data=PageData(
        items=[_news_to_response(n) for n in news_list],
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if page_size > 0 else 0,
    ))


@router.get("/{news_id}", response_model=ApiResponse[NewsResponse])
async def get_news(
    news_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    """新闻详情：已发布公开可见，草稿仅作者或管理员可见"""
    result = await db.execute(
        select(News).options(joinedload(News.author)).where(News.id == news_id)
    )
    news = result.unique().scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="新闻不存在")

    can_view_private = (
        current_user is not None
        and (current_user.role in ("admin", "teacher") or news.author_id == current_user.id)
    )
    if news.status != "published" and not can_view_private:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="新闻不存在")

    return ApiResponse(data=_news_to_response(news))


@router.post("/", response_model=ApiResponse[NewsResponse])
async def create_news(
    req: NewsCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """新建新闻"""
    news = News(
        title=req.title,
        content=req.content,
        cover_url=req.cover_url,
        category=req.category,
        author_id=current_user.id,
        status=req.status,
        published_at=None if req.status == "draft" else func.now(),
    )
    db.add(news)
    await db.commit()
    await db.refresh(news)
    return ApiResponse(data=_news_to_response(news))


@router.put("/{news_id}", response_model=ApiResponse[NewsResponse])
async def update_news(
    news_id: int,
    req: NewsUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """编辑新闻"""
    result = await db.execute(
        select(News).options(joinedload(News.author)).where(News.id == news_id)
    )
    news = result.unique().scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="新闻不存在")
    old_status = news.status
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(news, field, value)
    if old_status != "published" and news.status == "published" and news.published_at is None:
        news.published_at = func.now()
    await db.commit()
    await db.refresh(news)
    return ApiResponse(data=_news_to_response(news))


@router.delete("/{news_id}", response_model=ApiResponse)
async def delete_news(
    news_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """删除新闻（本人仅可删草稿，管理员可删任意）"""
    result = await db.execute(select(News).where(News.id == news_id))
    news = result.scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="新闻不存在")
    snapshot = model_snapshot(news)
    title = news.title
    await db.delete(news)
    await db.commit()
    await create_log(db, current_user.id, "delete_news", "news", news_id, f"删除新闻: {title}", snapshot, True)
    return ApiResponse(message="删除成功")


@router.put("/{news_id}/publish", response_model=ApiResponse[NewsResponse])
async def publish_news(
    news_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """发布新闻"""
    result = await db.execute(
        select(News).options(joinedload(News.author)).where(News.id == news_id)
    )
    news = result.unique().scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="新闻不存在")
    news.status = "published"
    news.published_at = func.now()
    await db.commit()
    await db.refresh(news)
    await create_log(db, current_user.id, "publish_news", "news", news_id, f"发布新闻: {news.title}")
    return ApiResponse(data=_news_to_response(news))


@router.put("/{news_id}/top", response_model=ApiResponse[NewsResponse])
async def toggle_top_news(
    news_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """置顶/取消置顶"""
    result = await db.execute(
        select(News).options(joinedload(News.author)).where(News.id == news_id)
    )
    news = result.unique().scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="新闻不存在")
    news.is_top = 1 if news.is_top == 0 else 0
    await db.commit()
    await db.refresh(news)
    return ApiResponse(data=_news_to_response(news))
