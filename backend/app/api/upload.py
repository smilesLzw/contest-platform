"""文件上传接口"""
import os
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.core.deps import get_current_user, require_teacher_or_admin
from app.core.config import (
    UPLOAD_DIR, MAX_IMAGE_SIZE, MAX_AUDIO_SIZE, MAX_VIDEO_SIZE, MAX_FILE_SIZE,
    ALLOWED_IMAGE_TYPES, ALLOWED_AUDIO_TYPES, ALLOWED_VIDEO_TYPES, ALLOWED_FILE_TYPES,
)
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/upload", tags=["文件上传"])


def _generate_filename(original_name: str) -> str:
    """生成存储文件名：{年月日}_{uuid[:8]}_{原始文件名}"""
    date_str = datetime.now().strftime("%Y%m%d")
    short_uuid = uuid.uuid4().hex[:8]
    return f"{date_str}_{short_uuid}_{original_name}"


@router.post("/image", response_model=ApiResponse)
async def upload_image(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """上传图片（封面图、Logo等），最大5MB"""
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"不支持的图片格式，仅支持 JPG/PNG/WebP")

    content = await file.read()
    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="图片大小不能超过5MB")

    filename = _generate_filename(file.filename or "image.png")
    save_dir = os.path.join(UPLOAD_DIR, "images")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)

    with open(save_path, "wb") as f:
        f.write(content)

    url = f"/uploads/images/{filename}"
    return ApiResponse(data={"url": url})


@router.post("/file", response_model=ApiResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """上传附件（PDF/ZIP，最大50MB）"""
    if file.content_type not in ALLOWED_FILE_TYPES and not file.filename.endswith((".pdf", ".zip")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"不支持的文件类型，仅支持 PDF/ZIP")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="文件大小不能超过50MB")

    filename = _generate_filename(file.filename or "file.zip")
    save_dir = os.path.join(UPLOAD_DIR, "files")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)

    with open(save_path, "wb") as f:
        f.write(content)

    url = f"/uploads/files/{filename}"
    return ApiResponse(data={"url": url})


@router.post("/audio", response_model=ApiResponse)
async def upload_audio(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """上传音频（MP3/WAV/OGG/AAC/FLAC，最大100MB）"""
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"不支持的音频格式，仅支持 MP3/WAV/OGG/AAC/FLAC")

    content = await file.read()
    if len(content) > MAX_AUDIO_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="音频大小不能超过100MB")

    filename = _generate_filename(file.filename or "audio.mp3")
    save_dir = os.path.join(UPLOAD_DIR, "audio")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)

    with open(save_path, "wb") as f:
        f.write(content)

    url = f"/uploads/audio/{filename}"
    return ApiResponse(data={"url": url})


@router.post("/video", response_model=ApiResponse)
async def upload_video(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """上传视频（MP4/WebM/MOV，最大1GB）"""
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"不支持的视频格式，仅支持 MP4/WebM/MOV")

    content = await file.read()
    if len(content) > MAX_VIDEO_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="视频大小不能超过1GB")

    filename = _generate_filename(file.filename or "video.mp4")
    save_dir = os.path.join(UPLOAD_DIR, "videos")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)

    with open(save_path, "wb") as f:
        f.write(content)

    url = f"/uploads/videos/{filename}"
    return ApiResponse(data={"url": url})
