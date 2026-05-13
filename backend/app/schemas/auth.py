"""认证相关请求/响应体"""
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, description="工号/账号")
    password: str = Field(..., min_length=1, description="密码")


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserInfo"


class UserInfo(BaseModel):
    id: int
    username: str
    role: str
    name: str
    department: str | None = None
    phone: str | None = None
    avatar_url: str | None = None

    class Config:
        from_attributes = True


class UpdateProfileRequest(BaseModel):
    username: str | None = Field(None, min_length=1, max_length=50, description="工号/账号")
    name: str | None = Field(None, min_length=1, max_length=50)
    department: str | None = Field(None, max_length=100)
    phone: str | None = Field(None, max_length=30)
    avatar_url: str | None = None


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, description="密码最少8位，需包含字母和数字")
