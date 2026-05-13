"""文件上传接口"""
import os
import re
import uuid
from datetime import datetime
import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
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
UPLOAD_CHUNK_SIZE = 1024 * 1024


def _generate_filename(original_name: str) -> str:
    """生成存储文件名：{年月日}_{uuid[:8]}_{原始文件名}"""
    date_str = datetime.now().strftime("%Y%m%d")
    short_uuid = uuid.uuid4().hex[:8]
    return f"{date_str}_{short_uuid}_{original_name}"


def _safe_name(value: str) -> str:
    """保留中文、字母、数字和少量分隔符，避免路径穿越和奇怪文件名。"""
    value = (value or "").strip()
    value = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-._")
    return value[:80] or "作品"


def _extension(original_name: str, default_ext: str) -> str:
    ext = os.path.splitext(original_name or "")[1].lower()
    return ext if ext else default_ext


def _work_filename(
    original_name: str,
    default_name: str,
    default_ext: str,
    academic_year: str | None,
    semester: int | None,
    title: str | None,
    suffix: str | None = None,
) -> str:
    """生成作品稳定文件名：2025-2026-2-作品名[_suffix].ext。"""
    if not academic_year or not semester or not title:
        return _generate_filename(original_name or default_name)

    prefix = f"{_safe_name(academic_year)}-{semester}-{_safe_name(title)}"
    safe_suffix = f"_{_safe_name(suffix)}" if suffix else ""
    return f"{prefix}{safe_suffix}{_extension(original_name or default_name, default_ext)}"


async def _save_upload(file: UploadFile, save_path: str, max_size: int, size_message: str) -> None:
    """分块写入上传文件，避免大文件一次性读入内存。"""
    tmp_path = f"{save_path}.{uuid.uuid4().hex}.tmp"
    total = 0
    try:
        async with aiofiles.open(tmp_path, "wb") as f:
            while True:
                chunk = await file.read(UPLOAD_CHUNK_SIZE)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_size:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=size_message)
                await f.write(chunk)
        os.replace(tmp_path, save_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@router.post("/image", response_model=ApiResponse)
async def upload_image(
    file: UploadFile = File(...),
    title: str | None = Form(None),
    academic_year: str | None = Form(None),
    semester: int | None = Form(None),
    suffix: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """上传图片（封面图、Logo等），最大10MB"""
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"不支持的图片格式，仅支持 JPG/PNG/WebP")

    filename = _work_filename(file.filename or "image.png", "image.png", ".png", academic_year, semester, title, suffix)
    save_dir = os.path.join(UPLOAD_DIR, "images")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    await _save_upload(file, save_path, MAX_IMAGE_SIZE, "图片大小不能超过10MB")

    url = f"/uploads/images/{filename}"
    return ApiResponse(data={"url": url})


@router.post("/file", response_model=ApiResponse)
async def upload_file(
    file: UploadFile = File(...),
    title: str | None = Form(None),
    academic_year: str | None = Form(None),
    semester: int | None = Form(None),
    suffix: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """上传附件（PDF/ZIP，最大50MB）"""
    if file.content_type not in ALLOWED_FILE_TYPES and not (file.filename or "").endswith((".pdf", ".zip")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"不支持的文件类型，仅支持 PDF/ZIP")

    filename = _work_filename(file.filename or "file.zip", "file.zip", ".zip", academic_year, semester, title, suffix)
    save_dir = os.path.join(UPLOAD_DIR, "files")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    await _save_upload(file, save_path, MAX_FILE_SIZE, "文件大小不能超过50MB")

    url = f"/uploads/files/{filename}"
    return ApiResponse(data={"url": url})


@router.post("/audio", response_model=ApiResponse)
async def upload_audio(
    file: UploadFile = File(...),
    title: str | None = Form(None),
    academic_year: str | None = Form(None),
    semester: int | None = Form(None),
    suffix: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """上传音频（MP3/WAV/OGG/AAC/FLAC，最大100MB）"""
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"不支持的音频格式，仅支持 MP3/WAV/OGG/AAC/FLAC")

    filename = _work_filename(file.filename or "audio.mp3", "audio.mp3", ".mp3", academic_year, semester, title, suffix)
    save_dir = os.path.join(UPLOAD_DIR, "audio")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    await _save_upload(file, save_path, MAX_AUDIO_SIZE, "音频大小不能超过100MB")

    url = f"/uploads/audio/{filename}"
    return ApiResponse(data={"url": url})


@router.post("/video", response_model=ApiResponse)
async def upload_video(
    file: UploadFile = File(...),
    title: str | None = Form(None),
    academic_year: str | None = Form(None),
    semester: int | None = Form(None),
    suffix: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin),
):
    """上传视频（MP4/WebM/MOV，最大1GB）"""
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"不支持的视频格式，仅支持 MP4/WebM/MOV")

    filename = _work_filename(file.filename or "video.mp4", "video.mp4", ".mp4", academic_year, semester, title, suffix)
    save_dir = os.path.join(UPLOAD_DIR, "videos")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    await _save_upload(file, save_path, MAX_VIDEO_SIZE, "视频大小不能超过1GB")

    url = f"/uploads/videos/{filename}"
    return ApiResponse(data={"url": url})
