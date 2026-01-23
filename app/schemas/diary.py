from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DiaryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(...)


class DiaryCreate(DiaryBase):
    pass


class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class DiaryResponse(DiaryBase):
    id: int
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True  # Tortoise 객체를 Pydantic으로 자동 변환
