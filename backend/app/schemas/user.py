"""用户管理相关请求/响应体"""
from datetime import datetime
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, description="工号")
    password: str = Field(..., min_length=8, description="密码，至少8位")
    name: str = Field(..., max_length=50)
    department: str | None = None
    phone: str | None = Field(None, max_length=30)
    role: str = "teacher"


class UserUpdate(BaseModel):
    username: str | None = Field(None, min_length=1, max_length=50)
    name: str | None = Field(None, min_length=1, max_length=50)
    department: str | None = None
    phone: str | None = Field(None, max_length=30)


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    name: str
    department: str | None = None
    phone: str | None = None
    avatar_url: str | None = None
    status: int = 1
    created_at: datetime | None = None

    class Config:
        from_attributes = True
