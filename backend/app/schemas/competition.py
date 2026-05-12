"""赛事 Schema"""
from datetime import datetime
from pydantic import BaseModel, Field


class CompetitionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    academic_year: str = Field(..., min_length=1, max_length=20)
    semester: int = Field(..., ge=1, le=2)


class CompetitionUpdate(BaseModel):
    name: str | None = None
    academic_year: str | None = None
    semester: int | None = None


class CompetitionResponse(BaseModel):
    id: int
    name: str
    academic_year: str
    semester: int
    is_active: bool
    created_at: datetime | None = None

    class Config:
        from_attributes = True
