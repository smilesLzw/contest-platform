"""AI工具相关请求/响应体"""
from datetime import datetime
from pydantic import BaseModel, Field


class AiCategoryCreate(BaseModel):
    name: str = Field(..., max_length=50)
    icon: str | None = None
    sort_order: int = 0


class AiCategoryUpdate(AiCategoryCreate):
    pass


class AiCategoryResponse(BaseModel):
    id: int
    name: str
    icon: str | None = None
    sort_order: int = 0

    class Config:
        from_attributes = True


class AiToolCreate(BaseModel):
    name: str = Field(..., max_length=100)
    logo_url: str | None = None
    url: str = Field(..., max_length=500)
    description: str | None = Field(None, max_length=300)
    category_id: int | None = None
    region: str = "domestic"
    is_free: int = 1
    rating: int = 5
    is_featured: int = 0
    sort_order: int = 0


class AiToolUpdate(AiToolCreate):
    pass


class AiToolResponse(BaseModel):
    id: int
    name: str
    logo_url: str | None = None
    url: str
    description: str | None = None
    category_id: int | None = None
    category_name: str | None = None
    region: str = "domestic"
    is_free: int = 1
    rating: int = 5
    is_featured: int = 0
    sort_order: int = 0
    created_at: datetime | None = None

    class Config:
        from_attributes = True
