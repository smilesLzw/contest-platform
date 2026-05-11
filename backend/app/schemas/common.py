"""通用响应格式"""
from typing import Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应格式"""
    code: int = 200
    message: str = "success"
    data: T | None = None


class PageData(BaseModel, Generic[T]):
    """统一分页响应格式"""
    items: list[T] = []
    total: int = 0
    page: int = 1
    page_size: int = 12
    pages: int = 0


class PageParams(BaseModel):
    """分页查询参数"""
    page: int = 1
    page_size: int = 12
