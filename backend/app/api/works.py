"""作品接口"""
import math
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, asc
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models.work import Work
from app.models.user import User
from app.core.deps import get_optional_user, require_teacher_or_admin, require_admin
from app.schemas.work import WorkCreate, WorkUpdate, WorkResponse
from app.schemas.common import ApiResponse, PageData
from app.crud.log import create_log

router = APIRouter(prefix="/works", tags=["作品"])


def _work_to_response(work: Work) -> WorkResponse:
    """Work 模型转响应"""
    return WorkResponse(
        id=work.id,
        title=work.title,
        author_names=work.author_names,
        guide_teacher=work.guide_teacher,
        class_name=work.class_name,
        major_id=work.major_id,
        major_name=work.major.name if work.major else None,
        academic_year=work.academic_year,
        semester=work.semester,
        contest_name=work.contest_name,
        award=work.award,
        work_type=work.work_type,
        cover_url=work.cover_url,
        content=work.content,
        demo_url=work.demo_url,
        attachment_url=work.attachment_url,
        audio_url=work.audio_url,
        video_url=work.video_url,
        embed_url=work.embed_url,
        gallery_urls=work.gallery_urls,
        status=work.status,
        publisher_id=work.publisher_id,
        publisher_name=work.publisher.name if work.publisher else None,
        published_at=work.published_at,
        created_at=work.created_at,
        updated_at=work.updated_at,
    )


