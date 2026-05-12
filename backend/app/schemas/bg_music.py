"""背景音乐请求/响应体"""
from datetime import datetime
from pydantic import BaseModel, Field


class BgMusicCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    artist: str | None = None
    audio_url: str = Field(..., min_length=1)
    source: str = "preset"
    work_id: int | None = None
    sort_order: int = 0


class BgMusicUpdate(BaseModel):
    title: str | None = None
    artist: str | None = None
    audio_url: str | None = None
    sort_order: int | None = None


class BgMusicResponse(BaseModel):
    id: int
    title: str
    artist: str | None = None
    audio_url: str
    source: str
    work_id: int | None = None
    is_active: bool
    sort_order: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True
