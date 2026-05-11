"""新闻相关请求/响应体"""
from datetime import datetime
from pydantic import BaseModel, Field


class NewsCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str | None = None
    cover_url: str | None = None
    category: str = "tutorial"
    status: str = "draft"


class NewsUpdate(NewsCreate):
    pass


class NewsResponse(BaseModel):
    id: int
    title: str
    content: str | None = None
    cover_url: str | None = None
    category: str
    author_id: int | None = None
    author_name: str | None = None
    status: str
    is_top: int = 0
    published_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class NewsListParams(BaseModel):
    page: int = 1
    page_size: int = 10
    category: str | None = None
    keyword: str | None = None
