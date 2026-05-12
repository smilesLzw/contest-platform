"""专业 Schema"""
from pydantic import BaseModel, Field


class MajorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class MajorUpdate(BaseModel):
    name: str | None = None


class MajorResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