@router.get("/", response_model=ApiResponse[PageData[WorkResponse]])
async def list_works(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    academic_year: str | None = None,
    semester: int | None = None,
    major_id: int | None = None,
    work_type: str | None = None,
    keyword: str | None = None,
    sort: str = "created_at_desc",
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    """作品列表（公开仅 published，管理员可传 status 参数）"""
    query = select(Work).options(joinedload(Work.major), joinedload(Work.publisher))

    if status:
        if current_user is None or current_user.role != "admin":
            raise HTTPException(status_code=403, detail="需要管理员权限")
        query = query.where(Work.status == status)
    else:
        query = query.where(Work.status == "published")

    if academic_year:
        query = query.where(Work.academic_year == academic_year)
    if semester:
        query = query.where(Work.semester == semester)
    if major_id:
        query = query.where(Work.major_id == major_id)
    if work_type:
        query = query.where(Work.work_type == work_type)
    if keyword:
        query = query.where(
            Work.title.contains(keyword) | Work.author_names.contains(keyword)
        )

    # 排序
    if sort == "title_asc":
        query = query.order_by(asc(Work.title))
    else:
        query = query.order_by(desc(Work.created_at))

    # 总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # 分页
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    works = result.unique().scalars().all()

    return ApiResponse(data=PageData(
        items=[_work_to_response(w) for w in works],
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if page_size > 0 else 0,
    ))


@router.get("/my", response_model=ApiResponse[PageData[WorkResponse]])
async def list_my_works(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """我发布的作品"""
    query = (
        select(Work)
        .options(joinedload(Work.major), joinedload(Work.publisher))
        .where(Work.publisher_id == current_user.id)
        .order_by(desc(Work.created_at))
    )

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    works = result.unique().scalars().all()

    return ApiResponse(data=PageData(
        items=[_work_to_response(w) for w in works],
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if page_size > 0 else 0,
    ))


@router.get("/admin/all", response_model=ApiResponse[PageData[WorkResponse]])
async def admin_list_works(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    status: str | None = None,
    academic_year: str | None = None,
    keyword: str | None = None,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """管理员查看所有作品（含草稿）"""
    query = (
        select(Work)
        .options(joinedload(Work.major), joinedload(Work.publisher))
    )

    if status:
        query = query.where(Work.status == status)
    if academic_year:
        query = query.where(Work.academic_year == academic_year)
    if keyword:
        query = query.where(Work.title.contains(keyword))

    query = query.order_by(desc(Work.created_at))

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    works = result.unique().scalars().all()

    return ApiResponse(data=PageData(
        items=[_work_to_response(w) for w in works],
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if page_size > 0 else 0,
    ))


@router.get("/{work_id}", response_model=ApiResponse[WorkResponse])
async def get_work(
    work_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    """作品详情：已发布公开可见，草稿/下架仅作者或管理员可见"""
    result = await db.execute(
        select(Work)
        .options(joinedload(Work.major), joinedload(Work.publisher))
        .where(Work.id == work_id)
    )
    work = result.unique().scalar_one_or_none()
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="作品不存在")

    can_view_private = (
        current_user is not None
        and (current_user.role == "admin" or work.publisher_id == current_user.id)
    )
    if work.status != "published" and not can_view_private:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="作品不存在")

    return ApiResponse(data=_work_to_response(work))


@router.post("/", response_model=ApiResponse[WorkResponse])
async def create_work(
    req: WorkCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """新建作品"""
    work = Work(
        title=req.title,
        author_names=req.author_names,
        guide_teacher=req.guide_teacher,
        class_name=req.class_name,
        major_id=req.major_id,
        academic_year=req.academic_year,
        semester=req.semester,
        contest_name=req.contest_name,
        award=req.award,
        work_type=req.work_type,
        cover_url=req.cover_url,
        content=req.content,
        demo_url=req.demo_url,
        attachment_url=req.attachment_url,
        audio_url=req.audio_url,
        video_url=req.video_url,
        embed_url=req.embed_url,
        gallery_urls=req.gallery_urls,
        status=req.status,
        publisher_id=current_user.id,
        published_at=None if req.status == "draft" else func.now(),
    )
    db.add(work)
    await db.commit()
    await db.refresh(work)
    # 如果直接发布，记录日志
    if req.status == "published":
        await create_log(db, current_user.id, "publish_work", "work", work.id, f"发布作品: {work.title}")
    return ApiResponse(data=_work_to_response(work))


@router.put("/{work_id}", response_model=ApiResponse[WorkResponse])
async def update_work(
    work_id: int,
    req: WorkUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """编辑作品"""
    result = await db.execute(
        select(Work).options(joinedload(Work.major), joinedload(Work.publisher)).where(Work.id == work_id)
    )
    work = result.unique().scalar_one_or_none()
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="作品不存在")
    if current_user.role != "admin" and work.publisher_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能编辑自己的作品")

    old_status = work.status
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(work, field, value)
    if old_status != "published" and work.status == "published" and work.published_at is None:
        work.published_at = func.now()
    await db.commit()
    await db.refresh(work)
    return ApiResponse(data=_work_to_response(work))


@router.delete("/{work_id}", response_model=ApiResponse)
async def delete_work(
    work_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """删除作品（本人仅可删草稿，管理员可删任意）"""
    result = await db.execute(select(Work).where(Work.id == work_id))
    work = result.scalar_one_or_none()
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="作品不存在")
    if current_user.role != "admin":
        if work.publisher_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能删除自己的作品")
        if work.status != "draft":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="仅可删除草稿状态的作品")
    await db.delete(work)
    await db.commit()
    await create_log(db, current_user.id, "delete_work", "work", work_id, f"删除作品: {work.title}")
    return ApiResponse(message="删除成功")


@router.put("/{work_id}/publish", response_model=ApiResponse[WorkResponse])
async def publish_work(
    work_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """发布作品"""
    result = await db.execute(
        select(Work).options(joinedload(Work.major), joinedload(Work.publisher)).where(Work.id == work_id)
    )
    work = result.unique().scalar_one_or_none()
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="作品不存在")
    if current_user.role != "admin" and work.publisher_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    work.status = "published"
    work.published_at = func.now()
    await db.commit()
    await db.refresh(work)
    await create_log(db, current_user.id, "publish_work", "work", work_id, f"发布作品: {work.title}")
    return ApiResponse(data=_work_to_response(work))


@router.put("/{work_id}/archive", response_model=ApiResponse[WorkResponse])
async def archive_work(
    work_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """下架作品（管理员）"""
    result = await db.execute(
        select(Work).options(joinedload(Work.major), joinedload(Work.publisher)).where(Work.id == work_id)
    )
    work = result.unique().scalar_one_or_none()
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="作品不存在")
    work.status = "archived"
    await db.commit()
    await db.refresh(work)
    await create_log(db, current_user.id, "archive_work", "work", work_id, f"下架作品: {work.title}")
    return ApiResponse(data=_work_to_response(work))
