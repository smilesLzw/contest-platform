"""FastAPI 应用入口"""
import math
from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db, engine, Base
from app.models import User, Work, News, AiTool, OperationLog, Major, AiCategory
from app.core.deps import get_current_user, require_admin
from app.schemas.common import ApiResponse, PageData
from app.api import auth, works, news, ai_tools, users, upload, bg_music, competitions

app = FastAPI(
    title="院赛作品展示与AI工具导航平台",
    description="院赛作品展示与AI工具导航平台 API",
    version="1.0.0",
    docs_url="/docs",
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1")
app.include_router(works.router, prefix="/api/v1")
app.include_router(news.router, prefix="/api/v1")
app.include_router(ai_tools.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")
app.include_router(bg_music.router, prefix="/api/v1")
app.include_router(competitions.router, prefix="/api/v1")


# 静态文件服务（必须在路由之前 mount）
import os
os.makedirs("uploads/images", exist_ok=True)
os.makedirs("uploads/files", exist_ok=True)
os.makedirs("uploads/audio", exist_ok=True)
os.makedirs("uploads/videos", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# ---------- 公共接口 ----------

@app.get("/api/v1/majors", response_model=ApiResponse[list[dict]])
async def list_majors(db: AsyncSession = Depends(get_db)):
    """获取专业列表"""
    result = await db.execute(select(Major).order_by(Major.sort_order, Major.id))
    rows = result.scalars().all()
    data = []
    for m in rows:
        label = f"{m.grade} {m.duration} {m.name}"
        data.append({"id": m.id, "name": label, "sort_order": m.sort_order})
    return ApiResponse(data=data)


# ---------- 专业管理（管理员） ----------

@app.get("/api/v1/admin/majors", response_model=ApiResponse[list[dict]])
async def admin_list_majors(db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    result = await db.execute(select(Major).order_by(Major.sort_order, Major.id))
    majors_list = result.scalars().all()
    return ApiResponse(data=[{
        "id": m.id, "grade": m.grade, "duration": m.duration,
        "name": m.name, "sort_order": m.sort_order,
    } for m in majors_list])


@app.post("/api/v1/admin/majors", response_model=ApiResponse[dict])
async def admin_create_major(
    data: dict,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    major = Major(
        grade=data.get("grade", ""),
        duration=data.get("duration", ""),
        name=data.get("name", ""),
        sort_order=0,
    )
    db.add(major)
    await db.commit()
    await db.refresh(major)
    return ApiResponse(data={"id": major.id, "name": major.name})


@app.put("/api/v1/admin/majors/{major_id}", response_model=ApiResponse[dict])
async def admin_update_major(
    major_id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    result = await db.execute(select(Major).where(Major.id == major_id))
    major = result.scalar_one_or_none()
    if not major:
        raise HTTPException(status_code=404, detail="专业不存在")
    for field in ("grade", "duration", "name"):
        if field in data:
            setattr(major, field, data[field])
    await db.commit()
    await db.refresh(major)
    return ApiResponse(data={"id": major.id, "name": major.name})


@app.delete("/api/v1/admin/majors/{major_id}", response_model=ApiResponse)
async def admin_delete_major(
    major_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    result = await db.execute(select(Major).where(Major.id == major_id))
    major = result.scalar_one_or_none()
    if not major:
        raise HTTPException(status_code=404, detail="专业不存在")
    await db.delete(major)
    await db.commit()
    return ApiResponse(message="删除成功")


# ---------- 统计数据 ----------

@app.get("/api/v1/stats", response_model=ApiResponse[dict])
async def get_stats(db: AsyncSession = Depends(get_db)):
    """获取平台统计数据"""
    works_count = await db.scalar(select(func.count(Work.id)).where(Work.status == "published")) or 0
    news_count = await db.scalar(select(func.count(News.id)).where(News.status == "published")) or 0
    tools_count = await db.scalar(select(func.count(AiTool.id))) or 0
    return ApiResponse(data={
        "works_count": works_count,
        "news_count": news_count,
        "tools_count": tools_count,
    })


@app.get("/api/v1/logs", response_model=ApiResponse[PageData[dict]])
async def list_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """操作日志列表"""
    query = select(OperationLog).order_by(OperationLog.created_at.desc())

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    logs = result.scalars().all()

    return ApiResponse(data=PageData(
        items=[
            {
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "target_type": log.target_type,
                "target_id": log.target_id,
                "detail": log.detail,
                "created_at": log.created_at.isoformat() if log.created_at else None,
            }
            for log in logs
        ],
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if page_size > 0 else 0,
    ))
