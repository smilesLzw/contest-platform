"""作品相关请求/响应体"""
from datetime import datetime
from pydantic import BaseModel, Field


class WorkCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author_names: str = Field(..., min_length=1, max_length=200)
    guide_teacher: str | None = None
    class_name: str | None = None
    major_id: int | None = None
    academic_year: str = Field(..., min_length=1)
    semester: int = Field(..., ge=1, le=2)
    contest_name: str | None = None
    award: str | None = None
    work_type: str | None = None
    cover_url: str | None = None
    cover_original_url: str | None = None
    cover_card_url: str | None = None
    cover_detail_url: str | None = None
    cover_thumb_url: str | None = None
    cover_crop_data: str | None = None
    content: str | None = None
    demo_url: str | None = None
    attachment_url: str | None = None
    audio_url: str | None = None
    video_url: str | None = None
    embed_url: str | None = None
    gallery_urls: str | None = None
    status: str = "draft"


class WorkUpdate(WorkCreate):
    pass


class WorkResponse(BaseModel):
    id: int
    title: str
    author_names: str
    guide_teacher: str | None = None
    class_name: str | None = None
    major_id: int | None = None
    major_name: str | None = None
    academic_year: str
    semester: int
    contest_name: str | None = None
    award: str | None = None
    work_type: str | None = None
    cover_url: str | None = None
    cover_original_url: str | None = None
    cover_card_url: str | None = None
    cover_detail_url: str | None = None
    cover_thumb_url: str | None = None
    cover_crop_data: str | None = None
    content: str | None = None
    demo_url: str | None = None
    attachment_url: str | None = None
    audio_url: str | None = None
    video_url: str | None = None
    embed_url: str | None = None
    gallery_urls: str | None = None
    status: str
    publisher_id: int | None = None
    publisher_name: str | None = None
    published_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class WorkListParams(BaseModel):
    page: int = 1
    page_size: int = 12
    academic_year: str | None = None
    semester: int | None = None
    major_id: int | None = None
    work_type: str | None = None
    keyword: str | None = None
    sort: str = "created_at_desc"
    status: str | None = None
