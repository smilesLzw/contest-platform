"""背景音乐管理接口"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.database import get_db
from app.models.user import User
from app.models.bg_music import BackgroundMusic
from app.core.deps import require_admin
from app.schemas.bg_music import BgMusicCreate, BgMusicUpdate, BgMusicResponse
from app.schemas.common import ApiResponse
from app.crud.log import create_log

router = APIRouter(prefix="/bg-music", tags=["背景音乐"])


@router.get("/", response_model=ApiResponse[list[BgMusicResponse]])
async def list_bg_music(db: AsyncSession = Depends(get_db)):
    """获取所有活跃的背景音乐（公开，按排序）"""
    result = await db.execute(
        select(BackgroundMusic)
        .where(BackgroundMusic.is_active == True)
        .order_by(BackgroundMusic.sort_order, BackgroundMusic.id)
    )
    items = result.scalars().all()
    return ApiResponse(data=[BgMusicResponse.model_validate(m) for m in items])


@router.get("/admin/all", response_model=ApiResponse[list[BgMusicResponse]])
async def admin_list_bg_music(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """管理员获取全部背景音乐（含未启用）"""
    result = await db.execute(
        select(BackgroundMusic).order_by(desc(BackgroundMusic.is_active), BackgroundMusic.sort_order, BackgroundMusic.id)
    )
    items = result.scalars().all()
    return ApiResponse(data=[BgMusicResponse.model_validate(m) for m in items])


@router.post("/", response_model=ApiResponse[BgMusicResponse])
async def create_bg_music(
    req: BgMusicCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """添加背景音乐"""
    music = BackgroundMusic(
        title=req.title,
        artist=req.artist,
        audio_url=req.audio_url,
        source=req.source,
        work_id=req.work_id,
        sort_order=req.sort_order,
    )
    db.add(music)
    await db.commit()
    await db.refresh(music)
    await create_log(db, current_user.id, "create_bg_music", "bg_music", music.id, f"添加背景音乐: {music.title}")
    return ApiResponse(data=BgMusicResponse.model_validate(music))


@router.put("/{music_id}", response_model=ApiResponse[BgMusicResponse])
async def update_bg_music(
    music_id: int,
    req: BgMusicUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """编辑背景音乐"""
    result = await db.execute(select(BackgroundMusic).where(BackgroundMusic.id == music_id))
    music = result.scalar_one_or_none()
    if not music:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="背景音乐不存在")

    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(music, field, value)
    await db.commit()
    await db.refresh(music)
    await create_log(db, current_user.id, "update_bg_music", "bg_music", music.id, f"编辑背景音乐: {music.title}")
    return ApiResponse(data=BgMusicResponse.model_validate(music))


@router.delete("/{music_id}", response_model=ApiResponse)
async def delete_bg_music(
    music_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """删除背景音乐"""
    result = await db.execute(select(BackgroundMusic).where(BackgroundMusic.id == music_id))
    music = result.scalar_one_or_none()
    if not music:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="背景音乐不存在")

    await db.delete(music)
    await db.commit()
    await create_log(db, current_user.id, "delete_bg_music", "bg_music", music_id, f"删除背景音乐: {music.title}")
    return ApiResponse(message="删除成功")


@router.put("/{music_id}/toggle", response_model=ApiResponse[BgMusicResponse])
async def toggle_bg_music(
    music_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """启用/禁用背景音乐"""
    result = await db.execute(select(BackgroundMusic).where(BackgroundMusic.id == music_id))
    music = result.scalar_one_or_none()
    if not music:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="背景音乐不存在")

    music.is_active = not music.is_active
    await db.commit()
    await db.refresh(music)
    action = "启用" if music.is_active else "禁用"
    await create_log(db, current_user.id, "toggle_bg_music", "bg_music", music.id, f"{action}背景音乐: {music.title}")
    return ApiResponse(data=BgMusicResponse.model_validate(music))
